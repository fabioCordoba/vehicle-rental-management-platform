import { Navigate, useLocation } from 'react-router-dom'
import { isAdmin } from '../../utils/roles'

export function ProtectedRoute({ children, adminOnly }) {
  const token = localStorage.getItem('access_token')
  const location = useLocation()

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (adminOnly) {
    try {
      const user = JSON.parse(localStorage.getItem('user_data') ?? 'null')
      if (!isAdmin(user)) {
        return <Navigate to="/" replace />
      }
    } catch {
      return <Navigate to="/" replace />
    }
  }

  return children
}
