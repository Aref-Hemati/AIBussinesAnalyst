# تحلیلگر کسب‌وکار (Dify Chatflow)

## Import

1. Dify Studio → **Create App** → **Import DSL**
2. Select `business-analyst-fa-chatflow.dify.yml`
3. After import, open any **LLM** or **Question Classifier** node and confirm model **OpenAI-API-compatible → openai/gpt-4o** (or `moonshotai/kimi-k3` if you prefer)
4. Publish and chat — no Knowledge Base, plugins, or env vars required

Built-in default **org hard rules** apply until you upload your standards file.

## End-to-end flow

```mermaid
flowchart LR
  A[Start / sys.query + files] --> B{Files attached?}
  B -->|yes| C[Document Extractor]
  C --> D[Join file text]
  D --> E[Save last_uploaded_file_text]
  B -->|no| F[Clear file text]
  F --> G[Question Classifier]
  E --> G
  G --> R[Rules LLM]
  G --> Q[Requirements LLM]
  G --> V[Version freeze LLM]
  G --> H[HTML demo LLM]
  G --> X[General BA LLM]
  R --> R2[Parse canonical rules] --> RA[Answer]
  Q --> Q2[Update draft] --> QA[Answer]
  V --> V2[Version record + clear draft] --> VA[Answer]
  H --> HA[Answer with HTML block]
  X --> XA[Answer]
```

## Conversation memory (per chat)

| Variable | Purpose |
|----------|---------|
| `org_hard_rules` | Mandatory integration/UI/login standards |
| `draft_requirements` | Working set until version is frozen |
| `current_version_number` | Last frozen version index |
| `version_records` | Archive of frozen versions (markdown FA) |
| `project_title` | Optional project name |
| `last_uploaded_file_text` | Text from files in the current turn |

## User intents (Farsi examples)

| Intent | Example |
|--------|---------|
| Rules | «استاندارد فرم و SSO را از فایل بخوان» |
| Requirement | «ثبت کن: کاربر بتواند درخواست مرخصی ثبت کند» |
| Freeze version | «نسخه را قطع کن» / «freeze» |
| HTML demo | «نمونه HTML با داده دمو بساز» |
| BA dialogue | Clarifications, challenges, scope questions |

## Versioning policy (enforced in prompts)

- Changes accumulate in **draft** during an RFP cycle
- **Freeze** produces an immutable version document and clears the draft for the next cycle
- HTML demo uses draft + rules (+ optional uploaded RFP text)

## Model note

DSL references `langgenius/openai_api_compatible/openai_api_compatible` and `openai/gpt-4o`. If your credential uses another model id, change it once in the classifier and LLM nodes — the graph does not depend on OpenRouter or Knowledge Base.
