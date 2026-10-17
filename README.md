# IbiSure 🇳🇬

**An experimental address-resolution prototype for informal Nigerian addresses.**

IbiSure explores how informal descriptions, landmarks, spelling variations, and incomplete address details can be processed to suggest possible address matches while communicating uncertainty.

> **Status:** Early-stage prototype. The demonstration dataset contains synthetic records only. Real-world address accuracy has not yet been evaluated.

## The Problem

People often describe locations using landmarks and everyday expressions instead of complete, standardized street addresses. IbiSure explores how these descriptions can be processed without treating a text match as proof of a real-world location.

## Features

- Text normalization for case and punctuation.
- Similarity-based ranking of candidate addresses.
- Clarification for weak or unknown matches.
- Ambiguity handling for similar candidate scores.
- FastAPI backend and interactive API documentation.
- React frontend powered by Vite.
- Synthetic demonstration data.
- Automated tests and dataset quality checks.
- Verification-status and missing-coordinate handling.
- Documentation for responsible data collection.

## Technology Stack

- Python and FastAPI
- Pydantic
- React and JavaScript
- Vite
- Python unittest
- JSON and CSV

## Getting Started

### Backend

Activate the virtual environment and install dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --port 8001
```

API health check: http://127.0.0.1:8001/health

API documentation: http://127.0.0.1:8001/docs

### Frontend

Open a second PowerShell terminal:

```powershell
Set-Location "$HOME\Projects\Nigeria-Address-Resolver\frontend"
npm install
npm run dev -- --port 5174
```

Open http://localhost:5174/ in your browser.

## Testing

From the project root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
python .\scripts\audit_dataset.py
```

For frontend linting:

```powershell
Set-Location .\frontend
npm run lint
```

Passing these checks confirms software behavior and dataset structure; it does not establish real-world address accuracy.

## Responsible Data Use and Limitations

- The current records are synthetic demonstrations, not verified addresses.
- The matching threshold is provisional and requires evaluation.
- Text similarity is not a probability of correctness.
- Candidate matches are not verified locations.
- Coordinates must not be invented when unavailable.
- NIPOST integration must not be assumed until the required authorization is confirmed.
- Real data requires appropriate permission, provenance, and verification evidence.
- Unnecessary personal information should not be collected.

See `docs/` for the pilot plan, data collection protocol, collection template, and verification workflow.

## Roadmap

- [x] Build the initial matching engine.
- [x] Create the FastAPI API.
- [x] Build the React frontend.
- [x] Add automated tests.
- [x] Add a dataset audit.
- [ ] Publish the repository on GitHub.
- [ ] Obtain suitable permission for real pilot data.
- [ ] Evaluate matching quality using reviewed examples.
- [ ] Conduct a documented pilot in Ado-Ekiti.

## Learning Project

IbiSure is a practical project exploring API development, frontend integration, text processing, testing, data quality, and responsible address resolution.

## License

No license has been selected yet. Until a license is added, do not assume that others have permission to reuse or redistribute this code.
