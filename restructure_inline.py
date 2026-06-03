#!/usr/bin/env python3
"""Direct execution of restructuring"""

if __name__ == '__main__':
    import os
    import shutil
    from pathlib import Path
    
    os.chdir(r'f:\Projects\AutoGraph-Nexus-AI.worktrees\agents-improve-file-structure-clarity')
    
    # Create directories
    for d in ['src', 'src/core', 'config', 'docs', 'data', 'logs', 'notebooks']:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f'✓ {d}')
    
    # Move directories
    moves = [
        ('simulator', 'src/simulator'),
        ('kafka', 'src/kafka'),
        ('spark', 'src/spark'),
        ('lakehouse', 'src/lakehouse'),
        ('graph', 'src/graph'),
        ('ml', 'src/ml'),
        ('ai', 'src/ai'),
        ('dashboard', 'src/dashboard'),
        ('backend', 'src/backend'),
    ]
    
    for src, dst in moves:
        if Path(src).exists() and src != dst:
            try:
                shutil.move(src, dst)
                print(f'→ {src} → {dst}')
            except Exception as e:
                print(f'✗ {src}: {e}')
    
    # Move test files
    for f in ['test_import.py', 'test_spark.py']:
        src_path = Path(f)
        if src_path.exists():
            dst = Path(f'tests/{f}')
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst))
            print(f'→ {f} → tests/{f}')
    
    # Move docker-compose
    if Path('docker-compose.yml').exists():
        shutil.move('docker-compose.yml', 'config/docker-compose.yml')
        print(f'→ docker-compose.yml → config/')
    
    # Create __init__.py
    Path('src/__init__.py').touch()
    Path('src/core/__init__.py').touch()
    print('✓ __init__.py files created')
    
    print('\n✓ Restructuring complete!')
