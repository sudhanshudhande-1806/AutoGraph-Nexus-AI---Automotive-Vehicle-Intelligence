@echo off
REM Restructure the AutoGraph-Nexus-AI project directory layout
REM This script should be run from the project root

setlocal enabledelayedexpansion

echo Project root: %cd%
echo.
echo === Starting restructuring ===
echo.

REM Step 1: Create necessary directories
echo Step 1: Creating new directories...
if not exist "src" mkdir src
if not exist "src\core" mkdir src\core
if not exist "config" mkdir config
if not exist "docs" mkdir docs
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "notebooks" mkdir notebooks
echo. Directories created
echo.

REM Step 2: Move directories using git mv
echo ==================================================
echo Step 2: Moving directories to src using git mv...
echo ==================================================

setlocal enabledelayedexpansion
for %%d in (simulator kafka spark lakehouse graph ml ai dashboard backend) do (
  if exist "%%d" (
    echo Moving %%d to src\%%d...
    git mv "%%d" "src\%%d"
  ) else (
    echo Warning: %%d does not exist
  )
)
echo.

REM Step 3: Move test files
echo ==================================================
echo Step 3: Moving test files to tests...
echo ==================================================

for %%f in (test_import.py test_spark.py) do (
  if exist "%%f" (
    echo Moving %%f to tests\%%f...
    git mv "%%f" "tests\%%f"
  ) else (
    echo Warning: %%f does not exist
  )
)
echo.

REM Step 4: Move docker-compose.yml
echo ==================================================
echo Step 4: Moving docker-compose.yml to config...
echo ==================================================

if exist "docker-compose.yml" (
  git mv docker-compose.yml config\docker-compose.yml
  echo. Moved docker-compose.yml
) else (
  echo Warning: docker-compose.yml does not exist
)
echo.

REM Step 5: Create __init__.py files
echo ==================================================
echo Step 5: Creating __init__.py files...
echo ==================================================

type nul > src\__init__.py
type nul > src\core\__init__.py
echo. Created __init__.py files
git add src\__init__.py src\core\__init__.py
echo.

REM Step 6: Check git status
echo ==================================================
echo Step 6: Git status
echo ==================================================
git status
echo.

echo. Restructuring complete!
echo.
echo Next steps:
echo 1. Review the changes: git status
echo 2. Commit with: git commit -m "Restructure: improve file structure clarity"

endlocal
