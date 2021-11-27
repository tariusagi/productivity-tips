# Migrate a single branch to a new remote repo
## Scenario 1: Migrate a single branch to an empty remote repo
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

## Scenario 2: Migrate a single branch to a NOT empty remote repo
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

