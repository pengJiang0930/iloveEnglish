<template>
  <view class="container">
    <view class="profile-card">
      <view class="avatar">
        <text class="avatar-text">👤</text>
      </view>
      <text class="name">{{ userInfo?.nickname || '未登录' }}</text>
      <text class="level">{{ userInfo ? '零基础 → 初级' : '请先登录' }}</text>
    </view>
    
    <view class="menu-list">
      <view class="menu-item" @click="goToWordbook">
        <text class="menu-icon">📖</text>
        <text class="menu-text">我的单词本</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="goToHistory">
        <text class="menu-icon">💬</text>
        <text class="menu-text">翻译历史</text>
        <text class="menu-arrow">></text>
      </view>
      <view class="menu-item" @click="goToSettings">
        <text class="menu-icon">⚙️</text>
        <text class="menu-text">设置</text>
        <text class="menu-arrow">></text>
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

function goToWordbook() {
  uni.showToast({ title: '开发中', icon: 'none' })
}

function goToHistory() {
  uni.showToast({ title: '开发中', icon: 'none' })
}

function goToSettings() {
  uni.showToast({ title: '开发中', icon: 'none' })
}
</script>

<style scoped>
.container {
  padding: 20rpx;
}

.profile-card {
  background: linear-gradient(135deg, #4A90D9, #6BA5E7);
  border-radius: 20rpx;
  padding: 40rpx;
  color: #fff;
  text-align: center;
  margin-bottom: 30rpx;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  background: rgba(255,255,255,0.3);
  border-radius: 50%;
  margin: 0 auto 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 60rpx;
}

.name {
  font-size: 36rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 10rpx;
}

.level {
  font-size: 24rpx;
  opacity: 0.9;
}

.menu-list {
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.menu-text {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.menu-arrow {
  font-size: 28rpx;
  color: #ccc;
}
</style>
