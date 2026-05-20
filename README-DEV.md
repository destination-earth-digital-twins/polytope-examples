# Pre-Commit Hooks, Git LFS, and Notebook Test Guide

This repository uses **pre-commit hooks**, **Git LFS**, and automated **notebook execution tests** to maintain code quality, enforce formatting, handle large files, and ensure notebooks run correctly.

---


## Prerequisites

- Python installed  
- Git installed  
- Repository cloned locally  
- Git LFS installed (see below) 


### Development Environment Setup

All Python development dependencies can be installed at once:

pip install -r requirements-dev.txt

This will install everything needed for pre-commit hooks, notebook tests, and related checks.


---

## One-Time Setup

### 1. Install pre-commit
pip install pre-commit  

### 2. Install the Git hooks
Run this command from the root of the repository:  
pre-commit install  
This installs the hooks locally so they run automatically on every git commit.

---

## How Pre-Commit Hooks Work

- On every git commit, pre-commit runs all configured checks.  
- If a hook fails, the commit is blocked.  
- Some hooks may automatically modify files (e.g., formatting):
  - Review the changes  
  - Re-stage the files  
  - Commit again  

---

## Jupyter Notebook Output Handling

By default, all Jupyter notebook outputs are removed before committing to keep the repository clean and reduce file size.

### Preserving specific cell outputs

If you want to keep outputs for a specific cell (e.g., plots, images, tables):

1. Select the cell in Jupyter Notebook  
2. Add the cell tag: keep_output  

Cells tagged with keep_output will not have their outputs erased by the pre-commit hooks.

---

## Git LFS Setup

This repository uses **Git LFS (Large File Storage)** for large files. You need Git LFS installed locally to work properly with these files.

### Installing Git LFS

#### macOS
brew install git-lfs  
git lfs install

#### Linux
sudo apt install git-lfs   # Debian/Ubuntu  
git lfs install


After installation, Git automatically handles LFS files on pull, commit, and push. Without Git LFS, you will only see pointer files instead of the actual content.

---

## Running Hooks Manually (Optional)

- Run all hooks on all files:  
pre-commit run --all-files  

- Run a specific hook:  
pre-commit run <hook-id>  

---

## Notebook Execution Tests

We provide a **pass/fail test** to check that all notebooks execute without errors. This uses `pytest` and `nbclient`.

### Running the notebook tests

1. Install dependencies (if not already installed):
pip install pytest nbformat nbclient

2. Run the tests from the project root:
pytest tests/pass_fail_test.py

3. Optional configuration:
- Some notebooks may be skipped by default (see `SKIP_NOTEBOOKS` in the test file)
- The `LIVE_REQUEST` environment variable is automatically set to `false` to avoid making live API calls during testing.

### Test Behavior

- The test executes each notebook cell-by-cell using `nbclient`.  
- If a cell fails, the test **fails immediately** and prints:
  - Notebook path  
  - Original traceback for debugging  

- You can increase the timeout if needed (default: 600 seconds per notebook).

---

## Troubleshooting

- Hooks not running: Ensure `pre-commit install` was executed in this repository.  
- Commit fails: Read the error message, fix the issue, stage the updated files, and retry the commit.  
- Bypass hooks (not recommended):  
git commit --no-verify  

---

## Summary

- Install pre-commit once  
- Hooks run automatically on every commit  
- Notebook outputs are cleared by default  
- Use the keep_output tag to preserve selected cell outputs  
- Install Git LFS to handle large files properly  
- Run the notebook execution test to ensure notebooks run without errors  
