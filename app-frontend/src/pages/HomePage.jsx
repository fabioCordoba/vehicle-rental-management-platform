import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { vehiclesApi } from '../api/vehicles'
import { proceduresApi } from '../api/procedures'
import { useAuth } from '../hooks/useAuth'
import { isAdmin } from '../utils/roles'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'
import './HomePage.css'

function StatCard({ icon, label, value, color }) {
  return (
    <div className="stat-card" style={{ '--stat-color': color }}>
      <span className="stat-card__icon">{icon}</span>
      <div>
        <p className="stat-card__value">{value}</p>
        <p className="stat-card__label">{label}</p>
      </div>
    </div>
  )
}

export function HomePage() {
  const { user, token } = useAuth()
  const admin = isAdmin(user)
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const promises = [vehiclesApi.available()]
    if (token) promises.push(vehiclesApi.list(), proceduresApi.list())

    Promise.allSettled(promises).then((results) => {
      const available = results[0].value?.data
      const allVehicles = results[1]?.value?.data
      const allProcs = results[2]?.value?.data

      const toArr = (d) => Array.isArray(d) ? d : d?.results ?? []

      setStats({
        available: toArr(available).length,
        total: allVehicles ? toArr(allVehicles).length : null,
        procedures: allProcs ? toArr(allProcs).length : null,
      })
      setLoading(false)
    })
  }, [token])

  return (
    <div className="home-page">
      <section className="home-hero">
        <h1 className="home-hero__title">Sistema de Gestión de Alquiler</h1>
        <p className="home-hero__subtitle">
          Consulta los vehículos disponibles y reserva tu próximo alquiler.
        </p>
        <div className="home-hero__actions">
          <Link to="/vehicles" className="home-btn home-btn--primary">Ver vehículos</Link>
          {token && admin && (
            <Link to="/admin" className="home-btn home-btn--secondary">Panel admin</Link>
          )}
          {token && !admin && (
            <Link to="/my-rentals" className="home-btn home-btn--secondary">Mis alquileres</Link>
          )}
          {!token && (
            <Link to="/login" className="home-btn home-btn--secondary">Iniciar sesión</Link>
          )}
        </div>
      </section>

      <section className="home-stats">
        <h2 className="home-section__title">Resumen del sistema</h2>
        {loading ? (
          <LoadingSpinner message="Cargando estadísticas…" />
        ) : (
          <div className="stats-grid">
            <StatCard
              icon="✅"
              label="Vehículos disponibles"
              value={stats.available}
              color="#059669"
            />
            {stats.total !== null && (
              <StatCard
                icon="🚗"
                label="Total en flota"
                value={stats.total}
                color="#2563eb"
              />
            )}
            {stats.procedures !== null && (
              <StatCard
                icon="📋"
                label="Solicitudes registradas"
                value={stats.procedures}
                color="#d97706"
              />
            )}
          </div>
        )}
      </section>

      <section className="home-features">
        <h2 className="home-section__title">¿Qué puedes hacer?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <span className="feature-card__icon">🔍</span>
            <h3>Explorar vehículos</h3>
            <p>Busca por marca, modelo o disponibilidad y consulta el detalle de cada vehículo.</p>
            <Link to="/vehicles" className="feature-card__link">Ir a vehículos →</Link>
          </div>
          <div className="feature-card">
            <span className="feature-card__icon">📅</span>
            <h3>Solicitar alquiler</h3>
            <p>Selecciona fechas y registra una solicitud de alquiler directamente desde el detalle del vehículo.</p>
            {token && (
              <Link to="/vehicles" className="feature-card__link">Buscar vehículo →</Link>
            )}
          </div>
          {admin ? (
            <div className="feature-card">
              <span className="feature-card__icon">⚙️</span>
              <h3>Administración</h3>
              <p>Añade nuevos vehículos, actualiza disponibilidad y gestiona todas las solicitudes pendientes.</p>
              <Link to="/admin" className="feature-card__link">Ir a admin →</Link>
            </div>
          ) : token ? (
            <div className="feature-card">
              <span className="feature-card__icon">📋</span>
              <h3>Mis alquileres</h3>
              <p>Consulta el estado de tus solicitudes y lleva el seguimiento de tus alquileres activos.</p>
              <Link to="/my-rentals" className="feature-card__link">Ver mis alquileres →</Link>
            </div>
          ) : (
            <div className="feature-card">
              <span className="feature-card__icon">🔐</span>
              <h3>Accede a tu cuenta</h3>
              <p>Inicia sesión para solicitar alquileres y hacer seguimiento de tus reservas.</p>
              <Link to="/login" className="feature-card__link">Iniciar sesión →</Link>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}
