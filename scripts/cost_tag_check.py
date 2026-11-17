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


def check_plan(plan_path: str) -> int:
    """
    Returns an exit code: 0 if every resource being created or updated has
    `landlord_account_id`, non-zero otherwise.
    """
    with open(plan_path) as f:
        plan = json.load(f)

    # Keyed by address (unique per plan) and sorted, so output is stable across runs.
    missing = set()
    for rc in plan.get("resource_changes") or []:
        change = rc.get("change") or {}
        # "replace" is ["delete","create"], so test membership, not equality.
        if not {"create", "update"} & set(change.get("actions") or []):
            continue
        # `tags`, not `tags_all`: provider default tags would mask a missing tag.
        tags = (change.get("after") or {}).get("tags") or {}
        value = tags.get("landlord_account_id")
        if not isinstance(value, str) or not value.strip():
            missing.add(rc["address"])

    for address in sorted(missing):
        print(f"missing landlord_account_id: {address}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
