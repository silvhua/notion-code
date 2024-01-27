# This will push private files to the notion-code repo
git add src
git commit -m "$1"
git subtree push --prefix=src codeSubtree main