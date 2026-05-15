import api from './index'

export const wordBookApi = {
  getList(params?: { category?: string; include_inactive?: boolean }) {
    return api.get('/word-books', { params })
  },
  create(data: {
    name: string
    description?: string
    category: string
    word_count?: number
    cover_image?: string
    sort_order?: number
    is_free?: number
    status?: number
  }) {
    return api.post('/word-books', data)
  },
  update(bookId: number, data: Record<string, any>) {
    return api.put('/word-books/' + bookId, data)
  },
  delete(bookId: number) {
    return api.delete('/word-books/' + bookId)
  },
  toggleStatus(bookId: number) {
    return api.put('/word-books/' + bookId + '/status')
  }
}
