<template>
  <div class="memory-tip-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI速记管理</span>
          <el-button type="warning" icon="Clock">待审核列表</el-button>
        </div>
      </template>
      
      <div class="filter-bar">
        <el-select v-model="tipType" placeholder="速记类型" clearable>
          <el-option label="谐音法" value="phonetic" />
          <el-option label="拆词法" value="split" />
          <el-option label="联想法" value="association" />
          <el-option label="故事法" value="story" />
          <el-option label="词根词缀法" value="root" />
        </el-select>
        <el-select v-model="status" placeholder="审核状态" clearable style="width: 120px; margin-left: 16px;">
          <el-option label="待审核" :value="0" />
          <el-option label="已审核" :value="1" />
        </el-select>
        <el-input v-model="keyword" placeholder="搜索单词" clearable style="width: 200px; margin: 0 16px;" />
        <el-button type="primary" icon="Search">查询</el-button>
        <el-button icon="Refresh">重置</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="word" label="单词" width="120" />
        <el-table-column prop="tip_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.tip_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="内容" show-overflow-tooltip />
        <el-table-column prop="like_count" label="点赞" width="80" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status ? 'success' : 'warning'">{{ row.status ? '已审' : '待审' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button v-if="!row.status" type="success" link icon="Check">审核</el-button>
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
          :total="100"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const tipType = ref('')
const status = ref('')
const keyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)

const tableData = ref([
  {
    id: 1,
    word: 'abandon',
    tip_type: 'split',
    content: 'a + band + on：一个乐队在上面演奏，被放弃了',
    like_count: 10,
    status: 1
  },
  {
    id: 2,
    word: 'ability',
    tip_type: 'phonetic',
    content: '谐音：一个笨蛋，被抛弃了',
    like_count: 5,
    status: 0
  }
])

function getTypeLabel(type: string) {
  const map: Record<string, string> = {
    phonetic: '谐音法',
    split: '拆词法',
    association: '联想法',
    story: '故事法',
    root: '词根词缀法'
  }
  return map[type] || type
}
</script>

<style scoped>
.memory-tip-page {
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
