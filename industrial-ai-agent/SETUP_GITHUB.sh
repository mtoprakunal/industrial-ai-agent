#!/bin/bash
# ============================================================
# SETUP_GITHUB.sh
# Repoyu GitHub hesabına ilk kez yüklemek için çalıştır.
# ============================================================

GITHUB_USERNAME="SENIN_KULLANICI_ADIN"
REPO_NAME="industrial-ai-agent"

echo ""
echo "GitHub'a yükleniyor: $GITHUB_USERNAME/$REPO_NAME"
echo ""

git init
git add .
git commit -m "Initial commit: Industrial Automation AI Agent"
git branch -M main
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
git push -u origin main

echo ""
echo "Tamamlandı! https://github.com/$GITHUB_USERNAME/$REPO_NAME"
