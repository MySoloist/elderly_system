<template>
  <div class="quick-order">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">快速下单</h1>
      <el-button type="primary" @click="goBack">
        <el-icon><ArrowLeft /></el-icon>返回
      </el-button>
    </div>

    <!-- 下单表单 -->
    <el-card class="order-card">
      <el-form 
        :model="orderForm" 
        label-width="120px"
        :rules="formRules"
        ref="orderFormRef"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="选择老人" prop="elderlyId">
              <el-select v-model="orderForm.elderlyId" placeholder="请选择老人">
                <el-option
                  v-for="elderly in elderlyList"
                  :key="elderly.id"
                  :label="elderly.name"
                  :value="elderly.id"
                >
                  <div class="elderly-option">
                    <el-avatar :size="24" :style="{ backgroundColor: getAvatarColor(elderly.name) }">
                      {{ elderly.name.charAt(0) }}
                    </el-avatar>
                    <span>{{ elderly.name }}</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="选择餐品" prop="mealId">
              <el-select v-model="orderForm.mealId" placeholder="请选择餐品">
                <el-option
                  v-for="meal in mealList"
                  :key="meal.id"
                  :label="meal.name"
                  :value="meal.id"
                >
                  <div class="meal-option">
                    <span>{{ meal.name }}</span>
                    <span class="price">￥{{ meal.price }}</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="配送日期" prop="deliveryDate">
              <el-date-picker
                v-model="orderForm.deliveryDate"
                type="date"
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                :disabled-date="disabledDate"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="配送时间" prop="deliveryTime">
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
            placeholder="请输入备注信息（选填）"
          />
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            @click="submitOrder"
            :loading="submitting"
          >
            {{ submitting ? '提交中...' : '提交订单' }}
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 订单预览 -->
    <transition name="fade">
      <el-card class="preview-card" v-if="showPreview">
        <template #header>
          <span>订单预览</span>
        </template>
        <div class="preview-content">
          <div class="preview-item">
            <span class="label">老人姓名：</span>
            <span class="value">{{ selectedElderly?.name || '未选择' }}</span>
          </div>
          <div class="preview-item">
            <span class="label">餐品名称：</span>
            <span class="value">{{ selectedMeal?.name || '未选择' }}</span>
          </div>
          <div class="preview-item">
            <span class="label">餐品价格：</span>
            <span class="value price">￥{{ selectedMeal?.price || '0.00' }}</span>
          </div>
          <div class="preview-item">
            <span class="label">配送时间：</span>
            <span class="value">{{ orderForm.deliveryDate }} {{ orderForm.deliveryTime }}</span>
          </div>
          <div class="preview-item">
            <span class="label">备注：</span>
            <span class="value">{{ orderForm.remark || '无' }}</span>
          </div>
        </div>
      </el-card>
    </transition>

    <!-- 订单成功提示 -->
    <transition name="fade">
      <el-card class="success-card" v-if="orderSuccess">
        <div class="success-content">
          <div class="success-icon">
            <el-icon size="48" color="#10b981"><Check /></el-icon>
          </div>
          <h3>订单提交成功！</h3>
          <p>订单编号：{{ orderNumber }}</p>
          <p>订单金额：￥{{ selectedMeal?.price || '0.00' }}</p>
          <div class="success-actions">
            <el-button type="primary" @click="resetForm">继续下单</el-button>
            <el-button @click="goToOrders">查看订单</el-button>
          </div>
        </div>
      </el-card>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const orderFormRef = ref(null)

// 表单数据
const orderForm = reactive({
  elderlyId: '',
  mealId: '',
  deliveryDate: new Date(),
  deliveryTime: '12:00',
  remark: ''
})

// 表单验证规则
const formRules = {
  elderlyId: [
    { required: true, message: '请选择老人', trigger: 'change' }
  ],
  mealId: [
    { required: true, message: '请选择餐品', trigger: 'change' }
  ],
  deliveryDate: [
    { required: true, message: '请选择配送日期', trigger: 'change' }
  ],
  deliveryTime: [
    { required: true, message: '请选择配送时间', trigger: 'change' }
  ]
}

// 老人列表
const elderlyList = ref([
  { id: 1, name: '王大爷' },
  { id: 2, name: '李奶奶' },
  { id: 3, name: '张爷爷' },
  { id: 4, name: '赵奶奶' },
  { id: 5, name: '刘大爷' },
  { id: 6, name: '陈奶奶' }
])

// 餐品列表
const mealList = ref([
  { id: 1, name: '红烧肉套餐', price: 15 },
  { id: 2, name: '清蒸鱼套餐', price: 18 },
  { id: 3, name: '蔬菜沙拉套餐', price: 12 },
  { id: 4, name: '杂粮粥套餐', price: 10 },
  { id: 5, name: '宫保鸡丁套餐', price: 16 },
  { id: 6, name: '番茄鸡蛋汤套餐', price: 12 }
])

// 显示预览
const showPreview = ref(false)
// 提交状态
const submitting = ref(false)
// 订单成功状态
const orderSuccess = ref(false)
// 订单编号
const orderNumber = ref('')

// 选中的老人
const selectedElderly = computed(() => {
  return elderlyList.value.find(item => item.id === orderForm.elderlyId)
})

// 选中的餐品
const selectedMeal = computed(() => {
  return mealList.value.find(item => item.id === orderForm.mealId)
})

// 禁用日期（不能选择过去的日期）
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7 // 禁用今天之前的日期
}

// 返回
const goBack = () => {
  router.back()
}

// 提交订单
const submitOrder = async () => {
  // 表单验证
  if (!orderFormRef.value) return
  
  await orderFormRef.value.validate((valid) => {
    if (!valid) {
      ElMessage.error('请填写完整的订单信息')
      return
    }
    
    // 显示提交状态
    submitting.value = true
    
    // 模拟API请求延迟
    setTimeout(() => {
      // 生成订单编号
      orderNumber.value = 'ORD' + Date.now()
      orderSuccess.value = true
      submitting.value = false
      
      // 显示成功消息
      ElMessage.success('订单提交成功！')
    }, 1500)
  })
}

// 重置表单
const resetForm = () => {
  orderForm.elderlyId = ''
  orderForm.mealId = ''
  orderForm.deliveryDate = new Date()
  orderForm.deliveryTime = '12:00'
  orderForm.remark = ''
  showPreview.value = false
  orderSuccess.value = false
  orderNumber.value = ''
  
  // 重置表单验证
  if (orderFormRef.value) {
    orderFormRef.value.resetFields()
  }
}

// 跳转到订单管理页面
const goToOrders = () => {
  router.push('/orders')
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
</script>

<style scoped>
.quick-order {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.order-card {
  margin-bottom: 20px;
}

.preview-card {
  background: var(--bg-secondary);
  margin-bottom: 20px;
}

.preview-content {
  padding: 20px;
}

.preview-item {
  display: flex;
  margin-bottom: 15px;
  align-items: flex-start;
}

.preview-item:last-child {
  margin-bottom: 0;
}

.label {
  width: 80px;
  font-weight: 600;
  color: var(--text-secondary);
}

.value {
  flex: 1;
  color: var(--text-primary);
}

.value.price {
  color: var(--primary-color);
  font-weight: 700;
}

/* 老人和餐品选项样式 */
.elderly-option,
.meal-option {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.elderly-option span,
.meal-option span:first-child {
  flex: 1;
}

.meal-option .price {
  color: var(--primary-color);
  font-weight: 700;
}

/* 成功卡片样式 */
.success-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
  border: 1px solid rgba(16, 185, 129, 0.2);
  margin-top: 20px;
}

.success-content {
  text-align: center;
  padding: 40px 20px;
}

.success-icon {
  margin-bottom: 20px;
}

.success-content h3 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 16px 0;
  color: var(--text-primary);
}

.success-content p {
  margin: 8px 0;
  color: var(--text-secondary);
  font-size: 16px;
}

.success-content p:first-of-type {
  font-family: 'Courier New', Courier, monospace;
  color: var(--primary-color);
  font-weight: 600;
}

.success-actions {
  margin-top: 30px;
  display: flex;
  gap: 16px;
  justify-content: center;
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