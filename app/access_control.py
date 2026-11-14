"""
B2, part 1 — implement can_access_screening_report().

Read README.md's domain model first. A ScreeningReport belongs to a Tenant, a Tenant belongs to
a Property, and a Property belongs to a LandlordAccount. A PropertyManager is scoped to exactly
one LandlordAccount.

Work out from that hierarchy which boundary actually gates access to a ScreeningReport.
"""
from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    actor: the PropertyManager requesting access
    report: the ScreeningReport they're trying to view
    properties: all known Property records
    tenants: all known Tenant records

    Return True if actor may view report, False otherwise. Fail closed — if anything needed to
    make this determination is missing (tenant not found, property not found), return False.
    """
    tenant_by_id = {tenant.id: tenant for tenant in tenants}
    property_by_id = {property.id: property for property in properties}

    tenant = tenant_by_id.get(report.tenant_id)
    if tenant is None:
        return False

    property = property_by_id.get(tenant.property_id)
    if property is None:
        return False

    return actor.landlord_account_id == property.landlord_account_id

