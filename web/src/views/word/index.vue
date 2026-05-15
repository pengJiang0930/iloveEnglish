<template>
  <div class="word-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>单词管理</span>
          <div>
            <el-button type="primary" icon="Plus" @click="openDialog()">新增单词</el-button>
            <el-button type="success" icon="Upload" disabled>批量导入</el-button>
          </div>
        </div>
      </template>

      <div class="filter-bar">
        <el-select v-model="bookId" placeholder="选择词书" clearable @change="onFilterChange">
          <el-option v-for="book in bookList" :key="book.id" :label="book.name" :value="book.id" />
        </el-select>
        <el-button icon="Refresh" style="margin-left: 16px;" @click="resetFilter">重置</el-button>
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
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link icon="Edit" @click="openDialog(row)">编辑</el-button>
            <el-button type="danger" link icon="Delete" @click="handleDelete(row)">删除</el-button>
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑单词' : '新增单词'" width="520px" @closed="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="单词" prop="word">
          <el-input v-model="form.word" placeholder="英文单词" />
        </el-form-item>
        <el-form-item label="音标">
          <el-input v-model="form.phonetic" placeholder="如 /əˈbændən/" />
        </el-form-item>
        <el-form-item label="中文释义" prop="meaning_cn">
          <el-input v-model="form.meaning_cn" placeholder="中文释义" />
        </el-form-item>
        <el-form-item label="词性">
          <el-select v-model="form.part_of_speech" placeholder="词性" clearable>
            <el-option label="名词" value="n." />
            <el-option label="动词" value="v." />
            <el-option label="形容词" value="adj." />
            <el-option label="副词" value="adv." />
            <el-option label="介词" value="prep." />
            <el-option label="连词" value="conj." />
            <el-option label="代词" value="pron." />
          </el-select>
        </el-form-item>
        <el-form-item label="难度等级">
          <el-select v-model="form.level" placeholder="难度等级">
            <el-option label="入门 (1)" :value="1" />
            <el-option label="初级 (2)" :value="2" />
            <el-option label="中级 (3)" :value="3" />
            <el-option label="高级 (4)" :value="4" />
            <el-option label="专业 (5)" :value="5" />
          </el-select>
        </el-form-item>
        <el-form-item label="例句">
          <el-input v-model="form.example_sentence" type="textarea" placeholder="例句" />
        </el-form-item>
        <el-form-item label="例句翻译">
          <el-input v-model="form.example_translation" placeholder="例句翻译" />
        </el-form-item>
        <el-form-item label="所属词书" v-if="!isEdit">
          <el-select v-model="form.book_id" placeholder="选择词书（可选）" clearable>
            <el-option v-for="book in bookList" :key="book.id" :label="book.name" :value="book.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { wordApi } from '@/api/word'
import { wordBookApi } from '@/api/wordBook'

const bookId = ref<number | ''>('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)
const bookList = ref<{ id: number; name: string }[]>([])
const tableData = ref<any[]>([])

// Dialog
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const submitting = ref(false)
const formRef = ref()
const form = ref({
  word: '', phonetic: '', meaning_cn: '', part_of_speech: '',
  level: 1, example_sentence: '', example_translation: '', book_id: null as number | null
})
const rules = {
  word: [{ required: true, message: '请输入单词', trigger: 'blur' }],
  meaning_cn: [{ required: true, message: '请输入中文释义', trigger: 'blur' }],
}

async function loadBooks() {
  const res: any = await wordBookApi.getList({ include_inactive: true })
  bookList.value = res.data || []
}

async function loadWords() {
  if (!bookId.value) { tableData.value = []; total.value = 0; return }
  loading.value = true
  try {
    const res: any = await wordApi.getWordsByBook(bookId.value as number, currentPage.value, pageSize.value)
    tableData.value = res.data.list || []
    total.value = res.data.total || 0
  } finally { loading.value = false }
}

function onFilterChange() { currentPage.value = 1; loadWords() }
function resetFilter() { bookId.value = ''; currentPage.value = 1; tableData.value = []; total.value = 0 }

function openDialog(row?: any) {
  if (row) {
    isEdit.value = true
    editId.value = row.id
    form.value = {
      word: row.word, phonetic: row.phonetic || '', meaning_cn: row.meaning_cn,
      part_of_speech: row.part_of_speech || '', level: row.level,
      example_sentence: '', example_translation: '', book_id: null
    }
  } else {
    isEdit.value = false
    editId.value = 0
  }
  dialogVisible.value = true
}

function resetForm() {
  form.value = {
    word: '', phonetic: '', meaning_cn: '', part_of_speech: '',
    level: 1, example_sentence: '', example_translation: '', book_id: null
  }
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    if (isEdit.value) {
      await wordApi.update(editId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await wordApi.create(form.value as any)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadWords()
  } catch { /* error shown by interceptor */ }
  finally { submitting.value = false }
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确定要删除单词 "${row.word}" 吗？`, '警告', { type: 'warning' })
  } catch { return }
  try {
    await wordApi.delete(row.id)
    ElMessage.success('删除成功')
    loadWords()
  } catch { /* error shown by interceptor */ }
}

function getLevelType(level: number) {
  const map: Record<number, string> = { 1: 'success', 2: '', 3: 'warning', 4: 'danger', 5: 'danger' }
  return map[level] || ''
}
function getLevelLabel(level: number) {
  const map: Record<number, string> = { 1: '入门', 2: '初级', 3: '中级', 4: '高级', 5: '专业' }
  return map[level] || ''
}

onMounted(() => { loadBooks() })
</script>

<style scoped>
.word-page { padding: 0; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.filter-bar { margin-bottom: 20px; display: flex; align-items: center; }
.pagination { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
