<template>
  <div class="login">
    <h2>登录</h2>
    <el-form @submit.prevent="handleLogin">
      <el-form-item>
        <el-input
          v-model="phone"
          placeholder="请输入手机号"
          prefix-icon="Phone"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleLogin"
          style="width: 100%"
        >
          登录
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const phone = ref('13800138000')
const loading = ref(false)

async function handleLogin() {
  if (!phone.value) {
    ElMessage.warning('请输入手机号')
    return
  }
  
  loading.value = true
  try {
    await userStore.login(phone.value)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
}
</style>
