import client from './client'

export const usersApi = {
  list: (params) =>
    client.get('/api/users/', { params }),

  search: (field, value) =>
    client.get('/api/users/search/', { params: { field, value } }),

  get: (id) =>
    client.get(`/api/users/${id}/`),

  create: (data) =>
    client.post('/api/users/', data),

  update: (id, data) =>
    client.patch(`/api/users/${id}/`, data),

  remove: (id) =>
    client.delete(`/api/users/${id}/`),

  roles: () =>
    client.get('/api/authentication/roles/'),
}
