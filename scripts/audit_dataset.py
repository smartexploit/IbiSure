import json
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "sample_addresses.json"

ALLOWED_VERIFICATION_STATUSES = {
    "unverified",
    "pending",
    "verified",
    "rejected",
}

REQUIRED_FIELDS = (
    "record_id",
    "original_address_text",
    "normalized_address",
    "locality",
    "landmark",
    "data_source",
    "permission_status",
    "verification_status",
)


def audit_dataset():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Dataset root must be a JSON list.")

    errors = []
    warnings = []
    seen_ids = set()
    synthetic_count = 0
    non_synthetic_count = 0
    verified_count = 0
    coordinate_count = 0

    for index, record in enumerate(records):
        location = f"Record at index {index}"

        if not isinstance(record, dict):
            errors.append(f"{location} is not a JSON object.")
            continue

        record_id = record.get("record_id")
        label = (
            record_id
            if isinstance(record_id, str) and record_id.strip()
            else location
        )

        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if not isinstance(record.get(field), str)
            or not record[field].strip()
        ]

        if missing_fields:
            errors.append(
                f"{label}: missing or empty fields: "
                + ", ".join(missing_fields)
            )

        if isinstance(record_id, str) and record_id.strip():
            if record_id in seen_ids:
                errors.append(f"{label}: duplicate record ID.")
            seen_ids.add(record_id)

        source = record.get("data_source")
        is_synthetic = (
            isinstance(source, str)
            and source.strip().casefold() == "synthetic_test_data"
        )

        if is_synthetic:
            synthetic_count += 1
        else:
            non_synthetic_count += 1

            if not isinstance(source, str) or not source.strip():
                warnings.append(
                    f"{label}: data source provenance is missing."
                )

            permission = record.get("permission_status")
            if not isinstance(permission, str) or not permission.strip():
                warnings.append(
                    f"{label}: permission status needs review."
                )

        status = record.get("verification_status")

        if status not in ALLOWED_VERIFICATION_STATUSES:
            errors.append(
                f"{label}: invalid verification_status."
            )
        elif status == "verified":
            verified_count += 1

            if is_synthetic:
                warnings.append(
                    f"{label}: synthetic data must not be treated "
                    "as real-world verified evidence."
                )

        latitude = record.get("latitude")
        longitude = record.get("longitude")

        if (latitude is None) != (longitude is None):
            errors.append(
                f"{label}: provide both coordinates or neither."
            )
        elif latitude is not None:
            valid_numbers = all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                for value in (latitude, longitude)
            )

            if not valid_numbers:
                errors.append(
                    f"{label}: coordinates must be numeric."
                )
            elif not (
                -90 <= latitude <= 90
                and -180 <= longitude <= 180
            ):
                errors.append(
                    f"{label}: coordinates are outside valid ranges."
                )
            else:
                coordinate_count += 1

    normalized_addresses = [
        record["normalized_address"].strip().casefold()
        for record in records
        if isinstance(record, dict)
        and isinstance(record.get("normalized_address"), str)
        and record["normalized_address"].strip()
    ]

    duplicates = [
        address
        for address, count in Counter(normalized_addresses).items()
        if count > 1
    ]

    for address in duplicates:
        warnings.append(
            f"Repeated normalized address: {address!r}"
        )

    print("\nIBISURE DATA QUALITY REPORT")
    print("=" * 32)
    print(f"Total records: {len(records)}")
    print(f"Synthetic records: {synthetic_count}")
    print(f"Non-synthetic records: {non_synthetic_count}")
    print(f"Records labelled verified: {verified_count}")
    print(f"Records with coordinates: {coordinate_count}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nERRORS")
        for item in errors:
            print(f"- {item}")

    if warnings:
        print("\nWARNINGS")
        for item in warnings:
            print(f"- {item}")

    if not errors and not warnings:
        print("\nAll structural checks passed.")

    if synthetic_count == len(records) and records:
        print(
            "\nPILOT STATUS: Synthetic test data only. "
            "Real-world address accuracy has not been evaluated."
        )
    elif errors:
        print(
            "\nPILOT STATUS: Fix data errors before evaluation."
        )
    else:
        print(
            "\nPILOT STATUS: Review provenance, permissions, "
            "and verification evidence before real-world use."
        )

    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(audit_dataset())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Audit failed: {error}", file=sys.stderr)
        raise SystemExit(1)
