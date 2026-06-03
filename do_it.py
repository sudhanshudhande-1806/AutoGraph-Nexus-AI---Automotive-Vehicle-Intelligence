import os, shutil
from pathlib import Path
os.chdir(r'f:\Projects\AutoGraph-Nexus-AI.worktrees\agents-improve-file-structure-clarity')
for d in ['src', 'src/core', 'config', 'docs', 'data', 'logs', 'notebooks']:
    Path(d).mkdir(parents=True, exist_ok=True)
for s, d in [('simulator', 'src/simulator'), ('kafka', 'src/kafka'), ('spark', 'src/spark'), ('lakehouse', 'src/lakehouse'), ('graph', 'src/graph'), ('ml', 'src/ml'), ('ai', 'src/ai'), ('dashboard', 'src/dashboard'), ('backend', 'src/backend')]:
    if Path(s).exists() and s != d:
        shutil.move(s, d)
for f in ['test_import.py', 'test_spark.py']:
    if Path(f).exists():
        Path(f'tests/{f}').parent.mkdir(parents=True, exist_ok=True)
        shutil.move(f, f'tests/{f}')
if Path('docker-compose.yml').exists():
    shutil.move('docker-compose.yml', 'config/docker-compose.yml')
Path('src/__init__.py').touch()
Path('src/core/__init__.py').touch()
print("Done")
