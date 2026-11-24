import json

from scripts.cost_tag_check import check_plan


def test_plan_flags_only_created_or_updated_resources_missing_billing_tag(capsys):
    exit_code = check_plan("fixtures/plan.json")
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "aws_s3_bucket.listing_media" in output
    assert "aws_lambda_function.mls_feed_sync" in output
    assert "aws_s3_bucket.landlord_media[0]" not in output
    assert "aws_lambda_function.screening_report_export" not in output
    assert "aws_s3_bucket.archive_media" not in output
    assert "aws_s3_bucket.decommissioned_media" not in output


def test_check_is_idempotent_and_deduplicates_resource_addresses(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {"address": "aws_s3_bucket.example", "change": {"actions": ["create"], "after": {"tags": {"tenant_id": "t-1"}}}},
            {"address": "aws_s3_bucket.example", "change": {"actions": ["update"], "after": {"tags": {"tenant_id": "t-1"}}}},
            {"address": "aws_lambda_function.valid", "change": {"actions": ["create"], "after": {"tags": {"landlord_account_id": "la-1"}}}},
        ]
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    first_exit = check_plan(str(plan_path))
    first_output = capsys.readouterr().out
    second_exit = check_plan(str(plan_path))
    second_output = capsys.readouterr().out

    assert first_exit == second_exit == 1
    assert first_output == second_output
    assert first_output.count("aws_s3_bucket.example") == 1


def test_all_valid_resources_pass(tmp_path, capsys):
    plan_path = tmp_path / "valid-plan.json"
    plan_path.write_text(
        json.dumps({
            "resource_changes": [{
                "address": "aws_s3_bucket.valid",
                "change": {"actions": ["create"], "after": {"tags": {"landlord_account_id": "la-001"}}},
            }]
        }),
        encoding="utf-8",
    )
    assert check_plan(str(plan_path)) == 0
    assert "All created/updated resources" in capsys.readouterr().out
