import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import './LoginPage.css'

export function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { login, loading, error } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = location.state?.from?.pathname ?? '/'
  const registered = location.state?.registered

  const handleSubmit = async (e) => {
    e.preventDefault()
    const ok = await login(email, password)
    if (ok) navigate(from, { replace: true })
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-card__header">
          <span className="login-card__logo">🚗</span>
          <h1 className="login-card__title">AutoRent</h1>
          <p className="login-card__subtitle">Inicia sesión para continuar</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-form__field">
            <label className="login-form__label" htmlFor="email">Correo electrónico</label>
            <input
              id="email"
              type="email"
              className="login-form__input"
              placeholder="usuario@ejemplo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="login-form__field">
            <label className="login-form__label" htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              className="login-form__input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {registered && (
            <p className="login-form__success">Cuenta creada. Inicia sesión para continuar.</p>
          )}
          {error && <p className="login-form__error">{error}</p>}

          <button type="submit" className="login-form__submit" disabled={loading}>
            {loading ? 'Ingresando…' : 'Iniciar sesión'}
          </button>
        </form>

        <p className="login-card__footer">
          ¿No tienes cuenta?{' '}
          <Link to="/register" className="login-link">Regístrate</Link>
        </p>
      </div>
    </div>
  )
}
