# commit_private.sh
git add -f private
git commit -m "$1"
git push --force private main
git update-ref refs/heads/main HEAD^
git reset HEAD