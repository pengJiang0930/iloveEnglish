import api from './index'

export const wordBookApi = {
  // Admin: get all word books (including inactive) for management
  getList(params?: { category?: string }) {
    return api.get('/word-books', { params })
  }
}
