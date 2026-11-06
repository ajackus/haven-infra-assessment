
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
