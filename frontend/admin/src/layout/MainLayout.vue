<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="280px" class="aside">
      <div class="logo-container">
        <div class="logo-icon">
          <el-icon size="32" color="#fff"><Food /></el-icon>
        </div>
        <div class="logo-text">
          <span class="title gradient-text">颐养膳食</span>
          <span class="subtitle">社区老人餐管理系统</span>
        </div>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        class="modern-menu"
        router
        :unique-opened="true"
      >
        <el-menu-item index="/dashboard">
          <el-icon size="20"><Odometer /></el-icon>
          <span>工作台概览</span>
        </el-menu-item>
        
        <div class="menu-group-title">核心管理</div>
        <el-menu-item index="/elderly">
          <el-icon size="20"><User /></el-icon>
          <span>老人管理</span>
        </el-menu-item>
        <el-menu-item index="/members">
          <el-icon size="20"><User /></el-icon>
          <span>家属管理</span>
        </el-menu-item>
        <el-menu-item index="/delivery-staff">
          <el-icon size="20"><User /></el-icon>
          <span>跑腿管理</span>
        </el-menu-item>
        
        <div class="menu-group-title">运营调度</div>
        <el-menu-item index="/orders">
          <el-icon size="20"><List /></el-icon>
          <span>订单管理</span>
        </el-menu-item>
        <el-menu-item index="/meals">
          <el-icon size="20"><Dish /></el-icon>
          <span>餐品管理</span>
        </el-menu-item>

        <el-menu-item index="/communities">
          <el-icon size="20"><House /></el-icon>
          <span>社区管理</span>
        </el-menu-item>

        <div class="menu-group-title">服务质量</div>
        <el-menu-item index="/announcements">
          <el-icon size="20"><Bell /></el-icon>
          <span>通知管理</span>
        </el-menu-item>
        <el-menu-item index="/feedback">
          <el-icon size="20"><ChatLineRound /></el-icon>
          <span>评价管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container class="main-container">
      <el-header class="modern-header glass-effect">
        <div class="header-left">
          <div class="breadcrumb-wrapper">
            <el-breadcrumb separator-icon="ArrowRight">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
        </div>
        
        <div class="header-right">
          <div class="header-action" @click="toggleTheme">
            <el-icon size="24"><Moon v-if="!isDarkTheme" /><Sunny v-else /></el-icon>
          </div>
          <div class="header-action" @click="showNotifications = !showNotifications">
            <el-badge :value="unreadCount" type="danger" class="item">
              <el-icon size="24"><Bell /></el-icon>
            </el-badge>
            
            <!-- 通知列表下拉菜单 -->
            <div v-if="showNotifications" class="notification-dropdown">
              <div class="notification-header">
                <h3>通知中心</h3>
                <el-button size="small" link type="primary" @click="markAllAsRead">全部标为已读</el-button>
              </div>
              
              <div class="notification-list">
                <div 
                  v-for="notification in notifications" 
                  :key="notification.id"
                  class="notification-item"
                  :class="{ 'unread': !notification.read }"
                  @click="handleNotificationClick(notification)"
                >
                  <div class="notification-icon" :class="notification.type">
                    <el-icon>
                      <Van v-if="notification.type === 'delivery'" />
                      <List v-else-if="notification.type === 'order'" />
                      <Bell v-else-if="notification.type === 'system'" />
                      <Check v-else />
                    </el-icon>
                  </div>
                  <div class="notification-content">
                    <div class="notification-type-badge" :class="notification.type">
                      {{ getNotificationTypeName(notification.type) }}
                    </div>
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-message">{{ notification.message }}</div>
                    <div class="notification-time">{{ notification.time }}</div>
                  </div>
                </div>
                
                <div v-if="notifications.length === 0" class="empty-notifications">
                  暂无通知
                </div>
              </div>
              

            </div>
          </div>
          <el-divider direction="vertical" />
          <el-dropdown trigger="click">
            <div class="user-profile">
              <el-avatar :size="40" :style="{ backgroundColor: '#4ecdc4' }">
                管
              </el-avatar>
              <div class="user-info">
                <span class="name">管理员</span>
                <span class="role">超级管理员</span>
              </div>
              <el-icon size="16"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/profile')"><el-icon><User /></el-icon>个人中心</el-dropdown-item>
                <el-dropdown-item @click="$router.push('/settings')"><el-icon><Setting /></el-icon>系统设置</el-dropdown-item>
                <el-dropdown-item divided type="danger" @click="handleLogout"><el-icon><SwitchButton /></el-icon>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="modern-main">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Food, Odometer, User, UserFilled, List, Dish, Van, House, Bell, ChatLineRound, Moon, Sunny, ArrowDown, Setting, SwitchButton, Warning, Check } from '@element-plus/icons-vue'
import { adminService } from '../api/admin'

const route = useRoute()
const router = useRouter()
const activeMenu = computed(() => route.path)

// 主题管理
const isDarkTheme = ref(false)

// 通知管理
const showNotifications = ref(false)
const notifications = ref([])

// 计算未读通知数量
const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

// 加载通知数据 - 只监听exception表
const loadNotifications = async () => {
  try {
    const notificationItems = []
    
    // 获取配送异常通知（从exceptions表）
    try {
      const exceptionResponse = await adminService.getExceptions({ limit: 10 })
      if (exceptionResponse && exceptionResponse.items) {
        exceptionResponse.items.forEach(exception => {
          const timeText = formatRelativeTime(exception.created_at)
          let exceptionTypeName = ''
          switch (exception.type) {
            case 'elderly_not_home':
              exceptionTypeName = '老人不在家'
              break
            case 'address_error':
              exceptionTypeName = '地址错误'
              break
            case 'meal_problem':
              exceptionTypeName = '餐品问题'
              break
            default:
              exceptionTypeName = '其他问题'
          }
          notificationItems.push({
            id: `exception-${exception.id}`,
            title: '配送异常通知',
            message: `配送员报告：${exceptionTypeName} - ${exception.description}`,
            time: timeText,
            type: 'delivery',
            read: false,
            originalData: exception
          })
        })
      }
    } catch (error) {
      console.error('获取配送异常失败:', error)
    }
    
    notifications.value = notificationItems
  } catch (error) {
    console.error('加载通知失败:', error)
  }
}

// 格式化相对时间
const formatRelativeTime = (timestamp) => {
  const createdTime = new Date(timestamp)
  const now = new Date()
  const diffMs = now - createdTime
  const diffMinutes = Math.floor(diffMs / 60000)
  if (diffMinutes < 1) return '刚刚'
  else if (diffMinutes < 60) return `${diffMinutes}分钟前`
  else if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}小时前`
  else return `${Math.floor(diffMinutes / 1440)}天前`
}

// 标记全部已读（这里不需要实际调用API，因为没有单独的通知表）
const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
}

// 获取通知类型名称
const getNotificationTypeName = (type) => {
  const typeMap = {
    'delivery': '配送通知',
    'order': '订单通知',
    'system': '系统通知',
    'success': '用户操作'
  }
  return typeMap[type] || '通知'
}

// 处理通知点击
const handleNotificationClick = (notification) => {
  notification.read = true
  
  // 根据通知类型跳转到相应页面
  if (notification.type === 'delivery') {
    router.push('/delivery')
  } else if (notification.type === 'order') {
    router.push('/orders')
  } else if (notification.type === 'success') {
    router.push('/feedback')
  }
}

// 初始化主题和加载通知
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    enableDarkTheme()
  } else {
    disableDarkTheme()
  }
  
  // 加载通知数据
  loadNotifications()
})

// 切换主题
const toggleTheme = () => {
  if (isDarkTheme.value) {
    disableDarkTheme()
  } else {
    enableDarkTheme()
  }
}

// 启用深色主题
const enableDarkTheme = () => {
  document.documentElement.setAttribute('data-theme', 'dark')
  localStorage.setItem('theme', 'dark')
  isDarkTheme.value = true
}

// 禁用深色主题
const disableDarkTheme = () => {
  document.documentElement.removeAttribute('data-theme')
  localStorage.setItem('theme', 'light')
  isDarkTheme.value = false
}

// 退出登录
const handleLogout = () => {
  // 清除本地存储的token和用户信息
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  
  // 跳转到登录页面
  router.push('/login')
}

const currentRouteName = computed(() => {
  const names = {
    '/dashboard': '工作台概览',
    '/elderly': '老人管理',
    '/members': '家属管理',
    '/delivery-staff': '跑腿管理',
    '/meals': '餐品管理',
    '/orders': '订单管理',
    '/communities': '社区管理',
    '/announcements': '通知管理',
    '/feedback': '评价管理',
    '/settings': '系统设置',
    '/profile': '个人中心'
  }
  return names[route.path] || '首页'
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background-color: var(--bg-primary);
  overflow: hidden;
}

/* 侧边栏样式 */
.aside {
  background: var(--bg-secondary) !important;
  display: flex;
  flex-direction: column;
  padding: var(--spacing-lg) var(--spacing-md);
  box-sizing: border-box;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
  border-right: 1px solid var(--border-color);
  z-index: 10;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: 0 var(--spacing-md) var(--spacing-xl);
  position: relative;
  z-index: 1;
}

.logo-icon {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
  animation: float 4s ease-in-out infinite;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-text .title {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: 2px;
}

.logo-text .subtitle {
  font-size: 11px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.modern-menu {
  border-right: none !important;
  flex: 1;
  position: relative;
  z-index: 1;
  background-color: var(--bg-secondary) !important;
  --el-menu-bg-color: var(--bg-secondary);
  --el-menu-border-color: transparent;
}

:deep(.el-menu) {
  background-color: var(--bg-secondary) !important;
  border-right: none !important;
}

.menu-group-title {
  font-size: 11px;
  color: var(--text-muted);
  padding: var(--spacing-lg) var(--spacing-lg) var(--spacing-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

:deep(.el-menu-item) {
  height: 56px !important;
  line-height: 56px !important;
  margin: var(--spacing-xs) var(--spacing-md) !important;
  border-radius: var(--radius-lg) !important;
  color: var(--text-secondary) !important;
  font-weight: 600;
  transition: all var(--transition-normal) !important;
  background: rgba(99, 102, 241, 0.05) !important;
  border: 1px solid rgba(99, 102, 241, 0.1);
}

[data-theme="dark"] :deep(.el-menu-item) {
  background: rgba(255, 255, 255, 0.04) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1)) !important;
  color: var(--primary-light) !important;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
  transform: translateX(8px);
}

:deep(.el-menu-item:hover) {
  background: rgba(99, 102, 241, 0.12) !important;
  color: var(--text-primary) !important;
  transform: translateX(4px);
}

:deep(.el-menu-item .el-icon) {
  font-size: 20px !important;
  margin-right: var(--spacing-md) !important;
}

.aside-footer {
  padding: var(--spacing-lg) var(--spacing-md) 0;
  position: relative;
  z-index: 1;
}

.help-card {
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.help-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* 顶部 Header 样式 */
.modern-header {
  height: 80px !important;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-xl);
  border-bottom: 1px solid var(--border-color);
  position: relative;
  z-index: 100;
}

.header-left {
  flex: 1;
}

.breadcrumb-wrapper {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-lg);
  background: rgba(99, 102, 241, 0.05);
  backdrop-filter: blur(10px);
}

:deep(.el-breadcrumb__item) {
  font-size: 14px;
}

:deep(.el-breadcrumb__inner) {
  color: var(--text-secondary) !important;
  font-weight: 500;
}

:deep(.el-breadcrumb__inner.is-link) {
  color: var(--primary-color) !important;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.header-action {
  cursor: pointer;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  padding: var(--spacing-sm);
  border-radius: var(--radius-lg);
}

.header-action:hover {
  color: var(--primary-color);
  background: rgba(99, 102, 241, 0.1);
  transform: scale(1.1);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  cursor: pointer;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-xl);
  transition: all var(--transition-normal);
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
}

.user-profile:hover {
  background: var(--glass-bg);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-info .name {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.user-info .role {
  font-size: 12px;
  color: var(--text-muted);
}

/* 通知下拉菜单样式 */
.notification-dropdown {
  position: absolute;
  top: 60px;
  right: 0;
  width: 350px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  z-index: 1000;
  max-height: 500px;
  overflow-y: auto;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.notification-list {
  padding: var(--spacing-sm);
}

.notification-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
  margin-bottom: var(--spacing-sm);
}

.notification-item:hover {
  background: rgba(99, 102, 241, 0.1);
}

.notification-item.unread {
  background: rgba(99, 102, 241, 0.05);
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
}

.notification-icon.delivery {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
}

.notification-icon.order {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.notification-icon.system {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary-color);
}

.notification-icon.success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--secondary-color);
}

.notification-type-badge {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 16px;
  font-weight: 600;
  display: inline-block;
  margin-bottom: 8px;
}

.notification-type-badge.delivery {
  background: #ec4899;
  color: white;
}

.notification-type-badge.order {
  background: #f59e0b;
  color: white;
}

.notification-type-badge.system {
  background: var(--primary-color);
  color: white;
}

.notification-type-badge.success {
  background: var(--secondary-color);
  color: white;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  font-size: 14px;
}

.notification-message {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notification-time {
  color: var(--text-muted);
  font-size: 12px;
}

.empty-notifications {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--text-muted);
}



.modern-main {
  padding: var(--spacing-xl);
  overflow-x: hidden;
  height: calc(100vh - 80px);
  overflow-y: auto;
}
</style>
