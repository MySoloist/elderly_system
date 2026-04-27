<template>
  <div class="profile">
    <!-- 欢迎栏 -->
    <div class="welcome-bar">
      <div class="welcome-text">
        <h1 class="welcome-title">个人中心</h1>
        <p class="welcome-subtitle">管理您的个人信息和账户设置</p>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <template v-else>
      <el-row :gutter="24">
        <!-- 个人信息卡片 -->
        <el-col :span="8">
          <el-card class="profile-card">
            <template #header>
              <div class="card-header">
                <el-icon size="20"><UserFilled /></el-icon>
                <span class="title">个人信息</span>
              </div>
            </template>
            
            <div class="profile-info">
              <div class="avatar-section">
                <el-avatar :size="80" class="avatar">
                  {{ currentUser?.username?.charAt(0)?.toUpperCase() || '管' }}
                </el-avatar>
                <div class="user-info">
                  <h3 class="username">{{ currentUser?.username || '管理员' }}</h3>
                  <p class="user-type">{{ currentUser?.user_type === 'admin' ? '超级管理员' : '普通管理员' }}</p>
                </div>
              </div>
              
              <div class="info-details">
                <div class="info-item">
                  <span class="info-label">用户名</span>
                  <span class="info-value">{{ currentUser?.username || '管理员' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">邮箱</span>
                  <span class="info-value">{{ currentUser?.email || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">手机号</span>
                  <span class="info-value">{{ currentUser?.phone || '未设置' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">创建时间</span>
                  <span class="info-value">{{ formatDate(currentUser?.created_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">最后登录</span>
                  <span class="info-value">{{ formatDate(currentUser?.last_login) }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 个人信息编辑 -->
        <el-col :span="16">
          <el-card class="profile-card">
            <template #header>
              <div class="card-header">
                <el-icon size="20"><Edit /></el-icon>
                <span class="title">编辑个人信息</span>
              </div>
            </template>
            
            <el-form :model="editForm" label-width="120px">
              <el-form-item label="用户名">
                <el-input v-model="editForm.username" placeholder="请输入用户名" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="editForm.email" type="email" placeholder="请输入邮箱" />
              </el-form-item>
              <el-form-item label="手机号">
                <el-input v-model="editForm.phone" placeholder="请输入手机号" />
              </el-form-item>
              <el-form-item label="姓名">
                <el-input v-model="editForm.name" placeholder="请输入真实姓名" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveProfile">
                  <el-icon><Check /></el-icon>保存信息
                </el-button>
                <el-button @click="resetForm">取消</el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 修改密码 -->
          <el-card class="profile-card" style="margin-top: 24px">
            <template #header>
              <div class="card-header">
                <el-icon size="20"><Lock /></el-icon>
                <span class="title">修改密码</span>
              </div>
            </template>
            
            <el-form :model="passwordForm" label-width="120px">
              <el-form-item label="当前密码">
                <el-input v-model="passwordForm.currentPassword" type="password" placeholder="请输入当前密码" />
              </el-form-item>
              <el-form-item label="新密码">
                <el-input v-model="passwordForm.newPassword" type="password" placeholder="请输入新密码" />
              </el-form-item>
              <el-form-item label="确认新密码">
                <el-input v-model="passwordForm.confirmPassword" type="password" placeholder="请再次输入新密码" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="changePassword">
                  <el-icon><RefreshRight /></el-icon>修改密码
                </el-button>
                <el-button @click="resetPasswordForm">取消</el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- 安全设置 -->
          <el-card class="profile-card" style="margin-top: 24px">
            <template #header>
              <div class="card-header">
                <el-icon size="20"><Warning /></el-icon>
                <span class="title">安全设置</span>
              </div>
            </template>
            
            <el-form :model="securityForm" label-width="120px">
              <el-form-item label="双因素认证">
                <el-switch
                  v-model="securityForm.twoFactorAuth"
                  active-text="启用"
                  inactive-text="禁用"
                />
                <span class="form-tip">启用后登录需要验证码验证</span>
              </el-form-item>
              <el-form-item label="登录通知">
                <el-switch
                  v-model="securityForm.loginNotification"
                  active-text="启用"
                  inactive-text="禁用"
                />
                <span class="form-tip">登录时发送通知到邮箱</span>
              </el-form-item>
              <el-form-item label="异地登录提醒">
                <el-switch
                  v-model="securityForm.remoteLoginAlert"
                  active-text="启用"
                  inactive-text="禁用"
                />
                <span class="form-tip">异地登录时发送提醒</span>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveSecuritySettings">
                  <el-icon><Check /></el-icon>保存设置
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>

      <!-- 操作成功提示 -->
      <el-message
        v-if="showSuccessMessage"
        type="success"
        :message="successMessage"
        :duration="3000"
        @close="showSuccessMessage = false"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  UserFilled, Edit, Check, Lock, RefreshRight, Warning
} from '@element-plus/icons-vue'
import { adminService } from '../api/admin'

// 当前用户信息
const currentUser = ref({
  username: '管理员',
  user_type: 'admin',
  email: '',
  phone: '',
  name: '',
  created_at: '',
  last_login: ''
})

// 编辑表单
const editForm = ref({
  username: '',
  email: '',
  phone: '',
  name: ''
})

// 密码表单
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 安全设置表单
const securityForm = ref({
  twoFactorAuth: false,
  loginNotification: true,
  remoteLoginAlert: true
})

// 消息提示
const showSuccessMessage = ref(false)
const successMessage = ref('')

// 加载状态
const loading = ref(false)

// 方法
const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadProfile = async () => {
  loading.value = true
  try {
    const data = await adminService.getProfile()
    console.log('API返回的数据:', data)
    if (data) {
      currentUser.value = data
    }
    
    // 初始化表单数据
    editForm.value = { ...currentUser.value }
  } catch (error) {
    console.error('加载个人信息失败:', error)
    // 即使API调用失败，也显示默认内容
  } finally {
    loading.value = false
  }
}

const saveProfile = async () => {
  try {
    await adminService.updateProfile(editForm.value)
    
    // 更新当前用户信息
    Object.assign(currentUser.value, editForm.value)
    
    successMessage.value = '个人信息更新成功！'
    showSuccessMessage.value = true
  } catch (error) {
    console.error('保存个人信息失败:', error)
    successMessage.value = '保存失败，请重试'
    showSuccessMessage.value = true
  }
}

const changePassword = async () => {
  try {
    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
      successMessage.value = '两次输入的密码不一致'
      showSuccessMessage.value = true
      return
    }
    
    // 转换为后端期望的字段名格式
    const passwordData = {
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword
    }
    
    await adminService.changePassword(passwordData)
    
    successMessage.value = '密码修改成功！'
    showSuccessMessage.value = true
    resetPasswordForm()
  } catch (error) {
    console.error('修改密码失败:', error)
    successMessage.value = '密码修改失败，请检查当前密码是否正确'
    showSuccessMessage.value = true
  }
}

const saveSecuritySettings = async () => {
  try {
    // 转换为后端期望的字段名格式
    const securityData = {
      two_factor_auth: securityForm.value.twoFactorAuth,
      login_notification: securityForm.value.loginNotification,
      remote_login_alert: securityForm.value.remoteLoginAlert
    }
    
    await adminService.updateSecuritySettings(securityData)
    
    successMessage.value = '安全设置保存成功！'
    showSuccessMessage.value = true
  } catch (error) {
    console.error('保存安全设置失败:', error)
    successMessage.value = '保存失败，请重试'
    showSuccessMessage.value = true
  }
}

const resetForm = () => {
  editForm.value = { ...currentUser.value }
}

const resetPasswordForm = () => {
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}

onMounted(() => {
  // 加载个人信息
  loadProfile()
})
</script>

<style scoped>
.profile {
  padding: var(--spacing-xl);
}

.loading-container {
  padding: var(--spacing-xl);
}

.loading-container .el-skeleton {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
}

.profile-card {
  margin-bottom: var(--spacing-lg);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: 600;
}

.card-header .title {
  font-size: 16px;
  font-weight: 700;
}

.profile-info {
  padding: var(--spacing-md);
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: var(--spacing-lg);
}

.avatar {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  color: #fff;
  font-size: 32px;
  font-weight: 700;
}

.user-info {
  flex: 1;
}

.username {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: var(--spacing-xs);
}

.user-type {
  color: var(--text-secondary);
  font-size: 14px;
}

.info-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm) 0;
}

.info-label {
  color: var(--text-secondary);
}

.info-value {
  font-weight: 600;
  color: var(--text-primary);
}

.form-tip {
  margin-left: var(--spacing-md);
  color: var(--text-secondary);
  font-size: 12px;
}
</style>
