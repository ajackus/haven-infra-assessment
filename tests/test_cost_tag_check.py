"""
Write tests here proving:
  1. Happy path: running the check against fixtures/plan.json correctly flags the resources
     missing `landlord_account_id` (listing_media, mls_feed_sync) and passes the ones that
     have it (landlord_media[0], screening_report_export). The fixture also has a "no-op"
     entry and a "delete" entry with no `after` block at all — neither should appear in the
     output or crash the check.
  2. Idempotency: running the check twice against the same plan file produces the same
     result both times, with no duplicated output.

check_plan() takes a file path, not a dict — for a case that needs its own plan contents
instead of the shared fixture, write one with pytest's `tmp_path` rather than editing
fixtures/plan.json. You don't need to shell out to the real script for every case.
"""
from scripts.cost_tag_check import check_plan


def test_reports_resources_missing_landlord_account_tag(capsys):
    result = check_plan("fixtures/plan.json")

    assert result == 1
    assert capsys.readouterr().out.splitlines() == [
        "Missing landlord_account_id tag: aws_lambda_function.mls_feed_sync",
        "Missing landlord_account_id tag: aws_s3_bucket.listing_media",
    ]


def test_is_idempotent(capsys):
    first_result = check_plan("fixtures/plan.json")
    first_output = capsys.readouterr().out
    second_result = check_plan("fixtures/plan.json")
    second_output = capsys.readouterr().out

    assert first_result == second_result == 1
    assert first_output == second_output


def test_checks_tags_all_without_resource_type_specific_logic(tmp_path, capsys):
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(
        """{
            "resource_changes": [
                {
                    "address": "provider_custom_resource.example",
                    "type": "provider_custom_resource",
                    "change": {
                        "actions": ["create"],
                        "after": {"tags_all": {"landlord_account_id": "la-001"}}
                    }
                },
                {
                    "address": "provider_custom_resource.missing",
                    "type": "provider_custom_resource",
                    "change": {
                        "actions": ["update"],
                        "after": {"tags_all": {"tenant_id": "ten-001"}}
                    }
                },
                {
                    "address": "provider_custom_resource.untaggable",
                    "type": "provider_custom_resource",
                    "change": {
                        "actions": ["create"],
                        "after": {"name": "untaggable"}
                    }
                }
            ]
        }""",
        encoding="utf-8",
    )

    assert check_plan(str(plan_path)) == 1
    assert capsys.readouterr().out.splitlines() == [
        "Missing landlord_account_id tag: provider_custom_resource.missing"
    ]
