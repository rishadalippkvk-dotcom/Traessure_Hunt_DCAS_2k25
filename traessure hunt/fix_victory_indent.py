#!/usr/bin/env python3
"""Fix victory screen indentation"""

with open('final2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the else: line for victory screen (around line 1594)
else_line_idx = -1
footer_line_idx = -1

for i, line in enumerate(lines):
    if line.strip() == 'else:' and i > 1590 and i < 1600:
        if i > 0 and 'VICTORY SCREEN' in lines[i-1]:
            else_line_idx = i
            print(f"Found else at line {i+1}")
            break

# Find footer
for i in range(len(lines)-1, -1, -1):
    if lines[i].strip().startswith('# Footer'):
        footer_line_idx = i
        print(f"Found footer at line {i+1}")
        break

if else_line_idx == -1:
    print("Could not find else line!")
    exit(1)

# Everything from else_line_idx+3 (after rank, subtitle = get_rank()) to footer needs 4 more spaces
start_indent = else_line_idx + 3  # Skip else, elapsed=, rank=
end_indent = footer_line_idx

print(f"Will indent lines {start_indent+1} to {end_indent}")

fixed_lines = []
for i, line in enumerate(lines):
    if i > start_indent and i < end_indent:
        # Add 4 spaces if not empty
        if line.strip():
            fixed_lines.append('    ' + line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('final2.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Victory screen indentation fixed!")
