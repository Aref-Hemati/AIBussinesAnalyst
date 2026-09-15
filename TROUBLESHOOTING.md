# Dify troubleshooting — Business Analyst chatflow

## “Caution: DSL version difference may affect certain features”

This is a **normal import warning**, not a failure. It means the YAML `version:` (e.g. `0.7.0`) is not exactly the same as your Dify server’s current App DSL version.

**What to do:**

1. Click **Confirm / Import anyway** — the app usually works.
2. If import is blocked, tell us your Dify version (Settings → About) and we can match the YAML `version` field (`0.6.0` vs `0.7.0`).
3. After import, **Publish** again. The warning does not mean you must paste `WORKFLOW.md` anywhere.

---

## “This model is not available / Incompatible” (strikethrough model)

The DSL pins a **provider + model id**. If that pair is not enabled in your workspace, every LLM node shows **Incompatible** and runs fail with Internal Server Error.

**Current repo default (updated):**

| Field | Value |
|-------|--------|
| Provider | **OpenRouter** (`langgenius/openrouter/openrouter`) |
| Model | **`gpt-5.6-sol-pro`** (same as in your Studio screenshot) |

**Fix without re-import:**

1. Open **each** LLM node + **Question Classifier** (`تشخیص نیت کاربر`).
2. Model → choose **OpenRouter** → **`gpt-5.6-sol-pro`**.
3. Save → **Publish**.

**Fix with re-import:** Import the latest `business-analyst-fa-chatflow.dify.yml` from GitHub, then Publish.

**Do not use** OpenAI-API-compatible + `openai/gpt-4o` unless that exact model is configured and shows **no** strikethrough in the model picker.

Ensure **Settings → Model Provider → OpenRouter (My OpenRouter)** has a valid API key.

---

## Do I need WORKFLOW.md in Dify?

**No.** `WORKFLOW.md` is documentation for humans only.

In Dify you only:

1. **Studio → Create app → Import DSL** → select `business-analyst-fa-chatflow.dify.yml`
2. **Publish** the app
3. Chat in **Preview** or the published URL

Nothing from `WORKFLOW.md` is pasted into Knowledge Base, prompts, or Start node.

---

## What you saw is normal vs error

| What you see | Meaning |
|--------------|---------|
| Long Persian welcome + suggested questions | **Opening statement** from DSL `features.opening_statement` — OK |
| Your message (e.g. about گواهی مبدا) | User turn — OK |
| **Workflow Process → Internal Server Error** | A **workflow node failed** on the server — not fixed by WORKFLOW.md |

---

## Step 1 — Find the failing node (most important)

1. Open the app in **Studio**.
2. Send the same message again in **Preview**.
3. Open **Workflow Process** (or click the run trace).
4. Click the **red / failed** step.
5. Open **LAST RUN** on that node and read the **error text** (often API/model/document extractor).

Note the node title, e.g.:

- `تشخیص نیت کاربر` → Question Classifier / model
- `استخراج متن فایل` → Document Extractor
- `پاک کردن متن فایل` / `ذخیره متن فایل` → Variable Assigner
- Any `LLM` node → model provider / token limit

---

## Step 2 — Model provider (very common)

Your DSL uses:

- **Provider:** OpenAI-API-compatible  
- **Model:** `openai/gpt-4o`

Checklist:

1. **Settings → Model Provider → OpenAI-API-compatible** → credentials valid (base URL + API key).
2. In Studio, open **each LLM** and **Question Classifier** node → **Model** → pick the same model from the dropdown (names must match exactly, e.g. `openai/gpt-4o`).
3. If your listing shows **4K context** for that model, long prompts will fail. Either:
   - Use a **larger-context** model (e.g. OpenRouter `gpt-4o` 128K), and set that on all LLM + classifier nodes, or
   - Re-import the latest YAML (lower `max_tokens` and lighter classifier memory).

Quick test: duplicate the app, replace classifier + one LLM with **OpenRouter → gpt-4o-mini**; if it works, the issue is the compatible provider or context size.

---

## Step 3 — Self-hosted Dify logs

If you run Dify with Docker:

```bash
docker logs dify-api --tail 200
```

(or your `api` / `worker` container name). Search for the timestamp of the failed run and `ERROR` / traceback.

Document extraction often needs the **api** + **worker** stack and optional **Unstructured** / file parser services depending on version.

---

## Step 4 — File upload path

If the error happens **only with attachments**:

- Failed node is often **Document Extractor** (`استخراج متن فایل`).
- Try the same question **without** a file.
- Ensure **Features → File upload** is enabled (DSL already enables it).
- On self-hosted, confirm document parsing is configured in Dify docs for your version.

---

## Step 5 — Variable Assigner

If the error mentions **Variable Assigner** / `variables is required`:

- Node **پاک کردن متن فایل (بدون پیوست)** must use operation **Clear**, not Overwrite with empty string.
- Re-import `business-analyst-fa-chatflow.dify.yml` from this repo if you fixed that locally in an old import.

---

## Step 6 — Minimal isolation test in Studio

Temporarily disconnect branches to see how far execution gets:

1. **Start** → connect directly to **گفتگوی BA** LLM → **Answer** (bypass if-else and classifier).
2. If that works, reconnect **Question Classifier** next.
3. Then add file branch again.

---

## Step 7 — Re-import updated DSL

Pull latest from GitHub or copy `business-analyst-fa-chatflow.dify.yml`, then **Import DSL** (or replace workflow). Publish again.

---

## Your example message

«راجب نرم افزار گواهی مبدا» (no file) should route to **general BA** or **requirement** LLM after:

`Start → if-else (no file) → clear file text → Question Classifier → LLM → Answer`

If it dies at **1/2**, the failure is usually early: **if-else**, **assigner**, or **classifier** — use Step 1 to see which.

---

## Still stuck?

Capture and share:

1. Failed **node name** (English or Persian title from Studio)
2. **LAST RUN** error message (exact text)
3. Dify version (Cloud vs self-hosted + version)
4. Whether a **file** was attached
5. Screenshot of **Model Provider** test for `openai/gpt-4o`
