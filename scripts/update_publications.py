#!/usr/bin/env python3
"""
Script to update publication status based on email notifications
and update the academic homepage accordingly.
"""

import os
import re
from datetime import datetime

class PublicationUpdater:
    def __init__(self):
        self.publications_dir = "_publications"
        self.homepage_file = "index.html"
        
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
    
    def update_publication_status(self, publication_file, new_status, venue=None):
        """Update publication status in the markdown file"""
        metadata = self.parse_publication_file(publication_file)
        if not metadata:
            print(f"Could not parse {publication_file}")
            return False
            
        # Read the full file
        with open(publication_file, 'r') as f:
            content = f.read()
            
        # Update venue field
        if venue:
            venue_pattern = r'venue:\s*"[^"]*"'
            new_venue = f'venue: "{venue}"'
            content = re.sub(venue_pattern, new_venue, content)
            
        # Add or update status field
        status_pattern = r'status:\s*"[^"]*"'
        if re.search(status_pattern, content):
            content = re.sub(status_pattern, f'status: "{new_status}"', content)
        else:
            # Insert after title
            title_pattern = r'title:\s*"[^"]*"'
            content = re.sub(title_pattern, f'title: "{metadata.get("title", "")}"\nstatus: "{new_status}"', content)
            
        # Write updated content
        with open(publication_file, 'w') as f:
            f.write(content)
            
        print(f"Updated {publication_file} with status: {new_status}")
        return True
    
    def generate_publication_summary(self):
        """Generate a summary of all publications"""
        publications = []
        
        for filename in os.listdir(self.publications_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(self.publications_dir, filename)
                metadata = self.parse_publication_file(filepath)
                if metadata:
                    publications.append(metadata)
                    
        # Sort by date
        publications.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return publications

if __name__ == "__main__":
    updater = PublicationUpdater()
    
    # Example usage
    print("Publication Status Updater")
    print("=" * 50)
    
    publications = updater.generate_publication_summary()
    print(f"\nFound {len(publications)} publications:")
    
    for pub in publications:
        print(f"- {pub.get('title', 'Unknown')} ({pub.get('date', 'Unknown')})")
        print(f"  Status: {pub.get('status', 'Unknown')}")
        print(f"  Venue: {pub.get('venue', 'Unknown')}")
        print()