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
        <el-button type="primary" icon="Search" style="margin-left: 16px;">查询</el-button>
        <el-button icon="Refresh">重置</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="nickname" label="昵称" width="120" />
        <el-table-column prop="phone" label="手机号" width="150" />
        <el-table-column prop="level" label="等级" width="80">
          <template #default="{ row }">
            {{ getLevelLabel(row.level) }}
          </template>
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
        <el-table-column prop="created_at" label="注册时间" width="180" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" link icon="View">详情</el-button>
            <el-button v-if="row.status" type="danger" link icon="Lock">禁用</el-button>
            <el-button v-else type="success" link icon="Unlock">启用</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="100"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const phone = ref('')
const nickname = ref('')
const status = ref('')
const currentPage = ref(1)
const pageSize = ref(20)

const tableData = ref([
  {
    id: 1,
    nickname: '小明',
    phone: '138****8000',
    level: 2,
    vip_level: 0,
    status: 1,
    created_at: '2026-05-14 10:00:00'
  },
  {
    id: 2,
    nickname: '小红',
    phone: '139****1234',
    level: 3,
    vip_level: 1,
    status: 1,
    created_at: '2026-05-13 15:30:00'
  },
  {
    id: 3,
    nickname: '小刚',
    phone: '137****5678',
    level: 1,
    vip_level: 0,
    status: 0,
    created_at: '2026-05-12 09:15:00'
  }
])

function getLevelLabel(level: number) {
  const map: Record<number, string> = {
    1: '零基础',
    2: '初级',
    3: '中级',
    4: '高级',
    5: '精通'
  }
  return map[level] || ''
}

function getVipLabel(level: number) {
  const map: Record<number, string> = {
    0: '免费',
    1: '月度',
    2: '年度',
    3: '终身'
  }
  return map[level] || ''
}
</script>

<style scoped>
.user-page {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
