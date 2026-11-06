from access_control import can_view_screening_report


def test_same_landlord_account_allowed():
    result = can_view_screening_report(
        "L001",
        "L001"
    )

    assert result is True


def test_cross_landlord_account_denied():
    result = can_view_screening_report(
        "L001",
        "L002"
    )

    assert result is False


def test_missing_manager_account_denied():
    result = can_view_screening_report(
        "",
        "L001"
    )

    assert result is False


def test_missing_report_account_denied():
    result = can_view_screening_report(
        "L001",
        ""
    )

    assert result is False

