import api from './index'

export const authApi = {
  register(phone: string, password: string, nickname: string) {
    return api.post('/auth/register', { phone, password, nickname })
  },
  login(phone: string, password: string) {
    return api.post('/auth/login', { phone, password })
  },
  getMe() {
    return api.get('/auth/me')
  }
}
