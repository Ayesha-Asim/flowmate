# Publish this starter to GitHub

1. Extract the ZIP and open its `flowmate-template` folder in VS Code.
2. Create an empty **public** GitHub repository named `flowmate` (do not initialize with README/license, since these files already exist).
3. In VS Code Terminal (inside the extracted folder):

```powershell
git init
git add .
git commit -m "Initial FlowMate starter template"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/flowmate.git
git push -u origin main
```

4. On GitHub: Settings → Collaborators → Add people; invite your teammate.
5. Optional: Settings → General → check **Template repository**. This lets you create new repositories from this starter; it is not required for two-person collaboration.
6. Teammate clones the repo, then each creates a separate feature branch:

```powershell
git checkout -b feature/frontend-improvements
# OR
git checkout -b feature/backend-nebius
```

7. Commit and push work; open a Pull Request to merge into `main`.

```powershell
git add .
git commit -m "Describe changes"
git push -u origin YOUR-BRANCH-NAME
```

If Git is not installed, use GitHub's **Add file → Upload files** interface to upload extracted contents (not the ZIP itself), or install Git for VS Code collaboration.
