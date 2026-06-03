#!/usr/bin/env python3
"""
Restructure the AutoGraph-Nexus-AI project directory layout using git commands.
This preserves git history using git mv.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_git_command(cmd, cwd=None):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print(f"Error running: {cmd}")
            print(f"STDERR: {result.stderr}")
            return False
        print(f"✓ {cmd}")
        if result.stdout.strip():
            print(f"  Output: {result.stdout.strip()[:100]}")
        return True
    except Exception as e:
        print(f"Exception running {cmd}: {e}")
        return False

def ensure_directory(path):
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return True

def git_mv(src, dst, cwd):
    """Move a file/directory using git mv."""
    return run_git_command(f'git mv "{src}" "{dst}"', cwd=cwd)

def main():
    # Get the project root
    project_root = os.getcwd()
    print(f"Project root: {project_root}")
    print("\n=== Starting restructuring ===\n")

    # Step 1: Create necessary directories
    print("Step 1: Creating new directories...")
    dirs_to_create = ['src', 'src/core', 'config', 'docs', 'data', 'logs', 'notebooks']
    for dir_name in dirs_to_create:
        dir_path = os.path.join(project_root, dir_name)
        if ensure_directory(dir_path):
            print(f"✓ Created: {dir_path}")
    
    print("\n" + "="*50)
    print("Step 2: Moving directories to src/ using git mv...")
    print("="*50)
    
    # Step 2: Move directories using git mv
    dirs_to_move = [
        'simulator', 'kafka', 'spark', 'lakehouse', 'graph', 
        'ml', 'ai', 'dashboard', 'backend'
    ]
    
    for dir_name in dirs_to_move:
        src = dir_name
        dst = os.path.join('src', dir_name)
        if git_mv(src, dst, project_root):
            pass  # Success message already printed by run_git_command
        else:
            print(f"✗ Failed to move {src} to {dst}")
    
    print("\n" + "="*50)
    print("Step 3: Moving test files to tests/...")
    print("="*50)
    
    # Step 3: Move test files
    test_files = ['test_import.py', 'test_spark.py']
    for test_file in test_files:
        src = test_file
        dst = os.path.join('tests', test_file)
        if git_mv(src, dst, project_root):
            pass
        else:
            print(f"✗ Failed to move {src} to {dst}")
    
    print("\n" + "="*50)
    print("Step 4: Moving docker-compose.yml to config/...")
    print("="*50)
    
    # Step 4: Move docker-compose.yml
    if git_mv('docker-compose.yml', os.path.join('config', 'docker-compose.yml'), project_root):
        pass
    else:
        print("✗ Failed to move docker-compose.yml")
    
    print("\n" + "="*50)
    print("Step 5: Creating __init__.py files...")
    print("="*50)
    
    # Step 5: Create __init__.py files
    init_files = [
        os.path.join('src', '__init__.py'),
        os.path.join('src', 'core', '__init__.py')
    ]
    
    for init_file in init_files:
        init_path = os.path.join(project_root, init_file)
        with open(init_path, 'w') as f:
            f.write('')
        print(f"✓ Created: {init_file}")
    
    # Stage the __init__.py files
    run_git_command('git add src/__init__.py src/core/__init__.py', cwd=project_root)
    
    print("\n" + "="*50)
    print("Step 6: Checking git status...")
    print("="*50)
    
    # Check git status
    run_git_command('git status', cwd=project_root)
    
    print("\n" + "="*50)
    print("✓ Restructuring complete!")
    print("="*50)
    print("\nYou can now review the changes with: git status")
    print("Commit with: git commit -m 'Restructure: improve file structure clarity'")

if __name__ == '__main__':
    main()
