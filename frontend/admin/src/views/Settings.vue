<template>
  <div class="settings">
    <!-- 欢迎栏 -->
    <div class="welcome-bar">
      <div class="welcome-text">
        <h1 class="welcome-title">系统设置</h1>
        <p class="welcome-subtitle">管理系统配置和参数设置</p>
      </div>
      <div class="welcome-action">
        <el-button type="primary" size="large" class="welcome-button" @click="saveAllSettings">
          <el-icon><Check /></el-icon>保存设置
        </el-button>
      </div>
    </div>

    <el-row :gutter="24">
      <!-- 基本设置 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon size="20"><Setting /></el-icon>
              <span class="title">基本设置</span>
            </div>
          </template>
          <el-form :model="basicSettings" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" placeholder="请输入系统名称" />
            </el-form-item>
            <el-form-item label="系统描述">
              <el-input
                v-model="basicSettings.systemDescription"
                type="textarea"
                :rows="3"
                placeholder="请输入系统描述"
              />
            </el-form-item>
            <el-form-item label="联系邮箱">
              <el-input v-model="basicSettings.contactEmail" placeholder="请输入联系邮箱" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="basicSettings.contactPhone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="系统语言">
              <el-select v-model="basicSettings.language" placeholder="请选择语言">
                <el-option label="中文" value="zh-CN" />
                <el-option label="英文" value="en-US" />
              </el-select>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 通知设置 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon size="20"><Bell /></el-icon>
              <span class="title">通知设置</span>
            </div>
          </template>
          <el-form :model="notificationSettings" label-width="120px">
            <el-form-item label="邮件通知">
              <el-switch
                v-model="notificationSettings.emailEnabled"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
            <el-form-item label="短信通知">
              <el-switch
                v-model="notificationSettings.smsEnabled"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
            <el-form-item label="系统通知">
              <el-switch
                v-model="notificationSettings.systemEnabled"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
            <el-form-item label="订单通知">
              <el-switch
                v-model="notificationSettings.orderEnabled"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
            <el-form-item label="配送通知">
              <el-switch
                v-model="notificationSettings.deliveryEnabled"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px">
      <!-- 安全设置 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon size="20"><Lock /></el-icon>
              <span class="title">安全设置</span>
            </div>
          </template>
          <el-form :model="securitySettings" label-width="120px">
            <el-form-item label="密码强度">
              <el-select v-model="securitySettings.passwordStrength" placeholder="请选择密码强度">
                <el-option label="弱" value="weak" />
                <el-option label="中" value="medium" />
                <el-option label="强" value="strong" />
              </el-select>
            </el-form-item>
            <el-form-item label="密码有效期">
              <el-input-number
                v-model="securitySettings.passwordExpiryDays"
                :min="0"
                :max="365"
                placeholder="天数"
              />
              <span style="margin-left: 10px;">天</span>
            </el-form-item>
            <el-form-item label="登录失败限制">
              <el-input-number
                v-model="securitySettings.loginAttempts"
                :min="0"
                :max="10"
                placeholder="次数"
              />
              <span style="margin-left: 10px;">次</span>
            </el-form-item>
            <el-form-item label="登录超时">
              <el-input-number
                v-model="securitySettings.sessionTimeout"
                :min="5"
                :max="120"
                placeholder="分钟"
              />
              <span style="margin-left: 10px;">分钟</span>
            </el-form-item>
            <el-form-item label="双因素认证">
              <el-switch
                v-model="securitySettings.twoFactorAuth"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- AI设置 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon size="20"><Cpu /></el-icon>
              <span class="title">AI设置</span>
            </div>
          </template>
          <el-form :model="aiSettings" label-width="120px">
            <el-form-item label="聊天大模型">
              <el-select v-model="aiSettings.chatModel" placeholder="请选择聊天大模型" :loading="loadingModels">
                <el-option 
                  v-for="model in availableModels" 
                  :key="model.value" 
                  :label="model.label" 
                  :value="model.value" 
                />
              </el-select>
            </el-form-item>
            <el-form-item label="老人端聊天大模型">
              <el-select v-model="aiSettings.elderlyChatModel" placeholder="请选择老人端聊天大模型" :loading="loadingModels">
                <el-option 
                  v-for="model in availableModels" 
                  :key="model.value" 
                  :label="model.label" 
                  :value="model.value" 
                />
              </el-select>
            </el-form-item>
            <el-form-item label="审核评价与反馈大模型">
              <el-select v-model="aiSettings.reviewModel" placeholder="请选择审核大模型" :loading="loadingModels">
                <el-option 
                  v-for="model in availableModels" 
                  :key="model.value" 
                  :label="model.label" 
                  :value="model.value" 
                />
              </el-select>
            </el-form-item>
            <el-form-item label="API地址">
              <el-input v-model="aiSettings.apiUrl" placeholder="请输入API地址" />
            </el-form-item>
            <el-form-item label="API Key">
              <el-input v-model="aiSettings.apiKey" type="password" placeholder="请输入API密钥" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 数据备份 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon size="20"><Download /></el-icon>
              <span class="title">数据备份</span>
            </div>
          </template>
          <div class="backup-section">
            <div class="backup-info">
              <div class="info-item">
                <span class="info-label">上次备份时间：</span>
                <span class="info-value">{{ lastBackupTime }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">备份文件大小：</span>
                <span class="info-value">{{ backupSize }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">备份保留数量：</span>
                <span class="info-value">{{ backupRetention }}</span>
              </div>
            </div>
            <div class="backup-actions">
              <el-button type="primary" @click="performBackup" :loading="backupLoading">
                <el-icon><Download /></el-icon>立即备份
              </el-button>
            </div>
            
            <!-- 备份列表 -->
            <div class="backup-list" v-if="backupList.length > 0">
              <h4>备份文件列表</h4>
              <el-table :data="backupList" style="width: 100%" border>
                <el-table-column prop="filename" label="文件名" width="300" />
                <el-table-column prop="size_text" label="大小" width="120" />
                <el-table-column prop="created_at" label="创建时间" width="200">
                  <template #default="scope">
                    {{ new Date(scope.row.created_at).toLocaleString('zh-CN') }}
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                  <template #default="scope">
                    <el-button type="success" size="small" @click="downloadBackup(scope.row.filename)">
                      <el-icon><Document /></el-icon>下载
                    </el-button>
                    <el-button type="warning" size="small" @click="restoreBackup(scope.row.filename)">
                      <el-icon><RefreshRight /></el-icon>恢复
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            <div class="backup-settings">
              <el-form :model="backupSettings" label-width="120px">
                <el-form-item label="自动备份频率">
                  <el-select v-model="backupSettings.frequency" placeholder="请选择备份频率">
                    <el-option label="每天" value="daily" />
                    <el-option label="每周" value="weekly" />
                    <el-option label="每月" value="monthly" />
                  </el-select>
                </el-form-item>
                <el-form-item label="备份时间">
                  <el-time-picker
                    v-model="backupSettings.time"
                    format="HH:mm"
                    value-format="HH:mm"
                  />
                </el-form-item>
              </el-form>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统信息 -->
    <el-card class="settings-card" style="margin-top: 24px">
      <template #header>
        <div class="card-header">
          <el-icon size="20"><InfoFilled /></el-icon>
          <span class="title">系统信息</span>
        </div>
      </template>
      <div class="system-info">
        <div class="info-grid">
          <div class="info-card">
            <div class="info-icon">
              <el-icon size="24"><Cpu /></el-icon>
            </div>
            <div class="info-content">
              <div class="info-title">系统版本</div>
              <div class="info-value">v1.0.0</div>
            </div>
          </div>
          <div class="info-card">
            <div class="info-icon">
              <el-icon size="24"><Calendar /></el-icon>
            </div>
            <div class="info-content">
              <div class="info-title">运行时间</div>
              <div class="info-value">{{ systemUptime }}</div>
            </div>
          </div>
          <div class="info-card">
            <div class="info-icon">
              <el-icon size="24"><DataLine /></el-icon>
            </div>
            <div class="info-content">
              <div class="info-title">数据量</div>
              <div class="info-value">{{ dataSize }}</div>
            </div>
          </div>
          <div class="info-card">
            <div class="info-icon">
              <el-icon size="24"><UserFilled /></el-icon>
            </div>
            <div class="info-content">
              <div class="info-title">在线用户</div>
              <div class="info-value">{{ onlineUsers }}</div>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 操作成功提示 -->
    <el-message
      v-if="showSuccessMessage"
      type="success"
      message="设置已成功保存！"
      :duration="3000"
      @close="showSuccessMessage = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  Check, Setting, Bell, Lock, Download,
  Document, RefreshRight, InfoFilled, Cpu,
  Calendar, DataLine, UserFilled
} from '@element-plus/icons-vue'
import { adminService } from '../api/admin'

// 基本设置
const basicSettings = ref({
  systemName: '颐养膳食管理系统',
  systemDescription: '社区老人餐管理系统，提供专业的膳食配送服务',
  contactEmail: 'admin@example.com',
  contactPhone: '400-123-4567',
  language: 'zh-CN'
})

// 通知设置
const notificationSettings = ref({
  emailEnabled: true,
  smsEnabled: false,
  systemEnabled: true,
  orderEnabled: true,
  deliveryEnabled: true
})

// 安全设置
const securitySettings = ref({
  passwordStrength: 'medium',
  passwordExpiryDays: 90,
  loginAttempts: 5,
  sessionTimeout: 30,
  twoFactorAuth: false
})

// AI设置
const aiSettings = ref({
  chatModel: 'GPT-3.5',
  elderlyChatModel: 'GPT-3.5',
  reviewModel: 'GPT-3.5',
  apiUrl: '',
  apiKey: ''
})

// 动态模型列表
const availableModels = ref([])
const loadingModels = ref(false)

// 备份设置
const backupSettings = ref({
  frequency: 'daily',
  time: '02:00'
})

// 系统信息
const lastBackupTime = ref('2024-03-25 02:00:00')
const backupSize = ref('2.4 MB')
const backupRetention = ref('7个')
const systemUptime = ref('24天 12小时')
const dataSize = ref('156 MB')
const onlineUsers = ref('3')

// 消息提示
const showSuccessMessage = ref(false)
const backupLoading = ref(false)
const backupList = ref([])

// 方法
const saveAllSettings = async () => {
  try {
    // 保存AI设置
    const aiData = {
      chat_model: aiSettings.value.chatModel,
      elderly_chat_model: aiSettings.value.elderlyChatModel,
      review_model: aiSettings.value.reviewModel,
      api_url: aiSettings.value.apiUrl,
      api_key: aiSettings.value.apiKey
    }
    
    await adminService.updateAISettings(aiData)
    
    showSuccessMessage.value = true
  } catch (error) {
    console.error('保存设置失败:', error)
    showSuccessMessage.value = true
  }
}

// 加载备份列表
const loadBackupList = async () => {
  try {
    const response = await adminService.getBackupList()
    backupList.value = response.backups
    
    // 更新最新备份信息
    if (backupList.value.length > 0) {
      const latestBackup = backupList.value[0]
      lastBackupTime.value = new Date(latestBackup.created_at).toLocaleString('zh-CN')
      backupSize.value = latestBackup.size_text
    }
  } catch (error) {
    console.error('加载备份列表失败:', error)
  }
}

const performBackup = async () => {
  try {
    backupLoading.value = true
    const response = await adminService.createBackup()
    console.log('备份创建成功:', response)
    
    // 重新加载备份列表
    await loadBackupList()
    
    // 显示成功消息
    ElMessage.success('备份创建成功！')
  } catch (error) {
    console.error('备份创建失败:', error)
    ElMessage.error(`备份创建失败: ${error.response?.data?.detail || error.message}`)
  } finally {
    backupLoading.value = false
  }
}

const downloadBackup = async (filename) => {
  try {
    backupLoading.value = true
    const response = await adminService.downloadBackup(filename)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('备份文件下载成功！')
  } catch (error) {
    console.error('备份下载失败:', error)
    ElMessage.error(`备份下载失败: ${error.response?.data?.detail || error.message}`)
  } finally {
    backupLoading.value = false
  }
}

const restoreBackup = async (filename) => {
  try {
    if (!confirm('确定要恢复此备份吗？这将覆盖当前数据库！')) {
      return
    }
    
    backupLoading.value = true
    const response = await adminService.restoreBackup(filename)
    console.log('备份恢复成功:', response)
    
    ElMessage.success('备份恢复成功！')
  } catch (error) {
    console.error('备份恢复失败:', error)
    ElMessage.error(`备份恢复失败: ${error.response?.data?.detail || error.message}`)
  } finally {
    backupLoading.value = false
  }
}

const loadAISettings = async () => {
  try {
    const data = await adminService.getAISettings()
    aiSettings.value = {
      chatModel: data.chat_model,
      elderlyChatModel: data.elderly_chat_model,
      reviewModel: data.review_model,
      apiUrl: data.api_url,
      apiKey: data.api_key
    }
    // 加载模型列表
    if (data.api_url) {
      await fetchAvailableModels(data.api_url)
    }
  } catch (error) {
    console.error('加载AI设置失败:', error)
  }
}

const fetchAvailableModels = async (apiUrl) => {
  if (!apiUrl) {
    availableModels.value = []
    return
  }
  
  loadingModels.value = true
  try {
    const data = await adminService.getAIModels(apiUrl, aiSettings.value.apiKey)
    availableModels.value = data.models
  } catch (error) {
    console.error('获取模型列表失败:', error)
    availableModels.value = []
  } finally {
    loadingModels.value = false
  }
}

// 监听API地址变化，自动更新模型列表
aiSettings.value.apiUrl = ''
const unwatch = watch(() => aiSettings.value.apiUrl, async (newUrl) => {
  await fetchAvailableModels(newUrl)
})

onMounted(() => {
  // 加载AI设置
  loadAISettings()
  // 加载备份列表
  loadBackupList()
})
</script>

<style scoped>
.settings {
  padding: var(--spacing-xl);
}

.settings-card {
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

.backup-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.backup-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--border-color);
}

.info-label {
  color: var(--text-secondary);
}

.info-value {
  font-weight: 600;
  color: var(--text-primary);
}

.backup-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  padding: var(--spacing-md) 0;
}

.backup-settings {
  border-top: 1px solid var(--border-color);
  padding-top: var(--spacing-lg);
}

.system-info {
  padding: var(--spacing-md) 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
}

.info-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
}

.info-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.info-content {
  flex: 1;
}

.info-title {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: var(--spacing-xs);
}

.info-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}
</style>
