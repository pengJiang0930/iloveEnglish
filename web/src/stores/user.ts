import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<any>(null)

  async function register(phone: string, password: string, nickname: string) {
    const res: any = await authApi.register(phone, password, nickname)
    token.value = res.data.token
    localStorage.setItem('token', res.data.token)
    userInfo.value = res.data.user
  }

  async function login(phone: string, password: string) {
    const res: any = await authApi.login(phone, password)
    token.value = res.data.token
    localStorage.setItem('token', res.data.token)
    userInfo.value = res.data.user
  }

  async function getUserInfo() {
    const res: any = await authApi.getMe()
    userInfo.value = res.data
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    userInfo,
    register,
    login,
    getUserInfo,
    logout
  }
})
