<template>
  <div class="delivery-staff">
    <!-- 欢迎栏 -->
    <div class="welcome-bar">
      <div class="welcome-text">
        <h1 class="welcome-title">配送员信息管理</h1>
        <p class="welcome-subtitle">管理配送人员信息和工作状态</p>
      </div>
      <div class="welcome-action">
        <el-button type="primary" size="large" class="welcome-button" @click="showAddUserDialog = true">
          <el-icon><Plus /></el-icon>添加配送员
        </el-button>
      </div>
    </div>

    <!-- 筛选和搜索 -->
    <div class="filter-section">
      <el-card class="filter-card">
        <div class="filter-content">
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              placeholder="搜索姓名、手机号或工号"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          <div class="filter-controls">
            <el-select v-model="statusFilter" placeholder="选择状态" clearable>
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
          </el-select>
            <el-select v-model="areaFilter" placeholder="选择区域" clearable>
              <el-option label="城东区域" value="east" />
              <el-option label="城西区域" value="west" />
              <el-option label="城南区域" value="south" />
              <el-option label="城北区域" value="north" />
            </el-select>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 配送员列表 -->
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <span class="title gradient-text">配送员信息列表</span>
          <div class="header-stats">
            <div class="stat-item">
              <span class="stat-value">{{ staff.length }}</span>
              <span class="stat-label">总配送员</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ onlineStaffCount }}</span>
              <span class="stat-label">在线人数</span>
            </div>
          </div>
        </div>
      </template>
      <el-table :data="filteredStaff" stripe class="dark-theme-table" :style="tableStyle">
        <el-table-column prop="id" label="工号" width="100" />
        <el-table-column label="配送员信息" min-width="200">
          <template #default="scope">
            <div class="user-info">
              <el-avatar :size="40" :style="{ backgroundColor: getAvatarColor(scope.row.name) }">
                {{ scope.row.name.charAt(0) }}
              </el-avatar>
              <div class="user-details">
                <div class="username">{{ scope.row.name }}</div>
                <div class="user-phone">{{ scope.row.phone }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="负责区域" width="200  ">
          <template #default="scope">
            <el-tag type="info">{{ getAreaName(scope.row.area) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="车辆类型" width="120">
          <template #default="scope">
            <el-tag type="success">{{ scope.row.vehicleType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="今日订单" width="120">
          <template #default="scope">
            <span class="order-count">{{ scope.row.todayOrders }}</span>
          </template>
        </el-table-column>
        <el-table-column label="评分" width="220">
          <template #default="scope">
            <el-rate :model-value="scope.row.rating" disabled show-score text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="320">
          <template #default="scope">
            <div class="action-btns">
              <el-button type="primary" size="small" @click="editStaff(scope.row)" style="white-space: nowrap; margin-left: 10px;">
                <el-icon><Edit /></el-icon>编辑
              </el-button>
              <el-button type="success" size="small" @click="scheduleStaff(scope.row)" style="white-space: nowrap;">
                <el-icon><Calendar /></el-icon>排班
              </el-button>
              <el-button type="warning" size="small" @click="locateStaff(scope.row)" style="white-space: nowrap;">
                <el-icon><LocationFilled /></el-icon>定位
              </el-button>
              <el-button type="danger" size="small" @click="deleteStaff(scope.row)" style="white-space: nowrap;">
                <el-icon><Delete /></el-icon>删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredStaff.length"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑配送员对话框 -->
    <el-dialog
      v-model="showAddUserDialog"
      :title="isEditMode ? '编辑配送员' : '添加配送员'"
      width="500px"
    >
      <el-form :model="staffForm" label-width="100px" ref="formRef" :rules="rules">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="staffForm.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input v-model="staffForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="负责区域" prop="area">
          <el-select v-model="staffForm.area" placeholder="请选择负责区域">
            <el-option label="城东区域" value="east" />
            <el-option label="城西区域" value="west" />
            <el-option label="城南区域" value="south" />
            <el-option label="城北区域" value="north" />
          </el-select>
        </el-form-item>
        <el-form-item label="车辆类型" prop="vehicleType">
          <el-select v-model="staffForm.vehicleType" placeholder="请选择车辆类型">
            <el-option label="自行车" value="自行车" />
            <el-option label="电动车" value="电动车" />
            <el-option label="摩托车" value="摩托车" />
            <el-option label="汽车" value="汽车" />
          </el-select>
        </el-form-item>

      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddUserDialog = false">取消</el-button>
          <el-button type="primary" @click="saveStaff">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 地图定位对话框 -->
    <el-dialog
      v-model="showMapDialog"
      :title="selectedStaffForMap ? `${selectedStaffForMap.name} 实时位置` : '配送员定位'"
      width="800px"
      top="5vh"
    >
      <div id="staff-location-map" style="width: 100%; height: 500px;"></div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showMapDialog = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Search, Edit, Delete, Calendar, LocationFilled } from '@element-plus/icons-vue'
import { adminService } from '../api'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

// 配送员数据
const staff = ref([])
const loading = ref(false)

// 路由
const router = useRouter()

// 加载配送员数据
const loadStaffData = async () => {
  try {
    loading.value = true
    const response = await adminService.getDelivererUsers({ limit: 100 })
    staff.value = response.items.map(item => ({
      userId: item.id, // 保存真实的用户ID
      id: `P${String(item.id).padStart(3, '0')}`, // 工号
      name: item.profile.name,
      phone: item.profile.phone,
      status: item.profile.status || 'offline', // 使用数据库中的真实状态
      area: item.profile.area ? item.profile.area.name : '未分配区域', // 使用数据库中的真实区域
      vehicleType: item.profile.vehicle_type || '未设置', // 添加车辆类型
      todayOrders: item.today_orders || 0, // 使用数据库中的真实今日订单数
      rating: item.rating || 0, // 使用数据库中的真实评分
      avatar: ''
    }))
  } catch (error) {
    ElMessage.error('加载配送员数据失败')
    console.error('加载配送员数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 筛选条件
const searchQuery = ref('')
const statusFilter = ref('')
const areaFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 对话框
const showAddUserDialog = ref(false)
const isEditMode = ref(false)
const formRef = ref(null)
const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  area: [
    { required: true, message: '请选择负责区域', trigger: 'change' }
  ],
  vehicleType: [
    { required: true, message: '请选择车辆类型', trigger: 'change' }
  ]
}
const staffForm = ref({
  name: '',
  phone: '',
  area: '',
  vehicleType: ''
})

// 地图弹窗
const showMapDialog = ref(false)
const selectedStaffForMap = ref(null)
const map = ref(null)
const staffLocation = ref(null)

// 计算属性
const filteredStaff = computed(() => {
  let result = staff.value
  
  // 搜索
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(s => 
      s.name.toLowerCase().includes(query) ||
      s.phone.includes(query) ||
      s.id.includes(query)
    )
  }
  
  // 状态筛选
  if (statusFilter.value) {
    result = result.filter(s => s.status === statusFilter.value)
  }
  
  // 区域筛选
  if (areaFilter.value) {
    result = result.filter(s => s.area === areaFilter.value)
  }
  
  return result
})

const onlineStaffCount = computed(() => {
  return staff.value.filter(s => s.status === 'online').length
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

// 方法
const handleSearch = () => {
  currentPage.value = 1
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page) => {
  currentPage.value = page
}

const getStatusType = (status) => {
  const types = {
    online: 'success',
    available: 'success',
    offline: 'info'
  }
  return types[status] || 'info'
}

const getStatusName = (status) => {
  const names = {
    online: '在线',
    available: '在线',
    offline: '离线'
  }
  return names[status] || status
}

const getAreaName = (area) => {
  const areas = {
    east: '城东区域',
    west: '城西区域',
    south: '城南区域',
    north: '城北区域'
  }
  return areas[area] || area
}

// 获取头像颜色
const getAvatarColor = (name) => {
  const colors = [
    '#4ecdc4', '#45aaf2', '#ff6b6b', '#fed330', 
    '#667eea', '#764ba2', '#4facfe', '#43e97b',
    '#fa709a', '#fee140', '#30cfd0', '#30a9de'
  ]
  
  // 根据用户名生成一个固定的颜色索引
  let hash = 0
  for (let i = 0; i< name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return colors[index]
}

const editStaff = (staffItem) => {
  isEditMode.value = true
  staffForm.value = { 
    id: staffItem.id,
    name: staffItem.name,
    phone: staffItem.phone,
    area: staffItem.area,
    vehicleType: staffItem.vehicleType
  }
  showAddUserDialog.value = true
}

const deleteStaff = (staffItem) => {
  // 这里可以添加确认对话框
  console.log('删除配送员:', staffItem.id)
}

const scheduleStaff = (staffItem) => {
  // 跳转到排班管理页面，传递配送员ID
  router.push({
    path: '/staff-schedule',
    query: { staffId: staffItem.id, staffName: staffItem.name }
  })
}

// 定位配送员
const locateStaff = async (staffItem) => {
  try {
    selectedStaffForMap.value = staffItem
    showMapDialog.value = true
    
    // 获取配送员位置
    const response = await adminService.getDelivererLocations({ deliverer_id: staffItem.userId })
    
    if (response.locations && response.locations.length > 0) {
      const location = response.locations[0]
      staffLocation.value = {
        lat: parseFloat(location.latitude),
        lng: parseFloat(location.longitude)
      }
      // 根据在线状态显示不同的提示（数据库中的状态是英文：online/offline）
      if (staffItem.status === 'online' || staffItem.status === 'available') {
        ElMessage.success(`已定位到${staffItem.name}的位置`)
      } else {
        ElMessage.warning('由于该配送员尚未登录，位置信息可能不准确')
      }
    } else {
      staffLocation.value = null
      ElMessage.warning(`${staffItem.name}暂无位置信息`)
    }
    
    // 无论是否有位置数据，都初始化地图
    setTimeout(() => {
      initMap()
    }, 100)
  } catch (error) {
    ElMessage.error('获取配送员位置失败')
    console.error('获取配送员位置失败:', error)
    // 即使API调用失败，也显示默认地图
    staffLocation.value = null
    setTimeout(() => {
      initMap()
    }, 100)
  }
}

// 初始化地图
const initMap = () => {
  console.log('开始初始化地图...')
  
  if (typeof BMap === 'undefined') {
    console.log('百度地图API尚未加载，等待重试...')
    setTimeout(initMap, 100)
    return
  }
  
  console.log('百度地图API已加载，开始创建地图...')
  
  // 获取地图容器元素
  const mapContainer = document.getElementById('staff-location-map')
  if (!mapContainer) {
    console.error('地图容器元素不存在')
    return
  }
  
  console.log('地图容器已找到，尺寸:', mapContainer.offsetWidth, 'x', mapContainer.offsetHeight)
  
  // 创建地图实例
  try {
    map.value = new BMap.Map('staff-location-map')
    console.log('地图实例创建成功')
    
    // 设置地图中心点
    const centerPoint = staffLocation.value ? 
      new BMap.Point(staffLocation.value.lng, staffLocation.value.lat) : 
      new BMap.Point(116.4074, 39.9042)
    
    console.log('地图中心点:', centerPoint.lng, centerPoint.lat)
    
    map.value.centerAndZoom(centerPoint, 15)
    console.log('地图已设置中心点和缩放级别')
    
    // 添加地图控件
    map.value.addControl(new BMap.NavigationControl())
    map.value.addControl(new BMap.ScaleControl())
    map.value.addControl(new BMap.MapTypeControl())
    map.value.enableScrollWheelZoom(true)
    console.log('地图控件已添加')
    
    // 添加配送员标记
    if (staffLocation.value) {
      const point = new BMap.Point(staffLocation.value.lng, staffLocation.value.lat)
      const marker = new BMap.Marker(point, {
        icon: new BMap.Icon('https://api.map.baidu.com/img/markers.png', new BMap.Size(23, 25), {
          offset: new BMap.Size(10, 25),
          imageOffset: new BMap.Size(0, 0 - 7 * 25)
        })
      })
      
      // 添加标记标签
      const label = new BMap.Label(selectedStaffForMap.value.name, {
        position: point,
        offset: new BMap.Size(0, -30)
      })
      label.setStyle({
        color: '#fff',
        backgroundColor: '#6366f1',
        borderRadius: '4px',
        padding: '4px 8px',
        fontSize: '12px',
        fontWeight: 'bold'
      })
      
      map.value.addOverlay(marker)
      map.value.addOverlay(label)
      console.log('配送员标记已添加')
    } else {
      console.log('暂无位置数据，只显示默认地图')
    }
    
  } catch (error) {
    console.error('地图初始化失败:', error)
    ElMessage.error('地图初始化失败，请刷新页面重试')
  }
}

const saveStaff = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (valid) {
      if (isEditMode.value) {
        // 更新配送员
        const userData = {
          profile: {
            name: staffForm.value.name,
            phone: staffForm.value.phone,
            vehicle_type: staffForm.value.vehicleType,
            area_id: staffForm.value.area === 'east' ? 1 : 
                    staffForm.value.area === 'west' ? 2 : 
                    staffForm.value.area === 'south' ? 3 : 4
          }
        }
        await adminService.updateUser(staffForm.value.id, userData)
        ElMessage.success('配送员信息更新成功')
        
        // 更新本地数据
        const index = staff.value.findIndex(s => s.id === staffForm.value.id)
        if (index !== -1) {
          staff.value[index] = { ...staff.value[index], ...staffForm.value }
        }
      } else {
        // 添加配送员
        const userData = {
          username: staffForm.value.phone || `deliverer_${Date.now()}`,
          password: '123456', // 默认密码
          user_type: 'deliverer',
          profile: {
            name: staffForm.value.name,
            phone: staffForm.value.phone,
            vehicle_type: staffForm.value.vehicleType,
            area_id: staffForm.value.area === 'east' ? 1 : 
                    staffForm.value.area === 'west' ? 2 : 
                    staffForm.value.area === 'south' ? 3 : 4
          }
        }
        await adminService.createUser(userData)
        ElMessage.success('配送员添加成功')
        
        // 重新加载数据
        await loadStaffData()
      }
      showAddUserDialog.value = false
      resetForm()
    }
  } catch (error) {
    console.error('保存配送员失败:', error)
    ElMessage.error('保存失败，请检查输入信息')
  }
}

const resetForm = () => {
  staffForm.value = {
    name: '',
    phone: '',
    area: '',
    vehicleType: ''
  }
  isEditMode.value = false
}

// 更新表格样式
const updateTableStyles = () => {
  // 使用更频繁的更新频率和更直接的DOM操作
  const intervalId = setInterval(() => {
    const isDark = document.documentElement.hasAttribute('data-theme')
    const tableElements = document.querySelectorAll('.dark-theme-table')
    
    tableElements.forEach(table => {
      // 获取表格的所有行和单元格
      const rows = table.querySelectorAll('.el-table__row')
      const cells = table.querySelectorAll('.el-table__row td')
      const bodyWrapper = table.querySelector('.el-table__body-wrapper')
      const tableBody = table.querySelector('.el-table__body')
      
      // 确保表格主体区域也使用正确的背景色
      if (bodyWrapper) {
        bodyWrapper.style.backgroundColor = isDark ? '#1a1a2e' : '#ffffff'
      }
      if (tableBody) {
        tableBody.style.backgroundColor = isDark ? '#1a1a2e' : '#ffffff'
      }
      
      rows.forEach((row, index) => {
        // 直接设置行的背景色
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
        // 使用setAttribute来设置带!important的样式
        const bgColor = isDark ? (index % 2 === 0 ? '#1a1a2e' : 'rgba(255, 255, 255, 0.05)') : 
                               (index % 2 === 0 ? '#ffffff' : 'rgba(99, 102, 241, 0.02)')
        row.setAttribute('style', `background-color: ${bgColor} !important; background: ${bgColor} !important;`)
      })
      
      // 确保所有单元格背景透明
      cells.forEach(cell => {
        cell.style.backgroundColor = 'transparent'
        cell.style.background = 'transparent'
        cell.setAttribute('style', 'background-color: transparent !important; background: transparent !important;')
      })
    })
    
    // 如果找不到表格元素，清除定时器
    if (tableElements.length === 0) {
      clearInterval(intervalId)
    }
  }, 5)
}

// 组件挂载时加载数据和设置表格样式
onMounted(async () => {
  await loadStaffData()
  updateTableStyles()
})
</script>

<style>
/* 全局样式 - 确保表格行在深色模式下正确显示 */
.el-table__row,
.el-table tr,
.el-table .el-table__row {
  background-color: var(--bg-secondary) !important;
}

.el-table__row:nth-child(even),
.el-table tr:nth-child(even),
.el-table .el-table__row:nth-child(even) {
  background-color: rgba(99, 102, 241, 0.02) !important;
}

[data-theme="dark"] .el-table__row,
[data-theme="dark"] .el-table tr,
[data-theme="dark"] .el-table .el-table__row {
  background-color: #1a1a2e !important;
}

[data-theme="dark"] .el-table__row:nth-child(even),
[data-theme="dark"] .el-table tr:nth-child(even),
[data-theme="dark"] .el-table .el-table__row:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.05) !important;
}

/* 移除表格边框 */
.el-table,
.el-table__header-wrapper,
.el-table__body-wrapper,
.el-table__footer-wrapper {
  border: none !important;
}

.el-table__header tr,
.el-table__header th {
  border: none !important;
}

.el-table__row td {
  border: none !important;
}

/* 确保单元格背景透明 */
.el-table__row td,
.el-table tr td,
.el-table .el-table__row td {
  background-color: transparent !important;
}

/* 最高优先级覆盖 */
.el-table .el-table__body .el-table__row {
  background-color: var(--bg-secondary) !important;
}

[data-theme="dark"] .el-table .el-table__body .el-table__row {
  background-color: #1a1a2e !important;
}

/* 自定义深色主题表格样式 - 最高优先级 */
.dark-theme-table,
.dark-theme-table .el-table__body-wrapper,
.dark-theme-table .el-table__body {
  background-color: var(--bg-secondary) !important;
}

.dark-theme-table .el-table__row,
.dark-theme-table .el-table__row.el-table__row--striped {
  background-color: var(--bg-secondary) !important;
}

.dark-theme-table .el-table__row:nth-child(even),
.dark-theme-table .el-table__row.el-table__row--striped:nth-child(even) {
  background-color: rgba(99, 102, 241, 0.02) !important;
}

[data-theme="dark"] .dark-theme-table,
[data-theme="dark"] .dark-theme-table .el-table__body-wrapper,
[data-theme="dark"] .dark-theme-table .el-table__body {
  background-color: #1a1a2e !important;
}

[data-theme="dark"] .dark-theme-table .el-table__row,
[data-theme="dark"] .dark-theme-table .el-table__row.el-table__row--striped {
  background-color: #1a1a2e !important;
}

[data-theme="dark"] .dark-theme-table .el-table__row:nth-child(even),
[data-theme="dark"] .dark-theme-table .el-table__row.el-table__row--striped:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.05) !important;
}

/* 确保单元格背景透明 */
.dark-theme-table .el-table__row td,
.dark-theme-table .el-table__row.el-table__row--striped td {
  background-color: transparent !important;
}
</style>

<style scoped>
.delivery-staff {
  padding: var(--spacing-xl);
}

.welcome-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.welcome-text {
  flex: 1;
}

.welcome-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.welcome-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.welcome-button {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: 14px;
  font-weight: 600;
}

.filter-section {
  margin-bottom: var(--spacing-xl);
}

.filter-card {
  margin-bottom: var(--spacing-lg);
}

.filter-content {
  display: flex;
  gap: var(--spacing-lg);
  align-items: center;
}

.search-box {
  flex: 1;
}

.filter-controls {
  display: flex;
  gap: var(--spacing-md);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-stats {
  display: flex;
  gap: var(--spacing-xl);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
  color: var(--primary-color);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-details {
  flex: 1;
}

.username {
  font-weight: 600;
  color: var(--text-primary);
}

.user-phone {
  font-size: 12px;
  color: var(--text-muted);
}

.order-count {
  font-weight: 600;
  color: var(--primary-color);
}

.action-btns {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  flex-wrap: wrap;
  min-height: 40px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
