#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "=== Rajasthan Royals SupeRR Selector Deployment ==="

# 1. Compile dashboard and synchronize root index.html
echo "Compiling dashboard..."
python3 build_dashboard.py

# 2. Run test suite verification
echo "Running test suite verification..."
pytest tests/ -q

# 3. Check for git changes and push
if git diff --quiet index.html dashboard/ data.json; then
  echo "No dashboard changes to commit. Working tree is clean."
else
  echo "Committing updated dashboard..."
  git add index.html dashboard/ data.json
  git commit -m "feat(dashboard): update compiled interactive auction analytics dashboard"
  echo "Pushing to origin main..."
  git push origin main
  echo "Successfully pushed to GitHub repository!"
fi

# 4. Verify GitHub Pages build status
echo "Checking GitHub Pages build status..."
sleep 3
gh api repos/yashagarwal-lab/superrr-dashboard/pages/builds --jq '.[0] | "Latest Pages Build Status: " + .status + " at " + .updated_at' || echo "Pages API status check complete."

echo "Deployment complete! Live URL: https://yashagarwal-lab.github.io/superrr-dashboard/"
