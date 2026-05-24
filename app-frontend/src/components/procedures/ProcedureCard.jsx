import { StatusBadge } from '../ui/StatusBadge'
import './ProcedureCard.css'

export function ProcedureCard({ procedure, vehicleName, customerName, onConfirm, onCancel, canConfirm = true }) {
  const {
    id,
    vehicle_id,
    customer_id,
    request_date,
    start_date,
    end_date,
    status,
  } = procedure

  return (
    <div className="procedure-card">
      <div className="procedure-card__header">
        <span className="procedure-card__id">#{id?.slice(0, 8)}</span>
        <StatusBadge status={status} />
      </div>

      <dl className="procedure-card__info">
        <dt>Vehículo</dt>
        <dd>{vehicleName ?? `${vehicle_id?.slice(0, 8)}…`}</dd>
        <dt>Cliente</dt>
        <dd>{customerName ?? `${customer_id?.slice(0, 8)}…`}</dd>
        <dt>Fecha solicitud</dt>
        <dd>{request_date}</dd>
        <dt>Inicio</dt>
        <dd>{start_date}</dd>
        <dt>Fin</dt>
        <dd>{end_date}</dd>
      </dl>

      <div className="procedure-card__actions">
        {status === 'pending' && (
          <>
            {canConfirm && (
              <button
                className="procedure-card__btn procedure-card__btn--confirm"
                onClick={() => onConfirm(id)}
              >
                Confirmar
              </button>
            )}
            <button
              className="procedure-card__btn procedure-card__btn--cancel"
              onClick={() => onCancel(id)}
            >
              Cancelar
            </button>
          </>
        )}
        {status === 'active' && (
          <button
            className="procedure-card__btn procedure-card__btn--cancel"
            onClick={() => onCancel(id)}
          >
            Cancelar alquiler
          </button>
        )}
        {(status === 'completed' || status === 'cancelled') && (
          <span className="procedure-card__closed">Cerrado</span>
        )}
      </div>
    </div>
  )
}
