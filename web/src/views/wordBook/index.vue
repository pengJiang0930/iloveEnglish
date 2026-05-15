<template>
  <div class="word-book-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>词书管理</span>
          <el-button type="primary" icon="Plus" @click="openDialog()">新增词书</el-button>
        </div>
      </template>

      <div class="filter-bar">
        <el-select v-model="category" placeholder="选择分类" clearable @change="loadData">
          <el-option label="核心词汇" value="core" />
          <el-option label="考试词汇" value="exam" />
          <el-option label="日常词汇" value="daily" />
        </el-select>
        <el-button icon="Refresh" style="margin-left: 16px;" @click="onReset">重置</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%" v-loading="loading">
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
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link icon="Edit" @click="openDialog(row)">编辑</el-button>
            <el-button link :icon="row.status ? 'ArrowDown' : 'ArrowUp'" @click="toggleStatus(row)">
              {{ row.status ? '下架' : '上架' }}
            </el-button>
            <el-button type="danger" link icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑词书' : '新增词书'" width="520px" @closed="resetForm">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="词书名称" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="选择分类" style="width: 100%;">
            <el-option label="核心词汇" value="core" />
            <el-option label="考试词汇" value="exam" />
            <el-option label="日常词汇" value="daily" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" placeholder="词书描述" />
        </el-form-item>
        <el-form-item label="单词数">
          <el-input-number v-model="form.word_count" :min="0" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="免费">
          <el-switch v-model="form.is_free" :active-value="1" :inactive-value="0" active-text="是" inactive-text="否" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0" active-text="上架" inactive-text="下架" />
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
import { wordBookApi } from '@/api/wordBook'

const category = ref('')
const tableData = ref<any[]>([])
const loading = ref(false)

// Dialog
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const submitting = ref(false)
const formRef = ref()
const form = ref({
  name: '', description: '', category: '', word_count: 0,
  sort_order: 0, is_free: 1, status: 1
})
const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
}

async function loadData() {
  loading.value = true
  try {
    const params: any = { include_inactive: true }
    if (category.value) params.category = category.value
    const res: any = await wordBookApi.getList(params)
    tableData.value = res.data || []
  } finally {
    loading.value = false
  }
}

function onReset() { category.value = ''; loadData() }

function openDialog(row?: any) {
  if (row) {
    isEdit.value = true
    editId.value = row.id
    form.value = {
      name: row.name, description: row.description || '',
      category: row.category, word_count: row.word_count || 0,
      sort_order: 0, is_free: row.is_free, status: row.status
    }
  } else {
    isEdit.value = false
    editId.value = 0
  }
  dialogVisible.value = true
}

function resetForm() {
  form.value = {
    name: '', description: '', category: '', word_count: 0,
    sort_order: 0, is_free: 1, status: 1
  }
}

async function handleSubmit() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  try {
    if (isEdit.value) {
      await wordBookApi.update(editId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await wordBookApi.create(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch { /* error shown by interceptor */ }
  finally { submitting.value = false }
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确定要删除词书 "${row.name}" 吗？此操作不可恢复。`, '警告', { type: 'warning' })
  } catch { return }
  try {
    await wordBookApi.delete(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch { /* error shown by interceptor */ }
}

async function toggleStatus(row: any) {
  try {
    await wordBookApi.toggleStatus(row.id)
    ElMessage.success(row.status ? '已下架' : '已上架')
    loadData()
  } catch { /* error shown by interceptor */ }
}

function getCategoryType(c: string) {
  const map: Record<string, string> = { core: '', exam: 'warning', daily: 'success' }
  return map[c] || ''
}
function getCategoryLabel(c: string) {
  const map: Record<string, string> = { core: '核心', exam: '考试', daily: '日常' }
  return map[c] || c
}

onMounted(() => { loadData() })
</script>

<style scoped>
.word-book-page { padding: 0; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.filter-bar { margin-bottom: 20px; display: flex; align-items: center; }
</style>
