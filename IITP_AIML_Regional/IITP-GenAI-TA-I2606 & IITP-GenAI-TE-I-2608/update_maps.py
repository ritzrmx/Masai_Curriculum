import os
import glob

base_dir = r'E:\Masai\SME\IITP-GenAI-TA-I2606 & IITP-GenAI-TE-I-2608\IITP_AIML_Regional\IITP-GenAI-TA-I2606 & IITP-GenAI-TE-I-2608\Module-3'
files = glob.glob(os.path.join(base_dir, '**', 'mental-map*.md'), recursive=True)

old_init = "%%{init: {'flowchart': {'htmlLabels': true, 'nodeSpacing': 60, 'rankSpacing': 95, 'wrappingWidth': 620, 'padding': 18}}}%%"
new_init = "%%{init: {'themeVariables': {'fontSize': '16px'}, 'flowchart': {'useMaxWidth': false, 'htmlLabels': true, 'nodeSpacing': 80, 'rankSpacing': 120, 'wrappingWidth': 620, 'padding': 20}}}%%"

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(old_init, new_init)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated clarity/zoom settings.')
