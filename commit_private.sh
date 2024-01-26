# commit_private.sh
git add -f private
git add -f data
git add $(git ls-files -o --exclude-standard)
git commit -m "$1"
git push --force private cloud
git update-ref refs/heads/main HEAD^
git reset HEAD