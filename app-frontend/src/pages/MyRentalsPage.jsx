import { useEffect, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useProcedures } from '../hooks/useProcedures'
import { useVehicles } from '../hooks/useVehicles'
import { ProcedureCard } from '../components/procedures/ProcedureCard'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import './MyRentalsPage.css'

const STATUS_OPTIONS = [
  { value: '', label: 'Todos' },
  { value: 'pending', label: 'Pendientes' },
  { value: 'active', label: 'Activos' },
  { value: 'completed', label: 'Completados' },
  { value: 'cancelled', label: 'Cancelados' },
]

export function MyRentalsPage() {
  const { user } = useAuth()
  const { procedures, loading: pLoading, error: pError, fetchProcedures, cancelProcedure } = useProcedures()
  const { vehicles, fetchAll } = useVehicles()
  const [statusFilter, setStatusFilter] = useState('')
  const [feedback, setFeedback] = useState(null)

  // Load the complete vehicle catalogue once so name resolution works
  // across all pages, not just the first one.
  useEffect(() => {
    fetchAll()
  }, [fetchAll])

  useEffect(() => {
    if (!user?.id) return
    const params = { customer_id: user.id }
    if (statusFilter) params.status = statusFilter
    fetchProcedures(params)
  }, [user, statusFilter, fetchProcedures])

  const notify = (msg) => {
    setFeedback(msg)
    setTimeout(() => setFeedback(null), 3000)
  }

  const handleCancel = async (id) => {
    await cancelProcedure(id)
    notify('Solicitud cancelada.')
  }

  return (
    <div className="my-rentals-page">
      <h1 className="my-rentals-page__title">Mis Alquileres</h1>

      {feedback && <div className="my-rentals-feedback">{feedback}</div>}

      <div className="my-rentals-filter">
        <span className="my-rentals-filter__label">Filtrar por estado:</span>
        <div className="my-rentals-filter__pills">
          {STATUS_OPTIONS.map(({ value, label }) => (
            <button
              key={value}
              className={`my-rentals-pill ${statusFilter === value ? 'my-rentals-pill--active' : ''}`}
              onClick={() => setStatusFilter(value)}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {pLoading && <LoadingSpinner />}
      {pError && <p className="my-rentals-error">{pError}</p>}
      {!pLoading && procedures.length === 0 && (
        <p className="my-rentals-empty">No tienes solicitudes de alquiler registradas.</p>
      )}

      <div className="my-rentals-grid">
        {procedures.map((p, idx) => {
          const vehicle = vehicles.find((v) => v.id === p.vehicle_id)
          const vehicleName = vehicle ? `${vehicle.make} ${vehicle.model}` : null
          return (
            <ProcedureCard
              key={p.id ?? idx}
              procedure={p}
              vehicleName={vehicleName}
              customerName="Yo"
              canConfirm={false}
              onConfirm={() => {}}
              onCancel={handleCancel}
            />
          )
        })}
      </div>
    </div>
  )
}
