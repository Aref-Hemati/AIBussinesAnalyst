# Software and implementation

Paper method first. Tools second. Dify is one front-end, not the research platform.

Last updated: 2026-09-16.

## What already exists (company prototype)

Repo root:

| File | Role |
|------|------|
| `business-analyst-fa-chatflow.dify.yml` | Dify advanced-chat: file ingest, intent classifier, rules / requirements / freeze / HTML demo / general BA |
| `WORKFLOW.md` | Human docs for the chatflow |
| `TROUBLESHOOTING.md` | Import/model issues |

Conversation state already useful for the paper:

- `org_hard_rules` — domain constraints (SSO, RTL, forms, RBAC)
- `draft_requirements` — working spec
- `current_version_number` + `version_records` — **RE management / freeze**
- `last_uploaded_file_text` — RFP path
- `project_title`

**Gap vs the paper:** there is no Requirement Decision object, no forced critic, no schema gate, no evaluation harness. The BA LLM can challenge in natural language, but Vanilla-like generation can still emit FR lists without REJECT.

## Implementation policy

1. Implement the method in **portable Python** (research + GitHub artifact).
2. Keep the **Persian Dify** app as the company UX; sync *behavior* when Dify can represent it.
3. Dify YAML updates are optional mirrors, not the source of truth for experiments.
4. Do not depend on a single vendor model. Config: OpenRouter / OpenAI-compatible / local.

Suggested languages/tools (research):

| Layer | Suggestion | Why |
|-------|------------|-----|
| Agents | Python, Pydantic models, one orchestrator | Reproducible, testable |
| Spec store | JSON files or SQLite | Simple artifact |
| RAG | Chroma or SQLite embeddings (Yin used Chroma) | Optional M4 |
| Eval | pytest + CSV metrics | Fills `07` |
| Optional UI | Open WebUI, Gradio, or keep Dify | Company already on Dify |
| Optional later | LangGraph / similar | Only if loops get hard |

Dify support: DSL can encode extra LLM nodes (Critic, Decision parse). Structured JSON via LLM + template/code node is possible but fragile. **Do not wait on Dify JSON mode to start experiments.**

## Target architecture (maps to RQs)

```
USER / FILE
   │
   ▼
Conversation Agent          # dialogue, language, tone
   │
   ▼
Candidate Extractor         # utterances → candidate statements
   │
   ▼
Requirement Critic          # RQ2  (can be 1 LLM + schema, not 6 agents)
   │    ambiguity | conflict | duplicate | unjustified
   │    evidence | feasibility | org-rule
   ▼
Decision + Question Policy  # M2 budgets
   │
   ├── CLARIFY / REJECT ──► question or alternative ──► USER
   │
   └── ACCEPT ──► Spec Writer (FR, NFR, story, AC)
                    │
                    ▼
              Requirement Store (JSON) + Trace
                    │
                    ▼
              Freeze / Version  ──► stakeholder confirm   # RQ5, SMS 8% gap
                    │
                    ▼
              Exporters: Markdown FRD, stories, HTML demo
```

Specialist agents (quality, conflict, completeness, priority) are **optional fans** behind the Critic, added only after ablation.

## Research code (started 2026-09-16)

Package `reqdecide` at the repo root, installed from `src/` via `pyproject.toml`.

| Module | Role |
|--------|------|
| [`src/reqdecide/schema.py`](../src/reqdecide/schema.py) | `Decision`, `Requirement`, `Project`, `TurnInput`, `CostModel`. **The M8 gate is a validator**: a `Project` containing a requirement whose `decision_id` is not an ACCEPT decision fails to construct |
| [`src/reqdecide/uncertainty.py`](../src/reqdecide/uncertainty.py) | K-sample interpretation entropy. Clusters independent readings of an utterance and returns `UncertaintySignal`; high entropy means the statement is ambiguous, low entropy with low confidence means the model lacks knowledge |
| [`src/reqdecide/adapters/github_issues.py`](../src/reqdecide/adapters/github_issues.py) | V3 corpus builder: fetch issues, keep feature requests, map maintainer outcomes to decision labels, drop capacity/staleness closures, emit the stratified audit CSV |
| [`tests/test_core.py`](../tests/test_core.py) | Behaviour that must survive every replay: label/action coherence, orphan-FR rejection, entropy, outcome mapping |

Still to write: `policy.py` (cost-sensitive admission), `critics/`, `eval/`, and the `reqpairs` / `gym` / `industrial` adapters.

Fetched corpora live under `data/` and are **git-ignored**; rebuild them from the adapters rather than committing issue dumps.

## Project model (schema sketch)

Implemented in [`src/reqdecide/schema.py`](../src/reqdecide/schema.py). A JSON Schema export (`research/schemas/project.schema.json`) can be generated from the pydantic models when we publish the dataset.

Minimum viable fields:

```text
Project
  id, title, language, org_rule_set_id
  messages[]          # role, text, t
  candidates[]        # Decision objects
  requirements[]      # only those with ACCEPT
  open_questions[]
  versions[]          # freeze snapshots
```

Generator rule (M8): **no requirement row without `decision_id`.**

## GitHub artifact plan (goal 2)

Public repo should contain:

- English README + quickstart
- `src/` agent loop
- `eval/` scripts and tiny public dialogues (not company secrets)
- `examples/` blockchain/WhatsApp script
- Export to Markdown
- License
- Model provider via env vars

Company fork or private submodule: Persian prompts, real `org_hard_rules`, Dify YAML.

## Syncing Dify (when we have a Decision loop)

If Dify can support it, add:

1. LLM node “Critic” → JSON
2. Template/code parse
3. If-else: ask question vs update `draft_requirements`
4. Store last decisions in a conversation variable `requirement_decisions`

If Dify cannot reliably parse JSON, **do not distort the method** to fit Dify. Run research code and keep Dify as a looser BA UX.

## Non-goals for v1 software

- Fine-tuning
- Mobile app
- Full ALM (Jira) integration — nice for industry, not for the first paper unless trace export is cheap
- HTML demo quality — product only
