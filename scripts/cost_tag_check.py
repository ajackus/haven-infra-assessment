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


def collect_resources(module):
    resources = module.get("resources", [])

    for resource in resources:
        yield resource

    for child in module.get("child_modules", []):
        yield from collect_resources(child)


def validate_tags(plan):
    root = plan.get("planned_values", {}).get(
        "root_module", {}
    )

    resources = sorted(
        collect_resources(root),
        key=lambda r: r.get("address", "")
    )

    failures = []

    for resource in resources:
        address = resource.get("address", "")
        values = resource.get("values") or {}
        tags = values.get("tags") or {}

        tag_value = tags.get(REQUIRED_TAG)

        if not isinstance(tag_value, str) or not tag_value.strip():
            failures.append(address)

    return failures


def main():
    with open("tfplan.json", encoding="utf-8") as file:
        plan = json.load(file)

    failures = validate_tags(plan)

    print("Landlord Account Tag Validation")

    if failures:
        print("FAILED: Missing required tag")

        for address in failures:
            print(f"- {address}")

        sys.exit(1)

    print("PASSED: All planned resources have the required tag")


if __name__ == "__main__":
    main()




