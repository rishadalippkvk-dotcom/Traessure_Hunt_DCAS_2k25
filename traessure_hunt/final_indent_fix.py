#!/usr/bin/env python3
"""Complete indentation fix for victory screen"""

with open('final2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# We need to find:
# 1. The line with "# Epic Victory Celebration" after the else: block
# 2. The footer line
# Then add 4 spaces to everything between them

victory_start = -1
footer_line = -1

for i, line in enumerate(lines):
    if '# Epic Victory Celebration' in line and i > 1590:
        victory_start = i
        print(f"Found victory start at line {i+1}")
    if '# Footer' in line and victory_start > 0:
        footer_line = i
        print(f"Found footer at line {i+1}")
        break

if victory_start == -1 or footer_line == -1:
    print("Could not find markers!")
    exit(1)

# Add 4 spaces to all lines from victory_start to footer_line (exclusive)
fixed_lines = []
for i, line in enumerate(lines):
    if i >= victory_start and i < footer_line:
        # Add 4 spaces if line is not empty
        if line.strip():
            fixed_lines.append('    ' + line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('final2.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"Added 4 spaces to lines {victory_start+1} through {footer_line}")
print("Victory screen indentation fixed!")
