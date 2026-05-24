import { useState, useCallback } from 'react'
import { usersApi } from '../api/users'

export function useUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchUsers = useCallback(async (params = {}) => {
    setLoading(true)
    setError(null)
    try {
      const res = await usersApi.list(params)
      const data = res.data
      setUsers(Array.isArray(data) ? data : data.results ?? [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar usuarios')
    } finally {
      setLoading(false)
    }
  }, [])

  const searchUsers = useCallback(async (field, value) => {
    setLoading(true)
    setError(null)
    try {
      const res = await usersApi.search(field, value)
      const data = res.data
      setUsers(Array.isArray(data) ? data : data.results ?? [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Error en la búsqueda')
    } finally {
      setLoading(false)
    }
  }, [])

  const createUser = useCallback(async (data) => {
    const res = await usersApi.create(data)
    setUsers((prev) => [res.data, ...prev])
    return res.data
  }, [])

  const updateUser = useCallback(async (id, data) => {
    const res = await usersApi.update(id, data)
    setUsers((prev) => prev.map((u) => (u.id === id ? res.data : u)))
    return res.data
  }, [])

  const removeUser = useCallback(async (id) => {
    await usersApi.remove(id)
    setUsers((prev) => prev.filter((u) => u.id !== id))
  }, [])

  return { users, loading, error, fetchUsers, searchUsers, createUser, updateUser, removeUser }
}
