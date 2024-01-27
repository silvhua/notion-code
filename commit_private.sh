# commit_private.sh
# This will push private files to the notion-private repo
git add -f private
git add -f data/parsed
git add -f data/raw
git add $(git ls-files -o --exclude-standard)
git commit -m "$1"
git push --force private cloud
git update-ref refs/heads/main HEAD^
git reset HEAD
git add data
git commit -m "$1"
git push private cloud