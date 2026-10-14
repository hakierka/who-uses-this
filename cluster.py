#!/usr/bin/env python3
"""16 segments. named after the email i would send, not a clustering paper.

i tried k-means on a previous dump. the clusters were 'uses it' and 'does not'
with extra decimals. rules were ruder and more useful.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
USERS = json.loads((ROOT / "data" / "users.json").read_text())
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

# order = who i would bother first this quarter
SEGMENT_ORDER = [
    "weekly-wrong-data",
    "weekly-happy-champions",
    "weekly-happy-not-champion",
    "monthly-wrong-data",
    "monthly-dont-trust",
    "monthly-ok",
    "once-dont-trust",
    "once-wrong-data",
    "once-dont-know-how",
    "never-dont-know-how",
    "never-doesnt-exist",
    "never-no-time",
    "legal-trust",
    "investment-light",
    "office-ignore",
    "other",
]


def segment(p: dict) -> str:
    if p["org"] == "office":
        return "office-ignore"
    if p["org"] == "legal" and p["blocker"] == "dont_trust_answers":
        return "legal-trust"
    if p["org"] == "investment" and p["usage"] in {"never", "once"}:
        return "investment-light"
    if p["usage"] == "weekly" and p["blocker"] == "wrong_data":
        return "weekly-wrong-data"
    if p["usage"] == "weekly" and p["champion"]:
        return "weekly-happy-champions"
    if p["usage"] == "weekly":
        return "weekly-happy-not-champion"
    if p["usage"] == "monthly" and p["blocker"] == "wrong_data":
        return "monthly-wrong-data"
    if p["usage"] == "monthly" and p["blocker"] == "dont_trust_answers":
        return "monthly-dont-trust"
    if p["usage"] == "monthly":
        return "monthly-ok"
    if p["usage"] == "once" and p["blocker"] == "dont_trust_answers":
        return "once-dont-trust"
    if p["usage"] == "once" and p["blocker"] == "wrong_data":
        return "once-wrong-data"
    if p["usage"] == "once":
        return "once-dont-know-how"
    if p["usage"] == "never" and p["blocker"] == "dont_know_how":
        return "never-dont-know-how"
    if p["usage"] == "never" and p["blocker"] == "dont_know_it_exists":
        return "never-doesnt-exist"
    if p["usage"] == "never":
        return "never-no-time"
    return "other"


MOVE = {
    "weekly-wrong-data": "fix the data product, then tell them. do not workshop this.",
    "weekly-happy-champions": "give them a one-pager and a named slack. they already do the job.",
    "weekly-happy-not-champion": "ask if they want the badge. some will say no. fine.",
    "monthly-wrong-data": "same as weekly-wrong-data, smaller fire.",
    "monthly-dont-trust": "show traces + a human review path. not a feature tour.",
    "monthly-ok": "leave them. invite to office hours.",
    "once-dont-trust": "pair with legal-trust materials. do not send '10 prompt tips'.",
    "once-wrong-data": "wait until weekly-wrong-data is less embarrassing.",
    "once-dont-know-how": "45 min workshop, their own files, not a toy dataset.",
    "never-dont-know-how": "same workshop, different calendar invite subject.",
    "never-doesnt-exist": "manager-forwarded mail, 4 sentences, one gif max.",
    "never-no-time": "do not hunt them. they will come when finance asks.",
    "legal-trust": "separate session with counsel. no sales tone.",
    "investment-light": "partner with a champion who already sits in their meeting.",
    "office-ignore": "out of scope unless they ask.",
    "other": "look at the rows, do not present this bucket.",
}


def main() -> None:
    buckets = defaultdict(list)
    for p in USERS:
        buckets[segment(p)].append(p)

    lines = ["# segments", ""]
    lines.append("generated from data/users.json. do not cite this as a real company.")
    lines.append("")
    total = len(USERS)
    champs = sum(1 for p in USERS if p["champion"])
    weekly = sum(1 for p in USERS if p["usage"] == "weekly")
    never = sum(1 for p in USERS if p["usage"] == "never")
    lines.append(f"{total} people, {weekly} weekly, {never} never, {champs} flagged as champions.")
    lines.append("")

    for name in SEGMENT_ORDER:
        rows = buckets.get(name, [])
        orgs = defaultdict(int)
        for p in rows:
            orgs[p["org"]] += 1
        org_s = ", ".join(f"{k} {v}" for k, v in sorted(orgs.items(), key=lambda x: -x[1])[:5])
        lines.append(f"## {name} ({len(rows)})")
        lines.append("")
        lines.append(MOVE[name])
        if org_s:
            lines.append(f"mostly: {org_s}")
        lines.append("")

    missing = set(buckets) - set(SEGMENT_ORDER)
    if missing:
        lines.append("also, i forgot: " + ", ".join(sorted(missing)))

    (OUT / "segments.md").write_text("\n".join(lines) + "\n")
    slim = {k: [p["id"] for p in v] for k, v in buckets.items()}
    (OUT / "segments.json").write_text(json.dumps(slim, indent=2))
    print(f"wrote out/segments.md ({sum(len(v) for v in buckets.values())} people)")


if __name__ == "__main__":
    main()
