# Install Second Brain Starter

Use this checklist in a **target repository**. Prefer the Cursor skill `.cursor/skills/install-second-brain/SKILL.md` when an agent drives the install (open **this kit** as the Cursor workspace, then pass the target path — the skill is not copied into the target).

**Kit root:** the clone of this repository (the directory that contains this file). The vault template folder is literally `obsidian/{{PROJECT}}/` until renamed.
**Principle:** Prefer **official** apps and plugins. This kit only ships the LLM wiki scaffold + thin Cursor rules; it does **not** vendor Hindsight.

| Piece | Official source |
|---|---|
| Obsidian | [obsidian.md](https://obsidian.md) (or Homebrew cask) |
| Hindsight Cursor plugin + hooks/MCP | [`hindsight-cursor`](https://hindsight.vectorize.io/sdks/integrations/cursor) (`pip install` + `init`) |
| Hindsight local daemon | `hindsight-embed` via the official plugin / `uvx` (port **9077**) |
| Wiki schema / vault seed | this repository |

Docs: [Obsidian](https://obsidian.md) · [Hindsight Cursor](https://hindsight.vectorize.io/sdks/integrations/cursor)

---

## 1. Choose project name

Pick `PROJECT` (filesystem-safe). Default: target repo folder name.

Vault will live at `obsidian/<PROJECT>/`.

## 2. Copy wiki scaffold from this kit

Copy into the target repo (merge; never delete unrelated files):

- `AGENTS.md`, `CLAUDE.md` — skip overwriting existing `AGENTS.md` unless user asks to replace
- `.cursor/rules/llm-wiki.mdc`
- `.cursor/rules/hindsight-vs-obsidian.mdc` (wiki ↔ memory boundary; complements the official Hindsight rule)
- `tools/` (`wiki-lint.py`, `wiki-search.py`, `wiki-config.example.json`)
- `obsidian/{{PROJECT}}/` tree

Do **not** copy a vendored Hindsight plugin, hooks, or MCP from this kit — those come from official `hindsight-cursor init` (next section).

Do **not** copy `hindsight-session.mdc` (generated at runtime).

### Substitute and rename

1. Rename `obsidian/{{PROJECT}}` → `obsidian/<PROJECT>`.
2. Replace every `{{PROJECT}}` string in copied file contents with `<PROJECT>`.
3. Write `tools/wiki-config.json`:

```json
{"vault": "obsidian/<PROJECT>"}
```

### Gitignore (wiki + Obsidian)

Ensure the target `.gitignore` includes:

```
.cursor/rules/hindsight-session.mdc
tools/wiki-config.json
obsidian/*/.obsidian/workspace.json
obsidian/*/.obsidian/workspace-mobile.json
obsidian/*/.obsidian/cache
obsidian/*/.trash/
obsidian/*/.obsidian/plugins/
__pycache__/
*.pyc
.DS_Store
```

(`hindsight-cursor init` may also append its own ignore line — keep both.)

## 3. Obsidian (official app)

1. If Obsidian is not installed:
   - macOS: `brew install --cask obsidian`
   - Windows / Linux / macOS: download from [https://obsidian.md](https://obsidian.md)
2. **Open folder as vault** → `<target-repo>/obsidian/<PROJECT>/` (absolute path preferred).
3. Confirm you see `wiki/`, `raw/`, and `home.md`.

Do **not** open the repo root as the vault.

## 4. Hindsight (official Cursor plugin)

Follow the [official Cursor integration](https://hindsight.vectorize.io/sdks/integrations/cursor). Prefer **local daemon** on port **9077** for this pack’s MCP expectations.

### 4a. Install + init in the target repo

```bash
pip install hindsight-cursor   # or: uvx hindsight-cursor …
cd /path/to/target-repo
hindsight-cursor init          # local / auto-daemon path — do NOT pass --api-url unless using cloud/self-hosted
```

What official `init` does (do not hand-roll these):

- Copies plugin into `.cursor-plugin/hindsight-memory/`
- Merges Hindsight entries into `.cursor/hooks.json`
- Writes `.cursor/mcp.json` Hindsight MCP endpoint
- Creates `~/.hindsight/cursor.json` **only if missing**

Use `--force` only when intentionally replacing an existing Hindsight install. Use cloud instead with `--api-url` / `--api-token` if you prefer hosted memory (then skip local health on 9077).

**Fully quit and reopen Cursor** after init — plugins load at startup.

### 4b. User-global + daemon profile (recommended stack)

`~/.hindsight/cursor.json` is **user-global**. Keep missions **domain-agnostic**. Merge missing keys; do not wipe a working config.

**Model split (via [OpenRouter](https://openrouter.ai)):**

| Role | Model |
|---|---|
| Cursor / coding | **Qwen** (picker) |
| Retain / default Hindsight LLM | **Qwen** flash |
| Consolidation LLM | **GLM** 5.3 flash |
| Consolidation decisions | **Jev** (`typesafe/jev-1.14`) |
| Embeddings | e.g. Perplexity embed |
| Recall rerank | `rrf` (Jev **off** for recall) |

```bash
export OPENROUTER_API_KEY="…"
```

**Recommended `~/.hindsight/cursor.json`** (retain stays on Qwen):

```json
{
  "useLocalDaemon": true,
  "hindsightApiUrl": "",
  "apiPort": 9077,
  "bankId": "cursor",
  "agentName": "cursor",
  "bankMission": "You are a Cursor coding assistant. Remember decisions and rationale, working preferences, project context, important discoveries, topic relationships, and corrections/superseded assumptions. Do not memorize full Obsidian documents — those live in each project's vault. Prefer short durable facts over long prose.",
  "retainMission": "Extract decisions and their rationale, working preferences, project/context facts, important discoveries, relationships between topics, and corrections that supersede earlier assumptions. Ignore greetings, transient tool noise, and verbatim Obsidian page content.",
  "autoRecall": true,
  "autoRetain": true,
  "retainMode": "chunked",
  "retainEveryNTurns": 5,
  "retainOverlapTurns": 1,
  "retainToolCalls": false,
  "recallBudget": "mid",
  "recallMaxTokens": 1536,
  "llmProvider": "openrouter",
  "llmModel": "qwen/qwen3.7-flash",
  "llmApiKeyEnv": "OPENROUTER_API_KEY",
  "daemonIdleTimeout": 600
}
```

Replace model ids with **current** OpenRouter SKUs when they move.

**Recommended daemon profile env** (`hindsight-embed` profile `cursor` — set via `uvx hindsight-embed profile set-env …` or edit `~/.hindsight/profiles/cursor.env`, then restart the daemon). Keys shown as `***`:

```json
{
  "HINDSIGHT_API_PORT": "9077",
  "HINDSIGHT_EMBED_DAEMON_IDLE_TIMEOUT": "600",

  "HINDSIGHT_API_LLM_PROVIDER": "openrouter",
  "HINDSIGHT_API_LLM_MODEL": "qwen/qwen3.7-flash",
  "HINDSIGHT_API_LLM_API_KEY": "***",
  "HINDSIGHT_API_LLM_REASONING_EFFORT": "none",
  "HINDSIGHT_API_LLM_EXTRA_BODY": "{\"reasoning\":{\"effort\":\"none\",\"enabled\":false}}",
  "HINDSIGHT_API_RETAIN_LLM_REASONING_EFFORT": "none",
  "HINDSIGHT_API_RETAIN_LLM_EXTRA_BODY": "{\"reasoning\":{\"effort\":\"none\",\"enabled\":false}}",

  "HINDSIGHT_API_CONSOLIDATION_LLM_PROVIDER": "openrouter",
  "HINDSIGHT_API_CONSOLIDATION_LLM_MODEL": "z-ai/glm-5.3-flash",
  "HINDSIGHT_API_CONSOLIDATION_LLM_API_KEY": "***",
  "HINDSIGHT_API_CONSOLIDATION_LLM_REASONING_EFFORT": "high",
  "HINDSIGHT_API_CONSOLIDATION_LLM_EXTRA_BODY": "{\"reasoning\":{\"effort\":\"high\",\"enabled\":true}}",
  "HINDSIGHT_API_CONSOLIDATION_USE_DECISION_MODEL": "true",

  "HINDSIGHT_API_DECISION_MODEL_PROVIDER": "typesafe",
  "HINDSIGHT_API_DECISION_MODEL_BASE_URL": "https://openrouter.ai/api",
  "HINDSIGHT_API_DECISION_MODEL_MODEL": "typesafe/jev-1.14",
  "HINDSIGHT_API_DECISION_MODEL_API_KEY": "***",
  "HINDSIGHT_API_DECISION_MODEL_TOKENIZER": "jev",
  "HINDSIGHT_API_RECALL_DECISION_MODEL_PROVIDER": "none",

  "HINDSIGHT_API_EMBEDDINGS_PROVIDER": "openrouter",
  "HINDSIGHT_API_EMBEDDINGS_OPENROUTER_MODEL": "perplexity/pplx-embed-v1-0.6b",
  "HINDSIGHT_API_EMBEDDINGS_OPENROUTER_API_KEY": "***",
  "HINDSIGHT_API_EMBEDDINGS_LOCAL_FORCE_CPU": "1",
  "HINDSIGHT_API_RERANKER_PROVIDER": "rrf",
  "HINDSIGHT_API_RERANKER_LOCAL_FORCE_CPU": "1"
}
```

See also [`examples/hindsight-profile.env.example`](examples/hindsight-profile.env.example).

### 4c. Daemon health

Probe:

```bash
curl -sf http://127.0.0.1:9077/health && echo "Hindsight OK"
```

If unhealthy after init + config:

1. Ensure [uv](https://docs.astral.sh/uv/) / `uvx` is on PATH (plugin uses it for `hindsight-embed`).
2. Ensure `OPENROUTER_API_KEY` (or configured key) is available to the daemon.
3. Let the official plugin auto-start the daemon on next session, or start once:

```bash
uvx hindsight-embed@latest profile create cursor --merge --port 9077
uvx hindsight-embed@latest daemon --profile cursor start
```

4. Re-probe. Check `~/.hindsight/profiles/cursor.log` if it still fails.

Verify hooks later via official state files (`~/.hindsight/cursor-state/state/last_recall.json`, `last_retain.json`) — see Hindsight docs.

## 5. Verify wiki

```bash
python3 tools/wiki-lint.py
```

Expected: `clean — … pages, no findings`

Also:

- [ ] Obsidian vault open on `obsidian/<PROJECT>/`
- [ ] Official Hindsight plugin present (`.cursor-plugin/hindsight-memory/`)
- [ ] `curl -sf http://127.0.0.1:9077/health` (local mode)
- [ ] Project identity filled in `AGENTS.md`

## 6. Log

Append to `obsidian/<PROJECT>/wiki/log.md`:

```markdown
## [YYYY-MM-DD] install | Second Brain Starter + official Hindsight Cursor plugin
```
