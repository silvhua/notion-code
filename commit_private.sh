# commit_private.sh
# test
git add -f private
git add -f data
git commit -m "$1"
git push --force private main
git update-ref refs/heads/main HEAD^
git reset HEAD