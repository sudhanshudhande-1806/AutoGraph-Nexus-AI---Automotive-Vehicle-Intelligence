#!/usr/bin/env python3
"""Execute the restructuring."""
import subprocess
import sys
import os

os.chdir(r'f:\Projects\AutoGraph-Nexus-AI.worktrees\agents-improve-file-structure-clarity')

# Run the restructure script
exec(open('do_restructure.py').read())
