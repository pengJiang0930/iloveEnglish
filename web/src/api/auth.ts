import api from './index'

export const authApi = {
  login(phone: string) {
    return api.post('/auth/login', null, { params: { phone } })
  },
  getMe() {
    return api.get('/auth/me')
  }
}
