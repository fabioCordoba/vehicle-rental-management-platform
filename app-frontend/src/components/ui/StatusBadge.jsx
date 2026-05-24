import './StatusBadge.css'

const LABELS = {
  available: 'Disponible',
  unavailable: 'No disponible',
  pending: 'Pendiente',
  active: 'Activo',
  completed: 'Completado',
  cancelled: 'Cancelado',
}

export function StatusBadge({ status }) {
  const label = LABELS[status] ?? status
  return <span className={`badge badge--${status}`}>{label}</span>
}
