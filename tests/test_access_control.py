from app.access_control import can_access_screening_report


def test_property_manager_cannot_access_another_landlords_report(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0],
        screening_reports[1],
        properties=properties,
        tenants=tenants,
    ) is False


def test_property_manager_can_access_same_landlords_report(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0],
        screening_reports[0],
        properties=properties,
        tenants=tenants,
    ) is True


def test_access_fails_closed_when_tenant_or_property_is_missing(
    property_managers, properties, tenants, screening_reports
):
    assert can_access_screening_report(
        property_managers[0],
        screening_reports[0],
        properties=properties,
        tenants=[],
    ) is False
    assert can_access_screening_report(
        property_managers[0],
        screening_reports[0],
        properties=[],
        tenants=tenants,
    ) is False
