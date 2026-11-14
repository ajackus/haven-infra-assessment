# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide whether two resources in the
same run are "the same" for dedup purposes, and why running it twice against an unchanged
plan file produces identical output and exit code without the script keeping any record
between runs. Use the word "idempotency" in your explanation.

<!-- Your answer here -->
The exact idempotent key is "resource_changes[].address"
The check collects missing-tag addresses in a set and prints them in sorted order. Running it again against the same plan therefore produces the same findings and output without duplicate addresses or stored state.

I chose to treat an empty "landlord_account_id" value as missing. Checking only whether the key exists could let an empty value pass.

## Any other decision with a non-obvious alternative

<!-- Your answer here -->
