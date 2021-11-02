# Basic Git commands for daily uses
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

- **(DANGEROUS)** Discard un-staged local changes (changes are not staged yet): `git restore <file>`. This action will discard changes to local `file` and replace its content with the staged content. This action is marked dangerous, because it destroys local changes and **unrecoverable**.
- **(CAUTIOUS)** Un-staged staged changes (changes were already staged): `git restore --staged <file>` or `git reset <file>`. This action will remove `file` from stage, which makes it un-staged for commit, but its current (local) changes are untouched. *Simply put, this action remove the staged version of `file`*, but keep it local content intact. This action is marked to be cautious, because while the local (un-staged) changes are still there, changes made at the staged version will be lost and cannot be recovered. For example, a text files `test.txt` contains a text "A" and was staged, then you modified the text to be "B", then you decided to `git restore --staged test.txt`, now `test.txt` will only contain "B", and there's no way to recover the letter "A" anymore.
- **(VERY DANGEROUS)** Discard all changes (staged or not): `git reset --hard`. This action un-staged all staged changes, and replace all tracked, local files and directories with the latest commit (HEAD). Only untracked files and directories are left untouched. This action is marked very dangerous, because it recursively destroy all local changes, staged or not, and can't be recoverable.
- **(DANGEROUS)** Remove untracked files and directories: `git clean -f`. Should check with `git clean -n` first, because git will list files and directories that it would remove without actually doing it.

## Work with remote repo

1. Check remote URLs: `git remote -v`
2. Pull changes from remote and merge into local: `git pull`
3. Check for changes from remote:  run `git fetch` first, then `git diff origin main`
4. Push changes to remote: `git push origin`
5. Change remote URL: `git remote set-url origin <new_url>`

