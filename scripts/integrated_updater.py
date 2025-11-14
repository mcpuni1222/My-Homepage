#!/usr/bin/env python3
"""
Integrated publication updater that combines email analysis with publication updates
"""

import os
import re
from datetime import datetime

class IntegratedUpdater:
    def __init__(self):
        self.publications_dir = "_publications"
        self.email_keywords = {
            'camera-ready': 'camera_ready',
            'accepted': 'accepted',
            'oral presentation': 'oral_presentation',
            'oral': 'oral_presentation'
        }
        
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
    
    def extract_conference_from_title(self, title):
        """Extract conference name from publication title"""
        title_lower = title.lower()
        
        conferences = {
            'icml': 'ICML 2025',
            'neurips': 'NeurIPS 2025', 
            'colm': 'COLM 2025',
            'coai': 'COAI 2025',
            'coml': 'COML 2025',
            'lcfm': 'LCFM 2025',
            'icsbe': 'ICSBE 2025'
        }
        
        for keyword, conference in conferences.items():
            if keyword in title_lower:
                return conference
                
        return None
    
    def update_publication_based_on_email(self, publication_file, email_subject):
        """Update publication based on email subject"""
        metadata = self.parse_publication_file(publication_file)
        if not metadata:
            return False
            
        # Extract conference from publication title
        conference = self.extract_conference_from_title(metadata.get('title', ''))
        if not conference:
            return False
            
        # Check if email mentions this conference
        email_lower = email_subject.lower()
        if conference.lower() not in email_lower:
            return False
            
        # Determine status from email
        status = 'pending'
        for keyword, status_value in self.email_keywords.items():
            if keyword in email_lower:
                status = status_value
                break
                
        # Read the full file
        with open(publication_file, 'r') as f:
            content = f.read()
            
        updated = False
        
        # Update venue field
        venue_pattern = r'venue:\s*"[^"]*"'
        if re.search(venue_pattern, content):
            # Extract current venue
            current_venue_match = re.search(venue_pattern, content)
            if current_venue_match:
                current_venue = current_venue_match.group(0).split('"')[1]
                
                # Only update if status has changed
                if status == 'accepted' and 'accepted' not in current_venue.lower():
                    new_venue = f'venue: "Accepted at {conference}"'
                    content = re.sub(venue_pattern, new_venue, content)
                    updated = True
                elif status == 'camera_ready' and 'camera-ready' not in current_venue.lower():
                    new_venue = f'venue: "Camera-ready for {conference}"'
                    content = re.sub(venue_pattern, new_venue, content)
                    updated = True
                    
        # Add status field if not present
        status_pattern = r'status:\s*"[^"]*"'
        if not re.search(status_pattern, content):
            title_pattern = r'title:\s*"[^"]*"'
            if re.search(title_pattern, content):
                content = re.sub(title_pattern, f'title: "{metadata.get("title", "")}"\nstatus: "{status}"', content)
                updated = True
                
        if updated:
            # Write updated content
            with open(publication_file, 'w') as f:
                f.write(content)
                
            print(f"✓ Updated {metadata.get('title', 'Unknown')} -> Status: {status}")
            
        return updated
    
    def scan_and_update_publications(self, email_subjects):
        """Scan all publications and update based on email subjects"""
        print("Scanning publications for updates...")
        print("=" * 50)
        
        updated_count = 0
        
        for filename in os.listdir(self.publications_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(self.publications_dir, filename)
                
                for email_subject in email_subjects:
                    if self.update_publication_based_on_email(filepath, email_subject):
                        updated_count += 1
                        break
                        
        print(f"\nSummary: Updated {updated_count} publications")
        return updated_count

if __name__ == "__main__":
    updater = IntegratedUpdater()
    
    # Sample email subjects (in real scenario, this would come from email system)
    sample_emails = [
        "[COLM 2025] Camera-Ready Submission Portal Now Open",
        "[COAI 2025] Camera-Ready Instructions for Accepted Papers", 
        "[COML 2025] Camera-ready submission reminder",
        "[COML 2025] Oral presentation notification"
    ]
    
    print("Integrated Publication Updater")
    print("=" * 50)
    
    # Scan and update
    updated_count = updater.scan_and_update_publications(sample_emails)
    
    print(f"\nProcess completed. {updated_count} publications were updated.")