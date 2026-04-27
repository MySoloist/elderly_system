<template>
  <div class="orders-manage">
    <div class="page-header">
      <div class="header-info">
        <h1>订单管理</h1>
        <p>实时处理社区老人的订餐需求与支付状态</p>
      </div>
    </div>

    <el-card class="main-card">
      <div class="table-toolbar">
        <el-radio-group v-model="statusFilter" size="large" class="modern-radio" @change="loadOrders">
          <el-radio-button label="全部" />
          <el-radio-button label="待支付" />
          <el-radio-button label="待配送" />
          <el-radio-button label="配送中" />
          <el-radio-button label="已完成" />
          <el-radio-button label="已取消" />
          <el-radio-button label="已预定" />
        </el-radio-group>
        <div class="right-actions">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="default"
            style="width: 240px"
            @change="loadOrders"
          />
          <el-button type="success" plain :icon="Download" @click="exportToExcel">导出</el-button>
        </div>
      </div>

      <el-table :data="orders" style="width: 100%" class="modern-table dark-theme-table" :style="tableStyle">
        <el-table-column label="交易ID" width="180">
          <template #default="scope">
            <span class="order-id">
              {{ scope.row.status === '待支付' || scope.row.status === '已取消' ? '' : 
                 scope.row.transactionId || '' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="订餐老人" width="150">
          <template #default="scope">
            <div class="elderly-info">
              <el-avatar :size="24" :style="{ backgroundColor: getAvatarColor(scope.row.elderlyName) }">
                {{ scope.row.elderlyName.charAt(0) }}
              </el-avatar>
              <span>{{ scope.row.elderlyName }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="餐品内容" show-overflow-tooltip>
          <template #default="scope">
            <div class="meal-items">
              <div v-for="(item, index) in scope.row.items" :key="index" class="meal-item">
                {{ item.meal_name }} ×{{ item.quantity }}
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="实付金额" width="120">
          <template #default="scope">
            <span class="amount">￥{{ scope.row.amount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="orderTime" label="下单时间" width="180" />
        <el-table-column label="预计配送时间" width="180">
          <template #default="scope">
            <span v-if="scope.row.scheduledTime" class="scheduled-time">
              {{ scope.row.scheduledTime }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="订单状态" width="120">
          <template #default="scope">
            <transition name="status-change">
              <div class="status-dot-wrapper" :key="scope.row.status">
                <span class="status-dot" :class="getStatusClass(scope.row.status)"></span>
                <span class="status-text">{{ scope.row.status }}</span>
              </div>
            </transition>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <div class="action-btns">
              <el-button size="small" link type="primary" @click="handleViewDetail(scope.row)">查看详情</el-button>
              <transition name="fade">
                <el-button 
                  v-if="scope.row.status === '待配送'" 
                  size="small" 
                  type="primary" 
                  round
                  @click="handleDispatch(scope.row)"
                  :key="scope.row.orderId"
                >
                  指派配送
                </el-button>
              </transition>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          background
          layout="total, prev, pager, next, jumper"
          :total="pagination.total"
          :page-size="pagination.limit"
          :current-page="pagination.page"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 订单详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="订单详情"
      width="600px"
      center
    >
      <el-card v-if="selectedOrder" class="order-info-card">
        <div class="order-details">
          <div class="detail-section">
            <h3 class="section-title">订单基本信息</h3>
            <div class="detail-item">
              <span class="label">订单编号：</span>
              <span class="value">{{ selectedOrder.orderId }}</span>
            </div>
            <div class="detail-item">
              <span class="label">订餐老人：</span>
              <span class="value">{{ selectedOrder.elderlyName }}</span>
            </div>
            <div class="detail-item">
              <span class="label">下单时间：</span>
              <span class="value">{{ selectedOrder.orderTime }}</span>
            </div>
            <div class="detail-item">
              <span class="label">订单状态：</span>
              <span class="value">
                <span class="status-dot" :class="getStatusClass(selectedOrder.status)"></span>
                {{ selectedOrder.status }}
              </span>
            </div>
          </div>

          <div class="detail-section">
            <h3 class="section-title">餐品信息</h3>
            <div class="detail-item">
              <span class="label">餐品内容：</span>
              <span class="value">{{ selectedOrder.mealName }}</span>
            </div>
            <div class="detail-item">
              <span class="label">实付金额：</span>
              <span class="value amount">￥{{ selectedOrder.amount }}</span>
            </div>
          </div>

          <div class="detail-section">
            <h3 class="section-title">配送信息</h3>
            <div class="detail-item">
              <span class="label">配送地址：</span>
              <span class="value">{{ selectedOrder.address || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">联系电话：</span>
              <span class="value">{{ selectedOrder.phone || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">配送员：</span>
              <span class="value">{{ selectedOrder.deliveryStaff || '未分配' }}</span>
            </div>
          </div>
        </div>
      </el-card>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 指派配送弹窗 -->
    <el-dialog
      v-model="dispatchDialogVisible"
      title="指派配送员"
      width="500px"
      center
    >
      <el-form :model="dispatchForm" label-width="120px">
        <el-form-item label="订单信息">
          <el-card v-if="currentOrder" class="order-info-card">
            <div class="order-details">
              <div class="detail-item">
                <span class="label">订单编号：</span>
                <span class="value">#{{ currentOrder.orderId.slice(-8) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">订餐老人：</span>
                <span class="value">{{ currentOrder.elderlyName }}</span>
              </div>
              <div class="detail-item">
                <span class="label">餐品内容：</span>
                <span class="value">{{ currentOrder.mealName }}</span>
              </div>
              <div class="detail-item">
                <span class="label">金额：</span>
                <span class="value amount">￥{{ currentOrder.amount }}</span>
              </div>
            </div>
          </el-card>
        </el-form-item>
        
        <el-form-item label="选择配送员">
          <el-select v-model="dispatchForm.deliveryStaffId" placeholder="请选择配送员">
            <el-option
              v-for="staff in deliveryStaffList"
              :key="staff.id"
              :label="staff.name"
              :value="staff.id"
              :disabled="!staff.available"
            >
              <div class="staff-option">
                <el-avatar :size="24" :style="{ backgroundColor: getAvatarColor(staff.name) }">
                  {{ staff.name.charAt(0) }}
                </el-avatar>
                <span>{{ staff.name }} - {{ staff.phone }}</span>
                <el-tag :type="staff.status === 'online' || staff.status === 'available' ? 'success' : 'warning'" size="small">
                  {{ staff.status === 'online' || staff.status === 'available' ? '在线' : '离线' }}
                </el-tag>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="预计配送时间">
          <el-time-picker
            v-model="dispatchForm.estimatedTime"
            placeholder="选择时间"
            format="HH:mm"
            value-format="HH:mm"
          />
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            v-model="dispatchForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入配送备注信息"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dispatchDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmDispatch">确认指派</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { adminService } from '../api'
import * as XLSX from 'xlsx'

const statusFilter = ref('全部')
const dateRange = ref([])
const dispatchDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentOrder = ref(null)
const selectedOrder = ref(null)
const loading = ref(false)
const pagination = ref({
  page: 1,
  limit: 20,
  total: 0
})

// 指派配送表单
const dispatchForm = ref({
  deliveryStaffId: '',
  estimatedTime: '13:00',
  remark: ''
})

// 数据存储
const orders = ref([])
const deliveryStaffList = ref([])

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

// 加载订单列表
const loadOrders = async () => {
  try {
    loading.value = true
    
    const params = {
      page: pagination.value.page,
      limit: pagination.value.limit
    }
    
    // 添加状态筛选
    if (statusFilter.value !== '全部') {
      if (statusFilter.value === '已预定') {
        params.order_type = 'scheduled'
      } else {
        const statusMap = {
          '待支付': 'pending_payment',
          '待配送': 'pending_accept',
          '配送中': 'delivering',
          '已完成': 'completed',
          '已取消': 'cancelled'
        }
        params.status = statusMap[statusFilter.value]
      }
    }
    
    // 添加日期范围筛选
    if (dateRange.value.length === 2) {
      params.start_date = dateRange.value[0].toISOString().split('T')[0]
      params.end_date = dateRange.value[1].toISOString().split('T')[0]
    }
    
    const response = await adminService.getOrders(params)
    orders.value = response.items.map(item => ({
      id: item.id,
      orderId: item.order_no,
      transactionId: item.transaction_id || '',
      elderlyName: item.elderly_name,
      mealName: '', // 需要从订单详情中获取
      amount: item.total_amount,
      orderTime: new Date(item.created_at).toLocaleString('zh-CN'),
      scheduledTime: item.scheduled_time ? new Date(item.scheduled_time).toLocaleString('zh-CN') : '',
      status: getStatusText(item.status),
      address: item.delivery_address,
      phone: '', // 需要从老人信息中获取
      deliveryStaff: item.deliverer_name,
      items: item.items || [],
      orderType: item.order_type
    }))
    
    pagination.value.total = response.total
  } catch (error) {
    ElMessage.error('加载订单列表失败')
    console.error('加载订单列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载配送员列表
const loadDeliveryStaffList = async () => {
  try {
    const response = await adminService.getDelivererUsers({ limit: 100 })
    deliveryStaffList.value = response.items.map(item => ({
      id: item.id,
      name: item.profile.name,
      phone: item.profile.phone,
      status: item.profile.status || '离线', // 使用数据库中的实际状态
      available: item.profile.status === 'online' || item.profile.status === 'available' // 判断是否可用
    }))
  } catch (error) {
    console.error('加载配送员列表失败:', error)
  }
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending_payment': '待支付',
    'pending_accept': '待配送',
    'delivering': '配送中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

const getStatusClass = (status) => {
  const map = {
    '待支付': 'unpaid',
    '待配送': 'pending',
    '配送中': 'delivering',
    '已完成': 'completed',
    '已取消': 'cancelled'
  }
  return map[status] || ''
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

// 查看订单详情
const handleViewDetail = async (row) => {
  try {
    // 使用真实的订单ID
    const response = await adminService.getOrderDetail(row.id)
    
    // 构建订单详情数据
    selectedOrder.value = {
      orderId: response.order_no,
      elderlyName: response.elderly.name,
      mealName: response.items.map(item => `${item.meal_name} x${item.quantity}`).join(', '),
      amount: response.total_amount,
      orderTime: new Date(response.created_at).toLocaleString('zh-CN'),
      status: getStatusText(response.status),
      address: response.delivery_address,
      phone: response.elderly.phone,
      deliveryStaff: response.delivery?.deliverer_name || ''
    }
    
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('加载订单详情失败')
    console.error('加载订单详情失败:', error)
  }
}

// 打开指派配送弹窗
const handleDispatch = (row) => {
  currentOrder.value = row
  dispatchDialogVisible.value = true
}

// 确认指派配送
const confirmDispatch = async () => {
  if (!dispatchForm.value.deliveryStaffId) {
    ElMessage.warning('请选择配送员')
    return
  }
  
  // 验证所选配送员是否在线
  const selectedStaff = deliveryStaffList.value.find(staff => staff.id === dispatchForm.value.deliveryStaffId)
  if (!selectedStaff || !selectedStaff.available) {
    ElMessage.warning('只能选择在线的配送员')
    return
  }
  
  try {
    // 使用真实的订单ID
    const assignData = {
      order_id: currentOrder.value.id,
      deliverer_id: dispatchForm.value.deliveryStaffId,
      estimated_time: dispatchForm.value.estimatedTime,
      remark: dispatchForm.value.remark
    }
    
    await adminService.assignDelivery(assignData)
    
    // 显示成功消息
    ElMessage.success('指派配送成功！')
    
    // 关闭弹窗
    dispatchDialogVisible.value = false
    
    // 重置表单
    dispatchForm.value = {
      deliveryStaffId: '',
      estimatedTime: '13:00',
      remark: ''
    }
    
    // 重新加载订单列表
    await loadOrders()
  } catch (error) {
    ElMessage.error('指派配送失败')
    console.error('指派配送失败:', error)
  }
}

// 分页变化
const handleSizeChange = (val) => {
  pagination.value.limit = val
  pagination.value.page = 1
  loadOrders()
}

const handleCurrentChange = (val) => {
  pagination.value.page = val
  loadOrders()
}

// 导出Excel
const exportToExcel = () => {
  try {
    if (orders.value.length === 0) {
      ElMessage.warning('没有数据可以导出')
      return
    }
    
    // 准备导出数据
    const exportData = orders.value.map(order => ({
      '订单编号': order.orderId,
      '交易ID': order.transactionId || '-',
      '订餐老人': order.elderlyName,
      '餐品内容': order.mealName || '未知餐品',
      '实付金额': `￥${order.amount}`,
      '下单时间': order.orderTime,
      '订单状态': order.status,
      '配送地址': order.address || '-',
      '联系电话': order.phone || '-',
      '配送员': order.deliveryStaff || '未分配'
    }))
    
    // 创建工作簿
    const ws = XLSX.utils.json_to_sheet(exportData)
    
    // 创建工作簿
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '订单数据')
    
    // 设置列宽
    const colWidths = [
      { wch: 20 }, // 订单编号
      { wch: 20 }, // 交易ID
      { wch: 15 }, // 订餐老人
      { wch: 30 }, // 餐品内容
      { wch: 12 }, // 实付金额
      { wch: 20 }, // 下单时间
      { wch: 12 }, // 订单状态
      { wch: 30 }, // 配送地址
      { wch: 15 }, // 联系电话
      { wch: 15 }  // 配送员
    ]
    ws['!cols'] = colWidths
    
    // 生成文件名
    const timestamp = new Date().toLocaleString('zh-CN', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    }).replace(/[:\/]/g, '-')
    
    const fileName = `订单数据_${timestamp}.xlsx`
    
    // 下载文件
    XLSX.writeFile(wb, fileName)
    
    ElMessage.success('导出成功！')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败，请稍后重试')
  }
}

// 组件挂载时加载数据
onMounted(async () => {
  updateTableStyles()
  await Promise.all([
    loadOrders(),
    loadDeliveryStaffList()
  ])
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.action-btns {
  display: flex;
  align-items: center;
  gap: 8px;
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

.header-info h1 {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 8px 0;
}

.header-info p {
  color: var(--text-light);
  margin: 0;
}

.header-stats {
  display: flex;
  align-items: center;
  gap: 24px;
  background: var(--bg-secondary);
  padding: 16px 30px;
  border-radius: 20px;
  box-shadow: var(--shadow-sm);
}

.mini-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mini-stat .label {
  font-size: 12px;
  color: var(--text-light);
  margin-bottom: 4px;
}

.mini-stat .value {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-main);
}

.mini-stat .value.highlight {
  color: var(--primary-color);
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.right-actions {
  display: flex;
  gap: 12px;
}

.order-id {
  font-family: 'Courier New', Courier, monospace;
  font-weight: 700;
  color: var(--text-regular);
}

.elderly-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.amount {
  font-weight: 800;
  color: var(--text-main);
}

.status-dot-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.unpaid { background: #b2bec3; }
.status-dot.pending { background: #ff6b6b; }
.status-dot.delivering { background: #45aaf2; }
.status-dot.completed { background: #4ecdc4; }
.status-dot.cancelled { background: #95a5a6; }

.status-text {
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
}

.pagination-wrapper {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

/* 订单信息卡片样式 */
.order-info-card {
  border: none !important;
  box-shadow: none !important;
}

.order-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-item .label {
  font-size: 13px;
  color: #ffffff;
  font-weight: 600;
}

.detail-item .value {
  font-size: 14px;
  color: #ffffff;
  font-weight: 500;
}

.detail-item .value.amount {
  color: #ffffff;
  font-weight: 700;
}

/* 详情弹窗样式 */
.detail-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 16px 0;
  color: #ffffff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 8px;
}

/* 配送员选项样式 */
.staff-option {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.staff-option span {
  flex: 1;
  font-size: 14px;
}

/* 状态变化过渡动画 */
.status-change-enter-active,
.status-change-leave-active {
  transition: all 0.3s ease;
}

.status-change-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.status-change-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* 淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
