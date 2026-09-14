import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    if "ðŸ" in content or "â€”" in content or "âš" in content or "Â·" in content or "â‚¹" in content:
        print(f"Fixing {filepath}")
        try:
            raw_bytes = content.encode('cp1252')
            fixed_content = raw_bytes.decode('utf-8')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
        except Exception as e:
            print(f"Error on {filepath}: {e}")

for root, dirs, files in os.walk('.'):
    for name in files:
        if name.startswith('mental-map') or name.startswith('pre-read'):
            if name.endswith('.md'):
                fix_file(os.path.join(root, name))
