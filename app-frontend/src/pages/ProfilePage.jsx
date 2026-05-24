import { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { authApi } from '../api/auth'
import './ProfilePage.css'

export function ProfilePage() {
  const { user, updateProfile } = useAuth()
  const [profileForm, setProfileForm] = useState({ first_name: '', last_name: '', email: '' })
  const [pwdForm, setPwdForm] = useState({ old_password: '', new_password: '', confirm_password: '' })
  const [profileLoading, setProfileLoading] = useState(false)
  const [pwdLoading, setPwdLoading] = useState(false)
  const [profileFeedback, setProfileFeedback] = useState(null)
  const [pwdFeedback, setPwdFeedback] = useState(null)
  const [profileError, setProfileError] = useState(null)
  const [pwdError, setPwdError] = useState(null)

  useEffect(() => {
    if (user) {
      setProfileForm({
        first_name: user.first_name ?? '',
        last_name: user.last_name ?? '',
        email: user.email ?? '',
      })
    }
  }, [user])

  const setP = (field) => (e) => setProfileForm((f) => ({ ...f, [field]: e.target.value }))
  const setPwd = (field) => (e) => setPwdForm((f) => ({ ...f, [field]: e.target.value }))

  const notify = (setter, msg) => {
    setter(msg)
    setTimeout(() => setter(null), 3000)
  }

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    setProfileLoading(true)
    setProfileError(null)
    try {
      await updateProfile(profileForm)
      notify(setProfileFeedback, 'Perfil actualizado correctamente.')
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') {
        const key = Object.keys(data)[0]
        const val = data[key]
        setProfileError(`${key}: ${Array.isArray(val) ? val[0] : val}`)
      } else {
        setProfileError(data?.detail ?? 'Error al actualizar el perfil')
      }
    } finally {
      setProfileLoading(false)
    }
  }

  const handlePwdSubmit = async (e) => {
    e.preventDefault()
    if (pwdForm.new_password !== pwdForm.confirm_password) {
      setPwdError('Las contraseñas nuevas no coinciden.')
      return
    }
    setPwdLoading(true)
    setPwdError(null)
    try {
      await authApi.changePassword({
        old_password: pwdForm.old_password,
        new_password: pwdForm.new_password,
      })
      setPwdForm({ old_password: '', new_password: '', confirm_password: '' })
      notify(setPwdFeedback, 'Contraseña cambiada correctamente.')
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') {
        const key = Object.keys(data)[0]
        const val = data[key]
        setPwdError(`${key}: ${Array.isArray(val) ? val[0] : val}`)
      } else {
        setPwdError(data?.detail ?? 'Error al cambiar la contraseña')
      }
    } finally {
      setPwdLoading(false)
    }
  }

  if (!user) return null

  const fullName = [user.first_name, user.last_name].filter(Boolean).join(' ') || user.email

  return (
    <div className="profile-page">
      <div className="profile-page__hero">
        <div className="profile-avatar">{fullName.charAt(0).toUpperCase()}</div>
        <div>
          <h1 className="profile-page__title">{fullName}</h1>
          <p className="profile-page__email">{user.email}</p>
        </div>
      </div>

      <section className="profile-section">
        <h2 className="profile-section__title">Información personal</h2>
        {profileFeedback && <div className="profile-feedback">{profileFeedback}</div>}
        <form className="profile-form" onSubmit={handleProfileSubmit}>
          <div className="profile-form__row">
            <div className="profile-form__field">
              <label>Nombre</label>
              <input value={profileForm.first_name} onChange={setP('first_name')} placeholder="Nombre" />
            </div>
            <div className="profile-form__field">
              <label>Apellido</label>
              <input value={profileForm.last_name} onChange={setP('last_name')} placeholder="Apellido" />
            </div>
          </div>
          <div className="profile-form__field">
            <label>Correo electrónico</label>
            <input type="email" value={profileForm.email} onChange={setP('email')} required />
          </div>
          {profileError && <p className="profile-error">{profileError}</p>}
          <div className="profile-form__actions">
            <button type="submit" className="profile-btn" disabled={profileLoading}>
              {profileLoading ? 'Guardando…' : 'Guardar cambios'}
            </button>
          </div>
        </form>
      </section>

      <section className="profile-section">
        <h2 className="profile-section__title">Cambiar contraseña</h2>
        {pwdFeedback && <div className="profile-feedback">{pwdFeedback}</div>}
        <form className="profile-form" onSubmit={handlePwdSubmit}>
          <div className="profile-form__field">
            <label>Contraseña actual</label>
            <input
              type="password"
              value={pwdForm.old_password}
              onChange={setPwd('old_password')}
              required
            />
          </div>
          <div className="profile-form__row">
            <div className="profile-form__field">
              <label>Nueva contraseña</label>
              <input
                type="password"
                value={pwdForm.new_password}
                onChange={setPwd('new_password')}
                minLength={5}
                required
              />
            </div>
            <div className="profile-form__field">
              <label>Confirmar nueva</label>
              <input
                type="password"
                value={pwdForm.confirm_password}
                onChange={setPwd('confirm_password')}
                minLength={5}
                required
              />
            </div>
          </div>
          {pwdError && <p className="profile-error">{pwdError}</p>}
          <div className="profile-form__actions">
            <button type="submit" className="profile-btn" disabled={pwdLoading}>
              {pwdLoading ? 'Cambiando…' : 'Cambiar contraseña'}
            </button>
          </div>
        </form>
      </section>
    </div>
  )
}
