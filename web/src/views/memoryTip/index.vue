<template>
  <div class="memory-tip-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI速记管理</span>
        </div>
      </template>
      <el-alert
        title="AI 助记模块正在开发中，该功能将在下一阶段上线"
        type="info"
        :closable="false"
        show-icon
      />
    </el-card>
  </div>
</template>

<style scoped>
.memory-tip-page { padding: 0; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
