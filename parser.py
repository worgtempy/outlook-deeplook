import pandas as pd
import os
import logging
import re
from datetime import datetime
from config import (PROJECT_MAPPING, DOCUMENT_TYPES, 
                   REFERENCE_PATTERNS, DEPARTMENT_MAPPING)

class DocumentParser:
    def __init__(self):
        # Initialize logging
        logging.basicConfig(
            filename='parser_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Load configurations
        self.project_mapping = PROJECT_MAPPING
        self.doc_types = DOCUMENT_TYPES
        self.ref_patterns = REFERENCE_PATTERNS
        self.dept_mapping = DEPARTMENT_MAPPING
        
        # Create output directory if doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Track processed documents to avoid duplicates
        self.processed_docs = set()

    def identify_project(self, text):
        """Identify project from text using PROJECT_MAPPING"""
        text = text.upper()  # Standardize case for matching
        
        # First try exact project code match
        for code, project in self.project_mapping.items():
            if code in text:
                return code, project['name']
            
        # Then try aliases
        for code, project in self.project_mapping.items():
            for alias in project['aliases']:
                if alias.upper() in text:
                    return code, project['name']
                    
        return 'UNCAT', 'Uncategorized'  # For documents we can't categorize

    def parse_document(self, line):
        """Parse a single document line"""
        try:
            # Split by tabs and multiple spaces
            parts = [p.strip() for p in re.split(r'\t+|\s{2,}', line) if p.strip()]
            
            if len(parts) < 4:  # Minimum required fields
                return None
                
            # Extract basic information
            doc_info = {
                'File_Name': parts[0],
                'Document_ID': parts[1] if len(parts) > 1 else '',
                'Created_Date': datetime.now().strftime('%Y-%m-%d'),
                'Last_Modified': datetime.now().strftime('%Y-%m-%d')
            }
            
            # Generate unique identifier
            doc_id = f"{doc_info['File_Name']}_{doc_info['Document_ID']}"
            
            # Skip if already processed
            if doc_id in self.processed_docs:
                return None
                
            # Identify project
            project_code, project_name = self.identify_project(line)
            doc_info['Project_Code'] = project_code
            doc_info['Project_Name'] = project_name
            
            # Add to processed set
            self.processed_docs.add(doc_id)
            
            return doc_info
            
        except Exception as e:
            logging.error(f"Error parsing line: {str(e)}\nLine: {line}")
            return None

    def process_file(self, input_file):
        """Process input file and generate outputs"""
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]

            # Process each line
            projects = {}
            uncategorized = []
            
            for line in lines[1:]:  # Skip header
                doc_info = self.parse_document(line)
                if doc_info:
                    if doc_info['Project_Code'] == 'UNCAT':
                        uncategorized.append(doc_info)
                    else:
                        if doc_info['Project_Code'] not in projects:
                            projects[doc_info['Project_Code']] = []
                        projects[doc_info['Project_Code']].append(doc_info)

            # Create individual project CSV files
            for code, docs in projects.items():
                df = pd.DataFrame(docs)
                output_file = f"output/{code}.csv"
                df.to_csv(output_file, index=False)
                logging.info(f"Created: {output_file}")

            # Create uncategorized CSV
            if uncategorized:
                df = pd.DataFrame(uncategorized)
                df.to_csv("output/UNCATEGORIZED.csv", index=False)
                logging.info("Created: output/UNCATEGORIZED.csv")

            # Create merged CSV
            all_docs = []
            for docs in projects.values():
                all_docs.extend(docs)
            all_docs.extend(uncategorized)
            
            df = pd.DataFrame(all_docs)
            df.to_csv("output/MERGED.csv", index=False)
            logging.info("Created: output/MERGED.csv")

            return True

        except Exception as e:
            logging.error(f"Error processing file: {str(e)}")
            return False

def main():
    parser = DocumentParser()
    success = parser.process_file("input.txt")
    if success:
        print("Processing complete! Check output directory for results.")
    else:
        print("Processing failed. Check parser_log.txt for details.")

if __name__ == "__main__":
    main()