#!/bin/bash

set -euo pipefail

# Default branch is main, but can be overridden by argument
BRANCH="${1:-main}"
DRY_RUN="${2:-false}"

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
  "requirements-lock.txt"
  "conda-lock.yml"
)

FILES_EXCLUDE=(
  "climate-dt/data/"
  "climate-dt/explorer/data/"
  "extremes-dt/data/"
  "nextgems/data/"
  "on-demand-extremes-dt/data/"
)

# Print configuration
echo "=========================================="
echo "Merge Configuration:"
echo "  Branch: $BRANCH"
echo "  Dry Run: $DRY_RUN"
echo "=========================================="
echo ""

if [ "$DRY_RUN" = "true" ]; then
    echo "[DRY RUN] The following operations would be performed:"
    echo ""
fi

# Fetch the branch
FETCH_CMD="git fetch origin $BRANCH"
echo "Fetching latest $BRANCH from origin..."
if [ "$DRY_RUN" != "true" ]; then
    $FETCH_CMD
fi

# Checkout selected files/folders from remote branch
echo "Checking out selected paths from origin/$BRANCH..."
for path in "${FILES[@]}"; do
    CHECKOUT_CMD="git checkout origin/$BRANCH -- \"$path\""
    echo "  - $path"
    if [ "$DRY_RUN" != "true" ]; then
        eval $CHECKOUT_CMD
    fi
done

echo ""
echo "Restoring excluded paths back to current branch state..."
for path in "${FILES_EXCLUDE[@]}"; do
    RESTORE_CMD="git restore --source=HEAD -- \"$path\""
    echo "  - $path"
    if [ "$DRY_RUN" != "true" ]; then
        eval $RESTORE_CMD
    fi
done

echo ""
echo "Done."
if [ "$DRY_RUN" != "true" ]; then
    echo "Review changes with: git status"
else
    echo "[DRY RUN] No changes made. Run without 'true' as second argument to apply changes."
fi
