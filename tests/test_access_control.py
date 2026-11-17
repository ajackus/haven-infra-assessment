"""
B2.1 tests: cross-account denial, same-account allow, and fail-closed edge cases.
Seed data comes from conftest.py fixtures; extra objects are built locally.
"""
from dataclasses import replace

from app.access_control import can_access_screening_report as can_access
from app.models import Tenant


def by_id(items, id_):
    return next(i for i in items if i.id == id_)


def test_cross_account_denied(property_managers, properties, tenants, screening_reports):
    pm1 = by_id(property_managers, "pm-001")
    rep2 = by_id(screening_reports, "rep-002")
    assert can_access(pm1, rep2, properties=properties, tenants=tenants) is False


def test_same_account_allowed(property_managers, properties, tenants, screening_reports):
    pm1 = by_id(property_managers, "pm-001")
    rep1 = by_id(screening_reports, "rep-001")
    assert can_access(pm1, rep1, properties=properties, tenants=tenants) is True


def test_reverse_direction(property_managers, properties, tenants, screening_reports):
    pm2 = by_id(property_managers, "pm-002")
    kw = dict(properties=properties, tenants=tenants)
    assert can_access(pm2, by_id(screening_reports, "rep-001"), **kw) is False
    assert can_access(pm2, by_id(screening_reports, "rep-002"), **kw) is True


def test_orphan_tenant_denied(property_managers, properties, tenants, screening_reports):
    pm1 = by_id(property_managers, "pm-001")
    orphan = replace(by_id(screening_reports, "rep-001"), tenant_id="ten-999")
    assert can_access(pm1, orphan, properties=properties, tenants=tenants) is False


def test_orphan_property_denied(property_managers, properties, tenants, screening_reports):
    pm1 = by_id(property_managers, "pm-001")
    lost = Tenant(id="ten-003", name="Lost", property_id="prop-999")
    rep = replace(by_id(screening_reports, "rep-001"), tenant_id="ten-003")
    assert can_access(pm1, rep, properties=properties, tenants=[*tenants, lost]) is False


def test_blank_account_ids_denied(property_managers, properties, tenants, screening_reports):
    pm_blank = replace(by_id(property_managers, "pm-001"), landlord_account_id="")
    blank_props = [replace(p, landlord_account_id="") for p in properties]
    rep1 = by_id(screening_reports, "rep-001")
    assert can_access(pm_blank, rep1, properties=blank_props, tenants=tenants) is False


def test_empty_lists_denied(property_managers, properties, tenants, screening_reports):
    pm1 = by_id(property_managers, "pm-001")
    rep1 = by_id(screening_reports, "rep-001")
    assert can_access(pm1, rep1, properties=[], tenants=tenants) is False
    assert can_access(pm1, rep1, properties=properties, tenants=[]) is False


def test_duplicate_ids_denied(property_managers, properties, tenants, screening_reports):
    pm1 = by_id(property_managers, "pm-001")
    rep1 = by_id(screening_reports, "rep-001")
    dup_prop = replace(by_id(properties, "prop-001"), landlord_account_id="la-002")
    assert can_access(pm1, rep1, properties=[*properties, dup_prop], tenants=tenants) is False
    dup_ten = replace(by_id(tenants, "ten-001"), property_id="prop-002")
    assert can_access(pm1, rep1, properties=properties, tenants=[*tenants, dup_ten]) is False


def test_none_inputs_denied(property_managers, properties, tenants, screening_reports):
    kw = dict(properties=properties, tenants=tenants)
    assert can_access(None, by_id(screening_reports, "rep-001"), **kw) is False
    assert can_access(by_id(property_managers, "pm-001"), None, **kw) is False
