"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list, where each entry has a `type`, an `address`, and `change.after.tags`.

Implement check_plan() so it:
  - Looks at every resource being created or updated (skip anything whose change.actions
    isn't "create" or "update" — a "no-op"/"read" change, or a "delete" with no `after`
    block at all).
  - Fails (returns a non-zero exit code) if the resource is missing the tag that identifies
    the real billing unit, per README.md's domain model — not whatever tag the resource
    happens to already carry.
  - Is idempotent: running this twice against the same plan file produces the same result,
    with no duplicate output and no flipped pass/fail. This is about a single run being
    stable and repeatable — it does not require remembering anything between runs.
  - Prints which specific resource address(es) are missing the tag.

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""

import json
import sys


REQUIRED_TAG = "landlord_account_id"


def check_plan(plan_path: str) -> int:
    """Return 0 if all created/updated resources have the required billing tag."""
    with open(plan_path, "r", encoding="utf-8") as file:
        plan = json.load(file)

    resource_changes = plan.get("resource_changes", [])
    failures = set()

    for resource in resource_changes:
        change = resource.get("change") or {}
        actions = change.get("actions", [])

        # Only validate resources being created or updated.
        if not any(action in ("create", "update") for action in actions):
            continue

        address = resource.get("address", "<unknown resource>")
        after = change.get("after")

        tags = after.get("tags") if isinstance(after, dict) else None
        tag_value = tags.get(REQUIRED_TAG) if isinstance(tags, dict) else None

        if not isinstance(tag_value, str) or not tag_value.strip():
            failures.add(address)

    if failures:
        print("FAILED: Missing required landlord_account_id tag:")
        for address in sorted(failures):
            print(f"- {address}")
        return 1

    print("PASSED: All created/updated resources have landlord_account_id.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/cost_tag_check.py <plan.json>")
        sys.exit(2)

    sys.exit(check_plan(sys.argv[1]))

