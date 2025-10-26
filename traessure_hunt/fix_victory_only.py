#!/usr/bin/env python3
"""Fix only victory screen indentation"""

with open('final2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line after "rank, subtitle = get_rank()" and before "# Footer"
rank_line = -1
footer_line = -1

for i, line in enumerate(lines):
    if 'rank, subtitle = get_rank()' in line and i > 1590:
        rank_line = i
        print(f"Found rank line at {i+1}")
    if '# Footer' in line and i > 1900:
        footer_line = i
        print(f"Found footer at {i+1}")
        break

if rank_line == -1 or footer_line == -1:
    print("Could not find markers!")
    exit(1)

# Add 4 spaces to lines from rank_line+2 to footer (to get them to 8 total)
start = rank_line + 2  # Skip blank line after rank assignment
fixed_lines = []

for i, line in enumerate(lines):
    if i >= start and i < footer_line:
        # Only add 4 spaces if line currently has 4 spaces (not already 8)
        if line.startswith('    ') and not line.startswith('        ') and line.strip():
            fixed_lines.append('    ' + line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('final2.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"Fixed indentation from line {start+1} to {footer_line}")
print("Done!")
