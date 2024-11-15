import anthropic
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentSearcher:
    def __init__(self, csv_file="output/MERGED.csv"):
        self.client = anthropic.Client(api_key=os.getenv('CLAUDE_API_KEY'))
      
        # Load the CSV data
        print("Loading document database...")
        self.df = pd.read_csv(csv_file)
        print(f"Loaded {len(self.df)} documents")
        
    def search_with_claude(self, query):
        """Use Claude to search and analyze documents"""
        try:
            # Convert relevant data to context
            context = self.df.to_string()
            
            # Construct the prompt
            prompt = f"""
            You are a helpful document search assistant. Based on the following document database:
            {context}
            
            Query: {query}
            
            Please analyze and provide:
            1. Relevant documents found (with file names)
            2. Key information extracted
            3. Any relationships between documents
            4. Summary of findings
            
            Format your response in a clear, organized way.
            """
            
            # Get Claude's response
            message = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1024,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return str(message.content)  # Convert content to string
            
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    # Create output directory for search results
    os.makedirs('search_results', exist_ok=True)
    
    # Initialize searcher
    print("\nInitializing document searcher...")
    searcher = DocumentSearcher()
    
    while True:
        # Get user query
        query = input("\nEnter your search query (or 'quit' to exit): ")
        
        if query.lower() == 'quit':
            print("Thank you for using the document searcher!")
            break
            
        print("\nSearching documents...")
        result = searcher.search_with_claude(query)
        
        # Display results
        print("\nSearch Results:")
        print("-" * 80)
        print(result)
        print("-" * 80)
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"search_results/search_{timestamp}.txt"
        
        try:
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"Query: {query}\n\n")
                f.write(result)
            print(f"\nResults saved to: {result_file}")
        except Exception as e:
            print(f"\nError saving results: {str(e)}")

if __name__ == "__main__":
    main()