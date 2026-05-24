import './Pagination.css'

export function Pagination({ meta, onPrev, onNext, showing }) {
  const { count, next, previous } = meta

  if (!next && !previous) return null

  return (
    <div className="pagination">
      <button
        className="pagination__btn"
        onClick={onPrev}
        disabled={!previous}
      >
        ← Anterior
      </button>

      <span className="pagination__info">
        Mostrando <strong>{showing}</strong> de <strong>{count}</strong>
      </span>

      <button
        className="pagination__btn"
        onClick={onNext}
        disabled={!next}
      >
        Siguiente →
      </button>
    </div>
  )
}
