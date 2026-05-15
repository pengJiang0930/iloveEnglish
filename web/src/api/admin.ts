import api from './index'

export const adminApi = {
  getDashboard() {
    return api.get('/admin/dashboard')
  },
  getUserList(params?: {
    phone?: string
    nickname?: string
    status?: number
    page?: number
    page_size?: number
  }) {
    return api.get('/admin/users', { params })
  },
  toggleUserStatus(userId: number, action: string) {
    return api.put('/admin/users/' + userId + '/status', { action })
  }
}
