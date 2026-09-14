import os

def restore_A_logic(content):
    result = []
    for i, char in enumerate(content):
        if char == '·':
            prev_char = content[i-1] if i > 0 else ' '
            next_char = content[i+1] if i < len(content)-1 else ' '
            
            is_space_before = prev_char.isspace()
            is_space_after = next_char.isspace()
            
            if not is_space_after:
                result.append('A')
            elif not is_space_before:
                result.append('A')
            else:
                next_non_space = ''
                for j in range(i+1, len(content)):
                    if not content[j].isspace():
                        next_non_space = content[j]
                        break
                
                if next_non_space.isupper():
                    result.append('·')
                else:
                    result.append('A')
        else:
            result.append(char)
            
    return "".join(result)

for root, dirs, files in os.walk('.'):
    for name in files:
        if name.startswith('mental-map') or name.startswith('pre-read'):
            if name.endswith('.md'):
                filepath = os.path.join(root, name)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = restore_A_logic(content)
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Restored 'A's in {filepath}")
