#!/usr/bin/env python3
"""
Email parser to extract publication acceptance information from conference emails
"""

import re
from datetime import datetime

class EmailParser:
    def __init__(self):
        self.conference_keywords = [
            'camera-ready',
            'accepted',
            'oral presentation',
            'conference',
            'journal',
            'workshop'
        ]
        
    def parse_email_subject(self, subject):
        """Extract conference and status information from email subject"""
        subject_lower = subject.lower()
        
        # Look for conference names
        conferences = []
        if 'colm' in subject_lower:
            conferences.append('COLM 2025')
        elif 'coai' in subject_lower:
            conferences.append('COAI 2025')
        elif 'coml' in subject_lower:
            conferences.append('COML 2025')
        elif 'lcfm' in subject_lower:
            conferences.append('LCFM 2025')
        elif 'icsbe' in subject_lower:
            conferences.append('ICSBE 2025')
            
        # Determine status
        status = 'pending'
        if 'accepted' in subject_lower:
            status = 'accepted'
        elif 'camera-ready' in subject_lower:
            status = 'camera-ready'
        elif 'oral' in subject_lower:
            status = 'oral_presentation'
            
        return {
            'conferences': conferences,
            'status': status,
            'subject': subject
        }
    
    def extract_conference_info(self, email_content):
        """Extract conference information from email body"""
        info = {}
        
        # Look for conference deadlines
        deadline_patterns = [
            r'deadline[:\s]*([^\n]+)',
            r'closing[:\s]*([^\n]+)',
            r'reminder[:\s]*([^\n]+)'
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, email_content, re.IGNORECASE)
            if match:
                info['deadline'] = match.group(1).strip()
                break
                
        # Look for conference dates
        date_pattern = r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})'
        date_match = re.search(date_pattern, email_content)
        if date_match:
            info['date'] = date_match.group(1)
            
        return info
    
    def generate_publication_updates(self, email_data):
        """Generate publication updates based on email data"""
        updates = []
        
        for email in email_data:
            parsed = self.parse_email_subject(email['subject'])
            
            if parsed['conferences']:
                for conference in parsed['conferences']:
                    update = {
                        'conference': conference,
                        'status': parsed['status'],
                        'email_subject': email['subject'],
                        'date': email.get('date', ''),
                        'notes': f"Based on email: {email['subject']}"
                    }
                    updates.append(update)
                    
        return updates

if __name__ == "__main__":
    parser = EmailParser()
    
    # Test with sample email data
    test_emails = [
        {
            'subject': '[COLM 2025] Camera-Ready Submission Portal Now Open',
            'date': 'Fri, 14 Nov 2025 00:00:00 +0000'
        },
        {
            'subject': '[COAI 2025] Camera-Ready Instructions for Accepted Papers',
            'date': 'Thu, 13 Nov 2025 20:00:00 +0000'
        }
    ]
    
    updates = parser.generate_publication_updates(test_emails)
    
    print("Email Parser Test Results")
    print("=" * 50)
    for update in updates:
        print(f"Conference: {update['conference']}")
        print(f"Status: {update['status']}")
        print(f"Notes: {update['notes']}")
        print()