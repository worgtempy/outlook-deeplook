import win32com.client
import pythoncom
import os
from datetime import datetime
from typing import Dict, Any, List
import anthropic
from config import (PROJECT_MAPPING, DOCUMENT_TYPES, 
                   REFERENCE_PATTERNS, DEPARTMENT_MAPPING)

class OutlookDeepLook:
    def __init__(self, use_claude: bool = False, claude_api_key: str = None):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "outlook_deeplook")
        self.results_dir = os.path.join(self.base_dir, f"search_results_{self.timestamp}")
        self.use_claude = use_claude
        self.claude_api_key = claude_api_key
        self._setup_environment()
        
    def _setup_environment(self):
        """Initialize directories and Outlook connection"""
        os.makedirs(self.results_dir, exist_ok=True)
        
        try:
            pythoncom.CoInitialize()
            self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            self.inbox = self.outlook.GetDefaultFolder(6)
            print("✓ Connected to Outlook")
        except Exception as e:
            print(f"✗ Connection error: {str(e)}")
            raise

    def search_emails(self, query: str, project_code: str = None, max_results: int = 50):
        """Search emails with advanced filtering"""
        print(f"\nSearching for: '{query}'")
        results = []
        
        try:
            # Build search filter
            filter_string = f"@SQL=\"urn:schemas:httpmail:textdescription\" LIKE '%{query}%'"
            if project_code and project_code in PROJECT_MAPPING:
                project_aliases = PROJECT_MAPPING[project_code]['aliases']
                alias_filter = " OR ".join([f"'%{alias}%'" for alias in project_aliases])
                filter_string += f" AND (@SQL=\"urn:schemas:httpmail:subject\" LIKE {alias_filter})"
            
            messages = self.inbox.Items.Restrict(filter_string)
            messages.Sort("[ReceivedTime]", True)
            
            for idx, message in enumerate(messages):
                if idx >= max_results:
                    break
                    
                email_data = self._process_email(message)
                if email_data:
                    results.append(email_data)
                    
            return self._analyze_results(results, query)
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []

    def _process_email(self, message) -> Dict[str, Any]:
        """Process email with document pattern recognition"""
        try:
            email_data = {
                'subject': message.Subject,
                'sender': message.SenderEmailAddress,
                'received': str(message.ReceivedTime),
                'body': message.Body[:500],
                'project_code': None,
                'document_type': None,
                'reference_number': None
            }
            
            # Identify project code
            for code, project in PROJECT_MAPPING.items():
                if any(alias in message.Subject.upper() for alias in project['aliases']):
                    email_data['project_code'] = code
                    break
                    
            # Identify document type
            for doc_type, patterns in DOCUMENT_TYPES.items():
                if any(prefix in message.Subject.upper() for prefix in patterns['prefixes']):
                    email_data['document_type'] = doc_type
                    break
                    
            return email_data
            
        except Exception as e:
            print(f"Error processing email: {str(e)}")
            return None