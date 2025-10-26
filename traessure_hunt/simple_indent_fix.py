#!/usr/bin/env python3
"""Simple script to add 4 spaces to lines that need it"""

def main():
    with open('final2.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line number where we need to start indenting
    start_indent = -1
    end_indent = -1
    
    for i, line in enumerate(lines):
        # Find the start: right after "if not st.session_state.finished:"
        if '    if not st.session_state.finished:' in line and 'GAME LOGIC' in lines[i-2]:
            start_indent = i + 1
            print(f"Found start at line {i+1}: {line.strip()}")
        
        # Find the end: The footer section
        if start_indent > 0 and line.strip().startswith('# Footer'):
            end_indent = i
            print(f"Found end at line {i+1}: {line.strip()}")
            break
    
    if start_indent == -1 or end_indent == -1:
        print("Could not find markers!")
        return
    
    # Now add 4 spaces to every non-empty line between start and end
    fixed_lines = []
    for i, line in enumerate(lines):
        if i < start_indent or i >= end_indent:
            # Outside the range, keep as is
            fixed_lines.append(line)
        else:
            # Inside the range - add 4 spaces if not empty and not already super indented
            if line.strip() == '':
                fixed_lines.append(line)
            else:
                # Add 4 spaces
                fixed_lines.append('    ' + line)
    
    # Write back
    with open('final2.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"Added 4 spaces to lines {start_indent+1} through {end_indent}")
    print("Done!")

if __name__ == '__main__':
    main()
