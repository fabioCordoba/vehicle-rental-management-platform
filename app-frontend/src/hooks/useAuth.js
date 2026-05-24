import { useState, useEffect, useCallback } from 'react'
import { authApi } from '../api/auth'

function loadCachedUser() {
  try { return JSON.parse(localStorage.getItem('user_data')) } catch { return null }
}

export function useAuth() {
  const [user, setUser] = useState(loadCachedUser)
  const [token, setToken] = useState(() => localStorage.getItem('access_token'))
  const [loading, setLoading] = useState(!!localStorage.getItem('access_token'))
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!token) return
    setLoading(true)
    authApi.me()
      .then((res) => {
        setUser(res.data)
        localStorage.setItem('user_data', JSON.stringify(res.data))
      })
      .catch(() => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_data')
        setToken(null)
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [token])

  const login = useCallback(async (email, password) => {
    setError(null)
    setLoading(true)
    try {
      const res = await authApi.login(email, password)
      const { access, refresh } = res.data
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      setToken(access)
      return true
    } catch (err) {
      setError(err.response?.data?.detail || 'Credenciales incorrectas')
      return false
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(async () => {
    const refresh = localStorage.getItem('refresh_token')
    if (refresh) {
      try { await authApi.logout(refresh) } catch (_) {}
    }
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_data')
    setToken(null)
    setUser(null)
  }, [])

  const updateProfile = useCallback(async (data) => {
    const res = await authApi.updateMe(data)
    setUser(res.data)
    localStorage.setItem('user_data', JSON.stringify(res.data))
    return res.data
  }, [])

  return { user, token, loading, error, login, logout, updateProfile }
}
