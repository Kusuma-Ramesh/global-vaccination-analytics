/**
 * StatusMessage — shared loading / error / empty state for data panels.
 *
 * loading: renders a shimmering skeleton in place of the eventual content
 *          so the layout doesn't jump once data arrives.
 * error:   instructive, non-apologetic — states what happened.
 * empty:   invitation-style — states there's nothing for this selection.
 */
export default function StatusMessage({ loading, error, empty }) {
  if (loading) {
    return (
      <div className="loading" role="status" aria-live="polite">
        <span className="visually-hidden">Loading data…</span>
        <div className="skeleton-block" aria-hidden="true">
          <div className="skeleton-line w-40" />
          <div className="skeleton-line h-tall" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error" role="alert">
        <span>{error}</span>
      </div>
    );
  }

  if (empty) {
    return (
      <div className="empty">
        <span>Try a different country, vaccine, or year range.</span>
      </div>
    );
  }

  return null;
}
