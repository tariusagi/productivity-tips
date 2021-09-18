When you have an existing local Git repository, which may already tied to a remote repository (such as GitLab) and you want to imgrate/import it into a new remote repository, and also switch to this new remote, then follow these steps:
1. Create your new blank remote repository, and copy its URL, for example git@github.com:tariusagi/myrepo.git.
2. In your local repository, add this new remote: `git remote add github git@github.com:tariusagi/myrepo.git`.
3. Remove your current remote (origin): `git remote rm origin`
4. Rename your new remote (github) to be your new origin: `git remote rename github origin`
5. If your default local branch name is different from new remote default branch, you need to rename it. For example, GitLab default branch is called "master", while GitHub is "main". Run this command to rename it: `git branch -m master main`
6. Force pushing local repo to new remote, and also change tracking info to new remote branch: `git push -f --set-upstream origin main`
7. Update local repo main branch to track new remote main branch: `git branch -u origin/main main` and then `git remote set-head origin -a`.
8. Check different between local repo and new remote with `git diff origin`. There should be no difference.
9. Done.
