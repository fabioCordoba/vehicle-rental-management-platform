import client from './client'

export const vehiclesApi = {
  list: (params) =>
    client.get('/api/transports/', { params }),

  available: (params) =>
    client.get('/api/transports/available/', { params }),

  search: (params) =>
    client.get('/api/transports/search/', { params }),

  get: (id) =>
    client.get(`/api/transports/${id}/`),

  create: (data) =>
    client.post('/api/transports/', data),

  update: (id, data) =>
    client.patch(`/api/transports/${id}/`, data),

  toggleAvailability: (id) =>
    client.patch(`/api/transports/${id}/toggle-availability/`),

  remove: (id) =>
    client.delete(`/api/transports/${id}/`),

  searchByStatus: (status) =>
    client.get('/api/transports/search-by-status/', { params: { status } }),
}
