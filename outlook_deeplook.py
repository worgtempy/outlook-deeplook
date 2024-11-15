import win32com.client
import pythoncom
import os
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import anthropic

class OutlookDeepLook:
    def __init__(self, use_claude: bool = False, claude_api_key: str = None):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "outlook_deeplook")
        self.results_dir = os.path.join(self.base_dir, f"search_results_{self.timestamp}")
        self.use_claude = use_claude
        self.claude_api_key = claude_api_key
        self._setup_environment()

    def process_query(self, query: str) -> List[Dict[str, Any]]:
        """Two-step semantic search process"""
        print(f"\nAnalyzing query: '{query}'")
        
        # Step 1: Use Claude to analyze query and extract search parameters
        search_params = self._analyze_query(query)
        
        # Step 2: Search emails using the extracted parameters
        results = self._semantic_search(search_params)
        
        # Step 3: Optional detailed analysis of results
        if self.use_claude and results:
            results = self._analyze_results(results, query)
            
        return results

    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Extract search parameters using Claude API"""
        try:
            if self.use_claude and self.claude_api_key:
                client = anthropic.Client(api_key=self.claude_api_key)
                
                prompt = f"""Analyze this email search query: '{query}'
                Using the config data, extract:
                1. Main keywords for searching
                2. Project codes or aliases if mentioned
                3. Document types if specified
                4. Any date references
                5. Additional relevant search terms
                
                Format the response as a Python dictionary."""
                
                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=500,
                    temperature=0,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Parse Claude's response into search parameters
                return self._parse_claude_response(response.content)
            else:
                # Fallback to basic keyword extraction
                return {
                    'keywords': [w for w in query.lower().split() if len(w) > 3],
                    'project_code': None,
                    'doc_type': None
                }
                
        except Exception as e:
            print(f"Query analysis error: {str(e)}")
            return {'keywords': [query.lower()]}

    def _semantic_search(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search emails using extracted parameters"""
        print("Searching with parameters:", search_params)
        results = []
        
        try:
            messages = self.inbox.Items
            messages.Sort("[ReceivedTime]", True)
            
            for message in messages:
                try:
                    if self._matches_criteria(message, search_params):
                        email_data = self._process_email(message)
                        if email_data:
                            results.append(email_data)
                except Exception:
                    continue
                    
            return results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def _matches_criteria(self, message, search_params: Dict[str, Any]) -> bool:
        """Check if message matches search criteria"""
        try:
            subject = message.Subject.lower()
            body = message.Body.lower() if hasattr(message, 'Body') else ""
            
            # Check keywords
            if not any(kw in subject or kw in body for kw in search_params['keywords']):
                return False
                
            # Check project code
            if search_params.get('project_code'):
                if search_params['project_code'] not in subject:
                    return False
                    
            # Check document type
            if search_params.get('doc_type'):
                if not self._identify_document_type(subject) == search_params['doc_type']:
                    return False
                    
            return True
            
        except Exception:
            return False

    def _analyze_results(self, results: List[Dict], original_query: str) -> List[Dict]:
        """Analyze search results using Claude"""
        try:
            if not self.use_claude or not results:
                return results
                
            client = anthropic.Client(api_key=self.claude_api_key)
            
            # Prepare analysis prompt
            email_data = "\n".join([
                f"Subject: {r['subject']}\nDate: {r['received']}\nBody: {r['body'][:200]}..."
                for r in results[:5]
            ])
            
            prompt = f"""Analyze these email search results for the query: '{original_query}'
            {email_data}
            
            Provide:
            1. Key information found
            2. Relevant details
            3. Summary of findings"""
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Add analysis to results
            if response.content:
                results.append({
                    'subject': '--- Analysis Summary ---',
                    'body': response.content,
                    'type': 'analysis'
                })
            
            return results
            
        except Exception as e:
            print(f"Analysis error: {str(e)}")
            return results

    # Keep your existing helper methods (_setup_environment, _process_email, etc.)

    def _remove_duplicates(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate emails based on subject"""
        seen = set()
        unique_results = []
        
        for result in results:
            if result['subject'] not in seen:
                seen.add(result['subject'])
                unique_results.append(result)
                
        return unique_results

def main():
    try:
        # Get Claude API preference
        use_claude = input("Use Claude API for enhanced analysis? (y/n): ").lower() == 'y'
        claude_api_key = None
        if use_claude:
            claude_api_key = input("Enter Claude API key: ").strip()
        
        searcher = OutlookDeepLook(use_claude=use_claude, claude_api_key=claude_api_key)
        
        print("\nOutlook DeepLook Bot")
        print("Ask questions in natural language, for example:")
        print("- Find emails about agreement from Seven Hotel")
        print("- Show me all documents related to PD031")
        print("- What are the recent emails about payment?")
        
        while True:
            question = input("\nAsk a question (or 'quit' to exit): ").strip()
            if question.lower() == 'quit':
                break
            
            results = searcher.ask_bot(question)
            
            if results:
                print(f"\nFound {len(results)} relevant items:")
                for idx, result in enumerate(results, 1):
                    if result.get('type') == 'analysis':
                        print(f"\n{result['body']}")
                    else:
                        print(f"\n{idx}. Subject: {result['subject']}")
                        print(f"   Date: {result['received']}")
                        if result.get('document_type'):
                            print(f"   Type: {result['document_type']}")
            else:
                print("\nNo matching results found.")
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    main()