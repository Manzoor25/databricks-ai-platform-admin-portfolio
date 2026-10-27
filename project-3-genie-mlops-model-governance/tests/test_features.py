import pytest

from src.features import capital_buffer, distress_label, resolve_device


def test_capital_buffer() -> None:
    assert capital_buffer(0.10) == pytest.approx(0.02)


def test_distress_label() -> None:
    assert distress_label(0.12, failed=False) == 0
    assert distress_label(0.12, failed=True) == 1
    assert distress_label(0.03, failed=False) == 1


def test_device_default_contract() -> None:
    assert resolve_device("cpu") == "cpu"
    assert resolve_device("cuda") == "cuda"
    with pytest.raises(ValueError):
        resolve_device("gpu")
