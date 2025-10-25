#!/usr/bin/env python3
"""Complete fix for all indentation issues"""

with open('final2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "if not st.session_state.finished:" around line 1281
# Find the footer line
# Add 4 spaces to everything from the line after "if not st.session_state.finished:" to footer

if_not_finished_line = -1
footer_line = -1

for i, line in enumerate(lines):
    if line.strip() == 'if not st.session_state.finished:' and i > 1270 and i < 1290:
        if_not_finished_line = i
        print(f"Found 'if not finished' at line {i+1}")
    if '# Footer' in line and i > 1900:
        footer_line = i
        print(f"Found footer at line {i+1}")
        break

if if_not_finished_line == -1 or footer_line == -1:
    print("Could not find markers!")
    exit(1)

# Add 4 spaces to all lines from if_not_finished_line+1 to footer (exclusive)
start_line = if_not_finished_line + 1
fixed_lines = []

for i, line in enumerate(lines):
    if i >= start_line and i < footer_line:
        # Add 4 spaces if line is not empty
        if line.strip():
            fixed_lines.append('    ' + line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('final2.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print(f"Added 4 spaces to lines {start_line+1} through {footer_line}")
print("Complete indentation fixed!")
