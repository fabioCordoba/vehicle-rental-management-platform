import './LoadingSpinner.css'

export function LoadingSpinner({ message = 'Cargando...' }) {
  return (
    <div className="spinner-wrapper">
      <div className="spinner" />
      <p className="spinner-message">{message}</p>
    </div>
  )
}
