import { useState } from 'react'
import { useAuth } from '../../hooks/useAuth'
import './RentalForm.css'

const today = () => new Date().toISOString().split('T')[0]

function serializeApiError(data) {
  if (!data) return 'Error al registrar la solicitud'
  if (typeof data === 'string') return data
  if (data.detail) return data.detail
  if (data.non_field_errors?.[0]) return data.non_field_errors[0]
  if (typeof data === 'object') {
    const key = Object.keys(data)[0]
    const val = data[key]
    return `${key}: ${Array.isArray(val) ? val[0] : val}`
  }
  return 'Error al registrar la solicitud'
}

export function RentalForm({ vehicleId, onSubmit, onCancel }) {
  const { user } = useAuth()
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    if (!startDate || !endDate) {
      setError('Completa las fechas de inicio y fin.')
      return
    }
    if (endDate <= startDate) {
      setError('La fecha de fin debe ser posterior a la de inicio.')
      return
    }

    setSubmitting(true)
    try {
      await onSubmit({
        vehicle_id: vehicleId,
        customer_id: user?.id,
        request_date: today(),
        start_date: startDate,
        end_date: endDate,
      })
      setSuccess(true)
    } catch (err) {
      setError(serializeApiError(err.response?.data))
    } finally {
      setSubmitting(false)
    }
  }

  if (success) {
    return (
      <div className="rental-success">
        <span className="rental-success__icon">✅</span>
        <h3>¡Solicitud registrada!</h3>
        <p>Tu solicitud de alquiler ha sido creada con estado <strong>Pendiente</strong>.</p>
        <button className="rental-form__btn" onClick={onCancel}>Cerrar</button>
      </div>
    )
  }

  return (
    <form className="rental-form" onSubmit={handleSubmit}>
      <div className="rental-form__field">
        <label className="rental-form__label">Fecha de inicio</label>
        <input
          type="date"
          className="rental-form__input"
          value={startDate}
          min={today()}
          onChange={(e) => setStartDate(e.target.value)}
          required
        />
      </div>

      <div className="rental-form__field">
        <label className="rental-form__label">Fecha de fin</label>
        <input
          type="date"
          className="rental-form__input"
          value={endDate}
          min={startDate || today()}
          onChange={(e) => setEndDate(e.target.value)}
          required
        />
      </div>

      {error && <p className="rental-form__error">{error}</p>}

      <div className="rental-form__actions">
        <button type="button" className="rental-form__btn rental-form__btn--ghost" onClick={onCancel}>
          Cancelar
        </button>
        <button type="submit" className="rental-form__btn" disabled={submitting}>
          {submitting ? 'Registrando…' : 'Solicitar alquiler'}
        </button>
      </div>
    </form>
  )
}
