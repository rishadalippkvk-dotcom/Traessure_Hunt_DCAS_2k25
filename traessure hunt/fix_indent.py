#!/usr/bin/env python3
"""Script to fix indentation in final2.py for the game logic section"""

def fix_indentation():
    with open('final2.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line with "if not st.session_state.finished:"
    # Everything after that line (within the else block) needs to be indented by 4 spaces
    
    in_game_logic = False
    in_else_block = False
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Check if we're in the else block for logged_in
        if 'else:' in line and '# Show game (user is logged in)' in lines[i+1] if i+1 < len(lines) else False:
            in_else_block = True
            fixed_lines.append(line)
            continue
        
        # Check if we've reached the footer (end of else block)
        if in_else_block and line.strip().startswith('# Footer') and not line.startswith('    '):
            in_else_block = False
            fixed_lines.append('    ' + line)
            continue
        
        # If we're in else block but not in game logic, and line starts with "    if not st.session_state.finished:"
        if in_else_block and '    if not st.session_state.finished:' in line:
            in_game_logic = True
            fixed_lines.append(line)
            continue
        
        # If in game logic, add extra 4 spaces (total 8 from start for content inside if)
        if in_game_logic:
            # Check for victory screen section which signals end of game logic
            if line.strip().startswith('# ═══') and 'VICTORY SCREEN' in line:
                # Start of else block for victory
                fixed_lines.append('    ' + line)
                in_game_logic = False
                continue
            
            # If already indented with 4 spaces and we're in game logic, add 4 more
            if line.startswith('    ') and not line.startswith('        '):
                fixed_lines.append('    ' + line)
            elif not line.strip():  # Empty line
                fixed_lines.append(line)
            else:
                # Line that's not indented but should be in else block
                if in_else_block:
                    fixed_lines.append('    ' + line)
                else:
                    fixed_lines.append(line)
        else:
            # Normal case - if in else block, make sure it has 4 space indent
            if in_else_block:
                if line.strip() and not line.startswith('    ') and not line.startswith('#'):
                    fixed_lines.append('    ' + line)
                elif line.strip() and not line.startswith('    ') and line.startswith('#'):
                    # Comment line
                    fixed_lines.append('    ' + line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
    
    # Write back
    with open('final2.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Indentation fixed successfully!")

if __name__ == '__main__':
    fix_indentation()
