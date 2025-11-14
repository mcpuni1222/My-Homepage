#!/bin/bash
# Run the integrated publication updater test

echo "Running Integrated Publication Updater Test"
echo "=========================================="

python3 scripts/test_integrated_updater.py

echo ""
echo "Test completed!"
echo ""
echo "Check the output above to see which publications were updated."