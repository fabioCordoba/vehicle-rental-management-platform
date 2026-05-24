import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { authApi } from '../api/auth'
import './LoginPage.css'

export function RegisterPage() {
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '',
    password: '', password_confirmation: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.password_confirmation) {
      setError('Las contraseñas no coinciden.')
      return
    }
    setLoading(true)
    setError(null)
    try {
      await authApi.register({ ...form, username: form.email })
      navigate('/login', { state: { registered: true } })
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') {
        const key = Object.keys(data)[0]
        const val = data[key]
        setError(`${key}: ${Array.isArray(val) ? val[0] : val}`)
      } else {
        setError(data?.detail ?? 'Error al registrarse')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-card__header">
          <span className="login-card__logo">🚗</span>
          <h1 className="login-card__title">AutoRent</h1>
          <p className="login-card__subtitle">Crea tu cuenta</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-form__row">
            <div className="login-form__field">
              <label className="login-form__label">Nombre</label>
              <input
                className="login-form__input"
                value={form.first_name}
                onChange={set('first_name')}
                placeholder="Juan"
                required
              />
            </div>
            <div className="login-form__field">
              <label className="login-form__label">Apellido</label>
              <input
                className="login-form__input"
                value={form.last_name}
                onChange={set('last_name')}
                placeholder="Pérez"
                required
              />
            </div>
          </div>

          <div className="login-form__field">
            <label className="login-form__label" htmlFor="reg-email">Correo electrónico</label>
            <input
              id="reg-email"
              type="email"
              className="login-form__input"
              placeholder="usuario@ejemplo.com"
              value={form.email}
              onChange={set('email')}
              required
              autoFocus
            />
          </div>

          <div className="login-form__row">
            <div className="login-form__field">
              <label className="login-form__label">Contraseña</label>
              <input
                type="password"
                className="login-form__input"
                placeholder="••••••••"
                value={form.password}
                onChange={set('password')}
                minLength={5}
                required
              />
            </div>
            <div className="login-form__field">
              <label className="login-form__label">Confirmar</label>
              <input
                type="password"
                className="login-form__input"
                placeholder="••••••••"
                value={form.password_confirmation}
                onChange={set('password_confirmation')}
                minLength={5}
                required
              />
            </div>
          </div>

          {error && <p className="login-form__error">{error}</p>}

          <button type="submit" className="login-form__submit" disabled={loading}>
            {loading ? 'Registrando…' : 'Crear cuenta'}
          </button>
        </form>

        <p className="login-card__footer">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="login-link">Inicia sesión</Link>
        </p>
      </div>
    </div>
  )
}
