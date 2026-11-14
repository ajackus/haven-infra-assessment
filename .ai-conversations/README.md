# AI conversation records

If you used an AI assistant for B2, put the record of that here before submitting (export,
screenshot-transcribed text, or your own written summary of the exchange) — see B2's section
in DESIGN_NOTES.md for what to cover. Leave this folder empty if you didn't use one.


## Cost-tag implementation and correction

**Assistant’s first action filter:**

```python
if change.get("actions") not in (["create"], ["update"]):
    continue
```

**Assistant later identified a flaw in that suggestion:** Terraform represents replacements with combined action lists such as `["delete", "create"]` or `["create", "delete"]`. Exact-list comparison would skip those resources, even though the plan creates a replacement. See [Terraform’s JSON plan format](https://developer.hashicorp.com/terraform/internals/json-format).

**Corrected filter:**

```python
actions = change.get("actions") or []
if not any(action in ("create", "update") for action in actions):
    continue
```

A replacement test was added to ensure a resource with `["delete", "create"]` is checked for the billing tag.