# Basic

## Setting up a repository
- Clone a repo: `git clone <URL>`
- Initialize a git repo in the current directory: `git init`
- Set user name and email for current repo:
  ```sh
  git config user.name "Peter Pan"
  git config user.email "peterpan@wonderland.com"
  ```
  If you want to set these settings globally, add `--global` after `config`, for example:

  ```sh
  git config --global user.name "Peter Pan"
  ```
## Logs
- Show commit logs: `git log`.
- Show changes along with commits logs: `git log --name-only`.

## Diff
- Show differences between local and staged content: `git diff [path]`.
- Show differences between staged and HEAD content: `dif diff --staged [path]`.

The output format basically list chunks of lines which were changed from the local/unstaged content (b) in comparison to the staged/committed content (a). Lines that were in a are marked with minus `-` sign and redcolor, while the new lines (the replacement) in b are marked with plus `+` sign and green color. Lines that don't have markers are unchanged.

For example, if there's a file named lines.txt which this committed content:
```
First line
Second line
```

Then, change it to:
```
First line
2nd line
3rd line
```

Now run `git diff`, the output should be:
```
$git diff
diff --git a/lines.txt b/lines.txt
index 7d91453..4015d0d 100644
--- a/lines.txt
+++ b/lines.txt
@@ -1,2 +1,3 @@
 First line
-Second line
+2nd line
+3rd line
```
Which means:
1. `diff --git a/lines.txt b/lines.txt` says that `diff` will output in `git` format changes from `b` (local) to `a` (currently in commit/stage).
2. `7d91453..4015d0d 100644` show the first 7 digits of the hashes of `a` and `b` respectively, and the mode of the file.
3. There's one chunk of lines changed, which happens from line 1 to line 2 in `a`, and from line 1 to line 3 in `b`.
3. This chunk start with "First line". It doesn't start with "-" or "+", which means it stay unchanged. It's showed in this chunk as a marker.
4. Line "Second line" was from `a`.
5. Lines "2nd line" and "3rd line" were from `b`. Which means this 2 lines replace the "Second line" in `a`.

## Undoing changes
- **Un-staged** changes: `git reset <file>`, or `git restore --staged <file>`. This action unstage *local* changes. It's safe, because the local changes are *still there*. They're just not marked for commit (stage) yet.
- Discard **local** changes: `git restore <file>` **(DANGEROUS)** . This action will replace local `file` with its staged content. This is **unrecoverable**, because the local changes are lost.
- Discard **all** changes: `git reset --hard` **(VERY DANGEROUS)**. This action replace all local and staged changes to current respository with HEAD commit, and only *untracked* files and directories are left *untouched*. It's *unrecoverable*.
- Remove **untracked** changes: `git clean -fd [path]` **(VERY DANGEROUS)**. This action *recursively* removes all *untracked* changes from `path` or current directory if `path` was not given. If you want to remove *ignored* files and folders as well, include `-x`. it's *unrecoverable*, so it should be checked with `-n` first, such as `git clean -fdn`, which lists files and directories that it would remove without actually doing it.

## Remote repo
1. Show remote URLs: `git remote -v`.
2. Pull changes from remote and merge into local, active branch: `git pull [origin remote-branch-name]`. If `origin remote-branch-name` was given, then git will try to fetch and merge the local active branch into that specific remote branch. Otherwise, it will use the default, which means the remote branch that is tracking the local active branch.
3. Check for changes from remote:  run `git fetch` to get latest content from remote origin first, then `git diff origin [branch-name]` to show differences against given branch. If no branch was given, then the active branch will be used.
4. Push changes from a branch to remote: `git push origin [branch-name]`. If no branch was given, the active one will be used.
5. Change remote URL: `git remote set-url origin <new_url>`.

# Merging
## Unrelated merge
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

# Migration
## Migrate a single branch to an empty remote repo
1. You have an existing repo, which has or has not a remote link, and its main development branch is called "master".
2. You want to push your source from this "master" branch to a newly created, **empty**, remote repo, such as GitHub.
3. You also want to switch your local repo's remote from your old one to that new one.
4. Because the new remote used a different name for its default branch, for example GitHub use "main" instead of "master", you'd want to rename your current branch and track its remote at the same time.

How can you do all these with fewest steps? Follows these:
1. Set your origin (remote) to new remote: `git remote set-url origin git@github.com:tariusagi/myrepo.git`, or add a new origin, if your local repo doesn't have one, with `git remote add origin git@github.com:tariusagi/myrepo.git`.
2. Rename you current branch to "main": `git branch -m main`
3. Push your branch to new remote: `git push -u origin main`

And we're done!

### Short version:
```sh
git remote set-url origin git@github.com:tariusagi/myrepo.git
```
or
```sh
git remote add origin git@github.com:tariusagi/myrepo.git
```
then
```sh
git branch -m main
git push -u origin main
```

## Migrate a single branch to a non-empty remote repo
Everything is the same as Scenario 1, but your new remote is **not empty**. If you try steps from Scenario 1, then after last step (push), git will show an error, because the local and remote have unsolved differences. Therefore, you have to follow these steps:

1. Performe first 2 steps from Scenario 1.
2. Set upstream link to local "main" branch: `git branch --set-upstream-to=origin/main main`
3. Pull and merge changes from remote, allowing unrelated histories: `git pull --allow-unrelated-histories`
4. Push your "main" branch (including pulled and merged changes from new remote): `git push origin`. Note that this is different from step 3 of Scenario 1, because in this scenario's step 2, we already set the upstream link, therefore we don't need to set that link anymore.

And we're done!

### Short version
```sh
git remote set-url origin git@github.com:tariusagi/myrepo.git
```
or
```sh
git remote add origin git@github.com:tariusagi/myrepo.git
```
then
```sh
git branch -m main
git branch --set-upstream-to=origin/main main
git pull --allow-unrelated-histories
git push origin
```


