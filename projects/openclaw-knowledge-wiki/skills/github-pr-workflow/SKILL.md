---
name: github-pr-workflow
version: 0.1
status: draft-local-only
scope: project
safe_to_execute_default: false
---

# github-pr-workflow

## Purpose

Assist Neodaemon with a safe, manual GitHub PR workflow.

This skill reduces repetitive checklist work, but it is not autopilot and not a technical security boundary.

If repo, branch, paths, secrets, main status, diff, or authorization are unclear:

```text
BLOCK
```

## Non-goals

- No autopilot.
- No automatic commit.
- No automatic push.
- No gh pr create in MVP.
- No merge.
- No git add .
- No `git add -A`.
- No force push.
- No `git reset --hard` as standard rollback.
- No gateway/auth/tokens/systemd/.env/logs raw access.
- No modification of `~/.openclaw/skills` in MVP.

## Required inputs

- `repo_path`
- `base_branch`
- `working_branch`
- `intended_change_summary`
- `allowlisted_paths`
- `source_paths`
- `destination_paths`
- `requested_phase`

## Workflow states

```text
S0_IDLE
S1_CONTEXT_CHECK
S2_REPO_VERIFY
S3_BRANCH_VERIFY
S4_MAIN_SYNC_VERIFY
S5_WORKTREE_CLEAN_VERIFY
S6_ALLOWED_PATHS_VERIFY
S7_COPY_PLAN
S8_SECRET_SCAN
S9_DIFF_REVIEW
S10_COMMIT_TEXT_READY
S11_PUSH_PLAN_READY
S12_PR_TEXT_READY
S13_WAIT_HUMAN_REVIEW
S_BLOCKED
```

## Mandatory checks

Before any non-trivial step, verify:

1. repo path is explicit and correct;
2. branch is explicit and correct;
3. remote is explicit and correct;
4. `main` is verified against `origin/main`;
5. working tree is clean before copy;
6. source/destination paths are explicit;
7. allowlist is applied first;
8. forbidden paths are blocked;
9. secret scan is silent and complete;
10. diff is reviewed;
11. Albert authorization is present for the requested phase.

Never assume GitHub `main` is current without verification.

## Allowlist-first rule

Only paths explicitly authorized by Albert may be touched.

Everything outside allowlist:

```text
BLOCK
```

## Forbidden paths by default

```text
/openclaw/.env
/home/openclaw/.openclaw/
/openclaw/workspace/main/.git/
/openclaw/workspace/main/logs/
/openclaw/workspace/main/systemd/
/openclaw/workspace/main/rag_store/
/openclaw/workspace/main/context_repo/personal/
/openclaw/workspace/main/backups/
/etc/
/var/log/
```

Special cases:

- `/tmp` is forbidden as write destination or Git source.
- `/tmp` may only be used for authorized read-only safe scans.
- `/openclaw/bots` and `/openclaw/tools` are forbidden by default.
- `/openclaw/bots` and `/openclaw/tools` require explicit Albert authorization and a specific plan.

## Secret scan

Silent only. Output must include only:

```text
count
path
pattern_type
```

Never print matching lines or matched values.

Patterns:

```text
api.telegram.org/bot
bot<digits>:<secret>
TELEGRAM_BOT_TOKEN
OPENAI_API_KEY
ANTHROPIC_API_KEY
GITHUB_TOKEN
ghp_
gho_
ghs_
BEGIN PRIVATE KEY
password=
token=
secret=
credential=
```

Any finding:

```text
BLOCK until Albert reviews the finding type.
```

Never print the matched value.

## Allowed command templates

These are templates for proposing commands to Albert, not commands for autonomous execution.

```bash
git status --short
git branch --show-current
git remote -v
git fetch origin
git rev-parse HEAD
git rev-parse origin/main
git log --oneline --decorate -n 5
git diff --stat
git diff -- <allowlisted-path>
git diff --cached --stat
git add <allowlisted-path>
git commit -m "<message>"
git push origin <branch>
```

## Forbidden commands

```bash
git add .
git add -A
git commit -am
git push --force
git push --force-with-lease
git reset --hard
git clean -fd
git merge
git rebase
gh pr create
gh pr merge
gh repo sync
```

Also forbidden:

```text
sudo
docker
systemctl
openclaw gateway restart
editing ~/.openclaw/skills
reading raw logs
```

## Authorization gates

Albert must explicitly authorize each phase:

- copy files;
- `git add <path>`;
- `git commit`;
- `git push`;
- use generated PR text/URL;
- any path outside allowlist;
- any medium/high risk action;
- any secret-scan finding type review.

The skill can never authorize merge.

## Standard output

```yaml
workflow_state: S_BLOCKED
repo: ""
branch: ""
base: "main"
main_status: unknown
working_tree: unknown
allowed_paths: []
blocked_paths: []
secret_scan:
  status: not_run
  findings_count: 0
risk_level: medium
requires_albert_authorization: []
blocked_actions:
  - merge
  - gh_pr_create
next_recommended_action: ""
safe_to_execute: false
```

## PR text template

```markdown
## Summary

- ...

## Safety notes

- Scope limited to allowlisted paths.
- No gateway/auth/tokens/systemd/.env changes.
- No logs or raw secrets included.
- Secret scan: PASS/FAIL.
- Working tree before commit: clean/dirty.
- Base branch checked against origin/main.
- Automatic merge: prohibited.

## Validation

- [ ] File inspection
- [ ] Silent secret scan
- [ ] Diff reviewed
- [ ] Tests/lint if applicable

## Rollback

- Before commit: restore explicit files only.
- After commit: revert commit or abandon branch.
- After push: close PR or push revert commit.
```

## Rollback by phase

- Before copy: no-op.
- After copy, before add: restore explicit files only.
- After add: `git restore --staged <path>`.
- After commit: `git revert <commit>` or abandon branch.
- After push: close PR or push revert commit.
- After PR text generated: discard text.
- After merge: out of MVP; requires human plan.

## Stop conditions

Immediately block if:

- repo unknown;
- branch unknown;
- `main` not verified;
- working tree unexpectedly dirty;
- path outside allowlist;
- forbidden path touched;
- secret scan finding exists and Albert has not reviewed finding type;
- command would print secrets;
- user requests merge;
- user requests `git add .`;
- user requests `gh pr create` in MVP;
- authorization is missing.
