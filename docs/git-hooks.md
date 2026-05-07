# Git hooks

This repo ships a `pre-push` hook in `.githooks/` that blocks pushes when
`origin` doesn't match the canonical remote recorded in
`.githooks/expected-remote.txt`. This is Layer 3 of the three-layer
remote-verification rule (the ADR lives in the private opennod-knowledge
repo: `decisions/2026-05-05-three-layer-remote-verification.md`).

## One-time install (per clone)

After cloning, run once:

```
git config core.hooksPath .githooks
```

This points git at the in-repo hooks directory. The setting is local to
your clone (stored in `.git/config`) and does not propagate to others, so
every fresh clone needs it once.

## What it does

On `git push`, the hook compares `git remote get-url origin` against
`.githooks/expected-remote.txt`. If they differ (after normalizing SSH /
HTTPS / `.git`-suffix variants), the push is blocked with a loud error.

SSH and HTTPS forms of the same repo are treated as equivalent — only the
underlying `OWNER/REPO` matters.

## If you hit a block

1. Run `git remote -v` to see what `origin` actually points at.
2. Compare against `.githooks/expected-remote.txt`.
3. Fix the remote (`git remote set-url origin <canonical>`) or move your
   work to the correct clone.

## Why

A directory named for a canonical repo is no guarantee the clone actually
points there — forks, re-pulls, and renamed remotes can silently put a
working copy on the wrong remote. This hook fails closed at push time so
mistakes don't propagate.
