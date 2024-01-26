# commit_private.sh
git add -f "$1"
git commit -m "$2"
git push --force private main