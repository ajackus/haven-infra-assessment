# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide whether two resources in the
same run are "the same" for dedup purposes, and why running it twice against an unchanged
plan file produces identical output and exit code without the script keeping any record
between runs. Use the word "idempotency" in your explanation.

<!-- Your answer here -->

## Any other decision with a non-obvious alternative


# Design Notes

## 1. Access Control

Property Manager access is restricted by comparing the landlord account ID from trusted manager identity context with the landlord account ID associated with the requested screening report.

Access is allowed only when both IDs match. Missing account IDs and cross-account requests are denied.

## 2. Cost Tagging

The validation checks Terraform planned resources generically and verifies that each applicable resource has a non-empty `landlord_account_id` tag.

The existing `tenant_id` tag is not considered a substitute because landlord_account_id is the actual billing unit.

## 3. Idempotency

The exact idempotency key used is the Terraform resource address (`address`) from the Terraform plan JSON.

Each resource is identified by its unique Terraform address. Validation results are sorted by this address to ensure deterministic output.

The validator does not modify the Terraform plan or infrastructure. Therefore, running it repeatedly against an unchanged plan produces the same result.

## 4. Design Decisions and Alternatives

- Used `for_each` instead of `count` for stable resource identity.
- Used Python for reusable validation and automated testing.
- Used Terraform plan JSON instead of hardcoding individual AWS resource types.
- Used pytest for authorization and cost-tagging tests.
- Used landlord_account_id instead of tenant_id for billing attribution.



