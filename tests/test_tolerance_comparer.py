from __future__ import annotations

import pytest

from . import ToleranceComparer


class TestToleranceComparer:
    @pytest.fixture
    def comparer(self) -> ToleranceComparer:
        return ToleranceComparer(relative_tolerance=0.01, absolute_zero_threshold=0.001)

    def test_grams_is_zero_for_very_small_values(self, comparer: ToleranceComparer):
        assert comparer.value_is_zero(0.0)
        assert comparer.value_is_zero(0.0005)
        assert comparer.value_is_zero(-0.0005)
        assert comparer.value_is_zero(0.0009)
        assert not comparer.value_is_zero(0.001)
        assert not comparer.value_is_zero(0.002)
        assert not comparer.value_is_zero(-0.002)

    def test_values_are_equal_exact_match(self, comparer: ToleranceComparer):
        assert comparer.values_are_equal(5.0, 5.0)
        assert comparer.values_are_equal(0.0, 0.0)
        assert comparer.values_are_equal(-10.5, -10.5)

    def test_values_are_equal_within_tolerance(self, comparer: ToleranceComparer):
        # 1% tolerance means 100 ± 1
        assert comparer.values_are_equal(100.0, 101.0)
        assert comparer.values_are_equal(100.0, 99.0)
        assert comparer.values_are_equal(100.0, 100.5)
        assert not comparer.values_are_equal(100.0, 101.1)
        assert not comparer.values_are_equal(100.0, 98.9)

    def test_values_are_equal_with_negative_numbers(self, comparer: ToleranceComparer):
        assert comparer.values_are_equal(-100.0, -101.0)
        assert comparer.values_are_equal(-100.0, -99.0)
        assert not comparer.values_are_equal(-100.0, -101.1)

    def test_values_are_equal_zero_edge_case(self, comparer: ToleranceComparer):
        assert comparer.values_are_equal(0.0, 0.0)
        # When one value is zero, any non-zero value is not equal
        assert not comparer.values_are_equal(0.0, 0.01)
        assert not comparer.values_are_equal(0.01, 0.0)

    def test_first_greater_than_second(self, comparer: ToleranceComparer):
        assert comparer.first_greater_than_second(first=10.0, second=5.0)
        assert comparer.first_greater_than_second(first=100.0, second=98.0)
        # Within tolerance - not greater
        assert not comparer.first_greater_than_second(first=100.0, second=99.5)
        assert not comparer.first_greater_than_second(first=5.0, second=10.0)
        assert not comparer.first_greater_than_second(first=100.0, second=100.0)

    def test_first_less_than_second(self, comparer: ToleranceComparer):
        assert comparer.first_less_than_second(first=5.0, second=10.0)
        assert comparer.first_less_than_second(first=98.0, second=100.0)
        # Within tolerance - not less
        assert not comparer.first_less_than_second(first=99.5, second=100.0)
        assert not comparer.first_less_than_second(first=10.0, second=5.0)
        assert not comparer.first_less_than_second(first=100.0, second=100.0)

    def test_comparison_methods_with_tolerance_boundary(
        self, comparer: ToleranceComparer
    ):
        # Test exactly at tolerance boundary (1% of 100 = 1)
        assert not comparer.first_greater_than_second(first=101.0, second=100.0)
        assert not comparer.first_less_than_second(first=99.0, second=100.0)
        # Just beyond tolerance
        assert comparer.first_greater_than_second(first=101.1, second=100.0)
        assert comparer.first_less_than_second(first=98.9, second=100.0)
