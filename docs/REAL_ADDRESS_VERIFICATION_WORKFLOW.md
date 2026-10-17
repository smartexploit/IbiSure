# IbiSure Real-Address Collection and Verification Guide

## 1. Purpose

This guide defines how IbiSure collects, documents, and reviews
real address examples for the initial Ado-Ekiti pilot.

The current dataset contains synthetic test records only.
Those records must not be represented as real locations.

## 2. Record fields

- record_id: Unique identifier, such as ADDR-0001.
- original_address_text: The address description as supplied.
- normalized_address: A cleaned version that preserves meaningful
  geographic names and landmarks.
- locality: Town, neighbourhood, or locality.
- state: State in Nigeria.
- landmark: The specific landmark mentioned or independently identified.
- latitude and longitude: Coordinates only when supported by evidence.
- data_source: Where the information came from.
- permission_status: Whether collection and intended use are permitted.
- verification_status: unverified, pending, verified, or rejected.
- verification_method: How the address or location was checked.
- evidence_reference: A safe reference to supporting evidence.
- collected_at: Collection date in ISO format, YYYY-MM-DD.
- reviewer_notes: Relevant limitations and review notes.

## 3. Collection rules

1. Collect only information necessary for the pilot.
2. Prefer public, authorized, or explicitly consented sources.
3. Record the source and applicable permission before using a record.
4. Do not scrape restricted databases or bypass access controls.
5. Do not collect unnecessary personal or private residential details.
6. Preserve the supplied address text separately from the normalized text.
7. Never guess coordinates, postcodes, street names, or landmarks.
8. Do not treat a text match as proof that a physical location exists.
9. Keep synthetic test records separate from real collected records.
10. Review applicable privacy requirements and source terms before use.

## 4. Verification statuses

### unverified
The record has been collected but has not been independently checked.

### pending
A review has started, but sufficient supporting evidence is not yet available.

### verified
A reviewer has examined documented evidence sufficient for the
specific claim being made. Record the verification method, evidence
reference, date, and reviewer. Verification of a name or text description
does not automatically verify coordinates or postal delivery coverage.

### rejected
The record is unsuitable, contradicted by evidence, unauthorized for
the intended use, or otherwise fails the project's acceptance criteria.
Document the reason without retaining unnecessary personal information.

## 5. Evidence and coordinate rules

- Use authoritative or otherwise permitted evidence where available.
- Cross-check important location claims where practical.
- Record what was actually verified: landmark identity, locality,
  street location, coordinates, or another specific claim.
- Do not label a record fully verified when only part of it was checked.
- Store an evidence reference rather than sensitive documents or
  personal details whenever possible.
- If reliable coordinates are unavailable, leave both coordinate fields blank.
- Coordinates must be checked for plausibility and correct locality.
- A similarity score is a ranking signal, not a confidence guarantee.

## 6. Review process

1. Confirm that collection and use are permitted.
2. Check required fields and unique record IDs.
3. Review spelling and normalization without changing the original text.
4. Inspect supporting evidence.
5. Check the specific claims that the evidence supports.
6. Assign a status and record the verification method.
7. Have another reviewer check high-impact or uncertain records when feasible.
8. Run the dataset audit before importing approved records into a pilot dataset.

## 7. Pilot safeguards

- Keep the synthetic dataset unchanged for regression tests.
- Store real records in a separate dataset until their provenance,
  permission, and schema have been reviewed.
- Do not use unverified records to direct emergency responders or
  make safety-critical decisions.
- Do not claim nationwide coverage from an Ado-Ekiti pilot.
- Document limitations and correct errors when they are discovered.

## 8. NIPOST integration

The NIPOST application is awaiting a response according to the
project tracker. Do not assume approval, data access, or credentials.
Update this section only when an official response is received and
the permitted scope of use is clear.
