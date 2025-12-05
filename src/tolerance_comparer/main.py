from __future__ import annotations


class ToleranceComparer:
    def __init__(
        self,
        *,
        relative_tolerance: float = 0.01,
        absolute_zero_threshold: float = 1e-6,
    ):
        self._relative_tolerance = relative_tolerance
        self._absolute_zero_threshold = absolute_zero_threshold

    def value_is_zero(self, value: float) -> bool:
        return abs(value) < self._absolute_zero_threshold

    def values_are_equal(self, first: float, second: float) -> bool:
        if first == second:
            return True

        reference_magnitude = max(abs(first), abs(second))
        if reference_magnitude == 0:
            return True

        relative_difference = abs(first - second) / reference_magnitude
        return relative_difference <= self._relative_tolerance

    def first_greater_than_second(self, first: float, second: float) -> bool:
        return first > second and not self.values_are_equal(first, second)

    def first_less_than_second(self, first: float, second: float) -> bool:
        return first < second and not self.values_are_equal(first, second)