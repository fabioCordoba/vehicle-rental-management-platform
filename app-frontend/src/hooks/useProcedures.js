import { useState, useCallback } from 'react'
import { proceduresApi } from '../api/procedures'

export function useProcedures() {
  const [procedures, setProcedures] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchProcedures = useCallback(async (params = {}) => {
    setLoading(true)
    setError(null)
    try {
      const res = await proceduresApi.list(params)
      const data = res.data
      setProcedures(Array.isArray(data) ? data : data.results ?? [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar solicitudes')
    } finally {
      setLoading(false)
    }
  }, [])

  const createProcedure = useCallback(async (data) => {
    const res = await proceduresApi.create(data)
    setProcedures((prev) => [res.data, ...prev])
    return res.data
  }, [])

  const confirmProcedure = useCallback(async (id) => {
    const res = await proceduresApi.confirm(id)
    setProcedures((prev) => prev.map((p) => (p.id === id ? res.data : p)))
    return res.data
  }, [])

  const cancelProcedure = useCallback(async (id) => {
    const res = await proceduresApi.cancel(id)
    setProcedures((prev) => prev.map((p) => (p.id === id ? res.data : p)))
    return res.data
  }, [])

  const removeProcedure = useCallback(async (id) => {
    await proceduresApi.remove(id)
    setProcedures((prev) => prev.filter((p) => p.id !== id))
  }, [])

  return {
    procedures,
    loading,
    error,
    fetchProcedures,
    createProcedure,
    confirmProcedure,
    cancelProcedure,
    removeProcedure,
  }
}
