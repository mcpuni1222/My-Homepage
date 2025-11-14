#!/usr/bin/env python3
"""
Test the integrated publication updater with actual email subjects
"""

import sys
import os

# Add scripts directory to path
sys.path.append(os.path.dirname(__file__))

from integrated_updater import IntegratedUpdater

def test_integrated_updater():
    updater = IntegratedUpdater()
    
    # Actual email subjects from inbox
    actual_emails = [
        "[COLM 2025] Camera-Ready Submission Portal Now Open",
        "[COAI 2025] Camera-Ready Instructions for Accepted Papers",
        "[COML 2025] Camera-ready deadline reminder",
        "[COML 2025] Reminder: Video recording deadline approaching",
        "[COML 2025] Oral presentation notification",
        "[COML 2025] Camera-ready submission reminder"
    ]
    
    print("Testing Integrated Publication Updater")
    print("=" * 50)
    
    print("\nEmail Subjects:")
    for i, email in enumerate(actual_emails, 1):
        print(f"{i}. {email}")
    
    print("\n" + "=" * 50)
    
    # Scan and update
    updated_count = updater.scan_and_update_publications(actual_emails)
    
    print(f"\nProcess completed. {updated_count} publications were updated.")
    
    # Show final status
    print("\nFinal Publication Status:")
    print("-" * 30)
    
    for filename in os.listdir(updater.publications_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(updater.publications_dir, filename)
            metadata = updater.parse_publication_file(filepath)
            if metadata:
                print(f"{metadata.get('title', 'Unknown')}")
                print(f"  Date: {metadata.get('date', 'Unknown')}")
                print(f"  Venue: {metadata.get('venue', 'Unknown')}")
                print(f"  Status: {metadata.get('status', 'Unknown')}")
                print()

if __name__ == "__main__":
    test_integrated_updater()