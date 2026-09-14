import os

def recover_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if len(content) > 1 and content.startswith('·') and content.endswith('·'):
        # Verify it's exactly the alternating corruption
        if all(c == '·' for c in content[0::2]):
            print(f"Recovering alternating corruption in {filepath}")
            recovered = content[1::2]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(recovered)

for root, dirs, files in os.walk('.'):
    for name in files:
        if name.startswith('mental-map') or name.startswith('pre-read'):
            if name.endswith('.md'):
                recover_file(os.path.join(root, name))
