"""
Validate that every Terraform resource being created or updated carries the
real cost-allocation tag: landlord_account_id.
"""
import json
import sys
from pathlib import Path

REQUIRED_TAG = "landlord_account_id"
RELEVANT_ACTIONS = {"create", "update"}


def check_plan(plan_path: str) -> int:
    """
    Return 0 when all created/updated resources have a non-empty
    landlord_account_id tag; otherwise print missing resource addresses and
    return 1. Output is sorted and deduplicated for deterministic reruns.
    """
    try:
        with Path(plan_path).open(encoding="utf-8") as plan_file:
            plan = json.load(plan_file)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read Terraform plan '{plan_path}': {exc}", file=sys.stderr)
        return 2

    resource_changes = plan.get("resource_changes", [])
    if not isinstance(resource_changes, list):
        print("Invalid Terraform plan: resource_changes must be a list.", file=sys.stderr)
        return 2

    missing_addresses = set()

    for resource in resource_changes:
        if not isinstance(resource, dict):
            continue

        change = resource.get("change")
        if not isinstance(change, dict):
            continue

        actions = change.get("actions", [])
        if not isinstance(actions, list) or not RELEVANT_ACTIONS.intersection(actions):
            continue

        after = change.get("after")
        tags = after.get("tags") if isinstance(after, dict) else None
        tag_value = tags.get(REQUIRED_TAG) if isinstance(tags, dict) else None

        if not isinstance(tag_value, str) or not tag_value.strip():
            address = resource.get("address") or "<unknown-resource-address>"
            missing_addresses.add(address)

    if missing_addresses:
        for address in sorted(missing_addresses):
            print(f"Missing required tag '{REQUIRED_TAG}': {address}")
        return 1

    print(f"All created/updated resources have the required '{REQUIRED_TAG}' tag.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(sys.argv[0]).as_posix()} <terraform-plan.json>", file=sys.stderr)
        sys.exit(2)
    sys.exit(check_plan(sys.argv[1]))
