
import pytest

from warranty_claims import (
    out_of_warranty_charge,
    claim_allowed,
    sla_status,
)


def test_invalid_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_invalid_age():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_registered_basic_plan():
    assert out_of_warranty_charge("basic", 15, "defect", True) == 0


def test_premium_registered_plan():
    assert out_of_warranty_charge("premium", 36, "defect", True) == 0


def test_small_excess_charge():
    assert out_of_warranty_charge("basic", 20, "defect", True) == 200


def test_accidental_charge():
    assert out_of_warranty_charge("standard", 30, "accidental", False) == 1200


def test_long_accidental_charge():
    assert out_of_warranty_charge("standard", 40, "accidental", False) == 4400


def test_long_defect_charge():
    assert out_of_warranty_charge("standard", 40, "defect", False) == 2400


def test_recall_claim_allowed():
    assert claim_allowed(0, 5, True) is True


def test_recall_claim_rejected():
    assert claim_allowed(60, 6, True) is False


def test_claim_too_soon():
    assert claim_allowed(29, 0, False) is False


def test_normal_claim_allowed():
    assert claim_allowed(30, 2, False) is True


def test_normal_claim_limit_exceeded():
    assert claim_allowed(60, 3, False) is False


def test_hardware_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_hardware_at_risk():
    assert sla_status(36, True, False) == "at_risk"


def test_hardware_critical():
    assert sla_status(35, True, False) == "critical"


def test_software_priority_on_track():
    assert sla_status(48, False, True) == "on_track"


def test_software_priority_at_risk():
    assert sla_status(36, False, True) == "at_risk"


def test_software_priority_critical():
    assert sla_status(35, False, True) == "critical"
