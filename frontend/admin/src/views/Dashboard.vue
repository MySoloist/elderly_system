<template>
  <div class="dashboard">
    <!-- 加载状态显示骨架屏 -->
    <SkeletonLoader 
      v-if="loading" 
      type="stats" 
      :stats="8" 
      :showTitle="false"
    />
    
    <!-- 实际内容 -->
    <template v-else>
      <!-- 欢迎栏 -->
      <div class="welcome-bar">
        <div class="welcome-text">
          <h1 class="welcome-title">早安，管理员 ☀️</h1>
          <p class="welcome-subtitle">今天是 {{ currentDate }}，社区共有 <span class="highlight">{{ deliveringOrders }}</span> 位老人的餐点正在配送中。</p>
        </div>
        <div class="welcome-action">
          <el-button type="primary" size="large" class="welcome-button" @click="quickOrderDialogVisible = true">
            <el-icon><Plus /></el-icon>快速下单
          </el-button>
        </div>
      </div>

      <!-- 统计卡片 -->
      <el-row :gutter="24" class="stat-row">
        <el-col :span="6" v-for="(item, index) in stats" :key="item.title">
          <div class="stat-card glass-effect" :style="{ animationDelay: index * 0.1 + 's' }">
            <div class="stat-icon" :style="{ background: item.bg }">
              <el-icon size="28" :color="item.color"><component :is="item.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <span class="stat-label">{{ item.title }}</span>
              <div class="stat-value-group">
                <span class="stat-value gradient-text">{{ item.value }}</span>
                <span class="stat-unit">{{ item.unit }}</span>
              </div>
              <div class="stat-trend" :class="item.trendType">
                <el-icon><CaretTop v-if="item.trendType === 'up'" /><CaretBottom v-else /></el-icon>
                {{ item.trend }}% 较昨日
              </div>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="24" class="mt-30">
        <!-- 订单数量趋势图 -->
        <el-col :span="12">
          <el-card class="main-card">
            <template #header>
              <div class="card-header">
                <div class="title-group">
                  <span class="title gradient-text">订单数量趋势</span>
                  <span class="subtitle">展示最近7天订单数量变化</span>
                </div>
              </div>
            </template>
            <div class="chart-container">
              <div v-if="trendData.length > 0" class="order-trend-chart">
                <div v-for="(item, index) in trendData" :key="index" class="chart-column" :style="{ animationDelay: index * 0.05 + 's' }">
                  <div class="column-bar" :style="{ height: (item.orders * 8) + 'px', opacity: item.orders > 0 ? 0.8 : 0 }"></div>
                  <div class="column-tooltip">{{ item.orders }}单</div>
                  <span class="column-label">{{ item.date }}</span>
                </div>
              </div>
              <div v-else class="empty-chart">
                <text class="empty-text">暂无数据</text>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 每日收益图表 -->
        <el-col :span="12">
          <el-card class="main-card">
            <template #header>
              <div class="card-header">
                <div class="title-group">
                  <span class="title gradient-text">每日收益趋势</span>
                  <span class="subtitle">展示最近7天收益变化</span>
                </div>
              </div>
            </template>
            <div class="chart-container">
              <div v-if="revenueData.length > 0" class="revenue-trend-chart">
                <div v-for="(item, index) in revenueData" :key="index" class="chart-column" :style="{ animationDelay: index * 0.05 + 's' }">
                  <div class="column-bar" :style="{ height: (item.revenue / 5) + 'px', opacity: item.revenue > 0 ? 0.8 : 0 }"></div>
                  <div class="column-tooltip">¥{{ item.revenue }}</div>
                  <span class="column-label">{{ item.date }}</span>
                </div>
              </div>
              <div v-else class="empty-chart">
                <text class="empty-text">暂无数据</text>
              </div>
            </div>
          </el-card>
        </el-col>


      </el-row>
    </template>
  </div>

  <!-- 快速下单弹窗 -->
  <el-dialog
    v-model="quickOrderDialogVisible"
    title="快速下单"
    width="600px"
    center
  >
    <el-form :model="orderForm" label-width="120px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="选择老人">
            <el-select v-model="orderForm.elderlyId" placeholder="请选择老人">
              <el-option
                v-for="elderly in elderlyList"
                :key="elderly.id"
                :label="elderly.name"
                :value="elderly.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="选择餐品">
            <el-select v-model="orderForm.mealId" placeholder="请选择餐品">
              <el-option
                v-for="meal in mealList"
                :key="meal.id"
                :label="meal.name"
                :value="meal.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="配送日期">
            <el-date-picker
              v-model="orderForm.deliveryDate"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="配送时间">
            <el-time-picker
              v-model="orderForm.deliveryTime"
              placeholder="选择时间"
              format="HH:mm"
              value-format="HH:mm"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="备注">
        <el-input
          v-model="orderForm.remark"
          type="textarea"
          :rows="3"
          placeholder="请输入备注信息"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="quickOrderDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitOrder">提交订单</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import { adminService } from '../api'

// 加载状态
const loading = ref(true)

// 快速下单弹窗
const quickOrderDialogVisible = ref(false)

// 表单数据
const orderForm = reactive({
  elderlyId: '',
  mealId: '',
  deliveryDate: new Date(),
  deliveryTime: '12:00',
  remark: ''
})

// 数据存储
const stats = ref([])
const trendData = ref([])
const revenueData = ref([])
const deliveringOrders = ref(0)
const elderlyList = ref([])
const mealList = ref([])

// 获取当前日期
const currentDate = computed(() => {
  const now = new Date()
  return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`
})

// 加载仪表盘数据
const loadDashboardData = async () => {
  try {
    loading.value = true
    const response = await adminService.getDashboard()
    
    // 检查trendData字段
    if (response.trendData) {
      trendData.value = response.trendData
    } else {
      trendData.value = []
    }
    
    // 检查收益数据
    if (response.revenueData) {
      revenueData.value = response.revenueData
    } else {
      revenueData.value = []
    }
    
    // 过滤掉不需要的统计卡片
    const statsList = response.stats || []
    stats.value = statsList.filter(item => {
      return !['今日订单总数', '平均配送时长', '好评率', '社区数量'].includes(item.title)
    })
    
    deliveringOrders.value = response.deliveringOrders || 0
  } catch (error) {
    ElMessage.error('加载仪表盘数据失败')
    console.error('加载仪表盘数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载老人列表
const loadElderlyList = async () => {
  try {
    const response = await adminService.getElderlyUsers({ limit: 100 })
    elderlyList.value = response.items.map(item => ({
      id: item.id,
      name: item.profile.name,
      address: item.profile.address
    }))
  } catch (error) {
    console.error('加载老人列表失败:', error)
  }
}

// 加载餐品列表
const loadMealList = async () => {
  try {
    const response = await adminService.getMeals({ limit: 100 })
    mealList.value = response.items.map(item => ({
      id: item.id,
      name: item.name
    }))
  } catch (error) {
    console.error('加载餐品列表失败:', error)
  }
}

// 提交订单
const submitOrder = async () => {
  try {
    // 获取选中老人的地址
    const selectedElderly = elderlyList.value.find(elderly => elderly.id === orderForm.elderlyId)
    const deliveryAddress = selectedElderly ? selectedElderly.address : ''
    
    const orderData = {
      elderly_id: orderForm.elderlyId,
      items: [{
        meal_id: orderForm.mealId,
        quantity: 1
      }],
      delivery_address: deliveryAddress,
      notes: orderForm.remark,
      payment_method: 'cash'
    }
    
    console.log('发送的订单数据:', orderData)
    
    const response = await adminService.quickOrder(orderData)
    console.log('订单创建成功:', response)
    ElMessage.success('快速下单成功')
    quickOrderDialogVisible.value = false
    
    // 重置表单
    orderForm.elderlyId = ''
    orderForm.mealId = ''
    orderForm.remark = ''
    
    // 重新加载数据
    await loadDashboardData()
  } catch (error) {
    ElMessage.error('下单失败')
    console.error('下单失败:', error)
    console.error('错误详情:', error.response)
  }
}

// 组件挂载时加载数据
onMounted(async () => {
  await Promise.all([
    loadDashboardData(),
    loadElderlyList(),
    loadMealList()
  ])
})

</script>

<style scoped>
.welcome-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-xl);
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

/* 日期选择器深色模式样式 */
:deep(.el-popper),
:deep(.el-date-picker__popper),
:deep(.el-popper.is-light),
:deep(.el-popper__inner) {
  background: var(--bg-secondary) !important;
  border-color: var(--border-color) !important;
}

:deep(.el-date-picker__content),
:deep(.el-date-table),
:deep(.el-month-table),
:deep(.el-year-table) {
  background: var(--bg-secondary) !important;
}

:deep(.el-date-table th) {
  color: var(--text-secondary) !important;
}

:deep(.el-date-table td) {
  color: var(--text-primary) !important;
}

:deep(.el-date-table td.today) {
  color: var(--primary-color) !important;
}

:deep(.el-date-table td.current:not(.disabled):not(.range-start):not(.range-end)) {
  background: var(--primary-color) !important;
  color: white !important;
}

:deep(.el-date-table td:not(.disabled):hover) {
  background: rgba(99, 102, 241, 0.1) !important;
}

.welcome-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
  transition: left var(--transition-slow);
}

.welcome-bar:hover::before {
  left: 100%;
}

.welcome-text {
  flex: 1;
}

.welcome-title {
  font-size: 32px;
  font-weight: 900;
  margin: 0 0 var(--spacing-sm) 0;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-subtitle {
  color: var(--text-secondary);
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  line-height: 1.5;
}

.welcome-subtitle .highlight {
  color: var(--primary-color);
  font-weight: 700;
  font-size: 18px;
}

.welcome-action {
  position: relative;
  z-index: 1;
}

.welcome-button {
  padding: var(--spacing-md) var(--spacing-xl) !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  border-radius: var(--radius-full) !important;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark)) !important;
  border: none !important;
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
  transition: all var(--transition-normal);
}

.welcome-button:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 12px 35px rgba(99, 102, 241, 0.5);
}

.stat-row {
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  border-radius: var(--radius-xl);
  transition: all var(--transition-normal);
  animation: fadeInUp 0.6s ease-out;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
}

.stat-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: var(--shadow-xl);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.stat-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left var(--transition-normal);
}

.stat-card:hover .stat-icon::before {
  left: 100%;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1);
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: var(--text-muted);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value-group {
  margin: var(--spacing-xs) 0;
  display: flex;
  align-items: baseline;
  gap: var(--spacing-xs);
}

.stat-value {
  font-size: 32px;
  font-weight: 900;
  line-height: 1;
}

.stat-unit {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-trend {
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-full);
}

.stat-trend.up { 
  color: var(--secondary-color);
  background: rgba(16, 185, 129, 0.1);
}

.stat-trend.down { 
  color: var(--primary-color);
  background: rgba(99, 102, 241, 0.1);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.main-card {
  height: 480px;
  position: relative;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-group {
  display: flex;
  flex-direction: column;
}

.title-group .title {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: var(--spacing-xs);
}

.title-group .subtitle {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}

.chart-container {
  height: 380px;
  display: flex;
  align-items: flex-end;
  padding-top: var(--spacing-lg);
  position: relative;
}

.chart-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.order-trend-chart, .revenue-trend-chart {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 0 var(--spacing-md);
  position: relative;
  z-index: 1;
}

.chart-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  max-width: 50px;
  animation: growUp 0.8s ease-out;
}

.chart-column:hover {
  transform: translateY(-4px);
}

.column-bar {
  width: 100%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
  border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-sm);
  position: relative;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.column-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left var(--transition-normal);
}

.column-bar:hover::before {
  left: 100%;
}

.column-bar:hover {
  opacity: 1 !important;
  transform: scaleX(1.15) translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.column-tooltip {
  position: absolute;
  top: -35px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: #fff;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  opacity: 0;
  transition: all 0.3s ease;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  z-index: 10;
}

.chart-column:hover .column-tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(-5px);
}

.column-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
  text-align: center;
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  background: rgba(99, 102, 241, 0.05);
}

@keyframes growUp {
  from {
    opacity: 0;
    transform: scaleY(0);
  }
  to {
    opacity: 1;
    transform: scaleY(1);
  }
}

.mt-30 { margin-top: var(--spacing-xl); }

.empty-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: var(--text-muted);
  font-size: 16px;
}

.empty-text {
  text-align: center;
}
</style>
