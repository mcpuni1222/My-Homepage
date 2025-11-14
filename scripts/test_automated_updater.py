#!/usr/bin/env python3
"""
Test the automated publication updater
"""

import sys
import os

# Add scripts directory to path
sys.path.append(os.path.dirname(__file__))

from automated_updater import AutomatedUpdater

def test_automated_updater():
    updater = AutomatedUpdater()
    
    # Sample email data
    sample_emails = [
        {
            'subject': '[COLM 2025] Camera-Ready Submission Portal Now Open',
            'date': 'Fri, 14 Nov 2025 00:00:00 +0000'
        },
        {
            'subject': '[COAI 2025] Camera-Ready Instructions for Accepted Papers',
            'date': 'Thu, 13 Nov 2025 20:00:00 +0000'
        },
        {
            'subject': '[COML 2025] Camera-ready submission reminder',
            'date': 'Wed, 12 Nov 2025 03:00:00 +0000'
        }
    ]
    
    print("Testing Automated Publication Updater")
    print("=" * 50)
    
    # Generate report
    updater.generate_report(sample_emails)
    
    # Show current publication status
    print("\nCurrent Publication Status:")
    print("-" * 30)
    
    publications = []
    for filename in os.listdir(updater.publications_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(updater.publications_dir, filename)
            metadata = updater.parse_publication_file(filepath)
            if metadata:
                publications.append(metadata)
    
    for pub in publications:
        print(f"{pub.get('title', 'Unknown')}")
        print(f"  Date: {pub.get('date', 'Unknown')}")
        print(f"  Venue: {pub.get('venue', 'Unknown')}")
        print()

if __name__ == "__main__":
    test_automated_updater()