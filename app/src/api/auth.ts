import { request } from './index'

export const authApi = {
  login(phone: string) {
    return request({
      url: '/auth/login',
      method: 'POST',
      data: null,
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  getMe() {
    return request({
      url: '/auth/me'
    })
  }
}
