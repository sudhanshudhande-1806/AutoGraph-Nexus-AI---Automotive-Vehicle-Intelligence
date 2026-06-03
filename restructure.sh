#!/bin/bash
# Restructure the AutoGraph-Nexus-AI project directory layout
# This script should be run from the project root

set -e  # Exit on error

PROJECT_ROOT=$(pwd)
echo "Project root: $PROJECT_ROOT"
echo ""
echo "=== Starting restructuring ==="
echo ""

# Step 1: Create necessary directories
echo "Step 1: Creating new directories..."
mkdir -p src/core
mkdir -p config
mkdir -p docs
mkdir -p data
mkdir -p logs
mkdir -p notebooks
echo "✓ Directories created"
echo ""

# Step 2: Move directories using git mv
echo "=============================================="
echo "Step 2: Moving directories to src/ using git mv..."
echo "=============================================="

DIRS_TO_MOVE=("simulator" "kafka" "spark" "lakehouse" "graph" "ml" "ai" "dashboard" "backend")

for dir in "${DIRS_TO_MOVE[@]}"; do
  if [ -d "$dir" ]; then
    echo "Moving $dir to src/$dir..."
    git mv "$dir" "src/$dir"
  else
    echo "Warning: $dir does not exist"
  fi
done
echo ""

# Step 3: Move test files
echo "=============================================="
echo "Step 3: Moving test files to tests/..."
echo "=============================================="

TEST_FILES=("test_import.py" "test_spark.py")

for file in "${TEST_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "Moving $file to tests/$file..."
    git mv "$file" "tests/$file"
  else
    echo "Warning: $file does not exist"
  fi
done
echo ""

# Step 4: Move docker-compose.yml
echo "=============================================="
echo "Step 4: Moving docker-compose.yml to config/..."
echo "=============================================="

if [ -f "docker-compose.yml" ]; then
  git mv docker-compose.yml config/docker-compose.yml
  echo "✓ Moved docker-compose.yml"
else
  echo "Warning: docker-compose.yml does not exist"
fi
echo ""

# Step 5: Create __init__.py files
echo "=============================================="
echo "Step 5: Creating __init__.py files..."
echo "=============================================="

touch src/__init__.py
touch src/core/__init__.py
echo "✓ Created __init__.py files"
git add src/__init__.py src/core/__init__.py
echo ""

# Step 6: Check git status
echo "=============================================="
echo "Step 6: Git status"
echo "=============================================="
git status
echo ""

echo "✓ Restructuring complete!"
echo ""
echo "Next steps:"
echo "1. Review the changes: git status"
echo "2. Commit with: git commit -m 'Restructure: improve file structure clarity'"
