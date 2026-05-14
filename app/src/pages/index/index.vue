<template>
  <view class="container">
    <view class="greeting">
      <text class="title">早上好，{{ userInfo?.nickname || '同学' }} 👋</text>
      <text class="subtitle">今天也要加油学习哦</text>
    </view>
    
    <view class="stats-card">
      <text class="card-title">📊 今日学习数据</text>
      <view class="stats-row">
        <view class="stat-item">
          <text class="number">0</text>
          <text class="label">正式学习</text>
        </view>
        <view class="stat-item">
          <text class="number">0</text>
          <text class="label">额外接触</text>
        </view>
        <view class="stat-item">
          <text class="number">0</text>
          <text class="label">陌生单词</text>
        </view>
      </view>
    </view>
    
    <view class="quick-actions">
      <view class="action-card" @click="goToWord">
        <text class="icon">📖</text>
        <text class="text">继续背单词</text>
      </view>
      <view class="action-card" @click="goToSpeaking">
        <text class="icon">💬</text>
        <text class="text">说句英语</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const userInfo = ref(userStore.userInfo)

onMounted(async () => {
  if (userStore.token) {
    try {
      await userStore.getUserInfo()
      userInfo.value = userStore.userInfo
    } catch {
      userStore.logout()
    }
  }
})

function goToWord() {
  uni.switchTab({ url: '/pages/word/index' })
}

function goToSpeaking() {
  uni.switchTab({ url: '/pages/speaking/index' })
}
</script>

<style scoped>
.container {
  padding: 20rpx;
}

.greeting {
  margin-bottom: 30rpx;
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  display: block;
}

.subtitle {
  font-size: 28rpx;
  color: #999;
  display: block;
  margin-top: 8rpx;
}

.stats-card {
  background: linear-gradient(135deg, #4A90D9, #6BA5E7);
  border-radius: 20rpx;
  padding: 30rpx;
  color: #fff;
  margin-bottom: 30rpx;
}

.card-title {
  font-size: 28rpx;
  opacity: 0.9;
  display: block;
  margin-bottom: 20rpx;
}

.stats-row {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.number {
  font-size: 48rpx;
  font-weight: bold;
  display: block;
}

.label {
  font-size: 24rpx;
  opacity: 0.8;
}

.quick-actions {
  display: flex;
  gap: 20rpx;
}

.action-card {
  flex: 1;
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
}

.icon {
  font-size: 48rpx;
  display: block;
  margin-bottom: 10rpx;
}

.text {
  font-size: 28rpx;
  color: #333;
}
</style>
