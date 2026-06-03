import subprocess
import sys

result = subprocess.run(
    [sys.executable, r'f:\Projects\AutoGraph-Nexus-AI.worktrees\agents-improve-file-structure-clarity\restructure_final.py'],
    cwd=r'f:\Projects\AutoGraph-Nexus-AI.worktrees\agents-improve-file-structure-clarity'
)
sys.exit(result.returncode)
