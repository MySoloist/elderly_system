<template>
  <div class="delivery-manage">
    <div class="page-header">
      <div class="header-info">
        <h1>配送调度管理</h1>
        <p>实时监控配送员位置与订单送达进度</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" size="large" round @click="handleSmartRouting">
          <el-icon><Van /></el-icon>智能排线
        </el-button>
      </div>
    </div>

    <el-row :gutter="24">
      <!-- 配送员列表 -->
      <el-col :span="8">
        <el-card class="staff-card-v2">
          <template #header>
            <div class="card-header">
              <span class="title">配送团队 ({{ staffList.length }})</span>
              <el-button link type="primary" @click="handleManageStaff">管理人员</el-button>
            </div>
          </template>
          <div class="staff-list">
            <div v-for="staff in staffList" :key="staff.id" class="staff-item" :class="{ 'staff-item-selected': selectedStaff && selectedStaff.id === staff.id }" @click="handleStaffClick(staff)">
              <div class="staff-main">
                <el-avatar :size="48" :style="{ backgroundColor: getAvatarColor(staff.name) }">
                  {{ staff.name.charAt(0) }}
                </el-avatar>
                <div class="staff-info">
                  <div class="name-row">
                    <span class="name">{{ staff.name }}</span>
                    <el-tag :type="staff.status === '空闲' ? 'success' : 'warning'" size="small" effect="dark" round>
                      {{ staff.status }}
                    </el-tag>
                  </div>
                  <div class="phone">{{ staff.phone }}</div>
                  <div class="vehicle-type">车辆: {{ staff.vehicleType }}</div>
                </div>
              </div>
              <div class="staff-stats">
                <div class="stat-box">
                  <span class="val">{{ staff.todayOrders }}</span>
                  <span class="lab">今日单量</span>
                </div>
                <div class="stat-box">
                  <span class="val">{{ staff.rating }}</span>
                  <span class="lab">评分</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 调度地图 -->
      <el-col :span="16">
        <el-card class="map-card-v2">
          <template #header>
            <div class="card-header">
              <div class="title-group">
                <span class="title">实时调度中心</span>
                <span class="subtitle">当前共有 {{ activeOrderCount }} 个订单正在配送中</span>
              </div>
              <div class="map-controls">
                <el-checkbox-group v-model="mapLayers" size="small" @change="handleLayerChange">
                  <el-checkbox-button label="配送员" />
                  <el-checkbox-button label="订单点" />
                  <el-checkbox-button label="路线" />
                </el-checkbox-group>
              </div>
            </div>
          </template>
          <div class="map-container">
            <!-- 百度地图容器 -->
            <div id="baidu-map" class="baidu-map"></div>
            
            <div class="map-overlay">
              <div class="overlay-card">
                <h4>配送详情</h4>
                <p v-if="selectedStaff">配送员：{{ selectedStaff.name }}</p>
                <p v-if="selectedStaff">当前状态：{{ selectedStaff.status }}</p>
                <p v-if="selectedStaff">今日单量：{{ selectedStaff.todayOrders }}单</p>
                <p v-if="selectedStaff">评分：{{ selectedStaff.rating }}</p>
                <el-button v-if="selectedStaff" type="primary" size="small" block @click="handleContactStaff">联系配送员</el-button>
                <el-empty v-else description="请选择配送员" />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminService } from '../api'
import { Van, LocationFilled } from '@element-plus/icons-vue'

const mapLayers = ref(['配送员', '订单点'])
const staffList = ref([])
const selectedStaff = ref(null)
const loading = ref(false)
const map = ref(null) // 百度地图实例
const staffMarkers = ref([]) // 配送员标记点
const orderMarkers = ref([]) // 订单标记点
const activeOrderCount = ref(0) // 正在配送中的订单数量

// 获取正在配送中的订单数量
const loadActiveOrders = async () => {
  try {
    const response = await adminService.getOrders({ status: 'delivering', limit: 100 })
    console.log('获取配送中订单:', response)
    activeOrderCount.value = response.items ? response.items.length : 0
  } catch (error) {
    console.error('获取订单数量失败:', error)
    activeOrderCount.value = 0
  }
}

// 加载配送员列表
const loadDeliveryStaff = async () => {
  try {
    loading.value = true
    const response = await adminService.getDelivererUsers({ limit: 100 })
    console.log('API返回的配送员数据:', response.items)
    
    staffList.value = []
    
    // 逐个获取配送员信息和位置
    for (const item of response.items) {
      // 检查配送员是否有资料信息
      if (!item.profile || !item.profile.name) {
        console.warn(`配送员 ${item.id} (${item.username}) 没有完整的资料信息，跳过处理`)
        continue
      }
      
      console.log(`处理配送员: ${item.profile.name}, ID: ${item.id}`)
      try {
        // 获取配送员最新位置
        console.log(`调用getDelivererLocations API，deliverer_id: ${item.id}`)
        const locationResponse = await adminService.getDelivererLocations({ deliverer_id: item.id })
        console.log(`位置API返回:`, locationResponse)
        
        // 检查API返回的数据结构
        const locationsData = locationResponse.data || locationResponse
        console.log('位置数据:', locationsData)
        
        let location = null
        let isOnline = false
        
        // 根据 deliverer_profiles.status 判断在线状态
        const profileStatus = item.profile.status || 'offline'
        isOnline = profileStatus !== 'offline'
        
        // 获取配送员最新位置（仅用于显示）
        if (locationsData && locationsData.locations && locationsData.locations.length > 0) {
          const latestLocation = locationsData.locations[0]
          console.log('最新位置:', latestLocation)
          location = {
            lat: parseFloat(latestLocation.latitude),
            lng: parseFloat(latestLocation.longitude)
          }
          console.log('解析后的位置:', location)
        } else {
          console.log('位置数组为空')
        }
        
        const staff = {
            id: item.id,
            name: item.profile.name,
            phone: item.profile.phone,
            vehicleType: item.profile.vehicle_type || '未设置', // 添加车辆类型
            status: isOnline ? '在线' : '离线', // 根据 deliverer_profiles.status 判断在线状态
            todayOrders: Math.floor(Math.random() * 20), // 模拟今日单量
            rating: (4.5 + Math.random() * 0.6).toFixed(1), // 模拟评分
            location: location || {
              lat: 39.9042 + (Math.random() * 0.02 - 0.01),
              lng: 116.4074 + (Math.random() * 0.02 - 0.01)
            }
          }
        console.log('构建的配送员对象:', staff)
        staffList.value.push(staff)
      } catch (locationError) {
        console.error(`获取配送员 ${item.profile.name} 位置失败:`, locationError)
        // 使用默认位置
        const staff = {
          id: item.id,
          name: item.profile.name,
          phone: item.profile.phone,
          status: '离线',
          todayOrders: Math.floor(Math.random() * 20),
          rating: (4.5 + Math.random() * 0.6).toFixed(1),
          location: {
            lat: 39.9042 + (Math.random() * 0.02 - 0.01),
            lng: 116.4074 + (Math.random() * 0.02 - 0.01)
          }
        }
        staffList.value.push(staff)
      }
    }
    
    if (staffList.value.length > 0) {
      selectedStaff.value = staffList.value[0]
    }
    
    // 更新地图标记点
    updateMapMarkers()
  } catch (error) {
    ElMessage.error('加载配送员失败')
    console.error('加载配送员失败:', error)
  } finally {
    loading.value = false
  }
}

// 初始化百度地图
const initBaiduMap = () => {
  // 检查百度地图API是否加载完成
  const checkBMap = () => {
    if (typeof BMap !== 'undefined') {
      // 创建地图实例
      map.value = new BMap.Map('baidu-map')
      
      // 设置地图中心点（北京天安门）
      const centerPoint = new BMap.Point(116.4074, 39.9042)
      map.value.centerAndZoom(centerPoint, 13)
      
      // 添加地图控件
      map.value.addControl(new BMap.NavigationControl()) // 缩放控件
      map.value.addControl(new BMap.ScaleControl()) // 比例尺
      map.value.addControl(new BMap.MapTypeControl()) // 地图类型切换
      
      // 启用滚轮缩放
      map.value.enableScrollWheelZoom(true)
      
      // 更新地图标记点
      updateMapMarkers()
    } else {
      // 等待API加载完成
      setTimeout(checkBMap, 100)
    }
  }
  
  checkBMap()
}

// 更新地图标记点
const updateMapMarkers = () => {
  if (!map.value) return
  
  // 清除现有标记点
  staffMarkers.value.forEach(marker => map.value.removeOverlay(marker))
  orderMarkers.value.forEach(marker => map.value.removeOverlay(marker))
  staffMarkers.value = []
  orderMarkers.value = []
  
  // 添加配送员标记点
  if (mapLayers.value.includes('配送员')) {
    staffList.value.forEach(staff => {
      // 确保位置数据有效
      if (staff.location && staff.location.lat && staff.location.lng) {
        const point = new BMap.Point(staff.location.lng, staff.location.lat)
        const marker = new BMap.Marker(point, {
          icon: new BMap.Icon('https://api.map.baidu.com/img/markers.png', new BMap.Size(23, 25), {
            offset: new BMap.Size(10, 25),
            imageOffset: staff.status === '在线' ? new BMap.Size(0, 0 - 7 * 25) : new BMap.Size(0, 0 - 9 * 25)
          })
        })
        
        // 添加标记点点击事件
        marker.addEventListener('click', () => {
          handleStaffClick(staff)
        })
        
        // 添加标记点标签
        const label = new BMap.Label(staff.name, {
          position: point,
          offset: new BMap.Size(0, -30)
        })
        label.setStyle({
          color: '#fff',
          backgroundColor: staff.status === '在线' ? '#6366f1' : '#666',
          borderRadius: '4px',
          padding: '4px 8px',
          fontSize: '12px',
          fontWeight: 'bold'
        })
        
        map.value.addOverlay(marker)
        map.value.addOverlay(label)
        staffMarkers.value.push(marker)
      }
    })
  }
  
  // 添加订单标记点（模拟数据）
  if (mapLayers.value.includes('订单点')) {
    const orders = [
      { name: '幸福社区-张大爷', location: { lat: 39.9100, lng: 116.3950 } },
      { name: '幸福社区-王大爷', location: { lat: 39.9000, lng: 116.4100 } },
      { name: '阳光小区-李奶奶', location: { lat: 39.9050, lng: 116.4000 } },
      { name: '和谐家园-赵爷爷', location: { lat: 39.8950, lng: 116.4150 } }
    ]
    
    orders.forEach(order => {
      const point = new BMap.Point(order.location.lng, order.location.lat)
      const marker = new BMap.Marker(point, {
        icon: new BMap.Icon('https://api.map.baidu.com/img/markers.png', new BMap.Size(23, 25), {
          offset: new BMap.Size(10, 25),
          imageOffset: new BMap.Size(0, 0 - 10 * 25)
        })
      })
      
      // 添加标记点标签
      const label = new BMap.Label(order.name, {
        position: point,
        offset: new BMap.Size(0, -30)
      })
      label.setStyle({
        color: '#fff',
        backgroundColor: '#4ecdc4',
        borderRadius: '4px',
        padding: '4px 8px',
        fontSize: '12px',
        fontWeight: 'bold'
      })
      
      map.value.addOverlay(marker)
      map.value.addOverlay(label)
      orderMarkers.value.push(marker)
    })
  }
}

// 处理地图图层切换
const handleLayerChange = () => {
  updateMapMarkers()
}

// 处理配送员点击事件
const handleStaffClick = async (staff) => {
  selectedStaff.value = staff
  console.log('点击的配送员:', staff)
  
  // 如果地图已初始化
  if (map.value) {
    try {
      // 调用API获取配送员实时位置
      console.log('传递的配送员ID:', staff.id)
      const response = await adminService.getDelivererLocations({ deliverer_id: staff.id })
      console.log('API返回数据:', response)
      
      // 检查返回数据结构
      const locationsData = response.data || response
      console.log('位置数据:', locationsData)
      
      if (!locationsData || !locationsData.locations || locationsData.locations.length === 0) {
        ElMessage.warning(`${staff.name}暂无位置信息`)
        return
      }
      
      console.log('响应数据:', locationsData)
      const locations = locationsData.locations
      console.log('返回的位置数据:', locations)
      
      // 获取最新位置
      const latestLocation = locations[0]
      if (latestLocation && latestLocation.longitude && latestLocation.latitude) {
        const point = new BMap.Point(parseFloat(latestLocation.longitude), parseFloat(latestLocation.latitude))
        map.value.panTo(point) // 平滑移动到配送员位置
        map.value.setZoom(15) // 设置合适的缩放级别
        
        // 根据在线状态显示不同的提示
        if (staff.status === '在线') {
          ElMessage.success(`已定位到${staff.name}的位置`)
        } else {
          ElMessage.warning('由于该配送员尚未登录，位置信息可能不准确')
        }
        
        // 更新staff对象的位置信息
        staff.location = {
          lat: parseFloat(latestLocation.latitude),
          lng: parseFloat(latestLocation.longitude)
        }
        
        // 更新地图标记
        updateMapMarkers()
      } else {
        ElMessage.warning(`${staff.name}的位置信息不完整`)
      }
    } catch (error) {
      console.error('获取配送员位置失败:', error)
      ElMessage.error('获取位置信息失败')
    }
  }
}

// 处理管理人员按钮点击事件
const handleManageStaff = () => {
  ElMessage.info('管理人员功能开发中，敬请期待！')
}

// 处理智能排线按钮点击事件
const handleSmartRouting = () => {
  ElMessage.success('智能排线算法已启动，正在优化配送路线...')
}

// 处理联系配送员按钮点击事件
const handleContactStaff = () => {
  if (selectedStaff.value) {
    ElMessage.success(`正在拨打 ${selectedStaff.value.name} 的电话：${selectedStaff.value.phone}`)
  }
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



// 组件挂载时加载数据
onMounted(() => {
  // 先加载配送员数据
  loadDeliveryStaff()
  
  // 加载正在配送中的订单数量
  loadActiveOrders()
  
  // 初始化百度地图（延迟一下确保DOM已渲染）
  setTimeout(() => {
    initBaiduMap()
  }, 100)
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header-info h1 {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 8px 0;
}

.header-info p {
  color: var(--text-light);
  margin: 0;
}

.staff-card-v2 {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.staff-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.staff-item {
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: 20px;
  transition: all 0.3s;
}

.staff-item:hover {
  background: var(--bg-primary);
  box-shadow: var(--shadow-md);
  transform: scale(1.02);
}

.staff-item-selected {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1)) !important;
  border: 2px solid var(--primary-color);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
}

.staff-item-selected:hover {
  transform: scale(1.02);
}

.staff-main {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.name-row .name {
  font-weight: 800;
  font-size: 16px;
  color: white;
}

.phone {
  font-size: 12px;
  color: white;
}

.vehicle-type {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 2px;
}

.staff-stats {
  display: flex;
  justify-content: space-around;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-box .val {
  font-weight: 800;
  font-size: 16px;
  color: white;
}

.stat-box .lab {
  font-size: 10px;
  color: white;
  text-transform: uppercase;
}

.map-card-v2 {
  height: 600px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-group .title {
  font-size: 16px;
  font-weight: 700;
}

.title-group .subtitle {
  font-size: 12px;
  color: var(--text-light);
}

.map-container {
  height: 500px;
  background: var(--bg-primary);
  border-radius: 20px;
  position: relative;
  overflow: hidden;
}

.baidu-map {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 200px;
  z-index: 20;
}

.overlay-card {
  background: var(--bg-secondary);
  backdrop-filter: blur(10px);
  padding: 16px;
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
}

.overlay-card h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: white;
}

.overlay-card p {
  font-size: 12px;
  margin: 4px 0;
  color: white;
}
</style>
