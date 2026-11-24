# Design Notes

## B2 — idempotency key

The cost-tag check uses the Terraform resource **`address`**
(`resource_changes[].address`) as its idempotency/deduplication key within a
plan. Missing addresses are stored in a set and printed in sorted order.
Duplicate entries for the same Terraform address are reported once, and
rerunning the check against an unchanged plan produces the same output and
exit code. This idempotency is stateless: no run history or external database
is involved.

The validator checks each resource change whose action list contains `create`
or `update`, including replacements that include a create action. It skips
read/no-op and delete-only changes. It requires a non-empty
`landlord_account_id` tag; `tenant_id` does not identify the billing unit.

## Other decisions and alternatives

- **Authorization follows the ownership graph.** Resolve report -> tenant ->
  property -> landlord account, then compare with the authenticated
  PropertyManager's scope. Missing or ambiguous relationships fail closed.
- **Deterministic output.** A set deduplicates resource addresses and sorting
  makes output stable independent of plan ordering.
- **Non-empty values.** Empty or whitespace-only tag values are treated as
  missing.
- **No delayed deletion to avoid Glacier charges.** The deletion SLA is 30 days;
  retaining an object for the remaining Glacier minimum would violate it.
  Keep deletion-eligible objects out of minimum-duration archive tiers.
