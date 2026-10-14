#!/usr/bin/env python3
"""480 people, not a user research thesis.

Seeded. If the numbers move, i broke the seed, not the market.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

ORGS = [
    ("legal", 28),
    ("finance", 52),
    ("hr", 34),
    ("investment", 70),
    ("ops", 48),
    ("engineering", 90),
    ("data", 40),
    ("comms", 22),
    ("ir", 16),
    ("office", 30),
    ("other", 50),
]

# roughly 480
assert sum(n for _, n in ORGS) == 480

ROLES = {
    "legal": ["counsel", "paralegal", "ops"],
    "finance": ["controller", "fp&a", "analyst"],
    "hr": ["bp", "recruiting", "ops"],
    "investment": ["associate", "vp", "partner"],
    "ops": ["coordinator", "manager"],
    "engineering": ["engineer", "manager", "qa"],
    "data": ["analyst", "engineer"],
    "comms": ["editor", "lead"],
    "ir": ["associate", "lead"],
    "office": ["ea", "office"],
    "other": ["specialist", "manager"],
}

BLOCKERS = [
    "dont_know_it_exists",
    "dont_know_how",
    "dont_trust_answers",
    "wrong_data",
    "no_time",
    "works_fine",  # not a blocker, i still encode it here because i am lazy
]


def usage_bucket(rng: random.Random, org: str) -> str:
    # engineering and data skew heavy. legal and ir skew light.
    heavy = {"engineering", "data"}
    light = {"legal", "ir", "office", "other"}
    roll = rng.random()
    if org in heavy:
        if roll < 0.22:
            return "never"
        if roll < 0.40:
            return "once"
        if roll < 0.72:
            return "monthly"
        return "weekly"
    if org in light:
        if roll < 0.48:
            return "never"
        if roll < 0.72:
            return "once"
        if roll < 0.90:
            return "monthly"
        return "weekly"
    if roll < 0.32:
        return "never"
    if roll < 0.55:
        return "once"
    if roll < 0.82:
        return "monthly"
    return "weekly"


def blocker_for(rng: random.Random, usage: str, org: str) -> str:
    if usage == "weekly":
        return "works_fine" if rng.random() < 0.7 else "wrong_data"
    if usage == "never":
        return rng.choice(["dont_know_it_exists", "dont_know_how", "no_time"])
    if org == "legal" and rng.random() < 0.55:
        return "dont_trust_answers"
    if org in {"finance", "investment"} and rng.random() < 0.4:
        return "wrong_data"
    return rng.choice(BLOCKERS)


def queries(rng: random.Random, usage: str) -> int:
    if usage == "never":
        return 0
    if usage == "once":
        return rng.choice([1, 1, 2])
    if usage == "monthly":
        return rng.randint(3, 12)
    return rng.randint(15, 80)


def main() -> None:
    rng = random.Random(7)
    people = []
    i = 1
    for org, n in ORGS:
        for _ in range(n):
            usage = usage_bucket(rng, org)
            people.append(
                {
                    "id": f"p{i:03d}",
                    "org": org,
                    "role": rng.choice(ROLES[org]),
                    "usage": usage,
                    "queries_90d": queries(rng, usage),
                    "blocker": blocker_for(rng, usage, org),
                    "champion": False,
                }
            )
            i += 1

    # sprinkle champions: weekly users who are not office
    weekly = [p for p in people if p["usage"] == "weekly" and p["org"] != "office"]
    rng.shuffle(weekly)
    for p in weekly[:38]:
        p["champion"] = True

    (DATA / "users.json").write_text(json.dumps(people, indent=2))
    print(f"wrote {len(people)} people")


if __name__ == "__main__":
    main()
