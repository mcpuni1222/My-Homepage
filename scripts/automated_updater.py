#!/usr/bin/env python3
"""
Automated publication updater that combines email parsing with publication updates
"""

import os
import re
from datetime import datetime

class AutomatedUpdater:
    def __init__(self):
        self.publications_dir = "_publications"
        self.email_parser = EmailParser()  # This will be imported
        
    def parse_publication_file(self, filepath):
        """Parse a publication markdown file and extract metadata"""
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Extract YAML frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return None
            
        frontmatter = frontmatter_match.group(1)
        
        # Parse key-value pairs
        metadata = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')
                
        return metadata
    
    def update_publication_from_email(self, publication_file, email_data):
        """Update publication based on email information"""
        metadata = self.parse_publication_file(publication_file)
        if not metadata:
            return False
            
        # Read the full file
        with open(publication_file, 'r') as f:
            content = f.read()
            
        updated = False
        
        # Check if email indicates acceptance
        for email in email_data:
            email_parsed = self.email_parser.parse_email_subject(email['subject'])
            
            # Look for conference in publication title
            pub_title_lower = metadata.get('title', '').lower()
            for conference in email_parsed['conferences']:
                if conference.lower() in pub_title_lower:
                    # Update venue with conference info
                    venue_pattern = r'venue:\s*"[^"]*"'
                    new_venue = f'venue: "{email_parsed["subject"]}"'
                    content = re.sub(venue_pattern, new_venue, content)
                    
                    # Add status field
                    status_pattern = r'status:\s*"[^"]*"'
                    if not re.search(status_pattern, content):
                        title_pattern = r'title:\s*"[^"]*"'
                        content = re.sub(title_pattern, f'title: "{metadata.get("title", "")}"\nstatus: "{email_parsed["status"]}"', content)
                    
                    updated = True
                    break
                    
        if updated:
            # Write updated content
            with open(publication_file, 'w') as f:
                f.write(content)
                
            print(f"Updated {publication_file} based on email: {email_data[0]['subject']}")
            
        return updated
    
    def generate_report(self, email_data):
        """Generate a report of potential updates"""
        print("\nPotential Publication Updates")
        print("=" * 50)
        
        publications = []
        for filename in os.listdir(self.publications_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(self.publications_dir, filename)
                metadata = self.parse_publication_file(filepath)
                if metadata:
                    publications.append(metadata)
        
        for pub in publications:
            pub_title = pub.get('title', '')
            print(f"\nPublication: {pub_title}")
            print(f"Date: {pub.get('date', 'Unknown')}")
            
            # Check if any email mentions this conference
            for email in email_data:
                email_parsed = self.email_parser.parse_email_subject(email['subject'])
                pub_title_lower = pub_title.lower()
                
                for conference in email_parsed['conferences']:
                    if conference.lower() in pub_title_lower:
                        print(f"  → Email: {email['subject']}")
                        print(f"  → Status: {email_parsed['status']}")
                        print(f"  → Action: Update venue and status")

if __name__ == "__main__":
    updater = AutomatedUpdater()
    
    # Sample email data (in real scenario, this would come from email system)
    sample_emails = [
        {
            'subject': '[COLM 2025] Camera-Ready Submission Portal Now Open',
            'date': 'Fri, 14 Nov 2025 00:00:00 +0000'
        },
        {
            'subject': '[COAI 2025] Camera-Ready Instructions for Accepted Papers',
            'date': 'Thu, 13 Nov 2025 20:00:00 +0000'
        }
    ]
    
    print("Automated Publication Updater")
    print("=" * 50)
    
    # Generate report
    updater.generate_report(sample_emails)
    
    print("\nNote: In a real implementation, this would automatically update publication files.")