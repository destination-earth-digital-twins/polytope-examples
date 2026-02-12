#!/bin/bash

set -euo pipefail

FILES=(
  "climate-dt/"
  "extremes-dt/"
  "nextgems/"
  "on-demand-extremes-dt/"
  "README.md"
  "requirements.txt"
  "environment.yml"
  "desp-authentication.py"
  "LICENSE"
  ".gitignore"
  ".pre-commit-config.yaml"
)

FILES_EXCLUDE=(
  "climate-dt/data/"
  "extremes-dt/data/"
  "nextgems/data/"
  "on-demand-extremes-dt/data/"
)

echo "Fetching latest main from origin..."
git fetch origin main

echo "Checking out selected paths from origin/main..."
for path in "${FILES[@]}"; do
    git checkout origin/notebook-tests -- "$path"
done

echo "Restoring excluded paths back to current branch state..."
for path in "${FILES_EXCLUDE[@]}"; do
    git restore --source=HEAD -- "$path"
done

echo "Done."
echo "Review changes with: git status"
