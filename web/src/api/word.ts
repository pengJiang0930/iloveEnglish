import api from './index'

export const wordApi = {
  getWordsByBook(bookId: number, page: number = 1, pageSize: number = 20) {
    return api.get('/words/book/' + bookId, { params: { page, page_size: pageSize } })
  },
  getWordDetail(wordId: number) {
    return api.get('/words/' + wordId)
  },
  create(data: {
    word: string
    phonetic?: string
    meaning_cn: string
    meaning_en?: string
    part_of_speech?: string
    frequency?: number
    level?: number
    example_sentence?: string
    example_translation?: string
    audio_url?: string
    book_id?: number
  }) {
    return api.post('/words/admin', data)
  },
  update(wordId: number, data: Record<string, any>) {
    return api.put('/words/admin/' + wordId, data)
  },
  delete(wordId: number) {
    return api.delete('/words/admin/' + wordId)
  }
}
