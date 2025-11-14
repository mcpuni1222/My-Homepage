#!/usr/bin/env python3
"""
Test script for publication updater
"""

import sys
import os

# Add scripts directory to path
sys.path.append(os.path.dirname(__file__))

from update_publications import PublicationUpdater

def test_updater():
    updater = PublicationUpdater()
    
    print("Testing Publication Updater")
    print("=" * 50)
    
    # Test parsing
    publications = updater.generate_publication_summary()
    print(f"Found {len(publications)} publications:")
    
    for pub in publications:
        print(f"- {pub.get('title', 'Unknown')} ({pub.get('date', 'Unknown')})")
        print(f"  Status: {pub.get('status', 'Unknown')}")
        print(f"  Venue: {pub.get('venue', 'Unknown')}")
        print()
    
    # Test updating a publication
    if publications:
        first_pub = publications[0]
        filename = first_pub.get('permalink', '').split('/')[-2] + '.md'
        filepath = os.path.join(updater.publications_dir, filename)
        
        if os.path.exists(filepath):
            print(f"Testing update for: {first_pub.get('title')}")
            updater.update_publication_status(
                filepath, 
                "accepted", 
                "ICML 2025 - International Conference on Machine Learning"
            )

if __name__ == "__main__":
    test_updater()