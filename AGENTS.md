# AGENTS.md -- ansible-elasticsearch

This file is the vendor-neutral brief for coding agents. There is no `CLAUDE.md`.
Read it before opening a pull request.

Do not put private infrastructure, internal tool names, other repository names,
or environment topology in this file, in pull request titles, or in commit
messages. This repository is public.

## What this repo is

Public fork of [elastic/ansible-elasticsearch](https://github.com/elastic/ansible-elasticsearch).
Ansible role that installs and configures Elasticsearch. This repository is the
role only.

## Layout

```text
defaults/main.yml       Role defaults (version, paths, API, SSL, X-Pack)
tasks/                  Install, config, plugins, SSL, X-Pack/security
templates/              elasticsearch.yml, jvm.options, repo, security files
filter_plugins/custom.py  Jinja filters used by tasks and templates
handlers/main.yml       Restart/reload
molecule/               Integration scenarios: default, security, custom-config
tests/                  Unit tests for filter_plugins (pytest)
```

Most work happens in `tasks/`, `templates/`, `defaults/main.yml`, and
`filter_plugins/custom.py`.

## Pull request titles

The GitHub PR title is the primary signal for humans, release-drafter, and
coding agents. It must describe the actual change so someone can understand the
PR without opening the diff.

Use [Conventional Commits](https://www.conventionalcommits.org):

```text
type: imperative summary
type(scope): imperative summary
```

Allowed types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `ci`, `perf`.

**Required**

- Name the behaviour, file, or subsystem that changed (filters, SSL, molecule, FQCN, …).
- Match the title to the commits and the diff. If the work is a bug fix, the type is `fix:`, not `chore:` or `refactor:`.
- Keep it specific enough that an agent can decide whether the PR is relevant without reading the body.

**Forbidden** — these titles are not context-aware and must not be used:

- `Daily code improvement (YYYY-MM-DD)`
- `Weekly code improvement (YYYY-MM-DD)`
- `Daily code improvement`
- Dated batch names, generic agent labels, or “misc fixes”

| Bad | Good |
| --- | --- |
| `Daily code improvement (2026-09-08)` | `fix: avoid mutable default arguments in custom filter plugins` |
| `Weekly code improvement (2026-05-29)` | `refactor: extract shared reserved-entry predicate in custom filters` |
| `misc improvements` | `chore: qualify remaining module invocations with FQCNs` |

If a scheduled agent run produces several unrelated fixes, open **one PR per
change** (or at least one PR per concern), each with its own context-aware title.
Do not bundle them under a dated catch-all.

The PR title and the subject of the main commit should say the same thing.

## Commits

- Conventional Commits, imperative mood (`avoid`, `extract`, `qualify` — not `avoided` / `extracting`).
- Do not commit secrets, license files, or `.env`.
- Do not mention private systems, internal tools, or other repositories.

## Tests

- Filter changes: add or extend `tests/test_custom_filters.py` and run
  `python3 -m pytest tests -q`.
- Role behaviour: Molecule scenarios `default`, `security`, `custom-config`
  (`molecule test -s <scenario>`). CI runs Molecule on pull requests.
- Do not “fix” a filter by changing its default handling without a test that
  pins omitted arguments and the previously untested call paths.

## Coupled changes

- New Jinja filter → register it in `FilterModule.filters()`, unit-test it, and
  use it from a task or template.
- `es_config` / template change → check `templates/elasticsearch.yml.j2` and any
  `es_config_*` override variables.
- Security user/role filters (`filter_reserved`, `extract_role_users`) → tasks
  under `tasks/xpack/security/`. Call sites are positional Jinja pipes; keep
  parameter names consistent across sibling filters.

## Anti-patterns

- Do **not** use mutable default arguments (`values=[]`, `users={}`) in
  `filter_plugins/`. Default to `None` and assign with `if x is None:` (not
  `x = x or []`, which treats empty strings as missing).
- Do **not** edit rendered config on Elasticsearch hosts; change templates here.
- Do **not** add narrating comments that restate the next line.
- Do **not** retitle a specific change as a dated “daily/weekly improvement”.
