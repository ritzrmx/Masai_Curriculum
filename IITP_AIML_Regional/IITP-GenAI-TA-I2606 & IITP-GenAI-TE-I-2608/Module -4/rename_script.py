import os, re, subprocess

# We only target folders starting with 26-39
folder_pattern = re.compile(r'^(2[6-9]|3[0-9])\s*-\s*(.*)$')
# We target files starting with a single digit and a dash
file_pattern = re.compile(r'^(\d)\s*-\s*(.*)$')

def git_mv(src, dst):
    print(f"Renaming: '{src}' -> '{dst}'")
    subprocess.run(["git", "mv", src, dst], check=False)

# First, rename files inside the folders
for root, dirs, files in os.walk(".", topdown=False):
    # skip .git and other hidden dirs
    if ".git" in root:
        continue
    
    # Rename files
    for filename in files:
        if filename.endswith(".py"): continue # skip scripts if any
        m = file_pattern.match(filename)
        if m:
            new_name = m.group(2)
            old_path = os.path.join(root, filename)
            new_path = os.path.join(root, new_name)
            git_mv(old_path, new_path)

# Then, rename the directories
for dirname in os.listdir("."):
    if os.path.isdir(dirname):
        m = folder_pattern.match(dirname)
        if m:
            new_name = m.group(2)
            git_mv(dirname, new_name)

print("Renaming complete.")
