"""
B2, part 1 — tenant screening-report authorization.

Authorization follows ScreeningReport -> Tenant -> Property -> LandlordAccount.
A PropertyManager is scoped to exactly one LandlordAccount.
"""
from app.models import PropertyManager, ScreeningReport, Property, Tenant


def _unique_by_id(records, record_id):
    """Return the sole matching record; fail closed for missing/ambiguous IDs."""
    matches = [record for record in records if record.id == record_id]
    return matches[0] if len(matches) == 1 else None


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    Return True only when the report's tenant resolves through a property
    to the same landlord account that scopes the authenticated actor.

    Missing or ambiguous relationships fail closed.
    """
    tenant = _unique_by_id(tenants, report.tenant_id)
    if tenant is None:
        return False

    property_record = _unique_by_id(properties, tenant.property_id)
    if property_record is None:
        return False

    return (
        bool(actor.landlord_account_id)
        and actor.landlord_account_id == property_record.landlord_account_id
    )
