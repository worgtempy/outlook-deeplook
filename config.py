# config.py

## Project Code Mappings - Final Version
PROJECT_MAPPING = {
    'PD000': {
        'name': 'General Projects',
        'aliases': [
            'GEN', 
            'GENERAL',
            'PD000 - GENERAL PROJECTS'
        ]
    },
    'PD001': {
        'name': 'Movenpick Hotel & Spa and Oceana Residences',
        'aliases': [
            'MOV', 'OCEANA', 'OHA', 'DUKES',
            'Oceana Dukes Hotel & Apartments',
            'STL36', 'OCEANA DUKES',
            'PD001-Oceana',
            'STL036 - OCEANA HOTEL and APARTMENTS'
        ]
    },
    'PD002': {
        'name': 'Anantara Palm Jumeirah and Tiara Residences',
        'aliases': [
            'ANANTARA PALM', 'TIARA', 'WI', 'WORLD ISLANDS',
            'PD002-Tiara',
            'STL035 - ANANTARA WORLD ISLANDS DUBAI'
        ]
    },
    'PD003': {
        'name': 'The Royal Amwaj Resort & Spa',
        'aliases': [
            'AMWAJ', 'ROYAL', 'ROYAL AMWAJ',
            'PD003-ROYAL AMWAJ RESORT and SPA',
            'Royal Amwaj'
        ]
    },
    'PD004': {
        'name': 'Anantara Jumeirah Lake and Jumeirah Lake Apartments',
        'aliases': [
            'ANANTARA JLT', 
            'JLT', 
            'GOLF VIEWS LIMITED',
            'Jumeirah Lake Apartments and Offices',
            'PD004 - JLT (Old)',
            'JLT Villa 13',
            'JLT Villa 13 (Chairman Villa)'
        ]
    },
    'PD005': {
        'name': 'Alkhawaneej',
        'aliases': [
            'PD005-Alkhawaneej',
            'KHAWANEEJ'
        ]
    },
    'PD006': {
        'name': 'Movenpick Deira and The Centre Residences',
        'aliases': [
            'MOVENPICK DEIRA', 
            'DEIRA',
            'PD006-The Center Residence',
            'The Centre Residence Deira'
        ]
    },
    'PD009': {
        'name': 'Ibn Battuta Hotel & Spa and Gate Offices',
        'aliases': [
            'IBG',
            'IBGOB',
            'IBGHR',
            'IBGRB',
            'OIBG',
            'IBN BATTUTA',
            'IBGH',
            'IBGO',
            'IBN BATTUTA GATE',
            'IBN BATTUTA HOTEL',
            'IBN BATTUTA OFFICES',
            'IBG Hotel and Residences',
            'IBG Office',
            'IBG Robotic',
            'Ibn Battuta Oaks Hotel Building'
        ]
    },
    'PD00A': {
        'name': 'General Material Suppliers',
        'aliases': ['GMS', 'SUPPLIERS']
    },
    'PD012': {
        'name': 'DEC Residential Towers & Retail Complex',
        'aliases': ['DEC', 'DEC TOWERS']
    },
    'PD013': {
        'name': 'Robinson Club & Iberotel Hotels',
        'aliases': ['ROBINSON', 'IBEROTEL']
    },
    'PD015': {
        'name': 'Dubai Tiara Towers',
        'aliases': ['TIARA', 'DTT']
    },
    'PD016': {
        'name': 'Zabeel Investments Hotel Tower',
        'aliases': ['ZABEEL', 'ZIHT']
    },
    'PD017': {
        'name': 'Blue City',
        'aliases': ['PD017-Blue City']  # Corrected from PD0017
    },
    'PD031': {
        'name': 'Seven Hotel and Apartments',
        'aliases': [
            'SHA', 'P220', 'SEVEN HOTEL', 'PLOT P-220',
            'STRED001 - SEVEN HOTEL & APARTMENTS'
        ]
    },
    'PD037': {
        'name': 'Rahala Residences',
        'aliases': [
            'RAHALA',
            'STL037 - RAHALA RESIDENCES'
        ]
    },
    '7CJLT': {
        'name': 'Seven City JLT',
        'aliases': [
            'SEVEN CITY', 
            'GOLF VIEWS', 
            'GOLF VIEWS SEVEN CITY',
            'STRED002 - SEVEN CITY JLT'
        ]
    },
    'DHSB': {
        'name': 'Dubai Heights School Building',
        'aliases': [
            'DUBAI HEIGHTS ACADEMY', 
            'DHA',
            'STL00 - DUBAI HEIGHTS ACADEMY'
        ]
    }
}


# Document Type Patterns
DOCUMENT_TYPES = {
    # Core Documents
    'Letter': {
        'prefixes': ['LOA', 'LOI', 'LOP', 'LOW', 'LEM', 'LOR', 'LTR'],
        'keywords': ['Letter', 'Correspondence']
    },
    'Agreement': {
        'prefixes': ['SA', 'MSA', 'NDA', 'MOU', 'MOA', 'AMC'],
        'keywords': ['Agreement', 'Contract', 'Settlement']
    },
    'Minutes': {
        'prefixes': ['MOM', 'MOD', 'MOR'],
        'keywords': ['Minutes', 'Meeting']
    },
    'Email': {
        'prefixes': ['EMAIL'],
        'keywords': ['Email', 'Correspondence']
    },
    'Fax': {
        'prefixes': ['FAX'],
        'keywords': ['Fax', 'Facsimile']
    }
}

# Document Status
STATUS_TYPES = [
    'Original',
    'Copy',
    'Draft',
    'Final',
    'Expired'
]

# Department/Entity Mappings
DEPARTMENT_MAPPING = {
    'STRED': {
        'name': 'Seven Tides Real Estate Department',
        'aliases': ['STRE', 'STR']
    },
    'STOAM': {
        'name': 'Seven Tides Owner Association Management',
        'aliases': ['STO', 'ST-OAM']
    },
    'SASBS': {
        'name': 'Sultan Ahmed Sultan Bin Sulayem',
        'aliases': ['SAS', 'SASBSI']
    },
    'BSI': {
        'name': 'Bin Sulayem Investment',
        'aliases': ['BSIL', 'BS-INV']
    },
    'ABS': {
        'name': 'Abdullah Bin Sulayem',
        'aliases': ['ABSI', 'ABDULLAH']
    },
    'GBS': {
        'name': 'Ghanim Bin Sulayem',
        'aliases': ['GBSI', 'GHANIM', 'GHANAM', 'GHANEM']
    },
    'CAD': {
        'name': 'CAD Department',
        'aliases': ['CADD']
    },
    'HRA': {
        'name': 'Human Resources',
        'aliases': ['HR']
    },
    'FIN': {
        'name': 'Finance',
        'aliases': ['FXH', 'Financial']
    },
    'PRP': {
        'name': 'Property',
        'aliases': ['Property']
    },
    'ENG': {
        'name': 'Engineering',
        'aliases': ['ENGG']
    }
}

# Reference Patterns
REFERENCE_PATTERNS = {
    'standard': [
        r'(\d+)PD[-_](\d{4})',          # e.g., 340PD-2017
        r'[A-Z]+[-_](\d+)PD[-_](\d{4})', # e.g., SHA-340PD-2017
        r'[A-Z]+/[A-Z]+/\d+[-_](\d{4})'  # e.g., ST/AS/0426-2013
    ],
    
    'department_project': [
        r'STRED[-_][A-Z]+[-_][A-Z]+[-_][A-Z]+[-_]\d+PD[-_]\d{4}',  # e.g., STRED-NKHL-GBS-SHA-305PWB-21PD-2023
        r'STOAM[-_][A-Z]+[-_][A-Z]+[-_]\d+PD[-_]\d{4}',            # e.g., STOAM-SI_ABS_OR-01PD-20
        r'STL[-_][A-Z]+[-_][A-Z]+[-_][A-Z]+[-_]\d+[-_]\d{4}'       # e.g., STL-EME_ABS_OHA-340PD-2017
    ],
    
    'letter_references': [
        r'LOA[-_][A-Z]+[-_][A-Z]+[-_][A-Z]+[-_]\d+PD[-_]\d{4}',    # e.g., LOA-DHA-ASTECO-ABS-DHSB-04PD-2024
        r'LTR[-_][A-Z]+[-_]\d+[-_]\d{4}'                           # e.g., LTR-DEPT-001-2024
    ],
    
    'special_formats': [
        r'terminated letter ref\. no\. .*?(\d+PD[-_]\d{4})',
        r'Response to Letter Ref\. .*?(\d+PD[-_]\d{4})',
        r'STRED Letter No[-_](\d+PD[-_]\d{4})'
    ]
}

# Document Name Patterns
FILENAME_PATTERNS = {
    'dept_project': '',
    'project_ref': '',
    'letter_ref': '',
    'pwb_ref': ''
}

# Location/Building Codes
LOCATION_CODES = {
    'JLT': ''
}

# Document Controller Codes
CONTROLLER_CODES = {
    'ENG': ''
}

# Government Department References
GOVT_DEPT_CODES = {
    'DLD': ''
}

# Document Status Types
STATUS_TYPES = []

# Common Reference Prefixes
REFERENCE_PREFIXES = {
    'Project': [],
    'Department': [],
    'Document': []
}

# Special Document References
SPECIAL_REFERENCES = {
    'terminated': [],
    'response': [],
    'stred_letter': []
}

# Project Relationships
PROJECT_RELATIONSHIPS = {
    'PD031': {
        'related_codes': [],
        'sub_projects': []
    }
}

# Document Categories
DOCUMENT_CATEGORIES = {
    'Property': [],
    'Legal': [],
    'Technical': [],
    'Commercial': []
}

# Business Units
BUSINESS_UNITS = {
    'name': '',
    'departments': [],
    'codes': []
}

# Document Flow Types
DOCUMENT_FLOW = {
    'standard': [],
    'special': [],
    'terminated': []
}