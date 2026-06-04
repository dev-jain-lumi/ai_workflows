"""
CurveValidator — reference solution for facilitators.

Do NOT share this file with participants.
This is the expected outcome of M4 (test writing + implementation)
and M5 (scaffold-validator agent exercise).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from curve_pipeline.cet_converter import _is_october_day
from curve_pipeline.cet_converter import _is_cest, _is_october_day


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class CurveValidator:
    """Validate DC_FWD_POWERBERBPNCH curve records."""

    def validate_record(self, record: Dict) -> ValidationResult:
        """Validate a single record against all rules."""
        errors: List[str] = []
        warnings: List[str] = []

        # type check
        if record.get("type") not in ("CALCULATED", "INPUT"):
            errors.append(
                f"Invalid type: {record.get('type')!r}. Must be CALCULATED or INPUT."
            )

        # quote check — negative values are valid
        quote = record.get("quote", "")
        if quote == "" or quote is None:
            errors.append("quote is empty.")
        else:
            try:
                float(quote)
            except (ValueError, TypeError):
                errors.append(f"Invalid quote: {quote!r}. Must be numeric.")

        # order B on non-fall-back day
        order = record.get("order", "")
        start_date_str = record.get("startDate", "")
        start_time_str = record.get("startTime", "")
        if order == "B":
            try:
                d = date.fromisoformat(start_date_str)
                if not _is_october_day(d):
                    errors.append(
                        f"order=B is only valid on DST fall-back day (last Sunday October). "
                        f"Got startDate={start_date_str}, startTime={start_time_str}."
                    )
            except ValueError:
                errors.append(f"Cannot parse startDate: {start_date_str!r}")

        # 02:00 with no order field
        if start_time_str == "02:00:00" and not order:
            warnings.append(
                "02:00 record with no order field — ambiguous (could be DST fall-back A or B)."
            )

        # CET regime check
        cet_result = validate_cet_record(record)
        errors.extend(cet_result.get("errors", []))
        warnings.extend(cet_result.get("warnings", []))

        return ValidationResult(
            is_valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    def validate_batch(self, records: List[Dict]) -> List[ValidationResult]:
        """Validate each record and detect duplicates within the batch."""
        results = [self.validate_record(r) for r in records]

        # Duplicate detection — scoped to quotedDate + delivery slot
        key_counts: Counter = Counter(
            (
                r.get("quotedDate", ""),
                r.get("startDate", ""),
                r.get("startTime", ""),
                r.get("order", ""),
            )
            for r in records
        )

        for i, record in enumerate(records):
            key = (
                record.get("quotedDate", ""),
                record.get("startDate", ""),
                record.get("startTime", ""),
                record.get("order", ""),
            )
            if key_counts[key] > 1:
                results[i].warnings.append(
                    f"Duplicate delivery slot: quotedDate={key[0]} startDate={key[1]} "
                    f"startTime={key[2]} order={key[3]}"
                )

        return results

    def validate_cet_regime(self, record: Dict) -> ValidationResult:
        """Check cetStartDate/cetStarttime against the correct CET regime."""
        cet_result = validate_cet_record(record)
        return ValidationResult(
            is_valid=cet_result.get("is_valid", True),
            errors=cet_result.get("errors", []),
            warnings=cet_result.get("warnings", []),
        )

    def detect_order_b_violations(self, records: List[Dict]) -> List[ValidationResult]:
        """Return one ValidationResult per record where order=B is on a non-fall-back day."""
        violations = []
        for r in records:
            if r.get("order") != "B":
                continue
            try:
                d = date.fromisoformat(r["startDate"])
            except (KeyError, ValueError):
                continue
            if not _is_october_day(d):
                violations.append(
                    ValidationResult(
                        is_valid=False,
                        errors=[
                            f"order=B is only valid on DST fall-back day (last Sunday October). "
                            f"Got startDate={r.get('startDate')}, startTime={r.get('startTime')}."
                        ],
                    )
                )
        return violations

    def run_soda_checks(self, records: List[Dict]) -> dict:
        """Return a SODA-style summary of data quality issues."""
        summary = {
            "missing_cetStarttime": 0,
            "invalid_type": 0,
            "invalid_order": 0,
            "non_numeric_quote": 0,
            "order_b_violations": 0,
        }
        for r in records:
            if not r.get("cetStarttime"):
                summary["missing_cetStarttime"] += 1
            if r.get("type") not in ("CALCULATED", "INPUT"):
                summary["invalid_type"] += 1
            if r.get("order") not in ("A", "B", "", None):
                summary["invalid_order"] += 1
            quote = r.get("quote", "")
            if quote != "":
                try:
                    float(quote)
                except (ValueError, TypeError):
                    summary["non_numeric_quote"] += 1
            if r.get("order") == "B":
                try:
                    d = date.fromisoformat(r["startDate"])
                    if not _is_october_day(d):
                        summary["order_b_violations"] += 1
                except (KeyError, ValueError):
                    pass
        return summary


def validate_and_filter(records: List[Dict], strict: bool = False) -> List[Dict]:
    """Return only valid records. In strict mode, raise on any error."""
    validator = CurveValidator()
    results = validator.validate_batch(records)
    valid = []
    for record, result in zip(records, results):
        if result.is_valid:
            valid.append(record)
        elif strict:
            raise ValueError(f"Validation error: {result.errors}")
    return valid
