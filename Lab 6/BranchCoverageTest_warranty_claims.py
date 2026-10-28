
import pytest

from warranty_claims import (
    out_of_warranty_charge,
    claim_allowed,
    sla_status,
)


@pytest.mark.parametrize(
    "plan, age, claim_type, registered, expected",
    [
        ("basic", 12, "defect", False, 0),
        ("basic", 18, "defect", True, 0),
        ("premium", 36, "defect", True, 0),
        ("basic", 20, "defect", False, 800),
        ("standard", 30, "accidental", False, 1200),
        ("standard", 40, "accidental", False, 4400),
        ("standard", 40, "defect", False, 2400),
    ],
)
def test_charge_branches(plan, age, claim_type, registered, expected):
    assert out_of_warranty_charge(
        plan, age, claim_type, registered
    ) == expected


@pytest.mark.parametrize(
    "plan, age, message",
    [
        ("gold", 10, "unknown plan"),
        ("basic", -1, "invalid age"),
    ],
)
def test_charge_errors(plan, age, message):
    with pytest.raises(ValueError, match=message):
        out_of_warranty_charge(plan, age, "defect", False)


@pytest.mark.parametrize(
    "days, claims, recall, expected",
    [
        (0, 5, True, True),
        (0, 6, True, False),
        (29, 0, False, False),
        (30, 2, False, True),
        (30, 3, False, False),
    ],
)
def test_claim_decision_branches(days, claims, recall, expected):
    assert claim_allowed(days, claims, recall) is expected


@pytest.mark.parametrize(
    "hours, hardware, priority, expected",
    [
        (48, True, False, "on_track"),
        (36, True, False, "at_risk"),
        (35, True, False, "critical"),
        (24, False, False, "on_track"),
        (12, False, False, "at_risk"),
        (11, False, False, "critical"),
        (48, False, True, "on_track"),
        (36, False, True, "at_risk"),
        (35, False, True, "critical"),
    ],
)
def test_sla_decision_branches(hours, hardware, priority, expected):
    assert sla_status(hours, hardware, priority) == expected
