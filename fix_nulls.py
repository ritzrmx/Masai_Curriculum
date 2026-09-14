import os

def fix_utf16_corruption(filepath):
    with open(filepath, 'rb') as f:
        raw_bytes = f.read()
    
    # If the file contains a lot of null bytes, it was probably UTF-16 read as UTF-8
    if b'\x00' in raw_bytes:
        print(f"Fixing null bytes in {filepath}")
        # Assuming the file is ASCII but padded with nulls (like \x00#\x00 \x00M)
        # We can just decode it as UTF-16LE, OR if the BOM is messed up, we just strip \x00
        # Actually, let's just strip \x00 if it's mostly ASCII
        cleaned_bytes = raw_bytes.replace(b'\x00', b'')
        
        # Remove BOM if it exists
        if cleaned_bytes.startswith(b'\xff\xfe'):
            cleaned_bytes = cleaned_bytes[2:]
        elif cleaned_bytes.startswith(b'\xfe\xff'):
            cleaned_bytes = cleaned_bytes[2:]
            
        try:
            cleaned_text = cleaned_bytes.decode('utf-8', errors='ignore')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            print("Fixed successfully!")
        except Exception as e:
            print(f"Failed to fix {filepath}: {e}")

for root, dirs, files in os.walk('.'):
    for name in files:
        if name.startswith('mental-map') or name.startswith('pre-read'):
            if name.endswith('.md'):
                fix_utf16_corruption(os.path.join(root, name))
