<template>
  <div class="home">
    <h1>iLoveEnglish</h1>
    <p>AI英语学习平台</p>
    
    <div v-if="userStore.userInfo">
      <p>欢迎回来，{{ userStore.userInfo.nickname }}</p>
      <el-button @click="$router.push('/word')">开始学习</el-button>
    </div>
    
    <div v-else>
      <el-button @click="$router.push('/login')">登录</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(async () => {
  if (userStore.token) {
    try {
      await userStore.getUserInfo()
    } catch {
      userStore.logout()
    }
  }
})
</script>

<style scoped>
.home {
  text-align: center;
  padding: 40px;
}
</style>
