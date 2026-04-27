<template>
  <div class="community-manage">
    <!-- 顶部操作栏 -->
    <div class="action-header">
      <div class="search-box">
        <el-input
          v-model="search"
          placeholder="输入社区名称或地址搜索..."
          class="modern-input"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" class="add-btn" @click="handleAdd">
          <el-icon><Plus /></el-icon>添加新社区
        </el-button>
      </div>
      <div class="filter-group">
        <el-select v-model="filterStatus" placeholder="社区状态" style="width: 120px">
          <el-option label="全部" value="" />
          <el-option label="正常" value="正常" />
          <el-option label="暂停服务" value="暂停服务" />
        </el-select>
        <el-button-group>
          <el-button :icon="Grid" />
          <el-button :icon="List" />
        </el-button-group>
      </div>
    </div>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table :data="tableData" style="width: 100%; max-width: 100%" class="dark-theme-table" :style="tableStyle">
        <el-table-column label="社区信息" width="280">
          <template #default="scope">
            <transition name="fade">
              <div class="community-cell" :key="scope.row.id">
                <div class="community-icon">
                  <el-icon size="40" :color="getCommunityColor(scope.row.name)"><House /></el-icon>
                </div>
                <div class="community-meta">
                  <span class="name">{{ scope.row.name }}</span>
                  <span class="address">{{ scope.row.address }}</span>
                </div>
              </div>
            </transition>
          </template>
        </el-table-column>
        <el-table-column prop="elderlyCount" label="老人数量" width="100" />
        <el-table-column prop="contactPerson" label="联系人" width="100" />
        <el-table-column prop="deliveryTime" label="配送时间" width="120" />
        <el-table-column label="服务状态" width="90">
          <template #default="scope">
            <transition name="status-change">
              <el-tag 
                :type="scope.row.status === '正常' ? 'success' : 'warning'" 
                size="small"
                :key="scope.row.status"
              >
                {{ scope.row.status }}
              </el-tag>
            </transition>
          </template>
        </el-table-column>
        <el-table-column prop="deliveryRange" label="配送范围" width="100" />
        <el-table-column prop="contactPhone" label="联系电话" />
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="scope">
            <div class="action-btns">
              <el-button size="small" link type="primary" @click="handleDetail(scope.row)">详情</el-button>
              <el-button size="small" link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
              <el-divider direction="vertical" />
              <el-button size="small" link type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <span class="total-text">共 {{ totalCount }} 个社区</span>
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
      title="社区详细信息"
      size="500px"
      class="modern-drawer"
    >
      <div v-if="currentRow" class="detail-content">
        <div class="detail-header">
          <div class="community-icon-large">
            <el-icon size="64" :color="getCommunityColor(currentRow.name)"><House /></el-icon>
          </div>
          <h2>{{ currentRow.name }}</h2>
          <p>{{ currentRow.address }}</p>
        </div>
        
        <el-divider content-position="left">基本信息</el-divider>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="联系电话">{{ currentRow.contactPhone }}</el-descriptions-item>
          <el-descriptions-item label="老人数量">{{ currentRow.elderlyCount }} 位</el-descriptions-item>
          <el-descriptions-item label="配送时间">{{ currentRow.deliveryTime }}</el-descriptions-item>
          <el-descriptions-item label="服务状态">
            <el-tag :type="currentRow.status === '正常' ? 'success' : 'warning'">
              {{ currentRow.status }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider content-position="left">社区老人分布</el-divider>
        <div class="elderly-stats">
          <div class="stat-item">
            <span class="stat-label">60-70岁</span>
            <span class="stat-value">{{ elderlyStats.sixtyToSeventy || 0 }}人</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">70-80岁</span>
            <span class="stat-value">{{ elderlyStats.seventyToEighty || 0 }}人</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">80岁以上</span>
            <span class="stat-value">{{ elderlyStats.overEighty || 0 }}人</span>
          </div>
        </div>


      </div>
    </el-drawer>

    <!-- 添加/编辑社区弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditMode ? '编辑社区' : '添加新社区'"
      width="600px"
      center
    >
      <el-form :model="communityForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="社区名称" required>
              <el-input v-model="communityForm.name" placeholder="请输入社区名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系人" required>
              <el-input v-model="communityForm.contactPerson" placeholder="请输入联系人姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" required>
              <el-input v-model="communityForm.contactPhone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>

        </el-row>
        
        <el-form-item label="社区地址" required>
          <el-input v-model="communityForm.address" placeholder="请输入社区详细地址" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="配送时间">
              <el-input v-model="communityForm.deliveryTime" placeholder="如：11:30-13:00" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="配送范围">
              <el-input v-model="communityForm.deliveryRange" placeholder="如：1.5km" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="服务状态">
          <el-radio-group v-model="communityForm.status">
            <el-radio label="正常" />
            <el-radio label="暂停服务" />
          </el-radio-group>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveCommunity">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Grid, List, Search, Plus, House } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminService } from '../api'

const search = ref('')
const filterStatus = ref('')
const drawerVisible = ref(false)
const dialogVisible = ref(false)
const isEditMode = ref(false)
const currentRow = ref(null)
const totalCount = ref(0)
const loading = ref(false)
const isMounted = ref(true)

// 统计数据
const elderlyStats = ref({
  sixtyToSeventy: 0,
  seventyToEighty: 0,
  overEighty: 0
})

// 社区表单数据
const communityForm = ref({
  name: '',
  contactPerson: '',
  contactPhone: '',
  address: '',
  deliveryTime: '',
  deliveryRange: '',
  status: '正常'
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
  loadCommunities()
})

// 组件卸载时清理
onUnmounted(() => {
  isMounted.value = false
})

// 根据社区名称获取颜色
const getCommunityColor = (name) => {
  const colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
  if (!name || typeof name !== 'string') {
    return colors[0] // 返回默认颜色
  }
  const index = name.charCodeAt(0) % colors.length
  return colors[index]
}

const tableData = ref([])

// 加载社区数据
const loadCommunities = async () => {
  try {
    loading.value = true
    const response = await adminService.getCommunities()
    tableData.value = response.items.map(item => ({
      id: item.id,
      name: item.name,
      address: item.address,
      elderlyCount: item.elderly_count,
      contactPerson: item.manager_name || '',
      deliveryTime: '11:30-13:00', // 默认配送时间
      status: item.status || '正常', // 使用后端返回的状态
      serviceType: '老年餐配送',
      deliveryRange: '1.5km', // 默认配送范围
      contactPhone: item.contact_phone || item.manager_phone || ''
    }))
    totalCount.value = response.total
  } catch (error) {
    ElMessage.error('加载社区数据失败')
    console.error('加载社区数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载社区统计数据
const loadCommunityStats = async (communityId) => {
  try {
    // 获取社区老人年龄分布
    const elderlyResponse = await adminService.getElderlyUsers({ community_id: communityId })
    const elderlyUsers = elderlyResponse.items || []
    
    // 统计年龄分布
    let sixtyToSeventy = 0
    let seventyToEighty = 0
    let overEighty = 0
    
    elderlyUsers.forEach(user => {
      const age = user.profile?.age
      if (age >= 60 && age< 70) {
        sixtyToSeventy++
      } else if (age >= 70 && age< 80) {
        seventyToEighty++
      } else if (age >= 80) {
        overEighty++
      }
    })
    
    // 检查组件是否仍然挂载
    if (isMounted.value) {
      elderlyStats.value = {
        sixtyToSeventy,
        seventyToEighty,
        overEighty
      }
    }
    
  } catch (error) {
    console.error('加载社区统计数据失败:', error)
    if (isMounted.value) {
      elderlyStats.value = {
        sixtyToSeventy: 0,
        seventyToEighty: 0,
        overEighty: 0
      }
    }
  }
}

// 查看详情
const handleDetail = async (row) => {
  currentRow.value = row
  await loadCommunityStats(row.id)
  drawerVisible.value = true
}

// 添加社区
const handleAdd = () => {
  isEditMode.value = false
  communityForm.value = {
    name: '',
    contactPerson: '',
    contactPhone: '',
    address: '',
    deliveryTime: '',
    deliveryRange: '',
    status: '正常'
  }
  dialogVisible.value = true
}

// 编辑社区
const handleEdit = (row) => {
  isEditMode.value = true
  currentRow.value = row
  communityForm.value = { ...row }
  dialogVisible.value = true
}

// 删除社区
const handleDelete = async (row) => {
  ElMessageBox.confirm(
    `确定要删除社区 "${row.name}" 吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await adminService.deleteCommunity(row.id)
      const index = tableData.value.findIndex(item => item.id === row.id)
      if (index !== -1) {
        tableData.value.splice(index, 1)
        totalCount.value = tableData.value.length
        ElMessage.success('删除成功！')
      }
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除社区失败:', error)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 保存社区
const saveCommunity = async () => {
  // 表单验证
  if (!communityForm.value.name) {
    ElMessage.warning('请输入社区名称')
    return
  }
  if (!communityForm.value.contactPerson) {
    ElMessage.warning('请输入联系人')
    return
  }
  if (!communityForm.value.contactPhone) {
    ElMessage.warning('请输入联系电话')
    return
  }
  if (!communityForm.value.address) {
    ElMessage.warning('请输入社区地址')
    return
  }
  
  try {
    const communityData = {
      name: communityForm.value.name,
      address: communityForm.value.address,
      contact_phone: communityForm.value.contactPhone,
      manager_name: communityForm.value.contactPerson,
      manager_phone: communityForm.value.contactPhone,
      status: communityForm.value.status
    }
    
    if (isEditMode.value) {
      // 编辑模式
      await adminService.updateCommunity(currentRow.value.id, communityData)
      ElMessage.success('编辑成功！')
    } else {
      // 添加模式
      await adminService.createCommunity(communityData)
      ElMessage.success('添加成功！')
    }
    
    dialogVisible.value = false
    await loadCommunities()
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存社区失败:', error)
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

.community-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.community-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(99, 102, 241, 0.1);
  transition: all var(--transition-normal);
}

.community-cell:hover .community-icon {
  transform: scale(1.1);
}

.community-meta {
  display: flex;
  flex-direction: column;
}

.community-meta .name {
  font-weight: 700;
  color: var(--text-main);
  font-size: 16px;
}

.community-meta .address {
  font-size: 13px;
  color: var(--text-light);
  margin-top: 4px;
}

.action-btns {
  display: flex;
  align-items: center;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.community-icon-large {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(99, 102, 241, 0.1);
  margin-bottom: 16px;
}

.detail-header h2 {
  margin: 0 0 4px;
  font-size: 24px;
}

.detail-header p {
  color: var(--text-light);
  font-size: 14px;
}

.elderly-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
}

.stat-item .stat-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.stat-item .stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}

.order-stats {
  display: flex;
  gap: 16px;
}

.stat-card {
  flex: 1;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-card .stat-icon {
  font-size: 24px;
  color: var(--primary-color);
}

.stat-card .stat-title {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-card .stat-number {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}
</style>