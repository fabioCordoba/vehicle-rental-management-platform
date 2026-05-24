import client from './client'

export const authApi = {
  login: (email, password) =>
    client.post('/api/authentication/login/', { email, password }),

  register: (data) =>
    client.post('/api/authentication/register', data),

  me: () =>
    client.get('/api/authentication/me'),

  updateMe: (data) =>
    client.put('/api/authentication/me', data),

  changePassword: (data) =>
    client.post('/api/authentication/change_pwd/', data),

  forgotPassword: (email) =>
    client.post('/api/authentication/forgot_password/', { email }),

  checkToken: () =>
    client.get('/api/authentication/check-token/'),

  refresh: (refresh) =>
    client.post('/api/authentication/refresh/', { refresh }),

  logout: (refresh) =>
    client.post('/api/authentication/logout/', { refresh }),

  logoutAll: () =>
    client.post('/api/authentication/logout_all/'),
}
