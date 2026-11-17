# Design Notes

## B2 — idempotency key

`cost_tag_check.py` treats two resources in the same run as "the same" when they share the
same resource `address` (e.g. `aws_s3_bucket.landlord_media[0]`). Terraform guarantees an
address is unique within a plan, including indexed and module-nested resources, so it is the
natural key. Failing addresses are collected in a set keyed on it, so a repeated entry is
reported once.

The script's idempotency comes from being a pure function of the plan file: it reads the
file, writes nothing, and keeps no cache, lock or log between runs. The same plan therefore
always gives the same exit code. Output order is stable because failing addresses are
printed with `sorted()`; set iteration order can differ between Python processes (hash
seeding), which would otherwise make the output non-repeatable.

## Any other decision with a non-obvious alternative

- **Tag is `landlord_account_id`, not `tenant_id`.** `LandlordAccount` is the billing unit
  (README), so cost allocation must roll up to it. A resource tagged only with `tenant_id`
  (`listing_media`) fails.
- **Access boundary is the landlord account.** A PropertyManager may see every report under
  their own account, not just one property's. Tenant and Property carry no landlord ID of
  their own except Property, so access resolves report -> tenant -> property -> account.
- **Fail closed beyond the spec.** Duplicate tenant or property IDs and blank account IDs
  deny access: a duplicate is ambiguous, and `"" == ""` must never grant access. The spec
  only required denial for missing records.
- **Replace actions are checked.** A replace is `["delete","create"]`, so the check tests
  that `create` or `update` is in `actions` rather than comparing equality; otherwise a
  recreated untagged resource would slip through.
- **Reads `tags`, not `tags_all`.** `tags_all` includes provider default tags, which would
  mask a resource that doesn't carry the tag itself.
- **Empty or whitespace tag values count as missing.** An empty tag satisfies a key-presence
  check but allocates cost to nobody.
