import { useState } from 'react'
import './App.css'

function App() {
  const [address, setAddress] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleResolve(event) {
    event.preventDefault()

    const trimmedAddress = address.trim()

    if (!trimmedAddress) {
      setError('Please enter an address or nearby landmark.')
      setResult(null)
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('/api/resolve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: trimmedAddress }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to resolve this address.')
      }

      setResult(data)
    } catch (err) {
      setError(
        err.message ||
          'Could not connect to IbiSure. Check that the backend is running.',
      )
    } finally {
      setLoading(false)
    }
  }

  function clearSearch() {
    setAddress('')
    setResult(null)
    setError('')
  }

  const candidates = result?.candidates ?? []
  const needsReview =
    result && result.status !== 'candidate_found'

  const resultHeading = {
    candidate_found: 'Possible matches',
    ambiguous: 'More than one possible match',
    needs_input: 'Address needed',
    needs_clarification: 'We need more information',
  }

  const statusClass = {
    candidate_found: 'status-success',
    ambiguous: 'status-ambiguous',
    needs_input: 'status-clarification',
    needs_clarification: 'status-clarification',
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="IbiSure home">
          <span className="brand-mark">I</span>
          <span>IbiSure</span>
        </a>

        <span className="location-badge">
          <span className="status-dot" />
          Ado-Ekiti pilot
        </span>
      </header>

      <section className="hero">
        <span className="eyebrow">NIGERIAN ADDRESS RESOLUTION</span>

        <h1>
          Turn everyday directions
          <span> into useful address leads.</span>
        </h1>

        <p className="hero-copy">
          Describe a place the way you know it. IbiSure searches available
          records and suggests possible matches without inventing locations.
        </p>

        <form className="search-card" onSubmit={handleResolve}>
          <label htmlFor="address">
            Where are you trying to locate?
          </label>

          <textarea
            id="address"
            value={address}
            onChange={(event) => setAddress(event.target.value)}
            placeholder="e.g. Near the big roundabout, Ado-Ekiti"
            rows={3}
            maxLength={500}
            disabled={loading}
          />

          <div className="search-footer">
            <span className="character-count">
              {address.length}/500 characters
            </span>

            <div className="search-actions">
              <button
                className="clear-button"
                type="button"
                onClick={clearSearch}
                disabled={loading}
              >
                Clear
              </button>

              <button
                className="resolve-button"
                type="submit"
                disabled={loading}
              >
                {loading ? 'Searching...' : 'Resolve address'}
                {!loading && <span aria-hidden="true"> &rarr;</span>}
              </button>
            </div>
          </div>
        </form>

        <div className="example-prompts">
          <span>Try an example:</span>

          {[
            'Near the big roundabout, Ado-Ekiti',
            'Beside the main market in Ado',
            'Opposite the bus park, Ado-Ekiti',
          ].map((example) => (
            <button
              type="button"
              className="example-chip"
              key={example}
              onClick={() => {
                setAddress(example)
                setResult(null)
                setError('')
              }}
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </section>

      {error && (
        <section className="feedback error-feedback" role="alert">
          <strong>Something needs attention</strong>
          <p>{error}</p>
        </section>
      )}

      {result && (
        <section className="results-section" aria-live="polite">
          <div className="results-heading">
            <div>
              <span className="eyebrow">SEARCH RESULTS</span>
              <h2>
                {resultHeading[result.status] || 'Search results'}
              </h2>
            </div>

            <span className="result-count">
              {candidates.length} candidate
              {candidates.length === 1 ? '' : 's'}
            </span>
          </div>

          <div
            className={`feedback result-status ${
              statusClass[result.status] || 'status-clarification'
            }`}
            role="status"
          >
            <strong>
              {result.status === 'candidate_found'
                ? 'Possible text match - not location verified'
                : result.status === 'ambiguous'
                  ? 'Please distinguish between these candidates'
                  : result.status === 'needs_input'
                    ? 'Enter an address to begin'
                    : 'Do not treat these suggestions as confirmed matches'}
            </strong>

            <p>
              {result.message ||
                'Try adding a street name, nearby landmark, neighbourhood, or locality.'}
            </p>
          </div>

          {candidates.length > 0 && (
            <div
              className={`candidate-list ${
                needsReview ? 'candidate-list-review' : ''
              }`}
            >
              {candidates.map((candidate, index) => (
                <article
                  className={`candidate-card ${
                    needsReview
                      ? 'candidate-card-review'
                      : 'candidate-card-strong'
                  }`}
                  key={
                    candidate.record_id ??
                    `${candidate.landmark}-${index}`
                  }
                >
                  <div className="candidate-number">{index + 1}</div>

                  <div className="candidate-content">
                    <div className="candidate-title-row">
                      <h3>{candidate.landmark || 'Unnamed landmark'}</h3>

                      <span className="verification-badge">
                        {candidate.verification_status || 'Unverified'}
                      </span>
                    </div>

                    <p className="candidate-location">
                      {candidate.locality || 'Locality not specified'}
                    </p>

                    {candidate.record_id?.startsWith('SYN-') && (
                      <p className="synthetic-notice">
                        Synthetic demonstration record - not evidence
                        of a verified real-world location.
                      </p>
                    )}

                    <div className="candidate-meta">
                      <span>
                        Text similarity score:{' '}
                        <strong>
                          {Number.isFinite(candidate.similarity_score)
                            ? `${candidate.similarity_score.toFixed(1)}%`
                            : 'Unavailable'}
                        </strong>
                      </span>

                      <span>
                        Coordinates:{' '}
                        <strong>
                          {candidate.latitude != null &&
                          candidate.longitude != null
                            ? `${candidate.latitude}, ${candidate.longitude}`
                            : 'Not available'}
                        </strong>
                      </span>
                    </div>

                    <p className="candidate-disclaimer">
                      This score measures text similarity only. It is not
                      a probability, a measure of location accuracy, or
                      proof that the landmark exists at this location.
                    </p>
                  </div>
                </article>
              ))}
            </div>
          )}

          {needsReview && candidates.length > 0 && (
            <div className="feedback info-feedback">
              <strong>Next step: provide more detail</strong>
              <p>
                These suggestions need human review. Add a street name,
                a nearby known landmark, or more details to narrow the search.
                Do not select a candidate solely because its score is higher.
              </p>
            </div>
          )}

          <p className="results-disclaimer">
            IbiSure is a prototype. Confirm locations using reliable
            evidence before relying on them for navigation, delivery,
            or emergency response.
          </p>
        </section>
      )}

      {!result && !error && (
        <section className="how-it-works">
          <div className="section-heading">
            <span className="eyebrow">SIMPLE BY DESIGN</span>
            <h2>How IbiSure works</h2>
          </div>

          <div className="steps-grid">
            <article className="step-card">
              <span className="step-icon">01</span>
              <h3>Describe the place</h3>
              <p>Use familiar landmarks and everyday directions.</p>
            </article>

            <article className="step-card">
              <span className="step-icon">02</span>
              <h3>Compare records</h3>
              <p>
                The resolver compares your words against available records.
              </p>
            </article>

            <article className="step-card">
              <span className="step-icon">03</span>
              <h3>Review candidates</h3>
              <p>
                Check possible matches and clarify uncertain results.
              </p>
            </article>
          </div>
        </section>
      )}

      <footer className="site-footer">
        <span>IbiSure | Address discovery for Nigeria</span>
        <span>Prototype v0.1.0 | Ado-Ekiti pilot</span>
      </footer>
    </main>
  )
}

export default App
