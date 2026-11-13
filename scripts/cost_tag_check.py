"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list with planned `change.after` values. Check taggable resources generically through their
`tags` or `tags_all` attributes, rather than relying on resource types.

Implement check_plan() so it:
  - Looks at every resource being created or updated (skip changes without a "create" or
    "update" action, such as a "no-op"/"read" or a "delete" with no `after` block).
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
    try:
        with open(plan_path, encoding="utf-8") as plan_file:
            plan = json.load(plan_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to read Terraform plan '{plan_path}': {error}", file=sys.stderr)
        return 1

    if not isinstance(plan, dict) or not isinstance(plan.get("resource_changes"), list):
        print(
            "Invalid Terraform plan: expected a resource_changes list.",
            file=sys.stderr,
        )
        return 1

    missing_tags: set[str] = set()
    for resource_change in plan["resource_changes"]:
        if not isinstance(resource_change, dict):
            print(
                "Invalid Terraform plan: each resource change must be an object.",
                file=sys.stderr,
            )
            return 1

        change = resource_change.get("change")
        if not isinstance(change, dict) or not isinstance(change.get("actions"), list):
            print(
                "Invalid Terraform plan: each resource change must have an actions list.",
                file=sys.stderr,
            )
            return 1

        actions = change["actions"]
        if not any(action in ("create", "update") for action in actions):
            continue

        after = change.get("after")
        if not isinstance(after, dict):
            print(
                "Invalid Terraform plan: created or updated resources must have an after object.",
                file=sys.stderr,
            )
            return 1

        if "tags" not in after and "tags_all" not in after:
            continue

        tags = after.get("tags")
        tags_all = after.get("tags_all")
        has_landlord_account_tag = (
            isinstance(tags, dict) and "landlord_account_id" in tags
        ) or (
            isinstance(tags_all, dict) and "landlord_account_id" in tags_all
        )
        if not has_landlord_account_tag:
            address = resource_change.get("address")
            if not isinstance(address, str) or not address:
                print(
                    "Invalid Terraform plan: taggable resource is missing its address.",
                    file=sys.stderr,
                )
                return 1
            missing_tags.add(address)

    for address in sorted(missing_tags):
        print(f"Missing landlord_account_id tag: {address}")

    return 1 if missing_tags else 0


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
