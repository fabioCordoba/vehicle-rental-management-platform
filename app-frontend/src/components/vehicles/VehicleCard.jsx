import { Link } from 'react-router-dom'
import { StatusBadge } from '../ui/StatusBadge'
import './VehicleCard.css'

const CONDITION_LABELS = {
  excellent: 'Excelente',
  good: 'Bueno',
  fair: 'Regular',
  poor: 'Malo',
}

export function VehicleCard({ vehicle }) {
  const {
    id,
    make,
    model,
    year,
    color,
    daily_rental_price,
    passenger_capacity,
    condition,
    is_available,
  } = vehicle

  return (
    <Link to={`/vehicles/${id}`} className="vehicle-card">
      <div className="vehicle-card__image">
        <span className="vehicle-card__icon">🚗</span>
      </div>
      <div className="vehicle-card__body">
        <div className="vehicle-card__header">
          <h3 className="vehicle-card__title">
            {make} {model}
          </h3>
          <StatusBadge status={is_available ? 'available' : 'unavailable'} />
        </div>
        <p className="vehicle-card__year">{year} · {color}</p>
        <div className="vehicle-card__meta">
          <span>👤 {passenger_capacity} pasajeros</span>
          <span>🔧 {CONDITION_LABELS[condition] ?? condition}</span>
        </div>
        <p className="vehicle-card__price">
          ${Number(daily_rental_price).toLocaleString('es-CO')}
          <span className="vehicle-card__per"> / día</span>
        </p>
      </div>
    </Link>
  )
}
