import os

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changed = False

    if "flowchart TD" in content:
        content = content.replace("flowchart TD", "flowchart LR")
        changed = True
        print(f"Changed to flowchart LR in {filepath}")
        
    if "direction LR" in content:
        content = content.replace("direction LR", "direction TB")
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

for root, dirs, files in os.walk('.'):
    for name in files:
        if name.startswith('mental-map') or name.startswith('pre-read'):
            if name.endswith('.md'):
                process_file(os.path.join(root, name))
