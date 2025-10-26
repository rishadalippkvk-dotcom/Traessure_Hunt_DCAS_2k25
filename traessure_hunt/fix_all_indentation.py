#!/usr/bin/env python3
"""Complete indentation fix for the entire game after login check"""

with open('final2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find key markers:
# 1. Line with "# Animated Title" - start of game content that needs indenting
# 2. Line with "# Footer" - end of game content

game_start = -1
footer_line = -1

for i, line in enumerate(lines):
    if '# Animated Title' in line and i > 1240:
        game_start = i
        print(f"Found game start at line {i+1}: {line.strip()}")
    if '# Footer' in line and i > 1900:
        footer_line = i
        print(f"Found footer at line {i+1}: {line.strip()}")
        break

if game_start == -1 or footer_line == -1:
    print("Could not find markers!")
    print(f"game_start: {game_start}, footer_line: {footer_line}")
    exit(1)

# Add 4 spaces to all lines from game_start to footer_line+3 (to include footer content)
fixed_lines = []
for i, line in enumerate(lines):
    if i >= game_start and i <= footer_line + 3:
        # Add 4 spaces if line is not empty
        if line.strip():
            fixed_lines.append('    ' + line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('final2.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"Added 4 spaces to lines {game_start+1} through {footer_line+4}")
print("Complete indentation fixed!")
