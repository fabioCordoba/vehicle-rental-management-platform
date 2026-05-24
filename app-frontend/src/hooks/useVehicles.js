import { useState, useCallback } from 'react'
import { vehiclesApi } from '../api/vehicles'
import client from '../api/client'

const EMPTY_META = { count: 0, next: null, previous: null }

// Extract just the path+query from a full URL so the Axios client uses its
// own baseURL (HTTPS). The backend returns http:// which causes a redirect
// that browsers block for CORS preflights.
function toPath(url) {
  try {
    const { pathname, search } = new URL(url)
    return pathname + search
  } catch {
    return url
  }
}

function parseMeta(data) {
  if (Array.isArray(data)) {
    return { results: data, meta: { count: data.length, next: null, previous: null } }
  }
  return {
    results: data.results ?? [],
    meta: {
      count: data.count ?? 0,
      next: data.next ?? null,
      previous: data.previous ?? null,
    },
  }
}

export function useVehicles() {
  const [vehicles, setVehicles] = useState([])
  const [meta, setMeta] = useState(EMPTY_META)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const applyResponse = useCallback((data) => {
    const { results, meta: m } = parseMeta(data)
    setVehicles(results)
    setMeta(m)
  }, [])

  const fetchVehicles = useCallback(async (params = {}, onlyAvailable = false) => {
    setLoading(true)
    setError(null)
    try {
      const call = onlyAvailable ? vehiclesApi.available : vehiclesApi.list
      const res = await call(params)
      applyResponse(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar vehículos')
    } finally {
      setLoading(false)
    }
  }, [applyResponse])

  const searchVehicles = useCallback(async (params) => {
    setLoading(true)
    setError(null)
    try {
      const res = await vehiclesApi.search(params)
      applyResponse(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error en la búsqueda')
    } finally {
      setLoading(false)
    }
  }, [applyResponse])

  // Fetches every page and accumulates all results into vehicles[].
  // Use this when you need the full catalogue for a name lookup (e.g. MyRentalsPage).
  const fetchAll = useCallback(async (params = {}) => {
    setLoading(true)
    setError(null)
    const all = []
    try {
      let res = await vehiclesApi.list(params)
      let data = res.data
      all.push(...(Array.isArray(data) ? data : data.results ?? []))
      let nextUrl = Array.isArray(data) ? null : (data.next ?? null)

      while (nextUrl) {
        res = await client.get(toPath(nextUrl))
        data = res.data
        all.push(...(Array.isArray(data) ? data : data.results ?? []))
        nextUrl = Array.isArray(data) ? null : (data.next ?? null)
      }

      setVehicles(all)
      setMeta({ count: all.length, next: null, previous: null })
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar vehículos')
    } finally {
      setLoading(false)
    }
  }, [])

  // Navigates to the URL returned by next/previous fields.
  // Uses toPath() to strip the origin so the Axios client's HTTPS baseURL is used,
  // avoiding the HTTP→HTTPS redirect that browsers block for CORS preflights.
  const fetchPage = useCallback(async (url) => {
    if (!url) return
    setLoading(true)
    setError(null)
    try {
      const res = await client.get(toPath(url))
      applyResponse(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar la página')
    } finally {
      setLoading(false)
    }
  }, [applyResponse])

  const createVehicle = useCallback(async (data) => {
    const res = await vehiclesApi.create(data)
    setVehicles((prev) => [res.data, ...prev])
    return res.data
  }, [])

  const updateVehicle = useCallback(async (id, data) => {
    const res = await vehiclesApi.update(id, data)
    setVehicles((prev) => prev.map((v) => (v.id === id ? res.data : v)))
    return res.data
  }, [])

  const toggleAvailability = useCallback(async (id) => {
    const res = await vehiclesApi.toggleAvailability(id)
    setVehicles((prev) => prev.map((v) => (v.id === id ? res.data : v)))
    return res.data
  }, [])

  const removeVehicle = useCallback(async (id) => {
    await vehiclesApi.remove(id)
    setVehicles((prev) => prev.filter((v) => v.id !== id))
  }, [])

  return {
    vehicles,
    meta,
    loading,
    error,
    fetchVehicles,
    fetchAll,
    searchVehicles,
    fetchPage,
    createVehicle,
    updateVehicle,
    toggleAvailability,
    removeVehicle,
  }
}
