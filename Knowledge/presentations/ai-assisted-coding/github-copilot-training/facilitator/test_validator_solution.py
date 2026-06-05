"""
Reference test suite for CurveValidator — facilitator solution.

These are the tests participants write in M4 Part B.
Do NOT share this file with participants before they write their own.

Run from the repo root:
    pytest tests/test_validator_solution.py -v
"""

import pytest

from curve_pipeline.validator_solution import CurveValidator


@pytest.fixture
def v():
    return CurveValidator()


# ── validate_cet_regime ───────────────────────────────────────────────────────


class TestCetRegime:
    def test_winter_no_conversion(self, v):
        """Winter: cetStarttime == startTime, no conversion needed."""
        result = v.validate_record(
            {
                "startDate": "2026-02-06",
                "startTime": "12:00:00",
                "order": "A",
                "quote": "82.0",
                "type": "CALCULATED",
                "cetStartDate": "2026-02-06",
                "cetStarttime": "12:00:00",
            }
        )
        assert result.is_valid
        assert result.errors == []

    def test_summer_subtract_one_hour(self, v):
        """Summer: cetStarttime = startTime − 1h."""
        result = v.validate_record(
            {
                "startDate": "2026-06-15",
                "startTime": "12:00:00",
                "order": "A",
                "quote": "50.0",
                "type": "CALCULATED",
                "cetStartDate": "2026-06-15",
                "cetStarttime": "11:00:00",
            }
        )
        assert result.is_valid
        assert result.errors == []

    def test_summer_wrong_cet_is_error(self, v):
        """Summer with copy-through (cetStarttime == startTime) is an ERROR."""
        result = v.validate_record(
            {
                "startDate": "2026-06-15",
                "startTime": "12:00:00",
                "order": "A",
                "quote": "50.0",
                "type": "CALCULATED",
                "cetStartDate": "2026-06-15",
                "cetStarttime": "12:00:00",
            }
        )
        assert not result.is_valid
        assert any(
            "mismatch" in e.lower() or "summer" in e.lower() for e in result.errors
        )

    def test_summer_midnight_date_rollback(self, v):
        """Summer 00:00 local → 23:00 previous day CET."""
        result = v.validate_record(
            {
                "startDate": "2026-06-15",
                "startTime": "00:00:00",
                "order": "A",
                "quote": "50.0",
                "type": "CALCULATED",
                "cetStartDate": "2026-06-14",
                "cetStarttime": "23:00:00",
            }
        )
        assert result.is_valid
        assert result.errors == []

    def test_fallback_order_b_no_conversion(self, v):
        """DST fall-back order B at 02:00 — already in CET, no subtraction."""
        result = v.validate_record(
            {
                "startDate": "2025-10-26",
                "startTime": "02:00:00",
                "order": "B",
                "quote": "78.0",
                "type": "CALCULATED",
                "cetStartDate": "2025-10-26",
                "cetStarttime": "02:00:00",
            }
        )
        assert result.is_valid
        assert result.errors == []


# ── validate_record — field checks ────────────────────────────────────────────


class TestValidateRecord:
    def test_invalid_type_is_error(self, v):
        result = v.validate_record(
            {
                "startDate": "2026-02-06",
                "startTime": "12:00:00",
                "order": "A",
                "quote": "50.0",
                "type": "ESTIMATED",
                "cetStartDate": "2026-02-06",
                "cetStarttime": "12:00:00",
            }
        )
        assert not result.is_valid
        assert any("type" in e.lower() for e in result.errors)

    def test_empty_quote_is_error(self, v):
        result = v.validate_record(
            {
                "startDate": "2026-02-06",
                "startTime": "12:00:00",
                "order": "A",
                "quote": "",
                "type": "CALCULATED",
                "cetStartDate": "2026-02-06",
                "cetStarttime": "12:00:00",
            }
        )
        assert not result.is_valid
        assert any("quote" in e.lower() for e in result.errors)

    def test_negative_quote_is_valid(self, v):
        """Negative prices are valid in power markets — must not be flagged."""
        result = v.validate_record(
            {
                "startDate": "2026-02-06",
                "startTime": "05:00:00",
                "order": "A",
                "quote": "-14.8",
                "type": "CALCULATED",
                "cetStartDate": "2026-02-06",
                "cetStarttime": "05:00:00",
            }
        )
        assert result.is_valid
        assert result.errors == []

    def test_missing_order_at_0200_is_warning(self, v):
        """02:00 record with no order field is ambiguous — WARNING, not error."""
        result = v.validate_record(
            {
                "startDate": "2026-02-06",
                "startTime": "02:00:00",
                "order": "",
                "quote": "50.0",
                "type": "CALCULATED",
                "cetStartDate": "2026-02-06",
                "cetStarttime": "02:00:00",
            }
        )
        assert result.is_valid  # warning only
        assert any("02:00" in w or "order" in w.lower() for w in result.warnings)


# ── detect_order_b_violations ─────────────────────────────────────────────────


class TestOrderBViolations:
    def test_order_b_on_correct_fallback_day_is_valid(self, v):
        """order=B on the 2025 fall-back day (Oct 26) — no violation."""
        violations = v.detect_order_b_violations(
            [
                {
                    "startDate": "2025-10-26",
                    "startTime": "02:00:00",
                    "order": "B",
                    "quote": "78.0",
                    "type": "CALCULATED",
                }
            ]
        )
        assert violations == []

    def test_order_b_on_summer_date_is_error(self, v):
        violations = v.detect_order_b_violations(
            [
                {
                    "startDate": "2026-06-15",
                    "startTime": "02:00:00",
                    "order": "B",
                    "quote": "50.0",
                    "type": "CALCULATED",
                }
            ]
        )
        assert len(violations) == 1
        assert not violations[0].is_valid
        assert any(
            "fall-back" in e.lower() or "fallback" in e.lower()
            for e in violations[0].errors
        )

    def test_order_b_on_winter_date_is_error(self, v):
        violations = v.detect_order_b_violations(
            [
                {
                    "startDate": "2026-02-05",
                    "startTime": "02:00:00",
                    "order": "B",
                    "quote": "82.0",
                    "type": "CALCULATED",
                }
            ]
        )
        assert len(violations) == 1
        assert not violations[0].is_valid

    def test_order_a_never_flagged(self, v):
        violations = v.detect_order_b_violations(
            [
                {
                    "startDate": "2026-06-15",
                    "startTime": "02:00:00",
                    "order": "A",
                    "quote": "50.0",
                    "type": "CALCULATED",
                }
            ]
        )
        assert violations == []


# ── validate_batch — duplicate detection ─────────────────────────────────────


class TestDuplicateDetection:
    def _record(self, qd, sd, st, order="A"):
        return {
            "quotedDate": qd,
            "startDate": sd,
            "startTime": st,
            "order": order,
            "quote": "50.0",
            "type": "CALCULATED",
            "cetStartDate": sd,
            "cetStarttime": st,
        }

    def test_no_duplicates_no_warnings(self, v):
        records = [
            self._record("2026-06-02", "2026-06-03", "00:00:00"),
            self._record("2026-06-02", "2026-06-03", "01:00:00"),
        ]
        results = v.validate_batch(records)
        assert all(
            r.warnings == [] or not any("duplicate" in w.lower() for w in r.warnings)
            for r in results
        )

    def test_duplicate_pair_both_get_warning(self, v):
        records = [
            self._record("2026-06-02", "2026-06-03", "00:00:00"),
            self._record("2026-06-02", "2026-06-03", "00:00:00"),
        ]
        results = v.validate_batch(records)
        assert all(any("duplicate" in w.lower() for w in r.warnings) for r in results)

    def test_only_duplicates_get_warning(self, v):
        records = [
            self._record("2026-06-02", "2026-06-03", "00:00:00"),
            self._record("2026-06-02", "2026-06-03", "00:00:00"),
            self._record("2026-06-02", "2026-06-03", "01:00:00"),  # unique
        ]
        results = v.validate_batch(records)
        assert any("duplicate" in w.lower() for w in results[0].warnings)
        assert any("duplicate" in w.lower() for w in results[1].warnings)
        assert not any("duplicate" in w.lower() for w in results[2].warnings)

    def test_different_quoted_date_not_duplicate(self, v):
        """Same delivery slot but different quotedDate = different batch = not a duplicate."""
        records = [
            self._record("2026-06-01", "2026-06-03", "00:00:00"),
            self._record("2026-06-02", "2026-06-03", "00:00:00"),
        ]
        results = v.validate_batch(records)
        assert not any("duplicate" in w.lower() for w in results[0].warnings)
        assert not any("duplicate" in w.lower() for w in results[1].warnings)
