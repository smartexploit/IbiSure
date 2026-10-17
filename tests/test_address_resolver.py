import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.address_resolver import (
    normalize_text,
    calculate_similarity,
    resolve_address,
    load_addresses,
)


class TestIbiSureAddressResolver(unittest.TestCase):

    def test_normalization_ignores_case_and_punctuation(self):
        self.assertEqual(
            normalize_text("Near the Big Roundabout, Ado-Ekiti"),
            normalize_text("big roundabout ado ekiti"),
        )

    def test_normalization_handles_extra_whitespace(self):
        self.assertEqual(
            normalize_text("  big   roundabout   ado ekiti "),
            "big roundabout ado ekiti",
        )

    def test_identical_address_has_full_similarity(self):
        score = calculate_similarity(
            "near the big roundabout, Ado-Ekiti",
            "big roundabout ado ekiti",
        )
        self.assertEqual(score, 1.0)

    def test_similarity_is_between_zero_and_one(self):
        score = calculate_similarity(
            "main market ado",
            "bus park ado ekiti",
        )
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_known_description_returns_candidate(self):
        result = resolve_address(
            "near the big roundabout, Ado-Ekiti"
        )
        self.assertEqual(result["status"], "candidate_found")
        self.assertEqual(
            result["candidates"][0]["record_id"], "SYN-001"
        )

    def test_unknown_description_needs_clarification(self):
        result = resolve_address(
            "blue spaceship beside a mountain"
        )
        self.assertEqual(result["status"], "needs_clarification")

    def test_empty_input_needs_input(self):
        result = resolve_address("   ")
        self.assertEqual(result["status"], "needs_input")
        self.assertEqual(result["candidates"], [])

    def test_non_string_input_needs_input(self):
        result = resolve_address(None)
        self.assertEqual(result["status"], "needs_input")
        self.assertEqual(result["candidates"], [])

    def test_locality_only_needs_clarification(self):
        result = resolve_address("Ado-Ekiti")
        self.assertEqual(
            result["status"], "needs_clarification"
        )
        self.assertEqual(result["candidates"], [])

    def test_unrelated_landmark_returns_no_candidates(self):
        result = resolve_address(
            "blue spaceship beside a mountain"
        )
        self.assertEqual(
            result["status"], "needs_clarification"
        )
        self.assertEqual(result["candidates"], [])

    def test_candidates_are_not_claimed_as_verified(self):
        result = resolve_address(
            "near the big roundabout, Ado-Ekiti"
        )
        candidate = result["candidates"][0]

        self.assertEqual(
            candidate["verification_status"], "unverified"
        )
        self.assertIsNone(candidate["latitude"])
        self.assertIsNone(candidate["longitude"])

    def test_locality_names_are_preserved(self):
        self.assertEqual(
            normalize_text("Ado-Ekiti"),
            "ado ekiti",
        )

    def test_dataset_records_have_unique_ids(self):
        records = load_addresses()
        record_ids = [record["record_id"] for record in records]
        self.assertEqual(len(record_ids), len(set(record_ids)))

    def test_misspelled_landmark_requires_clarification(self):
        result = resolve_address(
            "near the big roundaboot, ado ekiti"
        )

        self.assertEqual(
            result["status"], "needs_clarification"
        )

        # A possible candidate may be shown for review, but
        # it must not be treated as a sufficiently strong match.
        if result["candidates"]:
            self.assertEqual(
                result["candidates"][0]["record_id"],
                "SYN-001",
            )

    def test_identical_candidates_are_reported_as_ambiguous(self):
        records = [
            {
                "record_id": "TEST-001",
                "original_address_text": "Big Roundabout Ado Ekiti",
                "normalized_address": "big roundabout ado ekiti",
                "locality": "Ado-Ekiti",
                "landmark": "Big Roundabout",
                "latitude": None,
                "longitude": None,
                "data_source": "synthetic_test_data",
                "permission_status": "not_applicable",
                "verification_status": "unverified",
            },
            {
                "record_id": "TEST-002",
                "original_address_text": "Big Roundabout Ado Ekiti",
                "normalized_address": "big roundabout ado ekiti",
                "locality": "Ado-Ekiti",
                "landmark": "Big Roundabout",
                "latitude": None,
                "longitude": None,
                "data_source": "synthetic_test_data",
                "permission_status": "not_applicable",
                "verification_status": "unverified",
            },
        ]

        with tempfile.TemporaryDirectory() as folder:
            dataset_path = Path(folder) / "test_addresses.json"
            dataset_path.write_text(
                json.dumps(records),
                encoding="utf-8",
            )

            with patch(
                "backend.address_resolver.DATA_FILE",
                dataset_path,
            ):
                result = resolve_address(
                    "Big Roundabout Ado Ekiti"
                )

        self.assertEqual(result["status"], "ambiguous")
        self.assertEqual(len(result["candidates"]), 2)

    def test_malformed_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            dataset_path = Path(folder) / "broken.json"
            dataset_path.write_text(
                "{invalid json",
                encoding="utf-8",
            )

            with patch(
                "backend.address_resolver.DATA_FILE",
                dataset_path,
            ):
                with self.assertRaises(json.JSONDecodeError):
                    load_addresses()


if __name__ == "__main__":
    unittest.main()

