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

def test_plan_flags_missing_tags_and_skips_noop_and_delete(capsys):
    result = check_plan("fixtures/plan.json")
    output = capsys.readouterr().out

    assert result == 1
    assert "aws_s3_bucket.listing_media" in output
    assert "aws_lambda_function.mls_feed_sync" in output

    assert "landlord_media[0]" not in output
    assert "screening_report_export" not in output
    assert "archive_media" not in output
    assert "decommissioned_media" not in output

def test_plan_output_is_idempotent(capsys):
    first_result = check_plan("fixtures/plan.json")
    first_output = capsys.readouterr().out

    second_result = check_plan("fixtures/plan.json")
    second_output = capsys.readouterr().out

    assert first_result == second_result == 1
    assert first_output == second_output
    assert first_output.count("aws_s3_bucket.listing_media") == 1
    assert first_output.count("aws_lambda_function.mls_feed_sync") == 1


def test_check_is_generic_for_other_resource_types(tmp_path, capsys):
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(
    """
    {
    "resource_changes": [
        {
          "address": "custom_provider_resource.example",
          "type": "custom_provider_resource",
          "change": {
            "actions": ["create"],
            "after": {
              "tags": { "tenant_id": "ten-001" }}
          }
          }
          ]
        }
    """,
    encoding="utf-8",
    )

    result = check_plan(str(plan_path))
    output = capsys.readouterr().out

    assert result == 1
    assert "custom_provider_resource.example" in output

def test_replacement_with_create_action_is_checked(tmp_path, capsys):
    plan_path = tmp_path / "replacement-plan.json"
    plan_path.write_text(
    """
        {
        "resource_changes": [
            {
              "address": "custom_provider_resource.replaced",
              "type": "custom_provider_resource",
              "change": {
                "actions": ["delete", "create"],
                "after": {
                  "tags": {}}
              }
              }
              ]
            }
        """,
        encoding="utf-8",)

    result = check_plan(str(plan_path))
    output = capsys.readouterr().out

    assert result == 1
    assert "custom_provider_resource.replaced" in output