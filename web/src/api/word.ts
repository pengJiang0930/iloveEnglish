import api from './index'

export const wordApi = {
  getWordsByBook(bookId: number, page: number = 1, pageSize: number = 20) {
    return api.get('/words/book/' + bookId, { params: { page, page_size: pageSize } })
  },
  getWordDetail(wordId: number) {
    return api.get('/words/' + wordId)
  }
}
