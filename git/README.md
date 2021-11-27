# Basic Git commands for daily uses
This document show basic command for daily uses. There're also other topics:
- [Repository migration](./Migration.md).
- [Merge unrelated branches](./Unrelated-Merge.md).

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
## Showing changes
- Show simple commit logs (only show commit messages): `git log`
- Show changed files along with commits log: `git log --name-only`

## Undoing changes
- `git restore <file>`: **(DANGEROUS)** Discard un-staged local changes (changes are not staged yet). This action will discard changes to local `file` and replace its content with the staged content. This action is marked dangerous, because it destroys local changes and **unrecoverable**.
- `git restore --staged <file>` or `git reset <file>`: **(CAUTIOUS)** Un-staged staged changes (changes were already staged). This action will remove `file` from stage, which makes it un-staged for commit, but its current (local) changes are untouched. *Simply put, this action remove the staged version of `file`*, but keep it local content intact. This action is marked to be cautious, because while the local (un-staged) changes are still there, changes made at the staged version will be lost and cannot be recovered. For example, a text files `test.txt` contains a text "A" and was staged, then you modified the text to be "B", then you decided to `git restore --staged test.txt`, now `test.txt` will only contain "B", and there's no way to recover the letter "A" anymore.
- `git reset --hard`: **(VERY DANGEROUS)** Discard all changes (staged or not). This action un-staged all staged changes, and replace all tracked, local files and directories with the latest commit (HEAD). Only untracked files and directories are left untouched. This action is marked very dangerous, because it recursively destroy all local changes, staged or not, and can't be recoverable.
- `git clean -fd`: **(VERY DANGEROUS)** Remove untracked files and directories. If you want to remove ignored files and folders as well, include `-x`. Should check with `-n` first, such as `git clean -fdn`, which lists files and directories that it would remove without actually doing it.

## Work with remote repo
1. Show remote URLs: `git remote -v`.
2. Pull changes from remote and merge into local, active branch: `git pull [origin remote-branch-name]`. If `origin remote-branch-name` was given, then git will try to fetch and merge the local active branch into that specific remote branch. Otherwise, it will use the default, which means the remote branch that is tracking the local active branch.
3. Check for changes from remote:  run `git fetch` to get latest content from remote origin first, then `git diff origin [branch-name]` to show differences against given branch. If no branch was given, then the active branch will be used.
4. Push changes from a branch to remote: `git push origin [branch-name]`. If no branch was given, the active one will be used.
5. Change remote URL: `git remote set-url origin <new_url>`.

