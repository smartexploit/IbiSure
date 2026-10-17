import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "sample_addresses.json"

# Remove conversational words, but preserve geographic names.
STOP_WORDS = {
    "near", "the", "in", "at", "by", "beside", "opposite",
    "behind", "front", "of", "to", "and", "around",
    "close", "next", "side", "from"
}

MINIMUM_SCORE = 75.0
MINIMUM_SCORE_GAP = 8.0
MAX_CANDIDATES = 3


def normalize_text(text: str) -> str:
    """Normalize text while preserving meaningful place names."""
    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    words = text.split()
    words = [word for word in words if word not in STOP_WORDS]
    return " ".join(words)


def load_addresses() -> list:
    """Load and validate the address dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("The address dataset must be a JSON list.")

    seen_ids = set()

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(
                f"Record at index {index} must be a JSON object."
            )

        record_id = record.get("record_id")
        landmark = record.get("landmark")
        address = record.get("normalized_address")
        locality = record.get("locality")

        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError(
                f"Record at index {index} needs a non-empty record_id."
            )

        if record_id in seen_ids:
            raise ValueError(f"Duplicate record_id: {record_id}")

        seen_ids.add(record_id)

        if not isinstance(landmark, str) or not landmark.strip():
            raise ValueError(
                f"Record {record_id} needs a non-empty landmark."
            )

        if not isinstance(address, str) or not address.strip():
            raise ValueError(
                f"Record {record_id} needs a normalized_address."
            )

        if not isinstance(locality, str) or not locality.strip():
            raise ValueError(
                f"Record {record_id} needs a non-empty locality."
            )

        for coordinate in ("latitude", "longitude"):
            value = record.get(coordinate)

            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
            ):
                raise ValueError(
                    f"Record {record_id} has an invalid {coordinate}."
                )

        latitude = record.get("latitude")
        longitude = record.get("longitude")

        if (latitude is None) != (longitude is None):
            raise ValueError(
                f"Record {record_id} must provide both coordinates "
                "or neither coordinate."
            )

        if latitude is not None and not (
            -90 <= latitude <= 90 and -180 <= longitude <= 180
        ):
            raise ValueError(
                f"Record {record_id} has coordinates outside valid ranges."
            )

    return records


def calculate_similarity(query: str, candidate: str) -> float:
    """Calculate text similarity from 0 to 1."""
    query_text = normalize_text(query)
    candidate_text = normalize_text(candidate)

    if not query_text or not candidate_text:
        return 0.0

    query_words = set(query_text.split())
    candidate_words = set(candidate_text.split())

    intersection = query_words & candidate_words
    union = query_words | candidate_words

    token_score = len(intersection) / len(union) if union else 0.0
    sequence_score = SequenceMatcher(
        None, query_text, candidate_text
    ).ratio()

    return (0.7 * token_score) + (0.3 * sequence_score)


def resolve_address(query: str) -> dict:
    """Rank text candidates without claiming physical verification."""
    if not isinstance(query, str) or not query.strip():
        return {
            "status": "needs_input",
            "message": "Please enter an address or landmark description.",
            "candidates": [],
        }

    records = load_addresses()
    query_text = normalize_text(query)

    if not query_text:
        return {
            "status": "needs_clarification",
            "message": (
                "The description contains no searchable words. "
                "Please enter a landmark or locality."
            ),
            "candidates": [],
        }

    query_words = set(query_text.split())
    ranked = []

    for record in records:
        candidate_text = record["normalized_address"]
        landmark_text = normalize_text(record["landmark"])
        landmark_words = set(landmark_text.split())

        # Require a shared landmark term. A shared locality alone should
        # not be enough to suggest a specific physical place.
        landmark_overlap = query_words & landmark_words

        if not landmark_overlap:
            continue

        score = calculate_similarity(query, candidate_text)

        ranked.append({
            "record_id": record["record_id"],
            "landmark": record["landmark"],
            "locality": record["locality"],
            "verification_status": record.get(
                "verification_status", "unverified"
            ),
            "similarity_score": round(score * 100, 1),
            "latitude": record.get("latitude"),
            "longitude": record.get("longitude"),
        })

    ranked.sort(
        key=lambda item: item["similarity_score"],
        reverse=True,
    )

    candidates = ranked[:MAX_CANDIDATES]

    if not ranked or ranked[0]["similarity_score"] < MINIMUM_SCORE:
        return {
            "status": "needs_clarification",
            "message": (
                "No sufficiently strong landmark text match was found. "
                "Try another landmark, street name, or more detail."
            ),
            "candidates": candidates,
        }

    if (
        len(ranked) > 1
        and ranked[0]["similarity_score"] - ranked[1]["similarity_score"]
        < MINIMUM_SCORE_GAP
    ):
        return {
            "status": "ambiguous",
            "message": (
                "Several candidates have similar text scores. "
                "Please clarify the landmark before selecting a location."
            ),
            "candidates": candidates,
        }

    return {
        "status": "candidate_found",
        "message": (
            "A possible text match was found. "
            "Text similarity does not verify the real-world location."
        ),
        "candidates": candidates,
    }


def main():
    query = " ".join(sys.argv[1:])

    if not query:
        query = input("Enter an address description: ").strip()

    try:
        result = resolve_address(query)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

