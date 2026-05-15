<template>
  <div class="user-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
        </div>
      </template>

      <div class="filter-bar">
        <el-input v-model="phone" placeholder="手机号" clearable style="width: 150px;" />
        <el-input v-model="nickname" placeholder="昵称" clearable style="width: 150px; margin-left: 16px;" />
        <el-select v-model="status" placeholder="状态" clearable style="width: 100px; margin-left: 16px;">
          <el-option label="正常" :value="1" />
          <el-option label="禁用" :value="0" />
        </el-select>
        <el-button type="primary" icon="Search" style="margin-left: 16px;" @click="onSearch">查询</el-button>
        <el-button icon="Refresh" @click="onReset">重置</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="nickname" label="昵称" width="120" />
        <el-table-column prop="phone" label="手机号" width="150" />
        <el-table-column prop="level" label="等级" width="80">
          <template #default="{ row }">{{ getLevelLabel(row.level) }}</template>
        </el-table-column>
        <el-table-column prop="vip_level" label="VIP" width="80">
          <template #default="{ row }">
            <el-tag :type="row.vip_level ? 'warning' : 'info'">{{ getVipLabel(row.vip_level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status ? 'success' : 'danger'">{{ row.status ? '正常' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status" type="danger" link icon="Lock" @click="toggleUser(row)">禁用</el-button>
            <el-button v-else type="success" link icon="Unlock" @click="toggleUser(row)">启用</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @current-change="loadUsers"
          @size-change="loadUsers"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '@/api/admin'

const phone = ref('')
const nickname = ref('')
const status = ref<number | ''>('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)
const tableData = ref<any[]>([])

async function loadUsers() {
  loading.value = true
  try {
    const params: any = { page: currentPage.value, page_size: pageSize.value }
    if (phone.value) params.phone = phone.value
    if (nickname.value) params.nickname = nickname.value
    if (status.value !== '') params.status = status.value
    const res: any = await adminApi.getUserList(params)
    tableData.value = res.data.list || []
    total.value = res.data.total || 0
  } finally {
    loading.value = false
  }
}

function onSearch() {
  currentPage.value = 1
  loadUsers()
}

function onReset() {
  phone.value = ''
  nickname.value = ''
  status.value = ''
  currentPage.value = 1
  loadUsers()
}

async function toggleUser(row: any) {
  const action = row.status ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确定要${action}用户 "${row.nickname}" 吗？`, '提示', { type: 'warning' })
  } catch { return }
  try {
    await adminApi.toggleUserStatus(row.id, row.status ? 'disable' : 'enable')
    ElMessage.success(`${action}成功`)
    loadUsers()
  } catch { ElMessage.error(`${action}失败`) }
}

function formatTime(t: string | null) {
  if (!t) return '-'
  return t.replace('T', ' ').substring(0, 19)
}

function getLevelLabel(level: number) {
  const map: Record<number, string> = { 1: '零基础', 2: '初级', 3: '中级', 4: '高级', 5: '精通' }
  return map[level] || ''
}

function getVipLabel(level: number) {
  const map: Record<number, string> = { 0: '免费', 1: '月度', 2: '年度', 3: '终身' }
  return map[level] || ''
}

onMounted(() => { loadUsers() })
</script>

<style scoped>
.user-page { padding: 0; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.filter-bar { margin-bottom: 20px; display: flex; align-items: center; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
