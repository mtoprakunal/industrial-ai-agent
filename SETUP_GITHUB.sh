

#!/bin/bash

GITHUB_USERNAME="mtoprakunal"
REPO_NAME="industrial-ai-agent"

git init
git add .
git commit -m "Initial commit: Industrial Automation AI Agent"
git branch -M main
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
git push -u origin main

echo "Tamamlandi! https://github.com/$GITHUB_USERNAME/$REPO_NAME"