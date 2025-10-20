# Instructions for Contributors

This branch contains files specific to building the Jupyter Book.
Some files (like _config.yml, _toc.yml, scripts/pre-build.py, etc.) are protected using .gitattributes and should never be overwritten by merges from main.
The ours merge driver enforces this behavior.

## Steps

### 1. Configure the merge driver (only once)

Ensures that the protected files defined in .gitattributes are kept when merging:

```bash
git config merge.ours.driver true
```

### 2. Fetch the latest updates from main
```bash
git fetch origin main
```

### 3. Merge main into your jupyterbook branch
```bash
git rebase origin/main
```
### 4. Push your changes to the remote
```bash
git push
```

Pushing triggers the GitHub Actions workflow, which builds the Jupyter Book and deploys it to GitHub Pages