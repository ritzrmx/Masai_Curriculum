import os, subprocess, re

TARGET_CONFIG = "%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 100, 'rankSpacing': 150, 'wrappingWidth': 850, 'padding': 25}, 'themeVariables': {'fontSize': '18px'}}}%%"

files_to_process = [
    r'E:\Masai\SME\IITP-GenAI-TA-I2606\Module-2\7.1 (Subqueries in Action)\7.1-mental-map.md',
    r'E:\Masai\SME\IITP-GenAI-TA-I2606\Module-2\7.1 (Subqueries in Action)\7.1-pre-read.md',
    r'E:\Masai\SME\IITP-GenAI-TA-I2606\Module-2\7.2 (CTEs and GenAI for SQL)\7.2-mental-map.md',
    r'E:\Masai\SME\IITP-GenAI-TA-I2606\Module-2\7.2 (CTEs and GenAI for SQL)\7.2-pre-read.md'
]

for filepath in files_to_process:
    if not os.path.exists(filepath):
        print(f"File missing: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if TARGET_CONFIG not in content:
        if '%%{init:' in content:
            content = re.sub(r'%%\{init:.*?\}%%', TARGET_CONFIG, content, flags=re.DOTALL)
        else:
            content = content.replace('```mermaid\n', f'```mermaid\n{TARGET_CONFIG}\n')
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Standardized {filepath}')
    
    if 'mental-map' in filepath:
        out_png = filepath.replace('.md', '.png')
        out_svg = filepath.replace('.md', '.svg')
        
        print(f'Generating PNG for {filepath}...')
        subprocess.run(['npx', '-y', '@mermaid-js/mermaid-cli@latest', '-i', filepath, '-o', out_png, '-s', '5', '-b', 'white'], shell=True)
        print(f'Generating SVG for {filepath}...')
        subprocess.run(['npx', '-y', '@mermaid-js/mermaid-cli@latest', '-i', filepath, '-o', out_svg, '-b', 'white'], shell=True)
