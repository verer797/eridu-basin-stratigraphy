#!/usr/bin/env python3
"""
Validate organic content data in the Eridu Basin stratigraphy dataset.
Cross-references the CSV data with the organic material master list.
"""

import csv
import json
import sys
from pathlib import Path

def main():
    # Paths relative to repository root
    data_dir = Path(__file__).parent.parent / 'data'
    csv_path = data_dir / 'eridu_basin_stratigraphy.csv'
    json_path = data_dir / 'organic_material_master_list.json'
    
    # Load master list
    with open(json_path, 'r') as f:
        master_list = json.load(f)
    
    # Load CSV data
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Identify inconsistencies
    inconsistencies = []
    for row in rows:
        sample_id = row['SampleID']
        organic_content = row['OrganicContent']
        if sample_id in master_list and organic_content == 'Undetermined':
            expected = master_list[sample_id]
            inconsistencies.append({
                'SampleID': sample_id,
                'current': organic_content,
                'expected': expected
            })
    
    # Print report
    if inconsistencies:
        print("Found inconsistencies:")
        for inc in inconsistencies:
            print(f"  Sample {inc['SampleID']}: CSV says '{inc['current']}', master list expects '{inc['expected']}'")
        sys.exit(1)
    else:
        print("No inconsistencies found.")
        sys.exit(0)

if __name__ == '__main__':
    main()