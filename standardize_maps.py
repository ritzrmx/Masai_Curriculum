import os
import re

TARGET_CONFIG = "%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 100, 'rankSpacing': 150, 'wrappingWidth': 850, 'padding': 25}, 'themeVariables': {'fontSize': '18px'}}}%%"

def fix_mojibake(content):
    # Fix the corrupted utf-8 characters left over from PowerShell
    content = content.replace('ðŸ’¡', '💡')
    content = content.replace('âš ï¸ ', '⚠️')
    content = content.replace('â€”', '—')
    content = content.replace('Â·', '·')
    content = content.replace('â‚¹', '₹')
    content = content.replace('â€¦', '…')
    
    # Fix the unrecoverable characters that became ? or Replacement Characters
    content = content.replace('?"', '—')
    content = content.replace('?"', '—')
    content = content.replace('A', '·')
    content = content.replace('', '·')
    return content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    
    content = fix_mojibake(content)
    
    # Standardize Mermaid Configuration
    content = re.sub(r'%%\{init:.*?\}%%', TARGET_CONFIG, content, flags=re.DOTALL)
    
    # Enforce Horizontal Flowchart Layout (overall Left-Right)
    if "flowchart TD" in content:
        content = content.replace("flowchart TD", "flowchart LR")
        
    # Enforce Vertical Subgraph Layout (boxes stack vertically inside nodes)
    if "direction LR" in content:
        content = content.replace("direction LR", "direction TB")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk('.'):
    for name in files:
        if name.startswith('mental-map') or name.startswith('pre-read'):
            if name.endswith('.md'):
                process_file(os.path.join(root, name))
