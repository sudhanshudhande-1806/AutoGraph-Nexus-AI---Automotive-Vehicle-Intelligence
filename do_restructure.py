import os
import subprocess
import shutil
from pathlib import Path

def run_cmd(cmd):
    """Run a shell command."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    if result.stdout:
        print(result.stdout)
    return True

os.chdir(r'f:\Projects\AutoGraph-Nexus-AI.worktrees\agents-improve-file-structure-clarity')
print(f"Working in: {os.getcwd()}")

# Create directories
print("\n=== Creating directories ===")
Path('src/core').mkdir(parents=True, exist_ok=True)
Path('config').mkdir(parents=True, exist_ok=True)
Path('docs').mkdir(parents=True, exist_ok=True)
Path('data').mkdir(parents=True, exist_ok=True)
Path('logs').mkdir(parents=True, exist_ok=True)
Path('notebooks').mkdir(parents=True, exist_ok=True)
print("✓ Directories created")

# Move directories with git mv
print("\n=== Moving directories ===")
dirs = ['simulator', 'kafka', 'spark', 'lakehouse', 'graph', 'ml', 'ai', 'dashboard', 'backend']
for d in dirs:
    if os.path.isdir(d):
        run_cmd(f'git mv {d} src\\{d}')

# Move test files
print("\n=== Moving test files ===")
files = ['test_import.py', 'test_spark.py']
for f in files:
    if os.path.isfile(f):
        run_cmd(f'git mv {f} tests\\{f}')

# Move docker-compose.yml
print("\n=== Moving docker-compose.yml ===")
if os.path.isfile('docker-compose.yml'):
    run_cmd('git mv docker-compose.yml config\\docker-compose.yml')

# Create __init__.py
print("\n=== Creating __init__.py files ===")
Path('src/__init__.py').touch()
Path('src/core/__init__.py').touch()
run_cmd('git add src/__init__.py src/core/__init__.py')

print("\n=== Final status ===")
run_cmd('git status')
