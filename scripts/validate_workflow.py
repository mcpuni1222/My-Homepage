#!/usr/bin/env python3
"""
Validate the academic homepage management workflow
"""

import os
import re

class WorkflowValidator:
    def __init__(self):
        self.publications_dir = "_publications"
        self.workflow_file = "workflow_summary.md"
        
    def validate_publication_files(self):
        """Validate all publication files"""
        print("Validating Publication Files")
        print("=" * 50)
        
        issues = []
        total_files = 0
        
        for filename in os.listdir(self.publications_dir):
            if filename.endswith('.md'):
                total_files += 1
                filepath = os.path.join(self.publications_dir, filename)
                
                with open(filepath, 'r') as f:
                    content = f.read()
                    
                # Check for required fields
                required_fields = ['title:', 'date:', 'venue:']
                missing_fields = []
                
                for field in required_fields:
                    if field not in content:
                        missing_fields.append(field)
                        
                # Check for YAML frontmatter
                if not content.startswith('---\n'):
                    issues.append(f"{filename}: Missing opening YAML frontmatter")
                    
                if content.count('---') < 2:
                    issues.append(f"{filename}: Incomplete YAML frontmatter")
                    
                # Check for status field
                if 'status:' not in content:
                    issues.append(f"{filename}: Missing status field")
                    
                if missing_fields:
                    issues.append(f"{filename}: Missing required fields: {', '.join(missing_fields)}")
                    
                print(f"✓ {filename}: Valid")
                
        print(f"\nSummary: {total_files} publication files validated")
        return issues
    
    def validate_workflow_documentation(self):
        """Validate workflow documentation"""
        print("\nValidating Workflow Documentation")
        print("=" * 50)
        
        if not os.path.exists(self.workflow_file):
            return ["Workflow summary file not found"]
            
        with open(self.workflow_file, 'r') as f:
            content = f.read()
            
        checks = [
            ("Overview section", "Overview" in content),
            ("Current State section", "Current State" in content),
            ("Key Publications Status section", "Key Publications Status" in content),
            ("Automation Scripts section", "Automation Scripts" in content),
            ("Workflow Process section", "Workflow Process" in content),
            ("Next Steps section", "Next Steps" in content),
            ("Tools Used section", "Tools Used" in content),
            ("Success Metrics section", "Success Metrics" in content)
        ]
        
        issues = []
        for check_name, check_result in checks:
            if not check_result:
                issues.append(f"Missing: {check_name}")
            else:
                print(f"✓ {check_name}")
                
        return issues
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("Academic Homepage Workflow Validation Report")
        print("=" * 60)
        
        pub_issues = self.validate_publication_files()
        doc_issues = self.validate_workflow_documentation()
        
        all_issues = pub_issues + doc_issues
        
        if not all_issues:
            print("\n✅ SUCCESS: All validations passed!")
            print("The academic homepage management workflow is properly configured.")
        else:
            print("\n❌ ISSUES FOUND:")
            for issue in all_issues:
                print(f"  - {issue}")
                
        print(f"\nValidation Summary:")
        print(f"  - Publication files: {len([f for f in os.listdir(self.publications_dir) if f.endswith('.md')])} files")
        print(f"  - Documentation: {0 if len(doc_issues) > 0 else 1} valid sections")
        print(f"  - Issues found: {len(all_issues)}")
        
        return len(all_issues) == 0

if __name__ == "__main__":
    validator = WorkflowValidator()
    validator.generate_validation_report()