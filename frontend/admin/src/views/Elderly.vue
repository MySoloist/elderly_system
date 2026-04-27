<template>
  <div class="elderly-manage">
    <!-- 顶部操作栏 -->
    <div class="action-header">
      <div class="search-box">
        <el-input
          v-model="search"
          placeholder="输入姓名、电话或住址搜索..."
          class="modern-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" class="add-btn" @click="handleAdd">
          <el-icon><Plus /></el-icon>登记新老人
        </el-button>
      </div>
      <div class="filter-group">
        <el-select v-model="filterCommunity" placeholder="选择社区" style="width: 150px" @change="handleCommunityChange">
          <el-option label="全部" value="" />
          <el-option 
            v-for="community in communities" 
            :key="community.id" 
            :label="community.name" 
            :value="community.id" 
          />
        </el-select>
        <el-select v-model="filterHealth" placeholder="健康状况" style="width: 120px" @change="handleHealthChange">
          <el-option label="全部" value="" />
          <el-option 
            v-for="tag in healthTags" 
            :key="tag.id" 
            :label="tag.name" 
            :value="tag.id" 
          />
        </el-select>
        <el-button-group>
          <el-button :icon="Grid" />
          <el-button :icon="List" />
        </el-button-group>
      </div>
    </div>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table :data="tableData" style="width: 100%" class="dark-theme-table" :style="tableStyle" v-loading="loading">
        <el-table-column label="老人信息" width="250">
          <template #default="scope">
            <div class="user-cell">
              <el-avatar :size="40" :style="{ backgroundColor: getAvatarColor(scope.row.name) }">
                {{ scope.row.name && scope.row.name.length > 0 ? scope.row.name.charAt(0) : '?' }}
              </el-avatar>
              <div class="user-meta">
                <span class="name">{{ scope.row.name }}</span>
                <span class="age">{{ scope.row.age }}岁 · {{ scope.row.gender }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="所属社区" width="150">
          <template #default="scope">
            <el-tag size="small" type="info">{{ scope.row.communityName || '未分配' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="address" label="居住地址" show-overflow-tooltip />
        <el-table-column label="健康标签" width="180">
          <template #default="scope">
            <div class="tag-group">
              <el-tag 
                v-for="tag in scope.row.tags" 
                :key="tag" 
                size="small" 
                :type="getTagType(tag)"
                effect="light"
                round
              >
                {{ tag }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
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
        <span class="total-text">共 {{ pagination.total }} 位老人</span>
        <el-pagination
          background
          layout="prev, pager, next, jumper"
          :total="pagination.total"
          :page-size="pagination.limit"
          :current-page="pagination.page"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          class="modern-pagination"
        />
      </div>
    </el-card>

    <!-- 详情抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="老人详细档案"
      size="500px"
      class="modern-drawer"
    >
      <div v-if="currentRow" class="detail-content">
        <div class="detail-header">
          <el-avatar :size="80" :style="{ backgroundColor: getAvatarColor(currentRow.name) }">
            {{ currentRow.name && currentRow.name.length > 0 ? currentRow.name.charAt(0) : '?' }}
          </el-avatar>
          <h2>{{ currentRow.name }}</h2>
          <p>{{ currentRow.address }}</p>
        </div>
        
        <!-- 绑定家属列表 -->
        <el-divider content-position="left">绑定家属列表</el-divider>
        <el-table
          :data="boundMembersList"
          style="width: 100%"
          v-loading="boundMembersLoading"
          size="small"
          :show-header="true"
          :border="false"
          :striped="false"
          :style="{
            '--el-table-bg-color': 'transparent',
            '--el-table-tr-bg-color': 'transparent',
            '--el-table-header-bg-color': 'transparent',
            '--el-table-header-text-color': '#94a3b8',
            '--el-table-text-color': '#ffffff',
            '--el-table-row-hover-bg-color': 'rgba(99, 102, 241, 0.08)'
          }"
        >
          <el-table-column prop="memberName" label="家属姓名" width="80" />
          <el-table-column prop="relationship" label="关系" width="70" />
          <el-table-column prop="emergencyContact" label="主要联系人" width="80">
            <template #default="scope">
              <el-tag :type="scope.row.emergencyContact ? 'success' : 'info'">
                {{ scope.row.emergencyContact ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="电话" width="100" />
          <el-table-column prop="createTime" label="绑定时间" width="120" />
        </el-table>
        <div v-if="boundMembersList.length === 0 && !boundMembersLoading" class="empty-state">
          <el-empty description="暂无绑定家属" />
        </div>
      </div>
    </el-drawer>

    <!-- 添加/编辑老人弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditMode ? '编辑老人信息' : '添加新老人'"
      width="600px"
      center
    >
      <el-form :model="elderlyForm" label-width="100px" ref="formRef" :rules="rules">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="elderlyForm.name" placeholder="请输入老人姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input v-model="elderlyForm.age" placeholder="请输入年龄" type="number" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="elderlyForm.gender" placeholder="请选择性别">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="elderlyForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="所属社区" prop="communityId">
          <el-select
            v-model="elderlyForm.communityId"
            placeholder="请选择社区"
          >
            <el-option
              v-for="community in communities"
              :key="community.id"
              :label="community.name"
              :value="community.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="居住地址" prop="address">
          <el-input
            v-model="elderlyForm.address"
            type="textarea"
            placeholder="请输入居住地址"
            :rows="3"
          />
        </el-form-item>
        
        <el-form-item label="健康标签">
          <el-select
            v-model="elderlyForm.tags"
            multiple
            placeholder="请选择健康标签"
          >
            <el-option label="良好" value="良好" />
            <el-option label="需关注" value="需关注" />
            <el-option label="高血压" value="高血压" />
            <el-option label="糖尿病" value="糖尿病" />
            <el-option label="心脏病" value="心脏病" />
            <el-option label="独居" value="独居" />
            <el-option label="视力障碍" value="视力障碍" />
            <el-option label="听力障碍" value="听力障碍" />
          </el-select>
        </el-form-item>
        

        
        <el-form-item label="饮食偏好">
          <el-select
            v-model="elderlyForm.preferences"
            multiple
            placeholder="请选择饮食偏好"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.name"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveElderly">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { Grid, List, Search, Plus } from '@element-plus/icons-vue'
import { adminService } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const search = ref('')
const filterCommunity = ref('')
const filterHealth = ref('')
const drawerVisible = ref(false)
const currentRow = ref(null)
const loading = ref(true)
const communities = ref([])
const healthTags = ref([])
const tags = ref([])

// 绑定家属列表（用于详情查看）
const boundMembersList = ref([])
const boundMembersLoading = ref(false)

// 分页
const pagination = ref({
  page: 1,
  limit: 20,
  total: 0
})

// 添加/编辑老人弹窗
const dialogVisible = ref(false)
const isEditMode = ref(false)
const formRef = ref(null)
const rules = {
  name: [
    { required: true, message: '请输入老人姓名', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' },
    { pattern: /^[0-9]+$/, message: '年龄必须是数字', trigger: 'blur' },
    { validator: (rule, value, callback) => {
        const num = parseInt(value)
        if (isNaN(num)) {
          callback(new Error('年龄必须是有效数字'))
        } else if (num < 60 || num > 120) {
          callback(new Error('年龄应在60-120岁之间'))
        } else {
          callback()
        }
      }, trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入居住地址', trigger: 'blur' }
  ],
  communityId: [
    { required: true, message: '请选择社区', trigger: 'change' }
  ]
}
const elderlyForm = reactive({
  id: '',
  name: '',
  age: '',
  gender: '',
  phone: '',
  address: '',
  communityId: '',
  tags: [],
  preferences: []
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

// 表格数据
const tableData = ref([])

// 加载社区数据
const loadCommunities = async () => {
  try {
    const response = await adminService.getCommunities()
    communities.value = response.items || []
  } catch (error) {
    console.error('加载社区数据失败:', error)
  }
}

// 加载健康标签数据
const loadHealthTags = async () => {
  try {
    console.log('开始加载健康标签数据...')
    const tags = await adminService.getHealthTags()
    console.log('健康标签API返回数据:', tags)
    healthTags.value = tags || []
    console.log('健康标签列表:', healthTags.value)
  } catch (error) {
    console.error('加载健康标签数据失败:', error)
  }
}

// 加载标签数据（用于饮食偏好）
const loadTags = async () => {
  try {
    console.log('开始加载标签数据...')
    const response = await adminService.getTags()
    console.log('标签API返回数据:', response)
    // 检查返回数据格式
    if (Array.isArray(response)) {
      tags.value = response || []
    } else if (response && response.tags) {
      tags.value = response.tags || []
    } else if (response && response.items) {
      tags.value = response.items || []
    } else {
      tags.value = []
    }
    console.log('标签列表:', tags.value)
  } catch (error) {
    console.error('加载标签数据失败:', error)
    tags.value = []
  }
}

// 加载老人数据
const loadElderlyData = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.value.page,
      limit: pagination.value.limit
    }
    
    if (search.value) {
      params.search = search.value
    }
    
    if (filterCommunity.value) {
      params.community_id = filterCommunity.value
    }
    
    if (filterHealth.value) {
      // 如果选择的是"良好"标签（ID为1），则发送0表示查找健康标签为null的老人
      params.health_tag_id = filterHealth.value == 1 ? 0 : filterHealth.value
    }
    
    const response = await adminService.getElderlyUsers(params)
    tableData.value = response.items.map(item => ({
      id: item.id,
      name: item.profile?.name || '未知',
      age: item.profile?.age || '',
      gender: item.profile?.gender || '',
      phone: item.profile?.phone || '',
      address: item.profile?.address || '',
      communityName: item.profile?.community?.name || '未分配',
      communityId: item.profile?.community_id || '',
      tags: item.profile?.health_tag ? [item.profile.health_tag.name] : ['良好']
    }))
    
    pagination.value.total = response.total
  } catch (error) {
    ElMessage.error('加载老人数据失败')
    console.error('加载老人数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化
const handleSizeChange = (val) => {
  pagination.value.limit = val
  pagination.value.page = 1
  loadElderlyData()
}

const handleCurrentChange = (val) => {
  pagination.value.page = val
  loadElderlyData()
}

// 搜索变化
const handleSearch = () => {
  pagination.value.page = 1
  loadElderlyData()
}

// 社区筛选变化
const handleCommunityChange = () => {
  pagination.value.page = 1
  loadElderlyData()
}

// 健康状况筛选变化
const handleHealthChange = () => {
  pagination.value.page = 1
  loadElderlyData()
}

// 组件挂载时加载数据
onMounted(async () => {
  updateTableStyles()
  await loadCommunities()
  await loadHealthTags()
  await loadTags()
  await loadElderlyData()
})

// 获取老人绑定的家属列表
const getBoundMembersList = async (elderId) => {
  try {
    boundMembersLoading.value = true
    const response = await adminService.getElderMemberRelations({ elder_id: elderId })
    boundMembersList.value = response.items.map(item =>({
      memberName: item.member_name,
      relationship: item.relationship,
      emergencyContact: item.is_primary,
      phone: item.member_phone,
      createTime: new Date(item.created_at).toLocaleString('zh-CN')
    }))
  } catch (error) {
    console.error('加载绑定家属列表失败:', error)
    boundMembersList.value = []
  } finally {
    boundMembersLoading.value = false
  }
}

// 获取头像颜色
const getAvatarColor = (name) => {
  const colors = [
    '#4ecdc4', '#45aaf2', '#ff6b6b', '#fed330', 
    '#667eea', '#764ba2', '#4facfe', '#43e97b',
    '#fa709a', '#fee140', '#30cfd0', '#30a9de'
  ]
  
  if (!name || name.length === 0) {
    return colors[0]
  }
  
  // 根据用户名生成一个固定的颜色索引
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return colors[index]
}

const getTagType = (tag) => {
  if (tag === '良好') return 'success'
  if (tag === '需关注') return 'danger'
  if (tag === '高血压' || tag === '糖尿病') return 'warning'
  return 'info'
}

const handleDetail = async (row) => {
  currentRow.value = row
  await getBoundMembersList(row.id)
  drawerVisible.value = true
}

// 添加老人弹窗处理方法
const handleAdd = () => {
  isEditMode.value = false
  elderlyForm.id = ''
  elderlyForm.name = ''
  elderlyForm.age = ''
  elderlyForm.gender = ''
  elderlyForm.phone = ''
  elderlyForm.address = ''
  elderlyForm.communityId = ''
  elderlyForm.tags = []
  elderlyForm.preferences = []
  dialogVisible.value = true
}

// 编辑老人弹窗处理方法
const handleEdit = (row) => {
  isEditMode.value = true
  elderlyForm.id = row.id || ''
  elderlyForm.name = row.name
  elderlyForm.age = row.age
  elderlyForm.gender = row.gender
  elderlyForm.phone = row.phone
  elderlyForm.address = row.address
  elderlyForm.communityId = row.communityId || ''
  elderlyForm.tags = [...row.tags]
  elderlyForm.preferences = []
  dialogVisible.value = true
}

// 删除老人确认方法
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除老人"${row.name}"吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await adminService.deleteUser(row.id)
    ElMessage.success(`老人"${row.name}"删除成功！`)
    loadElderlyData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除老人失败:', error)
      ElMessage.error('删除失败，请稍后重试')
    }
  }
}

// 保存老人信息方法
const saveElderly = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (valid) {
      const userData = {
        username: elderlyForm.phone || `elderly_${Date.now()}`,
        password: '123456', // 默认密码
        user_type: 'elderly',
        profile: {
          name: elderlyForm.name,
          age: elderlyForm.age,
          gender: elderlyForm.gender,
          phone: elderlyForm.phone,
          address: elderlyForm.address,
          community_id: elderlyForm.communityId,
          dietary_preferences: elderlyForm.preferences.join(',')
        }
      }
      
      if (isEditMode.value) {
        // 更新老人信息
        await adminService.updateUser(elderlyForm.id, {
          profile: {
            name: elderlyForm.name,
            age: parseInt(elderlyForm.age),
            gender: elderlyForm.gender,
            phone: elderlyForm.phone,
            address: elderlyForm.address,
            community_id: elderlyForm.communityId,
            dietary_preferences: elderlyForm.preferences.join(',')
          }
        })
        ElMessage.success('老人信息更新成功！')
      } else {
        // 添加新老人，确保年龄是数字类型
        userData.profile.age = parseInt(elderlyForm.age)
        await adminService.createUser(userData)
        ElMessage.success('老人登记成功！')
      }
      
      dialogVisible.value = false
      loadElderlyData()
    }
  } catch (error) {
    console.error('保存老人信息失败:', error)
    ElMessage.error('保存失败，请检查输入信息')
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

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-meta .name {
  font-weight: 700;
  color: var(--text-main);
}

.user-meta .age {
  font-size: 12px;
  color: var(--text-light);
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.detail-header h2 {
  margin: 16px 0 4px;
  font-size: 24px;
}

.detail-header p {
  color: var(--text-light);
  font-size: 14px;
}

.preference-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

/* 暗色模式下的抽屉样式 */
body[data-theme="dark"] .modern-drawer .el-drawer__header {
  background-color: #1a1a2e !important;
  border-bottom-color: #2d3748 !important;
}

body[data-theme="dark"] .modern-drawer .el-drawer__title {
  color: #ffffff !important;
}

body[data-theme="dark"] .modern-drawer .el-drawer__body {
  background-color: #1a1a2e !important;
}

body[data-theme="dark"] .modern-drawer .el-descriptions {
  background-color: #1a1a2e !important;
}

body[data-theme="dark"] .modern-drawer .el-descriptions__cell {
  background-color: #1a1a2e !important;
  border-color: #2d3748 !important;
}

body[data-theme="dark"] .modern-drawer .el-descriptions__label {
  color: #94a3b8 !important;
}

body[data-theme="dark"] .modern-drawer .el-descriptions__content {
  color: #ffffff !important;
}

body[data-theme="dark"] .modern-drawer .el-divider__text {
  color: #94a3b8 !important;
}

body[data-theme="dark"] .modern-drawer .el-timeline-item__content {
  color: #e2e8f0 !important;
}

body[data-theme="dark"] .modern-drawer .el-timeline-item__timestamp {
  color: #94a3b8 !important;
}
</style>
