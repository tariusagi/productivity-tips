There're times when unrelated branch exist in one repo, such as when you force push an existing repo into another remote repo. For example, you have a GitLab repo, which use "master" as the main branch, and then you want to migrate your code to a new repo created in GitHub, which, unfortunately, use "main" as its default branch. After adding GitHub remote and force push your local repo to it, it creates a new branch named "master" in the GitHub repo. Because "master" is not the default branch in GitHub, it will not be shown, initially, when you browse your repo in GitHub website, nor be pulled down when someone clone your repo. This is a real problem.

So how to make "master" the default branch after migration? Or better, merge "master" into "main", and then remove "master" to avoid confusion? Follow these steps, assumming that your repo in GitHub already existed with "main" and "master" branches, and your **local** HEAD is in "main":

1. Fetch data from remote: `git fetch`
2. List all branches to verify that "master" does exist in remote: `git branch -a`. Git should list all possible branches from local and remote. "master" branch should be in the remote list (shown as "remotes/origin/master").
3. Now, ask git to merge "master" into "main": `git merge origin/master --allow-unrelated-histories`. Note that `--allow-unrelated-histories` is used here to force git to accept merging from branches that have unrelated history, which usually happens when you migrate repos. After this step, source from "master" should be merged into "main", and you can see its files from local.
4. Verify that "master" source was merged succesfully by checking new changes in files and directories in your local repo.
5. Push changes to remote "main" branch: `git push origin`, and then verify that changes were actually there in GitHub repo, under "main" branch.
6. Delete "master" in remote: `git push origin --delete master`.
7. All done!

For short:
```
git fetch
git branch -a
git merge origin/master --allow-unrelated-histories
git push origin
git push origin --delete master
```
