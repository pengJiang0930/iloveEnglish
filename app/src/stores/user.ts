import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(uni.getStorageSync('token') || '')
  const userInfo = ref<any>(null)

  async function login(phone: string) {
    const res: any = await authApi.login(phone)
    token.value = res.access_token
    uni.setStorageSync('token', res.access_token)
    await getUserInfo()
  }

  async function getUserInfo() {
    const res: any = await authApi.getMe()
    userInfo.value = res
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync('token')
  }

  return {
    token,
    userInfo,
    login,
    getUserInfo,
    logout
  }
})
