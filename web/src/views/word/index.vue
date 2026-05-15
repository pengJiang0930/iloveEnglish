<template>
  <div class="word-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>单词管理</span>
          <div>
            <el-button type="primary" icon="Plus">新增单词</el-button>
            <el-button type="success" icon="Upload">批量导入</el-button>
          </div>
        </div>
      </template>

      <div class="filter-bar">
        <el-select v-model="bookId" placeholder="选择词书" clearable @change="onFilterChange">
          <el-option
            v-for="book in bookList"
            :key="book.id"
            :label="book.name"
            :value="book.id"
          />
        </el-select>
        <el-select v-model="level" placeholder="难度等级" clearable style="width: 120px; margin-left: 16px;" disabled>
          <el-option label="入门" :value="1" />
          <el-option label="初级" :value="2" />
          <el-option label="中级" :value="3" />
          <el-option label="高级" :value="4" />
          <el-option label="专业" :value="5" />
        </el-select>
        <el-input v-model="keyword" placeholder="搜索单词" clearable style="width: 200px; margin: 0 16px;" disabled />
        <el-button type="primary" icon="Search" disabled>查询</el-button>
        <el-button icon="Refresh" @click="resetFilter">重置</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="word" label="单词" width="150" />
        <el-table-column prop="phonetic" label="音标" width="150" />
        <el-table-column prop="meaning_cn" label="中文释义" />
        <el-table-column prop="part_of_speech" label="词性" width="80" />
        <el-table-column prop="level" label="难度" width="80">
          <template #default="{ row }">
            <el-tag :type="getLevelType(row.level)">{{ getLevelLabel(row.level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default>
            <el-button type="primary" link icon="Edit">编辑</el-button>
            <el-button type="danger" link icon="Delete">删除</el-button>
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
          @current-change="loadWords"
          @size-change="loadWords"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { wordApi } from '@/api/word'
import { wordBookApi } from '@/api/wordBook'

const bookId = ref<number | ''>('')
const level = ref('')
const keyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)

interface WordRow {
  id: number
  word: string
  phonetic: string | null
  meaning_cn: string
  part_of_speech: string | null
  level: number
  in_word_list: boolean
}

interface BookOption {
  id: number
  name: string
}

const bookList = ref<BookOption[]>([])
const tableData = ref<WordRow[]>([])

async function loadBooks() {
  const res: any = await wordBookApi.getList()
  bookList.value = res.data || []
}

async function loadWords() {
  if (!bookId.value) {
    tableData.value = []
    total.value = 0
    return
  }
  loading.value = true
  try {
    const res: any = await wordApi.getWordsByBook(bookId.value as number, currentPage.value, pageSize.value)
    tableData.value = res.data.list || []
    total.value = res.data.total || 0
  } finally {
    loading.value = false
  }
}

function onFilterChange() {
  currentPage.value = 1
  loadWords()
}

function resetFilter() {
  bookId.value = ''
  level.value = ''
  keyword.value = ''
  currentPage.value = 1
  tableData.value = []
  total.value = 0
}

function getLevelType(level: number) {
  const map: Record<number, string> = {
    1: 'success',
    2: '',
    3: 'warning',
    4: 'danger',
    5: 'danger'
  }
  return map[level] || ''
}

function getLevelLabel(level: number) {
  const map: Record<number, string> = {
    1: '入门',
    2: '初级',
    3: '中级',
    4: '高级',
    5: '专业'
  }
  return map[level] || ''
}

onMounted(() => {
  loadBooks()
})
</script>

<style scoped>
.word-page {
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
