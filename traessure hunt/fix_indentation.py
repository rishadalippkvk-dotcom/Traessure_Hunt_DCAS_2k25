#!/usr/bin/env python3
"""Fix indentation in final2.py"""

def fix_file():
    with open('final2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    
    # Track state
    in_else_logged_in = False
    in_if_not_finished = False
    found_else_logged_in_line = -1
    found_if_not_finished_line = -1
    footer_line = -1
    
    # First pass: find key line numbers
    for i, line in enumerate(lines):
        if 'else:' in line and i+1 < len(lines) and '# Show game (user is logged in)' in lines[i+1]:
            found_else_logged_in_line = i
        if line.strip() == 'if not st.session_state.finished:' and found_else_logged_in_line > 0 and i > found_else_logged_in_line:
            found_if_not_finished_line = i
            break
    
    # Find footer
    for i in range(len(lines)-1, -1, -1):
        if '# Footer' in lines[i]:
            footer_line = i
            break
    
    print(f"Found else (logged_in) at line: {found_else_logged_in_line}")
    print(f"Found if not finished at line: {found_if_not_finished_line}")
    print(f"Found footer at line: {footer_line}")
    
    # Second pass: fix indentation
    for i, line in enumerate(lines):
        # Before else block
        if i < found_else_logged_in_line:
            fixed_lines.append(line)
        # The else line itself
        elif i == found_else_logged_in_line:
            fixed_lines.append(line)
            in_else_logged_in = True
        # Between else and if not finished
        elif i > found_else_logged_in_line and i < found_if_not_finished_line:
            # Already properly indented with 4 spaces
            fixed_lines.append(line)
        # The if not finished line
        elif i == found_if_not_finished_line:
            # Should have 4 spaces
            if not line.startswith('    '):
                fixed_lines.append('    ' + line.strip())
            else:
                fixed_lines.append(line)
            in_if_not_finished = True
        # Inside if not finished block, before else (victory screen)
        elif i > found_if_not_finished_line and i < footer_line:
            # Check if this is the else line for victory screen
            if line.strip().startswith('# ═══') and 'VICTORY SCREEN' in line:
                # This is else block for finished
                in_if_not_finished = False
                # Should have 4 spaces (same level as if not finished)
                if line.strip():
                    fixed_lines.append('    ' + line.strip())
                else:
                    fixed_lines.append(line)
            elif line.strip() == 'else:' and i > found_if_not_finished_line:
                # else for the finished check
                in_if_not_finished = False
                fixed_lines.append('    else:')
            elif in_if_not_finished:
                # Inside if not finished - needs 8 spaces total
                if line.strip():
                    # Remove existing indentation and add 8 spaces
                    stripped = line.lstrip()
                    if stripped:
                        fixed_lines.append('        ' + stripped)
                    else:
                        fixed_lines.append('')
                else:
                    fixed_lines.append(line)
            else:
                # In else (victory) block - needs 8 spaces
                if line.strip():
                    stripped = line.lstrip()
                    if stripped:
                        fixed_lines.append('        ' + stripped)
                    else:
                        fixed_lines.append('')
                else:
                    fixed_lines.append(line)
        # Footer and after
        elif i >= footer_line:
            # Should have 4 spaces (in else logged_in block)
            if line.strip():
                # Check if already has correct indentation
                if line.startswith('    ') and not line.startswith('        '):
                    fixed_lines.append(line)
                elif not line.startswith(' '):
                    fixed_lines.append('    ' + line)
                else:
                    # Has some indentation, normalize to 4
                    fixed_lines.append('    ' + line.lstrip())
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Write back
    with open('final2.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("File fixed!")

if __name__ == '__main__':
    fix_file()
