"""B2.2 tests: landlord_account_id tag check on create/update resources."""
import json
from pathlib import Path

from scripts.cost_tag_check import check_plan

FIXTURE = str(Path(__file__).parent.parent / "fixtures" / "plan.json")


def write_plan(tmp_path, *changes):
    p = tmp_path / "plan.json"
    p.write_text(json.dumps({"resource_changes": list(changes)}))
    return str(p)


def rc(address, actions, tags=None, after=True):
    after_block = {"tags": tags} if tags is not None else {}
    return {"address": address, "change": {"actions": actions, "after": after_block if after else None}}


def test_fixture_flags_untagged(capsys):
    assert check_plan(FIXTURE) == 1
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 2
    flagged = " ".join(lines)
    assert "aws_s3_bucket.listing_media" in flagged
    assert "aws_lambda_function.mls_feed_sync" in flagged
    for ok in ("landlord_media", "screening_report_export", "archive_media", "decommissioned_media"):
        assert ok not in flagged


def test_idempotent(capsys):
    first = (check_plan(FIXTURE), capsys.readouterr().out)
    second = (check_plan(FIXTURE), capsys.readouterr().out)
    assert first == second


def test_all_tagged_passes(tmp_path, capsys):
    plan = write_plan(tmp_path, rc("a.x", ["create"], {"landlord_account_id": "la-001"}))
    assert check_plan(plan) == 0
    assert capsys.readouterr().out == ""


def test_skipped_actions_pass(tmp_path):
    plan = write_plan(
        tmp_path,
        rc("a.noop", ["no-op"], {}),
        rc("a.read", ["read"], {}),
        rc("a.del", ["delete"], after=False),
    )
    assert check_plan(plan) == 0


def test_replace_is_checked(tmp_path, capsys):
    plan = write_plan(tmp_path, rc("a.rep", ["delete", "create"], {}))
    assert check_plan(plan) == 1
    assert "a.rep" in capsys.readouterr().out


def test_empty_null_or_missing_tags_flagged(tmp_path, capsys):
    plan = write_plan(
        tmp_path,
        rc("a.empty", ["create"], {"landlord_account_id": ""}),
        rc("a.blank", ["update"], {"landlord_account_id": "  "}),
        rc("a.null", ["create"], {"landlord_account_id": None}),
        rc("a.notags", ["create"]),
    )
    assert check_plan(plan) == 1
    out = capsys.readouterr().out
    assert all(a in out for a in ("a.empty", "a.blank", "a.null", "a.notags"))


def test_duplicate_address_reported_once_and_sorted(tmp_path, capsys):
    plan = write_plan(
        tmp_path,
        rc("b.x", ["create"], {}),
        rc("a.x", ["create"], {}),
        rc("b.x", ["create"], {}),
    )
    assert check_plan(plan) == 1
    assert capsys.readouterr().out.splitlines() == [
        "missing landlord_account_id: a.x",
        "missing landlord_account_id: b.x",
    ]
