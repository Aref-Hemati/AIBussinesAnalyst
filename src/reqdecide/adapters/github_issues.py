"""V3: feature requests labeled by the people who had to live with the decision.

Maintainers accept, decline, deduplicate, and ask for more information every day,
and they record the outcome in the issue state. Those labels exist independently
of this project, which is the whole point: they cannot be accused of being our
opinion about our own taxonomy.

The catch is that ``wontfix`` often means "nobody has time", which is not a
statement about whether the request should become a requirement. Every mapped
item therefore carries the theme that produced it and the text that triggered
it, decision-irrelevant themes are dropped by default, and
``stratified_audit_sample`` draws the sample two humans must check before any
number from this tier is reported.

Usage::

    python -m reqdecide.adapters.github_issues fetch --repo pallets/flask --out data/v3/raw/flask.jsonl
    python -m reqdecide.adapters.github_issues build --raw "data/v3/raw/*.jsonl" --out data/v3/decisions.jsonl --audit data/v3/audit-sample.csv
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterable, Iterator, Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..schema import DecisionLabel, SuperClass, super_class_of

GITHUB_API = "https://api.github.com"
USER_AGENT = "reqdecide-v3-corpus-builder"


# --------------------------------------------------------------------------
# Raw records
# --------------------------------------------------------------------------


class IssueComment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    author: str | None = None
    body: str = ""
    author_association: str | None = None
    created_at: datetime | None = None

    @property
    def by_maintainer(self) -> bool:
        return (self.author_association or "").upper() in {"OWNER", "MEMBER", "COLLABORATOR"}


class IssueRecord(BaseModel):
    """One issue, flattened. Field names follow the GitHub REST payload so the
    Hugging Face ``open-index/open-github-issues`` export loads unchanged."""

    model_config = ConfigDict(extra="ignore")

    repo: str
    number: int
    title: str = ""
    body: str = ""
    state: str = "open"
    state_reason: str | None = None
    labels: list[str] = Field(default_factory=list)
    created_at: datetime | None = None
    closed_at: datetime | None = None
    html_url: str | None = None
    comments: list[IssueComment] = Field(default_factory=list)
    is_pull_request: bool = False
    linked_merged_pr: bool = False

    @property
    def text(self) -> str:
        return f"{self.title}\n\n{self.body}".strip()

    @property
    def closing_text(self) -> str:
        """Maintainer comments, newest last. Where the rationale usually lives."""
        return "\n".join(c.body for c in self.comments if c.by_maintainer)


# --------------------------------------------------------------------------
# Feature-request filter
# --------------------------------------------------------------------------

FEATURE_LABELS = {
    "enhancement",
    "feature",
    "feature request",
    "feature-request",
    "type: feature",
    "type:feature",
    "kind/feature",
    "new feature",
    "proposal",
    "rfc",
}

BUG_LABELS = {"bug", "type: bug", "type:bug", "kind/bug", "defect", "regression", "crash"}

_FEATURE_TITLE_RE = re.compile(
    r"\b(feature request|add support|please add|would be (nice|great)|it would be|"
    r"support for|ability to|allow (us|me|users)|proposal|rfc)\b",
    re.IGNORECASE,
)


def looks_like_feature_request(issue: IssueRecord) -> bool:
    """Requirement admission is about wanted capability, not broken behavior."""
    labels = {label.lower() for label in issue.labels}
    if labels & BUG_LABELS:
        return False
    if labels & FEATURE_LABELS:
        return True
    return bool(_FEATURE_TITLE_RE.search(issue.title))


# --------------------------------------------------------------------------
# Rejection themes
# --------------------------------------------------------------------------


class RejectionTheme(str, Enum):
    """Why a request was declined.

    Derived from the published qualitative studies of wontfix issues. Only the
    themes that say something about the *request* are usable as gold decisions;
    the rest say something about the *project's capacity*.
    """

    UNNECESSARY = "unnecessary"
    ALREADY_IMPLEMENTED = "already_implemented"
    OUT_OF_SCOPE = "out_of_scope"
    DUPLICATE = "duplicate"
    INFEASIBLE = "infeasible"
    WORKS_AS_INTENDED = "works_as_intended"
    NO_CAPACITY = "no_capacity"
    STALE_OR_NO_RESPONSE = "stale_or_no_response"
    USER_ENVIRONMENT = "user_environment"
    UNKNOWN = "unknown"


DECISION_RELEVANT_THEMES = frozenset(
    {
        RejectionTheme.UNNECESSARY,
        RejectionTheme.ALREADY_IMPLEMENTED,
        RejectionTheme.OUT_OF_SCOPE,
        RejectionTheme.DUPLICATE,
        RejectionTheme.INFEASIBLE,
        RejectionTheme.WORKS_AS_INTENDED,
    }
)

_THEME_PATTERNS: list[tuple[RejectionTheme, re.Pattern[str]]] = [
    (
        RejectionTheme.DUPLICATE,
        re.compile(r"\b(duplicate of|dupe of|already (tracked|reported|filed)|see #\d+)\b", re.IGNORECASE),
    ),
    (
        RejectionTheme.ALREADY_IMPLEMENTED,
        re.compile(
            r"\b(already (supported|implemented|possible|exists)|this (already )?works|you can already)\b",
            re.IGNORECASE,
        ),
    ),
    (
        RejectionTheme.OUT_OF_SCOPE,
        re.compile(
            r"\b(out of scope|outside (the |our )?scope|not in scope|belongs in|"
            r"not something (we|this project)|beyond the scope|use a plugin|third[- ]party)\b",
            re.IGNORECASE,
        ),
    ),
    (
        RejectionTheme.INFEASIBLE,
        re.compile(
            r"\b(not (technically )?possible|infeasible|cannot be (done|implemented)|"
            r"upstream limitation|breaking change we (can|will) not)\b",
            re.IGNORECASE,
        ),
    ),
    (
        RejectionTheme.WORKS_AS_INTENDED,
        re.compile(r"\b(works as (intended|designed|expected)|by design|intended behaviou?r|not a bug)\b", re.IGNORECASE),
    ),
    (
        RejectionTheme.UNNECESSARY,
        re.compile(
            r"\b(don'?t think (this|it) is needed|not (worth|needed|necessary)|"
            r"no (real )?use case|too niche|adds (too much )?complexity|maintenance burden)\b",
            re.IGNORECASE,
        ),
    ),
    (
        RejectionTheme.USER_ENVIRONMENT,
        re.compile(
            r"\b(your (setup|environment|configuration)|user error|please ask on|support question|"
            r"not a (bug|problem) (in|with) )\b",
            re.IGNORECASE,
        ),
    ),
    (
        RejectionTheme.NO_CAPACITY,
        re.compile(
            r"\b(no (one|body) (is )?(working|available)|lack of (time|resources|maintainers)|"
            r"we do not have (the )?(time|bandwidth|resources)|unmaintained|looking for (a )?maintainer|"
            r"pull requests? welcome|patches welcome|help wanted)\b",
            re.IGNORECASE,
        ),
    ),
    (
        RejectionTheme.STALE_OR_NO_RESPONSE,
        re.compile(r"\b(stale|inactivity|no (response|activity|reply)|closing due to|automatically closed)\b", re.IGNORECASE),
    ),
]


def classify_rejection_theme(text: str) -> tuple[RejectionTheme, str | None]:
    """Return the theme and the phrase that triggered it, for the human audit."""
    for theme, pattern in _THEME_PATTERNS:
        match = pattern.search(text or "")
        if match:
            return theme, match.group(0)
    return RejectionTheme.UNKNOWN, None


# --------------------------------------------------------------------------
# Outcome mapping
# --------------------------------------------------------------------------

_DUPLICATE_LABELS = {"duplicate", "dupe", "status: duplicate", "resolution: duplicate"}
_WONTFIX_LABELS = {"wontfix", "won't fix", "wont-fix", "status: wontfix", "resolution: wontfix", "declined"}
_NEEDS_INFO_LABELS = {
    "needs more info",
    "needs-info",
    "needs info",
    "more information needed",
    "awaiting response",
    "question",
    "status: needs-info",
    "state:needs-info",
    "needs reproduction",
}
_ACCEPTED_LABELS = {"accepted", "state:accepted", "status: accepted", "approved", "roadmap", "planned"}


class NaturalDecision(BaseModel):
    """A gold item for V3: the request plus the decision a maintainer actually made."""

    model_config = ConfigDict(extra="forbid")

    repo: str
    number: int
    html_url: str | None = None
    title: str
    body: str
    label: DecisionLabel
    super_class: SuperClass
    theme: RejectionTheme = RejectionTheme.UNKNOWN
    decision_relevant: bool = True
    mapping_rule: str
    mapping_evidence: str | None = None
    labels: list[str] = Field(default_factory=list)
    state: str
    state_reason: str | None = None
    closed_at: datetime | None = None
    needs_audit: bool = False

    @property
    def statement(self) -> str:
        return f"{self.title}\n\n{self.body}".strip()


def map_issue(issue: IssueRecord) -> NaturalDecision | None:
    """Map one issue to a gold decision, or None when the outcome is unreadable.

    Precedence matters: an issue closed as a duplicate is a DUPLICATE even
    though it is also ``not_planned``.
    """
    labels = {label.lower() for label in issue.labels}
    maintainer_text = issue.closing_text

    def build(
        label: DecisionLabel,
        rule: str,
        *,
        theme: RejectionTheme = RejectionTheme.UNKNOWN,
        evidence: str | None = None,
        relevant: bool = True,
        needs_audit: bool = False,
    ) -> NaturalDecision:
        return NaturalDecision(
            repo=issue.repo,
            number=issue.number,
            html_url=issue.html_url,
            title=issue.title,
            body=issue.body,
            label=label,
            super_class=super_class_of(label),
            theme=theme,
            decision_relevant=relevant,
            mapping_rule=rule,
            mapping_evidence=evidence,
            labels=sorted(issue.labels),
            state=issue.state,
            state_reason=issue.state_reason,
            closed_at=issue.closed_at,
            needs_audit=needs_audit,
        )

    if labels & _DUPLICATE_LABELS:
        return build(DecisionLabel.DUPLICATE, "duplicate label", theme=RejectionTheme.DUPLICATE)

    theme, evidence = classify_rejection_theme(maintainer_text)
    if theme is RejectionTheme.DUPLICATE and issue.state == "closed":
        return build(
            DecisionLabel.DUPLICATE, "duplicate phrase in maintainer comment", theme=theme, evidence=evidence
        )

    if issue.linked_merged_pr or (labels & _ACCEPTED_LABELS):
        rule = "linked merged PR" if issue.linked_merged_pr else "acceptance label"
        return build(DecisionLabel.ACCEPT, rule)

    if issue.state == "closed" and issue.state_reason == "completed":
        return build(DecisionLabel.ACCEPT, "closed as completed")

    if labels & _NEEDS_INFO_LABELS:
        return build(DecisionLabel.CLARIFY, "needs-info label", theme=theme, evidence=evidence)

    if issue.state == "closed" and (issue.state_reason == "not_planned" or labels & _WONTFIX_LABELS):
        rule = "closed not_planned" if issue.state_reason == "not_planned" else "wontfix label"
        if theme is RejectionTheme.STALE_OR_NO_RESPONSE:
            # Closed for silence after a maintainer asked something: the decision
            # in flight was CLARIFY, and the request never answered it.
            return build(
                DecisionLabel.CLARIFY,
                rule + " after unanswered question",
                theme=theme,
                evidence=evidence,
                relevant=False,
                needs_audit=True,
            )
        if theme is RejectionTheme.OUT_OF_SCOPE:
            return build(DecisionLabel.OUT_OF_SCOPE, rule, theme=theme, evidence=evidence)
        if theme in {RejectionTheme.UNNECESSARY, RejectionTheme.WORKS_AS_INTENDED}:
            return build(DecisionLabel.UNJUSTIFIED, rule, theme=theme, evidence=evidence)
        if theme is RejectionTheme.ALREADY_IMPLEMENTED:
            return build(DecisionLabel.DUPLICATE, rule, theme=theme, evidence=evidence)
        if theme is RejectionTheme.INFEASIBLE:
            return build(DecisionLabel.REJECT, rule, theme=theme, evidence=evidence)
        # No readable rationale, or a capacity/environment reason. The outcome is
        # real but it does not tell us the request was wrong.
        return build(
            DecisionLabel.REJECT,
            rule,
            theme=theme,
            evidence=evidence,
            relevant=theme in DECISION_RELEVANT_THEMES,
            needs_audit=True,
        )

    return None


def build_corpus(
    issues: Iterable[IssueRecord],
    feature_requests_only: bool = True,
    decision_relevant_only: bool = True,
) -> list[NaturalDecision]:
    """Apply the filter chain that the paper must describe in one paragraph."""
    out: list[NaturalDecision] = []
    for issue in issues:
        if issue.is_pull_request:
            continue
        if feature_requests_only and not looks_like_feature_request(issue):
            continue
        decision = map_issue(issue)
        if decision is None:
            continue
        if decision_relevant_only and not decision.decision_relevant:
            continue
        out.append(decision)
    return out


def corpus_stats(decisions: Sequence[NaturalDecision]) -> dict[str, Any]:
    by_label: dict[str, int] = {}
    by_super: dict[str, int] = {}
    by_theme: dict[str, int] = {}
    for d in decisions:
        by_label[d.label.value] = by_label.get(d.label.value, 0) + 1
        by_super[d.super_class.value] = by_super.get(d.super_class.value, 0) + 1
        by_theme[d.theme.value] = by_theme.get(d.theme.value, 0) + 1
    return {
        "total": len(decisions),
        "repos": len({d.repo for d in decisions}),
        "by_label": dict(sorted(by_label.items())),
        "by_super_class": dict(sorted(by_super.items())),
        "by_theme": dict(sorted(by_theme.items())),
        "needs_audit": sum(1 for d in decisions if d.needs_audit),
    }


# --------------------------------------------------------------------------
# Audit sampling
# --------------------------------------------------------------------------


def stratified_audit_sample(
    decisions: Sequence[NaturalDecision],
    n: int = 200,
    seed: int = 20260916,
) -> list[NaturalDecision]:
    """Draw a label-stratified sample for two annotators.

    They read the request and the maintainer thread and record the decision they
    would have made. Cohen's kappa between that reading and the natural label is
    what licenses the rest of this tier.
    """
    if n <= 0 or not decisions:
        return []

    rng = random.Random(seed)
    strata: dict[str, list[NaturalDecision]] = {}
    for d in decisions:
        strata.setdefault(d.label.value, []).append(d)

    total = len(decisions)
    sample: list[NaturalDecision] = []
    for label, items in sorted(strata.items()):
        share = max(1, round(n * len(items) / total))
        sample.extend(rng.sample(items, min(share, len(items))))

    rng.shuffle(sample)
    return sample[:n]


AUDIT_COLUMNS = [
    "repo",
    "number",
    "html_url",
    "title",
    "natural_label",
    "theme",
    "mapping_rule",
    "mapping_evidence",
    "annotator_label",
    "annotator_confident",
    "annotator_note",
]


def write_audit_csv(sample: Sequence[NaturalDecision], path: Path) -> None:
    """Annotator columns are written empty on purpose; two people fill them in."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_COLUMNS)
        writer.writeheader()
        for d in sample:
            writer.writerow(
                {
                    "repo": d.repo,
                    "number": d.number,
                    "html_url": d.html_url or "",
                    "title": d.title,
                    "natural_label": d.label.value,
                    "theme": d.theme.value,
                    "mapping_rule": d.mapping_rule,
                    "mapping_evidence": d.mapping_evidence or "",
                    "annotator_label": "",
                    "annotator_confident": "",
                    "annotator_note": "",
                }
            )


# --------------------------------------------------------------------------
# IO
# --------------------------------------------------------------------------


def write_jsonl(items: Iterable[BaseModel], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(item.model_dump_json() + "\n")
            count += 1
    return count


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Accept both the REST shape and the flattened dataset shape."""
    data = dict(payload)

    labels = data.get("labels")
    if isinstance(labels, str):
        try:
            labels = json.loads(labels)
        except json.JSONDecodeError:
            labels = [labels]
    if isinstance(labels, list):
        data["labels"] = [lab["name"] if isinstance(lab, dict) else str(lab) for lab in labels]

    if "repo" not in data:
        url = data.get("repository_url") or data.get("html_url") or ""
        match = re.search(r"repos/([^/]+/[^/]+)", url) or re.search(r"github\.com/([^/]+/[^/]+)/", url)
        data["repo"] = match.group(1) if match else "unknown/unknown"

    if "is_pull_request" not in data:
        data["is_pull_request"] = "pull_request" in payload

    comments = data.get("comments")
    if isinstance(comments, int):
        data["comments"] = []
    elif isinstance(comments, list):
        data["comments"] = [
            {
                "author": (c.get("user") or {}).get("login") if isinstance(c.get("user"), dict) else c.get("author"),
                "body": c.get("body") or "",
                "author_association": c.get("author_association"),
                "created_at": c.get("created_at"),
            }
            if isinstance(c, dict)
            else {"body": str(c)}
            for c in comments
        ]

    return data


def read_issue_jsonl(paths: Sequence[Path]) -> Iterator[IssueRecord]:
    """Read our own dumps, or a Hugging Face export with the same column names."""
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                yield IssueRecord.model_validate(normalize_payload(json.loads(line)))


# --------------------------------------------------------------------------
# GitHub REST fetch
# --------------------------------------------------------------------------


def _request(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code in (403, 429):
            reset = error.headers.get("X-RateLimit-Reset")
            wait = max(0, int(reset) - int(time.time())) if reset else 60
            raise RuntimeError(
                f"GitHub rate limit hit; resets in {wait}s. Set GITHUB_TOKEN for a higher quota."
            ) from error
        raise


def fetch_issue_comments(repo: str, number: int, token: str | None = None) -> list[IssueComment]:
    payload = _request(f"{GITHUB_API}/repos/{repo}/issues/{number}/comments?per_page=100", token)
    return [
        IssueComment.model_validate(
            {
                "author": (c.get("user") or {}).get("login"),
                "body": c.get("body") or "",
                "author_association": c.get("author_association"),
                "created_at": c.get("created_at"),
            }
        )
        for c in payload
    ]


def fetch_repo_issues(
    repo: str,
    token: str | None = None,
    state: str = "all",
    max_items: int = 500,
    with_comments: bool = True,
    per_page: int = 100,
    pause: float = 0.2,
) -> list[IssueRecord]:
    """Pull issues for one repository. Comments cost one request each, so they
    are fetched only for closed issues, where the rationale lives."""
    issues: list[IssueRecord] = []
    page = 1

    while len(issues) < max_items:
        query = urllib.parse.urlencode(
            {"state": state, "per_page": min(per_page, max_items - len(issues)), "page": page}
        )
        payload = _request(f"{GITHUB_API}/repos/{repo}/issues?{query}", token)
        if not payload:
            break

        for raw in payload:
            if "pull_request" in raw:
                continue
            record = IssueRecord.model_validate(normalize_payload({**raw, "repo": repo}))
            if with_comments and record.state == "closed" and raw.get("comments"):
                record.comments = fetch_issue_comments(repo, record.number, token)
                time.sleep(pause)
            issues.append(record)

        page += 1
        time.sleep(pause)

    return issues[:max_items]


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _cmd_fetch(args: argparse.Namespace) -> int:
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("warning: no GITHUB_TOKEN, unauthenticated quota is 60 requests/hour", file=sys.stderr)

    all_issues: list[IssueRecord] = []
    for repo in args.repo:
        print(f"fetching {repo} ...", file=sys.stderr)
        issues = fetch_repo_issues(
            repo, token=token, max_items=args.max_items, with_comments=not args.no_comments
        )
        print(f"  {len(issues)} issues", file=sys.stderr)
        all_issues.extend(issues)

    written = write_jsonl(all_issues, Path(args.out))
    print(f"wrote {written} issues to {args.out}", file=sys.stderr)
    return 0


def _cmd_build(args: argparse.Namespace) -> int:
    paths = [Path(p) for pattern in args.raw for p in glob.glob(pattern)]
    if not paths:
        print("no input files matched", file=sys.stderr)
        return 1

    issues = list(read_issue_jsonl(paths))
    decisions = build_corpus(
        issues,
        feature_requests_only=not args.include_bugs,
        decision_relevant_only=not args.keep_irrelevant,
    )

    written = write_jsonl(decisions, Path(args.out))
    print(json.dumps(corpus_stats(decisions), indent=2))
    print(f"wrote {written} decisions to {args.out}", file=sys.stderr)

    if args.audit:
        sample = stratified_audit_sample(decisions, n=args.audit_size, seed=args.seed)
        write_audit_csv(sample, Path(args.audit))
        print(f"wrote {len(sample)}-item audit sample to {args.audit}", file=sys.stderr)

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the V3 natural-decision corpus from GitHub issues.")
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="download issues for one or more repositories")
    fetch.add_argument("--repo", nargs="+", required=True, help="owner/name")
    fetch.add_argument("--out", required=True)
    fetch.add_argument("--max-items", type=int, default=500)
    fetch.add_argument("--token", default=None)
    fetch.add_argument("--no-comments", action="store_true")
    fetch.set_defaults(func=_cmd_fetch)

    build = sub.add_parser("build", help="map raw issues to gold decisions")
    build.add_argument("--raw", nargs="+", required=True, help="jsonl paths or globs")
    build.add_argument("--out", required=True)
    build.add_argument("--audit", default=None, help="write the stratified audit CSV here")
    build.add_argument("--audit-size", type=int, default=200)
    build.add_argument("--seed", type=int, default=20260916)
    build.add_argument("--include-bugs", action="store_true")
    build.add_argument(
        "--keep-irrelevant",
        action="store_true",
        help="keep capacity/staleness closures (reported separately, never as gold)",
    )
    build.set_defaults(func=_cmd_build)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
