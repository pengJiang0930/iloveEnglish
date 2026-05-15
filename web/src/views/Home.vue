<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>词书数量</span>
              <el-icon><Collection /></el-icon>
            </div>
          </template>
          <div class="stat-value">{{ stats.book_count }}</div>
          <div class="stat-label">本词书</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>单词总数</span>
              <el-icon><Document /></el-icon>
            </div>
          </template>
          <div class="stat-value">{{ stats.word_count }}</div>
          <div class="stat-label">个单词</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户数量</span>
              <el-icon><User /></el-icon>
            </div>
          </template>
          <div class="stat-value">{{ stats.user_count }}</div>
          <div class="stat-label">位用户</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" icon="Plus" @click="$router.push('/word-book')">新增词书</el-button>
            <el-button type="success" icon="Upload" @click="$router.push('/word')">导入单词</el-button>
            <el-button type="warning" icon="MagicStick" @click="$router.push('/memory-tip')">审核速记</el-button>
            <el-button icon="User" @click="$router.push('/user')">用户管理</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统信息</span>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="系统版本">v1.0.0</el-descriptions-item>
            <el-descriptions-item label="后端状态">
              <el-tag :type="healthStatus === 'healthy' ? 'success' : 'danger'">
                {{ healthStatus === 'healthy' ? '运行中' : '异常' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="数据库状态">
              <el-tag :type="dbStatus === 'connected' ? 'success' : 'danger'">
                {{ dbStatus === 'connected' ? '已连接' : '断开' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="当前用户">{{ userStore.userInfo?.nickname || '管理员' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { adminApi } from '@/api/admin'
import { Collection, Document, User, MagicStick } from '@element-plus/icons-vue'
import api from '@/api/index'

const userStore = useUserStore()
const healthStatus = ref('')
const dbStatus = ref('')
const stats = ref({ book_count: 0, word_count: 0, user_count: 0 })

onMounted(async () => {
  if (userStore.token) {
    try { await userStore.getUserInfo() } catch { userStore.logout() }
  }
  try {
    const h: any = await api.get('/health')
    healthStatus.value = h.status || 'error'
    dbStatus.value = h.database || 'error'
  } catch { healthStatus.value = 'error'; dbStatus.value = 'error' }
  try {
    const r: any = await adminApi.getDashboard()
    if (r.data) stats.value = r.data
  } catch { /* keep defaults */ }
})
</script>

<style scoped>
.home { padding: 0; }
.stat-card { height: 100%; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.stat-value { font-size: 32px; font-weight: bold; color: #409eff; text-align: center; }
.stat-label { text-align: center; color: #909399; font-size: 14px; margin-top: 8px; }
.quick-actions { display: flex; flex-wrap: wrap; gap: 12px; }
</style>
