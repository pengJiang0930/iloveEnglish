<template>
  <div class="register">
    <h2>注册</h2>
    <el-form @submit.prevent="handleRegister">
      <el-form-item>
        <el-input
          v-model="phone"
          placeholder="请输入手机号"
          prefix-icon="Phone"
        />
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="password"
          type="password"
          placeholder="请输入密码（至少6位）"
          prefix-icon="Lock"
          show-password
        />
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="confirmPassword"
          type="password"
          placeholder="请确认密码"
          prefix-icon="Lock"
          show-password
        />
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="nickname"
          placeholder="请输入昵称（选填）"
          prefix-icon="User"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleRegister"
          style="width: 100%"
        >
          注册
        </el-button>
      </el-form-item>
      <el-form-item>
        <div class="links">
          <router-link to="/login">已有账号？立即登录</router-link>
        </div>
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

const phone = ref('')
const password = ref('')
const confirmPassword = ref('')
const nickname = ref('')
const loading = ref(false)

async function handleRegister() {
  if (!phone.value) {
    ElMessage.warning('请输入手机号')
    return
  }
  if (!password.value) {
    ElMessage.warning('请输入密码')
    return
  }
  if (password.value.length < 6) {
    ElMessage.warning('密码长度不能少于6位')
    return
  }
  if (password.value !== confirmPassword.value) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  loading.value = true
  try {
    await userStore.register(phone.value, password.value, nickname.value)
    ElMessage.success('注册成功')
    router.push('/')
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
}

.links {
  text-align: center;
  width: 100%;
}

.links a {
  color: #409eff;
  text-decoration: none;
}

.links a:hover {
  text-decoration: underline;
}
</style>
