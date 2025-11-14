#!/usr/bin/env python3
"""
Debug the integrated publication updater
"""

import os
import re

class DebugUpdater:
    def __init__(self):
        self.publications_dir = "_publications"
        
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
    
    def debug_conference_extraction(self, title):
        """Debug conference extraction from title"""
        print(f"Debugging title: '{title}'")
        
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
                print(f"  Found conference: {conference}")
                return conference
                
        print(f"  No conference found")
        return None
    
    def debug_email_matching(self, email_subject, conference):
        """Debug email matching logic"""
        print(f"\nDebugging email: '{email_subject}'")
        print(f"Conference to match: {conference}")
        
        email_lower = email_subject.lower()
        
        # Check if email mentions this conference
        if conference.lower() in email_lower:
            print(f"  ✓ Email mentions conference")
            
            # Determine status from email
            email_keywords = {
                'camera-ready': 'camera_ready',
                'accepted': 'accepted',
                'oral presentation': 'oral_presentation',
                'oral': 'oral_presentation'
            }
            
            status = 'pending'
            for keyword, status_value in email_keywords.items():
                if keyword in email_lower:
                    status = status_value
                    print(f"  Status determined: {status}")
                    break
            else:
                print(f"  Status remains: {status}")
                
            return status
            
        else:
            print(f"  ✗ Email does not mention conference")
            return None

def debug_test():
    updater = DebugUpdater()
    
    # Test with actual publication
    publication_file = "_publications/2025-06-01-ipsum-lorem-all-you-need.md"
    metadata = updater.parse_publication_file(publication_file)
    
    if metadata:
        title = metadata.get('title', '')
        print(f"Publication: {title}")
        
        # Debug conference extraction
        conference = updater.debug_conference_extraction(title)
        
        # Test with actual email subjects
        actual_emails = [
            "[COLM 2025] Camera-Ready Submission Portal Now Open",
            "[COAI 2025] Camera-Ready Instructions for Accepted Papers", 
            "[COML 2025] Camera-ready deadline reminder",
            "[COML 2025] Reminder: Video recording deadline approaching",
            "[COML 2025] Oral presentation notification",
            "[COML 2025] Camera-ready submission reminder"
        ]
        
        for email in actual_emails:
            status = updater.debug_email_matching(email, conference)
            if status:
                print(f"\nWould update with status: {status}")
                break
        else:
            print(f"\nNo matching email found for this publication")

if __name__ == "__main__":
    debug_test()