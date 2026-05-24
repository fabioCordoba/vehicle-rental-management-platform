import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { vehiclesApi } from '../api/vehicles'
import { proceduresApi } from '../api/procedures'
import { StatusBadge } from '../components/ui/StatusBadge'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { Modal } from '../components/ui/Modal'
import { RentalForm } from '../components/procedures/RentalForm'
import './VehicleDetailPage.css'

const CONDITION_LABELS = {
  excellent: 'Excelente',
  good: 'Bueno',
  fair: 'Regular',
  poor: 'Malo',
}

function DetailRow({ label, value }) {
  return (
    <div className="detail-row">
      <dt className="detail-row__label">{label}</dt>
      <dd className="detail-row__value">{value}</dd>
    </div>
  )
}

export function VehicleDetailPage() {
  const { id } = useParams()
  const [vehicle, setVehicle] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showRentalModal, setShowRentalModal] = useState(false)

  const token = localStorage.getItem('access_token')

  useEffect(() => {
    vehiclesApi.get(id)
      .then((res) => setVehicle(res.data))
      .catch((err) => setError(err.response?.data?.detail ?? 'Vehículo no encontrado'))
      .finally(() => setLoading(false))
  }, [id])

  const handleRentSubmit = async (data) => {
    await proceduresApi.create(data)
  }

  if (loading) return <div className="detail-page"><LoadingSpinner /></div>

  if (error) {
    return (
      <div className="detail-page">
        <div className="detail-error">
          <p>⚠️ {error}</p>
          <Link to="/vehicles" className="detail-back">← Volver al listado</Link>
        </div>
      </div>
    )
  }

  const {
    make, model, year, color, license_plate,
    condition, mileage, passenger_capacity,
    daily_rental_price, is_available,
  } = vehicle

  return (
    <div className="detail-page">
      <Link to="/vehicles" className="detail-back">← Volver al listado</Link>

      <div className="detail-card">
        <div className="detail-card__image">
          <span className="detail-card__icon">🚗</span>
        </div>

        <div className="detail-card__content">
          <div className="detail-card__headline">
            <div>
              <h1 className="detail-card__title">{make} {model}</h1>
              <p className="detail-card__plate">{license_plate}</p>
            </div>
            <StatusBadge status={is_available ? 'available' : 'unavailable'} />
          </div>

          <dl className="detail-list">
            <DetailRow label="Año" value={year} />
            <DetailRow label="Color" value={color} />
            <DetailRow label="Condición" value={CONDITION_LABELS[condition] ?? condition} />
            <DetailRow label="Kilometraje" value={`${Number(mileage).toLocaleString('es-CO')} km`} />
            <DetailRow label="Pasajeros" value={passenger_capacity} />
            <DetailRow
              label="Precio por día"
              value={
                <strong className="detail-price">
                  ${Number(daily_rental_price).toLocaleString('es-CO')} COP
                </strong>
              }
            />
          </dl>

          {is_available ? (
            token ? (
              <button
                className="detail-rent-btn"
                onClick={() => setShowRentalModal(true)}
              >
                Solicitar alquiler
              </button>
            ) : (
              <p className="detail-login-hint">
                <Link to="/login">Inicia sesión</Link> para solicitar este vehículo.
              </p>
            )
          ) : (
            <p className="detail-unavailable">Este vehículo no está disponible actualmente.</p>
          )}
        </div>
      </div>

      {showRentalModal && (
        <Modal title="Solicitar alquiler" onClose={() => setShowRentalModal(false)}>
          <RentalForm
            vehicleId={id}
            onSubmit={handleRentSubmit}
            onCancel={() => setShowRentalModal(false)}
          />
        </Modal>
      )}
    </div>
  )
}
