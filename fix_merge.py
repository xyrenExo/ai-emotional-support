#!/usr/bin/env python3
# Script to fix the merge conflict in package-lock.json

file_path = r'c:\Users\XyrenExo\Desktop\AI_Counselling\emotional-support-ai\frontend\package-lock.json'

# Read all lines
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep only first 7052 lines (the correct version)
fixed_lines = lines[:7052]

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"File fixed! Kept first 7052 lines. Total lines now: {len(fixed_lines)}")
