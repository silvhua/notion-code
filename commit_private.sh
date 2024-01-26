# commit_private.sh
# This will push private files to the notion-private repo
git add -f private
git add -f data
git add .
git commit -m "$1"
git push --force private main
git update-ref refs/heads/main HEAD^
git reset HEAD