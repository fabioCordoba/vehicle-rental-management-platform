import client from './client'

export const proceduresApi = {
  list: (params) =>
    client.get('/api/procedures/', { params }),

  get: (id) =>
    client.get(`/api/procedures/${id}/`),

  create: (data) =>
    client.post('/api/procedures/', data),

  update: (id, data) =>
    client.patch(`/api/procedures/${id}/`, data),

  confirm: (id) =>
    client.patch(`/api/procedures/${id}/confirm/`),

  cancel: (id) =>
    client.patch(`/api/procedures/${id}/cancel/`),

  remove: (id) =>
    client.delete(`/api/procedures/${id}/`),
}
