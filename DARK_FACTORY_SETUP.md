# Dark Factory setup for app-int

Status: scaffolding complete, not yet run. This doc is the checklist —
check items off as you complete them. Once a first real run reaches
`COMPLETED`, this doc gets rewritten into the final "how this integration
works" reference.

## What's already done (scaffolded in this repo)

- [x] Minimal app (`src/app_int/`, `tests/test_main.py`) so there's real code
      for the pipeline to work on.
- [x] `.dark-factory.yaml` — four-role pipeline (BA → ARCHITECTURE →
      DEVELOPMENT → QA), `repository.github_owner`/`github_repo` set to
      `mariakravchenko/app-int`, quality gate = `pytest -q` + `ruff check .`.
- [x] `.dark-factory/roles/*.yaml` — all four roles assigned `worker: claude-code`
      for this first run (simplest to get working; reassign per-role later
      if you want Copilot/Hermes in the mix).
- [x] `.dark-factory/instructions/*.md` — the BA/Architect/Developer/QA
      instructions each role reads.
- [x] `.github/workflows/resume.yml` — the CI resume trigger.
- [x] `.env.example` — names every variable you need to fill in.
- [x] `.gitignore` — excludes `.env` and `.dark-factory/runs/`.

## What you need to do

### 1. Install the Dark Factory CLI

```bash
uv tool install "dark-factory @ git+https://github.com/mariakravchenko/dark-factory.git"
```

(Not on PyPI yet — once it is, this becomes `uv tool install dark-factory`.)

### 2. Fill in `.env`

```bash
cd /Users/maryiakrauchanka/portfolio/app-int
cp .env.example .env
```

Then edit `.env` and fill in each value. Here's exactly what each one is and
where to get it:

| Variable | What it is | Where to get it |
|---|---|---|
| `DATABASE_URL` | Pooled Neon connection string (host has `-pooler`) | Neon Console → your project → Connection Details → pooled string. Rewrite the scheme to `postgresql+psycopg://`. |
| `DATABASE_URL_DIRECT` | Direct (non-pooled) Neon connection string | Same screen, toggle "Connection pooling" off to reveal the direct host (no `-pooler`). Same scheme rewrite. |
| `GITHUB_TOKEN` | Dark Factory's own comment/PR credential | GitHub → Settings → Developer settings → Fine-grained tokens → New token, scoped to `mariakravchenko/app-int` only, with **Contents** (read/write), **Issues** (read/write), **Pull requests** (read/write). |
| `DISPATCH_GITHUB_TOKEN` | Lets the webhook receiver trigger `resume.yml` | Same screen, a **separate** fine-grained token scoped to `mariakravchenko/app-int` only, with **only** the **Actions** (read/write) permission. |
| `GITHUB_WEBHOOK_SECRET` | Verifies inbound webhook deliveries are really from GitHub | You choose this value yourself — any random string (e.g. `openssl rand -hex 32`). You'll enter the same value on the GitHub webhook side in step 5. |
| `ANTHROPIC_API_KEY` | Credential for the `claude-code` worker (all 4 roles use it) | console.anthropic.com → API Keys. (Already present in your `dark-factory` repo's `.env` if you want to reuse the same key.) |

**Do not paste any of these values into chat** — fill `.env` directly
yourself; I never need to see the actual secret values, only confirmation
that they're set.

### 3. Apply the database schema

```bash
uv run --with alembic --with "dark-factory @ git+https://github.com/mariakravchenko/dark-factory.git" \
  alembic upgrade head
```

(This creates the `runs`, `role_executions`, `run_events`, `human_interactions`,
and `artifacts` tables in your Neon database — the same schema Dark Factory's
own repo uses, applied against *your* connection string via `.env`.)

Tell me once `.env` is filled in and this command has run — I'll help
troubleshoot if it errors, but I won't run it for you since it touches your
real database credentials.

### 4. First local run — no GitHub, no webhook yet

```bash
cd /Users/maryiakrauchanka/portfolio/app-int
dark-factory run text:"Add a subtract(a, b) function to app_int/main.py, with a test"
dark-factory status <the-run-id-it-printed>
```

This exercises the whole pipeline (BA → Architect → Developer → QA → quality
gate) against this repo with zero GitHub involvement. If it reaches
`COMPLETED`, the core setup works.

### 5. GitHub issue intake + webhook (only once step 4 passes)

1. Push this repo to `mariakravchenko/app-int` (it's already empty with that
   remote configured) — I can do this once you confirm the content looks
   right.
2. Open a real issue on `mariakravchenko/app-int`, e.g. "Add a subtract
   function."
3. Run `dark-factory run github:<issue-number>`.
4. **Webhook receiver** — this is a separate process you host (not something
   `dark-factory run`/`resume` does on its own):
   - Install the optional extra: `uv tool install "dark-factory[webhook] @ git+https://github.com/mariakravchenko/dark-factory.git"`
   - Run it: `uvicorn dark_factory.webhook.app:build_app --factory --host 0.0.0.0 --port 8000`
   - Expose it to the internet somehow (a tunnel like `ngrok http 8000` is the
     fastest way to test this; a real deployment would put it behind a proper
     host).
   - On GitHub: repo Settings → Webhooks → Add webhook → Payload URL = your
     exposed URL, Content type = `application/json`, Secret =
     `GITHUB_WEBHOOK_SECRET`'s value, events = **Issue comments** only.
5. Reply on the issue with the clarifying answer (if the run paused) — the
   receiver should record it and dispatch `resume.yml` automatically.

### 6. Once a run completes and opens a real PR

That's the signal to rewrite this doc into the final reference — tell me and
I'll do that pass.

## Notes

- Run Dark Factory commands **from inside this repo** (`/Users/maryiakrauchanka/portfolio/app-int`),
  never from inside the `dark-factory` repo itself — `.dark-factory.yaml`,
  `.env`, and all git operations resolve against the current working
  directory.
- `.dark-factory/runs/<run-id>/` fills up with each run's artifacts locally;
  it's git-ignored.
