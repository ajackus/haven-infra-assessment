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
    # Blank account ids must never match each other.
    if actor is None or report is None or not actor.landlord_account_id:
        return False

    # Exactly one match: a missing or duplicated record is ambiguous, so deny.
    found = [t for t in tenants if t.id == report.tenant_id]
    if len(found) != 1:
        return False

    props = [p for p in properties if p.id == found[0].property_id]
    if len(props) != 1:
        return False

    return props[0].landlord_account_id == actor.landlord_account_id
