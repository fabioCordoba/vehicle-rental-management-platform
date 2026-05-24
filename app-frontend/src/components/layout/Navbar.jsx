import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { isAdmin } from '../../utils/roles'
import './Navbar.css'

export function Navbar() {
  const { user, token, logout } = useAuth()
  const navigate = useNavigate()
  const admin = isAdmin(user)

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  const linkClass = ({ isActive }) => isActive ? 'nav-link active' : 'nav-link'

  return (
    <nav className="navbar">
      <NavLink to="/" className="navbar-brand">
        🚗 AutoRent
      </NavLink>

      <ul className="navbar-links">
        <li>
          <NavLink to="/" className={linkClass} end>Inicio</NavLink>
        </li>
        <li>
          <NavLink to="/vehicles" className={linkClass}>Vehículos</NavLink>
        </li>
        {token && (
          <li>
            <NavLink to="/my-rentals" className={linkClass}>Mis Alquileres</NavLink>
          </li>
        )}
        {token && admin && (
          <li>
            <NavLink to="/admin" className={linkClass}>Administración</NavLink>
          </li>
        )}
      </ul>

      <div className="navbar-auth">
        {token ? (
          <>
            <NavLink
              to="/profile"
              className={({ isActive }) => `navbar-user ${isActive ? 'navbar-user--active' : ''}`}
            >
              {user?.email ?? 'Mi perfil'}
            </NavLink>
            <button className="btn-logout" onClick={handleLogout}>Salir</button>
          </>
        ) : (
          <NavLink to="/login" className="btn-login">Iniciar sesión</NavLink>
        )}
      </div>
    </nav>
  )
}
