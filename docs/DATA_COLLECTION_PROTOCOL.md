# IbiSure — Phase 1 Data Collection Protocol

## 1. Purpose

IbiSure aims to convert Nigerian addresses written in everyday,
informal language into structured, verifiable location records.

The initial pilot will focus on Ado-Ekiti, Ekiti State, Nigeria.

## 2. Data Collection Principles

- Collect only data needed to test address resolution.
- Use independently collected data or sources whose terms permit the intended use.
- Obtain consent when collecting information from individuals.
- Do not collect private home addresses unnecessarily.
- Never publish personal phone numbers or sensitive location details.
- Do not scrape or systematically harvest restricted NIPOST data.
- Do not treat an estimated map pin as a verified address.
- Record the source and verification status of each test record.

## 3. Initial Data Categories

The pilot may include:
- Public businesses that permit their location to be recorded.
- Public facilities and landmarks.
- Consenting participants' descriptions of how to find a location.
- Synthetic addresses created for software testing.

Do not mix synthetic records with real-world verified records.

## 4. Proposed Record Fields

Each test record may contain:

- record_id
- original_address_text
- normalized_address
- locality
- landmark
- latitude
- longitude
- data_source
- permission_status
- verification_status
- reviewer_notes

Avoid collecting names, phone numbers, or other personal identifiers
unless genuinely necessary and appropriately protected.

## 5. Verification Status

Use one of these labels:

- unverified: not independently checked
- candidate: a possible match has been identified
- confirmed: the location has been checked using an appropriate method
- rejected: the candidate is incorrect or unsuitable

A geocoder result alone does not prove that an address is correct.

## 6. Data Quality

- Preserve the original address text.
- Normalize a separate copy rather than overwriting the original.
- Record uncertainty and missing information explicitly.
- Never invent coordinates, postcodes, streets, or landmarks.
- Keep a record of how each location was verified.
- Remove duplicate records where appropriate.

## 7. Privacy and Security

- Restrict access to raw pilot data.
- Do not commit private participant data or credentials to GitHub.
- Use synthetic examples in public documentation.
- Define a retention and deletion process before collecting participant data.
- Review applicable privacy requirements before a live pilot.

## 8. External Services

Before using a mapping, geocoding, or postcode service, review its
terms, attribution requirements, data retention rules, and commercial
usage restrictions.

NIPOST integration remains pending until the relevant permission,
access, and terms are confirmed.

## 9. Pilot Readiness

Before real participant testing, document:
- What data will be collected and why.
- How consent will be obtained.
- Who can access the data.
- How test locations will be verified.
- How participants can request correction or deletion.
- How results and errors will be measured.
