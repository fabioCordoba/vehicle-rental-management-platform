import { useEffect, useState } from 'react'
import { useVehicles } from '../hooks/useVehicles'
import { useProcedures } from '../hooks/useProcedures'
import { useUsers } from '../hooks/useUsers'
import { usersApi } from '../api/users'
import { StatusBadge } from '../components/ui/StatusBadge'
import { ProcedureCard } from '../components/procedures/ProcedureCard'
import { Modal } from '../components/ui/Modal'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import { Pagination } from '../components/ui/Pagination'
import './AdminPage.css'

const EMPTY_VFILTER = {
  make: '', model: '', status: '', condition: '',
  color: '', min_year: '', max_year: '', min_price: '', max_price: '',
}

const EMPTY_VEHICLE = {
  make: '', model: '', year: new Date().getFullYear(),
  color: '', license_plate: '', condition: 'good',
  mileage: 0, passenger_capacity: 5, daily_rental_price: '',
}

function VehicleForm({ initial, onSubmit, onCancel }) {
  const [form, setForm] = useState(initial ?? EMPTY_VEHICLE)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      await onSubmit(form)
    } catch (err) {
      const data = err.response?.data
      setError(
        typeof data === 'string'
          ? data
          : data?.detail ?? JSON.stringify(data) ?? 'Error al guardar'
      )
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="vehicle-form" onSubmit={handleSubmit}>
      <div className="vehicle-form__row">
        <div className="vehicle-form__field">
          <label>Marca</label>
          <input value={form.make} onChange={set('make')} required placeholder="Toyota" />
        </div>
        <div className="vehicle-form__field">
          <label>Modelo</label>
          <input value={form.model} onChange={set('model')} required placeholder="Corolla" />
        </div>
      </div>
      <div className="vehicle-form__row">
        <div className="vehicle-form__field">
          <label>Año</label>
          <input type="number" value={form.year} onChange={set('year')} required min="1900" max="2100" />
        </div>
        <div className="vehicle-form__field">
          <label>Color</label>
          <input value={form.color} onChange={set('color')} required placeholder="Blanco" />
        </div>
      </div>
      <div className="vehicle-form__row">
        <div className="vehicle-form__field">
          <label>Placa</label>
          <input value={form.license_plate} onChange={set('license_plate')} required placeholder="ABC-123" />
        </div>
        <div className="vehicle-form__field">
          <label>Condición</label>
          <select value={form.condition} onChange={set('condition')}>
            <option value="excellent">Excelente</option>
            <option value="good">Bueno</option>
            <option value="fair">Regular</option>
            <option value="poor">Malo</option>
          </select>
        </div>
      </div>
      <div className="vehicle-form__row">
        <div className="vehicle-form__field">
          <label>Kilometraje</label>
          <input type="number" value={form.mileage} onChange={set('mileage')} required min="0" />
        </div>
        <div className="vehicle-form__field">
          <label>Pasajeros</label>
          <input type="number" value={form.passenger_capacity} onChange={set('passenger_capacity')} required min="1" />
        </div>
      </div>
      <div className="vehicle-form__field">
        <label>Precio por día (COP)</label>
        <input type="number" value={form.daily_rental_price} onChange={set('daily_rental_price')} required min="0" step="1000" placeholder="150000" />
      </div>

      {error && <p className="vehicle-form__error">{error}</p>}

      <div className="vehicle-form__actions">
        <button type="button" className="vf-btn vf-btn--ghost" onClick={onCancel}>Cancelar</button>
        <button type="submit" className="vf-btn" disabled={saving}>
          {saving ? 'Guardando…' : 'Guardar'}
        </button>
      </div>
    </form>
  )
}

function UserCreateForm({ onSubmit, onCancel }) {
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '',
    password: '', password_confirmation: '', role: '',
  })
  const [roles, setRoles] = useState([])
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    usersApi.roles()
      .then((res) => {
        const data = res.data
        setRoles(Array.isArray(data) ? data : data.results ?? [])
      })
      .catch(() => setRoles([]))
  }, [])

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.password_confirmation) {
      setError('Las contraseñas no coinciden.')
      return
    }
    setSaving(true)
    setError(null)
    try {
      await onSubmit({
        ...form,
        username: form.email,
      })
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') {
        const key = Object.keys(data)[0]
        const val = data[key]
        setError(`${key}: ${Array.isArray(val) ? val[0] : val}`)
      } else {
        setError(data?.detail ?? 'Error al crear el usuario')
      }
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="vehicle-form" onSubmit={handleSubmit}>
      <div className="vehicle-form__row">
        <div className="vehicle-form__field">
          <label>Nombre</label>
          <input value={form.first_name} onChange={set('first_name')} placeholder="Nombre" required />
        </div>
        <div className="vehicle-form__field">
          <label>Apellido</label>
          <input value={form.last_name} onChange={set('last_name')} placeholder="Apellido" required />
        </div>
      </div>
      <div className="vehicle-form__field">
        <label>Email</label>
        <input type="email" value={form.email} onChange={set('email')} placeholder="correo@ejemplo.com" required />
      </div>
      <div className="vehicle-form__field">
        <label>Rol</label>
        <select value={form.role} onChange={set('role')} required>
          <option value="">Seleccionar rol…</option>
          {roles.map((r) => (
            <option key={r.id} value={r.id}>{r.title ?? r.code_name}</option>
          ))}
        </select>
      </div>
      <div className="vehicle-form__row">
        <div className="vehicle-form__field">
          <label>Contraseña</label>
          <input type="password" value={form.password} onChange={set('password')} minLength={5} required />
        </div>
        <div className="vehicle-form__field">
          <label>Confirmar contraseña</label>
          <input type="password" value={form.password_confirmation} onChange={set('password_confirmation')} minLength={5} required />
        </div>
      </div>
      {error && <p className="vehicle-form__error">{error}</p>}
      <div className="vehicle-form__actions">
        <button type="button" className="vf-btn vf-btn--ghost" onClick={onCancel}>Cancelar</button>
        <button type="submit" className="vf-btn" disabled={saving}>{saving ? 'Creando…' : 'Crear usuario'}</button>
      </div>
    </form>
  )
}

function UserDetailRow({ label, value }) {
  return (
    <div className="user-detail__row">
      <dt className="user-detail__label">{label}</dt>
      <dd className="user-detail__value">{value}</dd>
    </div>
  )
}

function UserEditForm({ user, onSubmit, onCancel }) {
  const [form, setForm] = useState({
    first_name: user.first_name ?? '',
    last_name: user.last_name ?? '',
    email: user.email ?? '',
    is_active: user.is_active ?? true,
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  const set = (field) => (e) =>
    setForm((f) => ({ ...f, [field]: e.target.type === 'checkbox' ? e.target.checked : e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      await onSubmit(form)
    } catch (err) {
      const data = err.response?.data
      const key = data && typeof data === 'object' ? Object.keys(data)[0] : null
      setError(key ? `${key}: ${data[key][0] ?? data[key]}` : (data?.detail ?? 'Error al guardar'))
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="vehicle-form" onSubmit={handleSubmit}>
      <div className="vehicle-form__row">
        <div className="vehicle-form__field">
          <label>Nombre</label>
          <input value={form.first_name} onChange={set('first_name')} placeholder="Nombre" />
        </div>
        <div className="vehicle-form__field">
          <label>Apellido</label>
          <input value={form.last_name} onChange={set('last_name')} placeholder="Apellido" />
        </div>
      </div>
      <div className="vehicle-form__field">
        <label>Email</label>
        <input type="email" value={form.email} onChange={set('email')} required />
      </div>
      <div className="vehicle-form__field user-edit-active">
        <label className="user-edit-active__label">
          <input type="checkbox" checked={form.is_active} onChange={set('is_active')} />
          Usuario activo
        </label>
      </div>
      {error && <p className="vehicle-form__error">{error}</p>}
      <div className="vehicle-form__actions">
        <button type="button" className="vf-btn vf-btn--ghost" onClick={onCancel}>Cancelar</button>
        <button type="submit" className="vf-btn" disabled={saving}>{saving ? 'Guardando…' : 'Guardar'}</button>
      </div>
    </form>
  )
}

export function AdminPage() {
  const [tab, setTab] = useState('vehicles')
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editVehicle, setEditVehicle] = useState(null)
  const [feedback, setFeedback] = useState(null)

  // Vehicle filters
  const [vFilter, setVFilter] = useState(EMPTY_VFILTER)
  const [showAdvanced, setShowAdvanced] = useState(false)

  // Procedure status filter
  const [procedureStatus, setProcedureStatus] = useState('')

  const {
    vehicles, meta: vMeta, loading: vLoading, error: vError,
    fetchVehicles, searchVehicles, fetchPage: fetchVehiclePage,
    createVehicle, updateVehicle, toggleAvailability,
  } = useVehicles()

  const {
    procedures, loading: pLoading, error: pError,
    fetchProcedures, confirmProcedure, cancelProcedure,
  } = useProcedures()

  const { users, loading: uLoading, error: uError, fetchUsers, searchUsers, createUser, updateUser, removeUser } = useUsers()
  const [showCreateUser, setShowCreateUser] = useState(false)
  const [searchField, setSearchField] = useState('first_name')
  const [searchValue, setSearchValue] = useState('')
  const [viewUser, setViewUser] = useState(null)
  const [editUser, setEditUser] = useState(null)
  const [deleteUserId, setDeleteUserId] = useState(null)

  useEffect(() => { fetchVehicles() }, [fetchVehicles])
  useEffect(() => {
    if (tab === 'operations') {
      const params = procedureStatus ? { status: procedureStatus } : {}
      fetchProcedures(params)
      fetchUsers()
    }
  }, [tab, procedureStatus, fetchProcedures, fetchUsers])
  useEffect(() => { if (tab === 'users') fetchUsers() }, [tab, fetchUsers])

  const notify = (msg) => {
    setFeedback(msg)
    setTimeout(() => setFeedback(null), 3000)
  }

  const handleCreate = async (data) => {
    await createVehicle(data)
    setShowCreateModal(false)
    notify('Vehículo creado correctamente.')
  }

  const handleUpdate = async (data) => {
    await updateVehicle(editVehicle.id, data)
    setEditVehicle(null)
    notify('Vehículo actualizado.')
  }

  const handleToggle = async (id) => {
    await toggleAvailability(id)
    notify('Disponibilidad actualizada.')
  }

  const handleConfirm = async (id) => {
    await confirmProcedure(id)
    notify('Solicitud confirmada. El vehículo fue marcado como no disponible.')
  }

  const handleCancel = async (id) => {
    await cancelProcedure(id)
    notify('Solicitud cancelada.')
  }

  const setVF = (field) => (e) => setVFilter((f) => ({ ...f, [field]: e.target.value }))

  const applyVehicleFilter = (e) => {
    if (e) e.preventDefault()
    const params = Object.fromEntries(
      Object.entries(vFilter).filter(([, v]) => String(v).trim() !== '')
    )
    Object.keys(params).length === 0 ? fetchVehicles() : searchVehicles(params)
  }

  const clearVehicleFilter = () => {
    setVFilter(EMPTY_VFILTER)
    fetchVehicles()
  }

  const handleUserCreate = async (data) => {
    await createUser(data)
    setShowCreateUser(false)
    notify('Usuario creado correctamente.')
  }

  const handleUserSearch = (e) => {
    e.preventDefault()
    searchValue.trim() ? searchUsers(searchField, searchValue.trim()) : fetchUsers()
  }

  const handleUserSearchClear = () => {
    setSearchValue('')
    fetchUsers()
  }

  const handleUserUpdate = async (data) => {
    await updateUser(editUser.id, data)
    setEditUser(null)
    notify('Usuario actualizado.')
  }

  const handleUserDelete = async () => {
    await removeUser(deleteUserId)
    setDeleteUserId(null)
    notify('Usuario eliminado.')
  }

  return (
    <div className="admin-page">
      <div className="admin-page__header">
        <h1 className="admin-page__title">Panel de administración</h1>
      </div>

      {feedback && <div className="admin-feedback">{feedback}</div>}

      <div className="admin-tabs">
        <button
          className={`admin-tab ${tab === 'vehicles' ? 'admin-tab--active' : ''}`}
          onClick={() => setTab('vehicles')}
        >
          🚗 Vehículos
        </button>
        <button
          className={`admin-tab ${tab === 'operations' ? 'admin-tab--active' : ''}`}
          onClick={() => setTab('operations')}
        >
          📋 Solicitudes
        </button>
        <button
          className={`admin-tab ${tab === 'users' ? 'admin-tab--active' : ''}`}
          onClick={() => setTab('users')}
        >
          👥 Usuarios
        </button>
      </div>

      {/* VEHICLES TAB */}
      {tab === 'vehicles' && (
        <div className="admin-section">
          <div className="admin-section__toolbar">
            <h2 className="admin-section__subtitle">Flota de vehículos</h2>
            <button className="admin-btn" onClick={() => setShowCreateModal(true)}>
              + Nuevo vehículo
            </button>
          </div>

          <form className="admin-vehicle-filter" onSubmit={applyVehicleFilter}>
            <div className="admin-vehicle-filter__row">
              <input
                className="admin-vehicle-filter__input"
                placeholder="Marca"
                value={vFilter.make}
                onChange={setVF('make')}
              />
              <input
                className="admin-vehicle-filter__input"
                placeholder="Modelo"
                value={vFilter.model}
                onChange={setVF('model')}
              />
              <select className="admin-vehicle-filter__select" value={vFilter.status} onChange={setVF('status')}>
                <option value="">Todos los estados</option>
                <option value="available">Disponible</option>
                <option value="unavailable">No disponible</option>
              </select>
              <button type="submit" className="admin-btn">Buscar</button>
              <button type="button" className="admin-tbl-btn" onClick={clearVehicleFilter}>Limpiar</button>
              <button
                type="button"
                className="admin-tbl-btn"
                onClick={() => setShowAdvanced((v) => !v)}
              >
                {showAdvanced ? '▲ Menos' : '▼ Más filtros'}
              </button>
            </div>
            {showAdvanced && (
              <div className="admin-vehicle-filter__advanced">
                <input
                  className="admin-vehicle-filter__input"
                  placeholder="Color"
                  value={vFilter.color}
                  onChange={setVF('color')}
                />
                <select className="admin-vehicle-filter__select" value={vFilter.condition} onChange={setVF('condition')}>
                  <option value="">Cualquier condición</option>
                  <option value="excellent">Excelente</option>
                  <option value="good">Bueno</option>
                  <option value="fair">Regular</option>
                  <option value="poor">Malo</option>
                </select>
                <input
                  type="number"
                  className="admin-vehicle-filter__input"
                  placeholder="Año mín."
                  value={vFilter.min_year}
                  onChange={setVF('min_year')}
                />
                <input
                  type="number"
                  className="admin-vehicle-filter__input"
                  placeholder="Año máx."
                  value={vFilter.max_year}
                  onChange={setVF('max_year')}
                />
                <input
                  type="number"
                  className="admin-vehicle-filter__input"
                  placeholder="Precio mín."
                  value={vFilter.min_price}
                  onChange={setVF('min_price')}
                />
                <input
                  type="number"
                  className="admin-vehicle-filter__input"
                  placeholder="Precio máx."
                  value={vFilter.max_price}
                  onChange={setVF('max_price')}
                />
              </div>
            )}
          </form>

          {vLoading && <LoadingSpinner />}
          {vError && <p className="admin-error">{vError}</p>}

          {!vLoading && vehicles.length === 0 && (
            <p className="admin-empty">No se encontraron vehículos.</p>
          )}

          <div className="admin-vehicles-table-wrapper">
            {!vLoading && vehicles.length > 0 && (
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Vehículo</th>
                    <th>Placa</th>
                    <th>Año</th>
                    <th>Precio/día</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {vehicles.map((v, idx) => (
                    <tr key={v.id ?? idx}>
                      <td><strong>{v.make} {v.model}</strong><br /><small>{v.color}</small></td>
                      <td>{v.license_plate}</td>
                      <td>{v.year}</td>
                      <td>${Number(v.daily_rental_price).toLocaleString('es-CO')}</td>
                      <td><StatusBadge status={v.is_available ? 'available' : 'unavailable'} /></td>
                      <td>
                        <div className="admin-table__actions">
                          <button className="admin-tbl-btn" onClick={() => setEditVehicle(v)}>Editar</button>
                          <button
                            className={`admin-tbl-btn ${v.is_available ? 'admin-tbl-btn--warn' : 'admin-tbl-btn--ok'}`}
                            onClick={() => handleToggle(v.id)}
                          >
                            {v.is_available ? 'Deshabilitar' : 'Habilitar'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          <Pagination
            meta={vMeta}
            showing={vehicles.length}
            onPrev={() => fetchVehiclePage(vMeta.previous)}
            onNext={() => fetchVehiclePage(vMeta.next)}
          />
        </div>
      )}

      {/* OPERATIONS TAB */}
      {tab === 'operations' && (
        <div className="admin-section">
          <div className="admin-section__toolbar">
            <h2 className="admin-section__subtitle">Solicitudes de alquiler</h2>
            <div className="admin-procedure-filter">
              <label className="admin-procedure-filter__label">Estado:</label>
              <select
                className="admin-user-search__select"
                value={procedureStatus}
                onChange={(e) => setProcedureStatus(e.target.value)}
              >
                <option value="">Todos</option>
                <option value="pending">Pendientes</option>
                <option value="active">Activos</option>
                <option value="completed">Completados</option>
                <option value="cancelled">Cancelados</option>
              </select>
            </div>
          </div>

          {pLoading && <LoadingSpinner />}
          {pError && <p className="admin-error">{pError}</p>}

          {!pLoading && procedures.length === 0 && (
            <p className="admin-empty">No hay solicitudes registradas.</p>
          )}

          <div className="admin-procedures-grid">
            {procedures.map((p, idx) => {
              const vehicle = vehicles.find((v) => v.id === p.vehicle_id)
              const customer = users.find((u) => u.id === p.customer_id)
              const vehicleName = vehicle ? `${vehicle.make} ${vehicle.model}` : null
              const customerName = customer
                ? ([customer.first_name, customer.last_name].filter(Boolean).join(' ') || customer.email)
                : null
              return (
                <ProcedureCard
                  key={p.id ?? idx}
                  procedure={p}
                  vehicleName={vehicleName}
                  customerName={customerName}
                  onConfirm={handleConfirm}
                  onCancel={handleCancel}
                />
              )
            })}
          </div>
        </div>
      )}

      {/* USERS TAB */}
      {tab === 'users' && (
        <div className="admin-section">
          <div className="admin-section__toolbar">
            <h2 className="admin-section__subtitle">Usuarios registrados</h2>
            <button className="admin-btn" onClick={() => setShowCreateUser(true)}>+ Nuevo usuario</button>
          </div>

          <form className="admin-user-search" onSubmit={handleUserSearch}>
            <select
              className="admin-user-search__select"
              value={searchField}
              onChange={(e) => setSearchField(e.target.value)}
            >
              <option value="first_name">Nombre</option>
              <option value="last_name">Apellido</option>
              <option value="email">Email</option>
            </select>
            <input
              className="admin-user-search__input"
              type="text"
              placeholder="Valor a buscar…"
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
            />
            <button type="submit" className="admin-btn">Buscar</button>
            <button type="button" className="admin-tbl-btn" onClick={handleUserSearchClear}>
              Limpiar
            </button>
          </form>

          {uLoading && <LoadingSpinner />}
          {uError && <p className="admin-error">{uError}</p>}

          {!uLoading && users.length === 0 && (
            <p className="admin-empty">No se encontraron usuarios.</p>
          )}

          <div className="admin-vehicles-table-wrapper">
            {!uLoading && users.length > 0 && (
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Roles</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u, idx) => (
                    <tr key={u.id ?? idx}>
                      <td>{[u.first_name, u.last_name].filter(Boolean).join(' ') || '—'}</td>
                      <td>{u.email}</td>
                      <td>
                        {u.roles?.length
                          ? u.roles.map((r) => (
                              <span key={r.id ?? r.code_name} className="user-role-pill">
                                {r.title ?? r.code_name}
                              </span>
                            ))
                          : <span className="user-role-pill user-role-pill--empty">Sin rol</span>
                        }
                      </td>
                      <td>
                        <StatusBadge status={u.is_active ? 'available' : 'unavailable'} />
                      </td>
                      <td>
                        <div className="admin-table__actions">
                          <button className="admin-tbl-btn" onClick={() => setViewUser(u)}>Ver</button>
                          <button className="admin-tbl-btn admin-tbl-btn--ok" onClick={() => setEditUser(u)}>Editar</button>
                          <button className="admin-tbl-btn admin-tbl-btn--warn" onClick={() => setDeleteUserId(u.id)}>Eliminar</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      )}

      {/* USER CREATE MODAL */}
      {showCreateUser && (
        <Modal title="Nuevo usuario" onClose={() => setShowCreateUser(false)}>
          <UserCreateForm onSubmit={handleUserCreate} onCancel={() => setShowCreateUser(false)} />
        </Modal>
      )}

      {/* USER DETAIL MODAL */}
      {viewUser && (
        <Modal title="Detalle del usuario" onClose={() => setViewUser(null)}>
          <dl className="user-detail">
            <UserDetailRow label="Nombre" value={[viewUser.first_name, viewUser.last_name].filter(Boolean).join(' ') || '—'} />
            <UserDetailRow label="Email" value={viewUser.email} />
            <UserDetailRow label="Estado" value={<StatusBadge status={viewUser.is_active ? 'available' : 'unavailable'} />} />
            <UserDetailRow
              label="Roles"
              value={
                viewUser.roles?.length
                  ? viewUser.roles.map((r) => (
                      <span key={r.id ?? r.code_name} className="user-role-pill">{r.title ?? r.code_name}</span>
                    ))
                  : <span className="user-role-pill user-role-pill--empty">Sin rol</span>
              }
            />
            {viewUser.image && (
              <UserDetailRow label="Avatar" value={<img src={viewUser.image} alt="avatar" className="user-avatar-preview" />} />
            )}
          </dl>
        </Modal>
      )}

      {/* USER EDIT MODAL */}
      {editUser && (
        <Modal title={`Editar: ${editUser.email}`} onClose={() => setEditUser(null)}>
          <UserEditForm user={editUser} onSubmit={handleUserUpdate} onCancel={() => setEditUser(null)} />
        </Modal>
      )}

      {/* USER DELETE CONFIRM */}
      {deleteUserId && (
        <Modal title="Confirmar eliminación" onClose={() => setDeleteUserId(null)}>
          <div className="user-delete-confirm">
            <p>¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.</p>
            <div className="user-delete-confirm__actions">
              <button className="vf-btn vf-btn--ghost" onClick={() => setDeleteUserId(null)}>Cancelar</button>
              <button className="vf-btn user-delete-confirm__confirm" onClick={handleUserDelete}>Eliminar</button>
            </div>
          </div>
        </Modal>
      )}

      {showCreateModal && (
        <Modal title="Nuevo vehículo" onClose={() => setShowCreateModal(false)}>
          <VehicleForm onSubmit={handleCreate} onCancel={() => setShowCreateModal(false)} />
        </Modal>
      )}

      {editVehicle && (
        <Modal title={`Editar: ${editVehicle.make} ${editVehicle.model}`} onClose={() => setEditVehicle(null)}>
          <VehicleForm initial={editVehicle} onSubmit={handleUpdate} onCancel={() => setEditVehicle(null)} />
        </Modal>
      )}
    </div>
  )
}
