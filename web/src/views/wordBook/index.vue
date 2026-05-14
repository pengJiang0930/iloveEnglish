<template>
  <div class="word-book-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>词书管理</span>
          <el-button type="primary" icon="Plus">新增词书</el-button>
        </div>
      </template>
      
      <div class="filter-bar">
        <el-select v-model="category" placeholder="选择分类" clearable>
          <el-option label="核心词汇" value="core" />
          <el-option label="考试词汇" value="exam" />
          <el-option label="日常词汇" value="daily" />
        </el-select>
        <el-input v-model="keyword" placeholder="搜索词书" clearable style="width: 200px; margin: 0 16px;" />
        <el-button type="primary" icon="Search">查询</el-button>
        <el-button icon="Refresh">重置</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="category" label="分类" width="100">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category)">{{ getCategoryLabel(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="word_count" label="单词数" width="100" />
        <el-table-column prop="is_free" label="免费" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_free ? 'success' : 'danger'">{{ row.is_free ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status ? 'success' : 'info'">{{ row.status ? '上架' : '下架' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default>
            <el-button type="primary" link icon="Edit">编辑</el-button>
            <el-button type="danger" link icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const category = ref('')
const keyword = ref('')

const tableData = ref([
  {
    id: 1,
    name: '高频核心1000词',
    category: 'core',
    word_count: 1000,
    is_free: 1,
    status: 1
  },
  {
    id: 2,
    name: '四级核心词汇',
    category: 'exam',
    word_count: 2000,
    is_free: 1,
    status: 1
  }
])

function getCategoryType(category: string) {
  const map: Record<string, string> = {
    core: '',
    exam: 'warning',
    daily: 'success'
  }
  return map[category] || ''
}

function getCategoryLabel(category: string) {
  const map: Record<string, string> = {
    core: '核心',
    exam: '考试',
    daily: '日常'
  }
  return map[category] || category
}
</script>

<style scoped>
.word-book-page {
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
</style>
