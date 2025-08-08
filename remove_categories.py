#!/usr/bin/env python3
"""
Script to remove all .category lines from battle_moves.h
"""

import re

def remove_category_lines():
    file_path = "src/data/battle_moves.h"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove lines containing .category
    lines = content.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Skip lines that contain .category
        if '.category' not in line:
            filtered_lines.append(line)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(filtered_lines))
    
    print("Removed all .category lines from battle_moves.h")

if __name__ == "__main__":
    remove_category_lines()
