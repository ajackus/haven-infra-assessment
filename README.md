# Haven — Platform Infrastructure Assessment

Haven is a multi-tenant real estate platform.

## Domain model

```
LandlordAccount  (the billing unit)
  └── Property
        └── Tenant
              └── ScreeningReport  (SSN, credit score)

PropertyManager  (scoped to exactly one LandlordAccount)
```

A `LandlordAccount` is the billing unit — every property, every tenant, every report underneath
it rolls up to exactly one. A `PropertyManager` is scoped to exactly one `LandlordAccount` and
everything under it.

This codebase currently tags and checks access using whatever ID happened to be on hand when
each piece was written — that reflects how it was built, not a spec to replicate.

## What not to modify

`app/seed_data.py`, `app/models.py`, `fixtures/plan.json`, `terraform/terraform.tfstate` — the
assignment's checks assume this data is unchanged.

`terraform/terraform.tfstate` is checked in deliberately, not an accident — it's a seeded state
representing 4 already-provisioned landlord media buckets, standing in for a real AWS account so
B0 can be reproduced with `terraform plan` instead of just reasoned about. See `terraform/main.tf`
for how to use it.

## Where things are

| Path | Task |
|---|---|
| `terraform/main.tf` | B0 |
| `terraform/lifecycle.tf` | B1 |
| `app/access_control.py`, `scripts/cost_tag_check.py` | B2 — stubs to implement |

## Submission

| Task | Answer | Status |
|---|---|---|
| B0 | `B0.md`: removing `la-002` plans 2 replaces + 1 destroy under `count`; fix is `for_each` keyed by account id. Plan output verified against the seeded state. | Written. `main.tf` not changed. |
| B1 | `B1.md`: Glacier 90-day minimum makes a day-40 deletion cost the remaining ~80 days; redesign gates the transition on an application-set eligibility tag. | Written. `lifecycle.tf` not changed, no dollar figure calculated. |
| B2.1 | `app/access_control.py`, `tests/test_access_control.py`: access is granted only when the actor's `landlord_account_id` matches the report's property's. | Implemented, 9 tests pass. |
| B2.2 | `scripts/cost_tag_check.py`, `tests/test_cost_tag_check.py`: fails create/update resources lacking a non-empty `landlord_account_id`. | Implemented, 7 tests pass. |
| Design notes | `DESIGN_NOTES.md`: idempotency key (resource address) and other decisions. | Written. |
| AI record | `.ai-conversations/b2-claude-session.txt`: export of the Claude Code session used for B2. | Included. |

Run the tests with `python -m pytest`. Check the real plan with
`python scripts/cost_tag_check.py fixtures/plan.json` (exits 1, flags `listing_media` and
`mls_feed_sync`).
