<template>
  <div class="announcement-manage">
    <!-- 顶部操作栏 -->
    <div class="action-header">
      <div class="search-box">
        <el-input
          v-model="search"
          placeholder="输入通知标题或内容搜索..."
          class="modern-input"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" class="add-btn" @click="handleAdd">
          <el-icon><Plus /></el-icon>发布新通知
        </el-button>
      </div>
      <div class="filter-group">
        <el-select v-model="filterStatus" placeholder="通知状态" style="width: 120px">
          <el-option label="全部" value="" />
          <el-option label="已发布" value="published" />
          <el-option label="草稿" value="draft" />
          <el-option label="已过期" value="expired" />
        </el-select>
        <el-select v-model="filterType" placeholder="通知类型" style="width: 120px">
          <el-option label="全部" value="" />
          <el-option label="系统公告" value="system" />
          <el-option label="活动通知" value="activity" />
          <el-option label="重要提醒" value="warning" />
        </el-select>
      </div>
    </div>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table :data="tableData" style="width: 100%" class="dark-theme-table" :style="tableStyle" fit>
        <el-table-column label="通知信息">
          <template #default="scope">
            <div class="announcement-cell">
              <div class="announcement-icon" :class="scope.row.type">
                <el-icon size="32">
                  <Bell v-if="scope.row.type === 'system'" />
                  <Promotion v-else-if="scope.row.type === 'activity'" />
                  <Warning v-else />
                </el-icon>
              </div>
              <div class="announcement-meta">
                <span class="title">{{ scope.row.title }}</span>
                <span class="summary">{{ scope.row.summary }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="通知类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeColor(scope.row.type)" size="small">
              {{ getTypeName(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="targetAudience" label="受众范围" width="100" />
        <el-table-column prop="publishTime" label="发布时间" width="160" />
        <el-table-column prop="expireTime" label="过期时间" width="160" />
        <el-table-column label="状态" width="150">
          <template #default="scope">
            <el-tag :type="getStatusColor(scope.row.status)" size="small">
              {{ getStatusName(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="scope">
            <div class="action-btns">
              <el-button size="small" link type="primary" @click="handleDetail(scope.row)">查看</el-button>
              <el-button size="small" link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
              <el-divider direction="vertical" />
              <el-button size="small" link type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <span class="total-text">共 {{ totalCount }} 条通知</span>
        <el-pagination
          background
          layout="prev, pager, next"
          :total="totalCount"
          class="modern-pagination"
        />
      </div>
    </el-card>

    <!-- 详情抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="通知详情"
      size="500px"
      class="modern-drawer"
    >
      <div v-if="currentRow" class="detail-content">
        <div class="detail-header">
          <div class="announcement-icon-large" :class="currentRow.type">
            <el-icon size="48">
              <Bell v-if="currentRow.type === 'system'" />
              <Promotion v-else-if="currentRow.type === 'activity'" />
              <Warning v-else />
            </el-icon>
          </div>
          <h2>{{ currentRow.title }}</h2>
          <div class="detail-meta">
            <span class="meta-item">
              <el-tag :type="getTypeColor(currentRow.type)" size="small">
                {{ getTypeName(currentRow.type) }}
              </el-tag>
            </span>
            <span class="meta-item">受众：{{ currentRow.targetAudience }}</span>
            <span class="meta-item">发布时间：{{ currentRow.publishTime }}</span>
            <span class="meta-item">过期时间：{{ currentRow.expireTime }}</span>
          </div>
        </div>
        
        <el-divider content-position="left">通知内容</el-divider>
        <div class="content-body" v-html="currentRow.content"></div>
      </div>
    </el-drawer>

    <!-- 发布/编辑通知弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditMode ? '编辑通知' : '发布新通知'"
      width="800px"
      center
    >
      <el-form :model="announcementForm" label-width="120px">
        <el-form-item label="通知标题">
          <el-input v-model="announcementForm.title" placeholder="请输入通知标题" />
        </el-form-item>
        
        <el-form-item label="通知内容">
          <el-input
            v-model="announcementForm.content"
            type="textarea"
            :rows="8"
            placeholder="请输入通知内容，支持HTML格式"
          />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="通知类型">
              <el-select v-model="announcementForm.type" placeholder="请选择通知类型">
                <el-option label="系统公告" value="system" />
                <el-option label="活动通知" value="activity" />
                <el-option label="重要提醒" value="warning" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="接收对象">
              <el-select
                v-model="announcementForm.targetAudience"
                multiple
                placeholder="请选择接收对象"
              >
                <el-option label="老人" value="老人" />
                <el-option label="家属" value="家属" />
                <el-option label="配送员" value="配送员" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发布时间">
              <el-date-picker
                v-model="announcementForm.publishTime"
                type="datetime"
                placeholder="选择发布时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="过期时间">
              <el-date-picker
                v-model="announcementForm.expireTime"
                type="datetime"
                placeholder="选择过期时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveDraft">保存草稿</el-button>
          <el-button type="success" @click="publishAnnouncement">发布通知</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { Search, Plus, Bell, Promotion, Warning } from '@element-plus/icons-vue'
import { adminService } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const search = ref('')
const filterStatus = ref('')
const filterType = ref('')
const drawerVisible = ref(false)
const currentRow = ref(null)
const totalCount = ref(0)
const loading = ref(false)

// 发布通知弹窗
const dialogVisible = ref(false)
const isEditMode = ref(false)
const announcementForm = reactive({
  id: '',
  title: '',
  content: '',
  type: 'system',
  targetAudience: ['老人'],
  publishTime: '',
  expireTime: '',
  status: 'draft'
})

// 表格样式计算属性
const tableStyle = computed(() => {
  const isDark = document.documentElement.hasAttribute('data-theme')
  if (isDark) {
    return {
      '--el-table-bg-color': '#1a1a2e',
      '--el-table-tr-bg-color': '#1a1a2e',
      '--el-table-tr-bg-color-deep': 'rgba(255, 255, 255, 0.05)',
      '--el-table-header-bg-color': '#0a0a0a',
      '--el-table-row-hover-bg-color': 'rgba(99, 102, 241, 0.08)'
    }
  } else {
    return {
      '--el-table-bg-color': '#ffffff',
      '--el-table-tr-bg-color': '#ffffff',
      '--el-table-tr-bg-color-deep': 'rgba(99, 102, 241, 0.02)',
      '--el-table-header-bg-color': '#f8fafc',
      '--el-table-row-hover-bg-color': 'rgba(99, 102, 241, 0.05)'
    }
  }
})

// 更新表格样式
const updateTableStyles = () => {
  const intervalId = setInterval(() => {
    const isDark = document.documentElement.hasAttribute('data-theme')
    const tableElements = document.querySelectorAll('.dark-theme-table')
    
    tableElements.forEach(table => {
      const rows = table.querySelectorAll('.el-table__row')
      const cells = table.querySelectorAll('.el-table__row td')
      const bodyWrapper = table.querySelector('.el-table__body-wrapper')
      const tableBody = table.querySelector('.el-table__body')
      
      if (bodyWrapper) {
        bodyWrapper.style.backgroundColor = isDark ? '#1a1a2e' : '#ffffff'
      }
      if (tableBody) {
        tableBody.style.backgroundColor = isDark ? '#1a1a2e' : '#ffffff'
      }
      
      rows.forEach((row, index) => {
        if (isDark) {
          if (index % 2 === 0) {
            row.style.backgroundColor = '#1a1a2e'
            row.style.background = '#1a1a2e'
          } else {
            row.style.backgroundColor = 'rgba(255, 255, 255, 0.05)'
            row.style.background = 'rgba(255, 255, 255, 0.05)'
          }
        } else {
          if (index % 2 === 0) {
            row.style.backgroundColor = '#ffffff'
            row.style.background = '#ffffff'
          } else {
            row.style.backgroundColor = 'rgba(99, 102, 241, 0.02)'
            row.style.background = 'rgba(99, 102, 241, 0.02)'
          }
        }
        const bgColor = isDark ? (index % 2 === 0 ? '#1a1a2e' : 'rgba(255, 255, 255, 0.05)') : 
                               (index % 2 === 0 ? '#ffffff' : 'rgba(99, 102, 241, 0.02)')
        row.setAttribute('style', `background-color: ${bgColor} !important; background: ${bgColor} !important;`)
      })
      
      cells.forEach(cell => {
        cell.style.backgroundColor = 'transparent'
        cell.style.background = 'transparent'
        cell.setAttribute('style', 'background-color: transparent !important; background: transparent !important;')
      })
    })
    
    if (tableElements.length === 0) {
      clearInterval(intervalId)
    }
  }, 5)
}

// 组件挂载时设置表格样式和加载数据
onMounted(() => {
  updateTableStyles()
  loadAnnouncements()
})

// 获取类型颜色
const getTypeColor = (type) => {
  const colors = {
    'system': 'primary',
    'activity': 'success',
    'warning': 'danger'
  }
  return colors[type] || 'info'
}

// 获取类型名称
const getTypeName = (type) => {
  const names = {
    'system': '系统公告',
    'activity': '活动通知',
    'warning': '重要提醒'
  }
  return names[type] || type
}

// 获取状态颜色
const getStatusColor = (status) => {
  const colors = {
    'published': 'success',
    'draft': 'info',
    'expired': 'warning'
  }
  return colors[status] || 'info'
}

// 获取状态名称
const getStatusName = (status) => {
  const names = {
    'published': '已发布',
    'draft': '草稿',
    'expired': '已过期'
  }
  return names[status] || status
}

const tableData = ref([])

// 加载通知数据
const loadAnnouncements = async () => {
  try {
    loading.value = true
    const response = await adminService.getAnnouncements()
    tableData.value = response.items.map(item => ({
      id: item.id,
      title: item.title,
      summary: item.content.substring(0, 50) + (item.content.length > 50 ? '...' : ''),
      type: item.type,
      targetAudience: '全体老人',
      publishTime: new Date(item.created_at).toLocaleString('zh-CN'),
      expireTime: '',
      status: item.status === 'active' ? 'published' : 'draft',
      content: item.content
    }))
    totalCount.value = response.total
  } catch (error) {
    ElMessage.error('加载通知数据失败')
    console.error('加载通知数据失败:', error)
  } finally {
    loading.value = false
  }
}

const handleDetail = (row) => {
  currentRow.value = row
  drawerVisible.value = true
}

// 发布通知弹窗处理方法
const handleAdd = () => {
  isEditMode.value = false
  announcementForm.id = ''
  announcementForm.title = ''
  announcementForm.content = ''
  announcementForm.type = 'system'
  announcementForm.targetAudience = ['老人']
  announcementForm.publishTime = ''
  announcementForm.expireTime = ''
  announcementForm.status = 'draft'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEditMode.value = true
  announcementForm.id = row.id
  announcementForm.title = row.title
  announcementForm.content = row.content
  announcementForm.type = row.type
  announcementForm.targetAudience = row.targetAudience.split('、')
  announcementForm.publishTime = row.publishTime
  announcementForm.expireTime = row.expireTime
  announcementForm.status = row.status
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  ElMessageBox.confirm(
    `确定要删除通知"${row.title}"吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await adminService.deleteAnnouncement(row.id)
      const index = tableData.value.findIndex(item => item.id === row.id)
      if (index !== -1) {
        tableData.value.splice(index, 1)
        totalCount.value = tableData.value.length
        ElMessage.success('删除成功！')
      }
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除通知失败:', error)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

const saveDraft = () => {
  announcementForm.status = 'draft'
  saveAnnouncement()
}

const publishAnnouncement = () => {
  announcementForm.status = 'active'
  saveAnnouncement()
}

const saveAnnouncement = async () => {
  try {
    const announcementData = {
      title: announcementForm.title,
      content: announcementForm.content,
      type: announcementForm.type,
      priority: 'normal',
      status: announcementForm.status
    }
    
    if (isEditMode.value) {
      // 编辑模式
      await adminService.updateAnnouncement(announcementForm.id, announcementData)
      ElMessage.success('编辑成功！')
    } else {
      // 添加模式
      await adminService.createAnnouncement(announcementData)
      ElMessage.success('创建成功！')
    }
    
    dialogVisible.value = false
    await loadAnnouncements()
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存通知失败:', error)
  }
}
</script>

<style scoped>
.action-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.search-box {
  display: flex;
  gap: 16px;
  flex: 1;
  max-width: 600px;
}

.modern-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  padding-left: 15px;
  box-shadow: var(--shadow-sm);
}

.add-btn {
  border-radius: 12px !important;
  padding: 12px 24px !important;
}

.filter-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.table-card {
  border-radius: var(--radius-md) !important;
  width: 100% !important;
  max-width: 100% !important;
}

:deep(.el-table__inner-wrapper) {
  width: 100% !important;
}

:deep(.el-table__header-wrapper) {
  width: 100% !important;
}

:deep(.el-table__body-wrapper) {
  width: 100% !important;
}

/* 移除表格边框 */
:deep(.el-table),
:deep(.el-table__header-wrapper),
:deep(.el-table__body-wrapper),
:deep(.el-table__footer-wrapper) {
  border: none !important;
}

:deep(.el-table__header tr),
:deep(.el-table__header th) {
  border: none !important;
}

:deep(.el-table__row td) {
  border: none !important;
}

.announcement-cell {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.announcement-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 4px;
  transition: all var(--transition-normal);
}

.announcement-icon.system {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary-color);
}

.announcement-icon.activity {
  background: rgba(16, 185, 129, 0.1);
  color: var(--secondary-color);
}

.announcement-icon.warning {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.announcement-cell:hover .announcement-icon {
  transform: scale(1.1);
}

.announcement-meta {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.announcement-meta .title {
  font-weight: 700;
  color: var(--text-main);
  font-size: 16px;
  margin-bottom: 8px;
}

.announcement-meta .summary {
  font-size: 13px;
  color: var(--text-light);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.action-btns {
  display: flex;
  align-items: center;
}

.action-btns :deep(.el-button) {
  color: rgb(255, 255, 255) !important;
}

.action-btns :deep(.el-button:hover) {
  color: rgba(255, 255, 255, 0.8) !important;
}

.action-btns :deep(.el-button--primary) {
  color: rgb(255, 255, 255) !important;
}

.action-btns :deep(.el-button--primary:hover) {
  color: rgba(255, 255, 255, 0.8) !important;
}

.action-btns :deep(.el-button--danger) {
  color: rgb(255, 255, 255) !important;
}

.action-btns :deep(.el-button--danger:hover) {
  color: rgba(255, 255, 255, 0.8) !important;
}

.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-text {
  font-size: 13px;
  color: var(--text-light);
}

.detail-content {
  padding: 0 20px;
}

.detail-header {
  margin-bottom: 30px;
}

.announcement-icon-large {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.announcement-icon-large.system {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary-color);
}

.announcement-icon-large.activity {
  background: rgba(16, 185, 129, 0.1);
  color: var(--secondary-color);
}

.announcement-icon-large.warning {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.detail-header h2 {
  margin: 0 0 12px;
  font-size: 24px;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 14px;
  color: var(--text-secondary);
}

.content-body {
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  line-height: 1.6;
  margin-bottom: 24px;
}

.content-body p {
  margin: 0 0 12px;
}

.content-body p:last-child {
  margin-bottom: 0;
}
</style>