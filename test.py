import win32com.client
import pythoncom
import os
from datetime import datetime
from typing import Dict, Any, List
from config import (PROJECT_MAPPING, DOCUMENT_TYPES, 
                   REFERENCE_PATTERNS, DEPARTMENT_MAPPING)

class OutlookDeepLook:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "outlook_deeplook")
        self.results_dir = os.path.join(self.base_dir, f"search_results_{self.timestamp}")
        self._setup_environment()
        
    def _setup_environment(self):
        """Initialize directories and Outlook connection"""
        os.makedirs(self.results_dir, exist_ok=True)
        
        try:
            pythoncom.CoInitialize()
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            self.namespace = self.outlook.GetNamespace("MAPI")
            self.inbox = self.namespace.GetDefaultFolder(6)
            print("✓ Connected to Outlook")
        except Exception as e:
            print(f"✗ Connection error: {str(e)}")
            raise

    def search_emails(self, query: str, project_code: str = None, max_results: int = 50):
        """Search emails with correct Outlook filter syntax"""
        print(f"\nSearching for: '{query}'")
        results = []
        
        try:
            # Get all items first
            messages = self.inbox.Items
            messages.Sort("[ReceivedTime]", True)
            
            # Filter using simple string matching
            count = 0
            for message in messages:
                if count >= max_results:
                    break
                    
                try:
                    # Check if query matches subject or body
                    if (query.lower() in message.Subject.lower() or 
                        (hasattr(message, 'Body') and query.lower() in message.Body.lower())):
                        
                        # Check project code if provided
                        if project_code:
                            if not any(alias.upper() in message.Subject.upper() 
                                     for alias in PROJECT_MAPPING[project_code]['aliases']):
                                continue
                        
                        # Process matching email
                        email_data = self._process_email(message, project_code)
                        if email_data:
                            results.append(email_data)
                            count += 1
                            
                except Exception as e:
                    print(f"Warning: Error processing message: {str(e)}")
                    continue
                    
            print(f"Found {len(results)} matching emails")
            return results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def _process_email(self, message, project_code: str = None) -> Dict[str, Any]:
        """Process email with document pattern recognition"""
        try:
            email_data = {
                'subject': message.Subject,
                'sender': message.SenderEmailAddress,
                'received': str(message.ReceivedTime),
                'body': message.Body[:500] if hasattr(message, 'Body') else "",
                'project_code': None,
                'document_type': None
            }
            
            # Identify project code
            if project_code and project_code in PROJECT_MAPPING:
                email_data['project_code'] = project_code
            else:
                for code, project in PROJECT_MAPPING.items():
                    if any(alias.upper() in message.Subject.upper() 
                          for alias in project['aliases']):
                        email_data['project_code'] = code
                        break
            
            # Identify document type
            for doc_type, patterns in DOCUMENT_TYPES.items():
                if any(prefix.upper() in message.Subject.upper() 
                      for prefix in patterns['prefixes']):
                    email_data['document_type'] = doc_type
                    break
                    
            return email_data
            
        except Exception as e:
            print(f"Error processing email: {str(e)}")
            return None

def test_search():
    """Test the OutlookDeepLook functionality"""
    try:
        searcher = OutlookDeepLook()
        
        test_queries = [
            {
                'query': 'agreement',
                'project_code': 'PD031',
                'max_results': 10
            },
            {
                'query': 'letter',
                'project_code': '7CJLT',
                'max_results': 5
            }
        ]
        
        for test in test_queries:
            print(f"\nTesting search: {test['query']}")
            print(f"Project code: {test['project_code']}")
            
            results = searcher.search_emails(
                query=test['query'],
                project_code=test['project_code'],
                max_results=test['max_results']
            )
            
            if results:
                print("\nResults:")
                for idx, result in enumerate(results, 1):
                    print(f"\n{idx}. Subject: {result['subject']}")
                    print(f"   Project: {result['project_code']}")
                    print(f"   Type: {result['document_type']}")
                    print(f"   Date: {result['received']}")
                
    except Exception as e:
        print(f"Test error: {str(e)}")
    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    test_search()