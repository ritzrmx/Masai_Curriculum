import os
import glob
import base64
import urllib.request
import re

base_dir = r'E:\Masai\SME\IITP-GenAI-TA-I2606 & IITP-GenAI-TE-I-2608\IITP_AIML_Regional\IITP-GenAI-TA-I2606 & IITP-GenAI-TE-I-2608'
files = glob.glob(os.path.join(base_dir, '**', 'mental-map*.md'), recursive=True)
files.extend(glob.glob(os.path.join(base_dir, '**', 'pre-read*.md'), recursive=True))

success_count = 0
fail_count = 0

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract mermaid block
    match = re.search(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
    if not match:
        continue
    
    mermaid_code = match.group(1).strip()
    
    # Generate PNG path
    png_path = file[:-3] + '.png'
    
    # Base64 encode
    # Mermaid.ink requires pako compression for base64, but base64 works for simple ones, wait!
    # Does mermaid.ink support raw base64 for large graphs?
    # Actually, let's use the json state base64 which mermaid.ink uses.
    # The format is {"code":"...","mermaid":"{\n  \"theme\": \"default\"\n}","autoSync":true,"updateDiagram":false}
    import json
    state = {
        "code": mermaid_code,
        "mermaid": "{\n  \"theme\": \"default\"\n}",
        "autoSync": True,
        "updateDiagram": False
    }
    json_str = json.dumps(state)
    b64 = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    url = f'https://mermaid.ink/img/pako:{b64}' # Wait, pako is different.
    # Without pako, it's just base64 of the state JSON:
    url = f'https://mermaid.ink/img/{b64}?type=png'
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response, open(png_path, 'wb') as out_file:
            out_file.write(response.read())
        success_count += 1
    except Exception as e:
        print(f'Failed for {file}: {e}')
        # Fallback to simple base64 (if it works better)
        try:
            simple_b64 = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
            url = f'https://mermaid.ink/img/{simple_b64}?type=png'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(png_path, 'wb') as out_file:
                out_file.write(response.read())
            success_count += 1
            print(f'Fallback success for {file}')
        except Exception as e2:
            print(f'Fallback failed for {file}: {e2}')
            fail_count += 1

print(f'Done. Success: {success_count}, Failed: {fail_count}')
