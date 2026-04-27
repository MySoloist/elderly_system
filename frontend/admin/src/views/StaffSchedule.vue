<template>
  <div class="staff-schedule">
    <!-- 欢迎栏 -->
    <div class="welcome-bar">
      <div class="welcome-text">
        <h1 class="welcome-title">配送员排班管理</h1>
        <p class="welcome-subtitle">为 {{ staffName }} 安排工作排班</p>
      </div>
      <div class="welcome-action">
        <el-button type="primary" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>返回
        </el-button>
      </div>
    </div>

    <!-- 排班标签页 -->
    <div class="schedule-tabs">
      <el-tabs v-model="activeTab" class="schedule-tabs-container">
        <el-tab-pane label="本周排班" name="week">
          <div class="week-schedule">
            <!-- 星期选择 -->
            <div class="week-header">
              <div 
                v-for="day in weekDays" 
                :key="day.value"
                :class="['day-item', { active: selectedDay === day.value }]"
                @click="selectedDay = day.value"
              >
                <div class="day-name">{{ day.label }}</div>
                <div class="day-date">{{ day.date }}</div>
              </div>
            </div>

            <!-- 时间段选择 -->
            <div class="time-slots">
              <h3 class="section-title">{{ getSelectedDayName() }} 排班</h3>
              <div class="time-slot-grid">
                <div 
                  v-for="slot in timeSlots" 
                  :key="slot.id"
                  :class="['time-slot', { 
                    'selected': isSlotSelected(slot.id),
                    'available': slot.type === 'available',
                    'rest': slot.type === 'rest'
                  }]"
                  @click="toggleSlot(slot.id)"
                >
                  <div class="slot-time">{{ slot.time }}</div>
                  <div class="slot-status">{{ slot.status }}</div>
                </div>
              </div>
            </div>

            <!-- 备注输入 -->
            <div class="note-section">
              <el-input
                v-model="scheduleNote"
                type="textarea"
                :rows="3"
                placeholder="请输入排班备注（如特殊要求、注意事项等）"
              />
            </div>

            <!-- 操作按钮 -->
            <div class="action-buttons">
              <el-button type="primary" @click="saveSchedule" :loading="saving">
                <el-icon><Check /></el-icon>保存排班
              </el-button>
              <el-button @click="resetSchedule">
                <el-icon><RefreshLeft /></el-icon>重置
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="月度排班" name="month">
          <div class="month-schedule">
            <!-- 月份选择器 -->
            <div class="month-selector">
              <el-date-picker
                v-model="selectedMonth"
                type="month"
                placeholder="选择月份"
                format="YYYY-MM"
                value-format="YYYY-MM"
                @change="handleMonthChange"
                :month-picker-options="{
                  months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                }"
              />
            </div>
            
            <!-- 日历视图 -->
            <div class="calendar-grid">
              <div class="calendar-header">
                <div v-for="day in weekDayNames" :key="day" class="week-day">{{ day }}</div>
              </div>
              <div class="calendar-body">
                <div 
                  v-for="day in calendarDays" 
                  :key="day.date"
                  :class="[
                    'calendar-day', 
                    { 
                      'other-month': !day.isCurrentMonth,
                      'today': day.isToday,
                      'has-schedule': day.hasSchedule,
                      'selected': selectedDate === day.date
                    }
                  ]"
                  @click="selectDate(day.date)"
                >
                  <div class="day-number">{{ day.day }}</div>
                  <div v-if="day.hasSchedule" class="schedule-indicator"></div>
                </div>
              </div>
            </div>

            <!-- 月度排班列表 -->
            <div class="month-schedule-list">
              <h3 class="section-title">{{ selectedDate ? selectedDate + ' 排班安排' : '本月排班安排' }}</h3>
              <el-table :data="filteredMonthSchedule" stripe class="schedule-table">
                <el-table-column prop="date" label="日期" width="120" />
                <el-table-column prop="timeRange" label="时间段" width="150" />
                <el-table-column label="状态" width="100">
                  <template #default="scope">
                    <el-tag :type="scope.row.status === 'confirmed' ? 'success' : 'info'">
                      {{ scope.row.statusText }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="note" label="备注" />
                <el-table-column label="操作" width="120">
                  <template #default="scope">
                    <el-button type="danger" size="small" @click="deleteSchedule(scope.row)">
                      <el-icon><Delete /></el-icon>删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  ArrowLeft, Check, RefreshLeft, Delete 
} from '@element-plus/icons-vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adminService } from '../api'

// 路由
const router = useRouter()
const route = useRoute()

// 获取路由参数
const staffId = ref(route.query.staffId || '')
const staffName = ref(route.query.staffName || '配送员')

// 状态管理
const activeTab = ref('week')
const selectedDay = ref('monday')
const selectedDate = ref('')
const scheduleNote = ref('')
const saving = ref(false)

// 当前选择的年份和月份
const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)

// 月份选择器绑定值
const selectedMonth = ref(`${new Date().getFullYear()}-${String(new Date().getMonth() + 1).padStart(2, '0')}`)

// 时间段数据
const timeSlots = ref([
  { id: 1, time: '08:00-10:00', type: 'available', status: '可选' },
  { id: 2, time: '10:00-12:00', type: 'available', status: '可选' },
  { id: 3, time: '14:00-16:00', type: 'available', status: '可选' },
  { id: 4, time: '16:00-18:00', type: 'available', status: '可选' },
  { id: 5, time: '18:00-20:00', type: 'available', status: '可选' },
])

// 已选择的时间段
const selectedSlots = ref([])

// 星期数据
const weekDays = ref([
  { label: '周一', value: 'monday' },
  { label: '周二', value: 'tuesday' },
  { label: '周三', value: 'wednesday' },
  { label: '周四', value: 'thursday' },
  { label: '周五', value: 'friday' },
  { label: '周六', value: 'saturday' },
  { label: '周日', value: 'sunday' },
])

const weekDayNames = ['日', '一', '二', '三', '四', '五', '六']

// 日历数据
const calendarDays = ref([])

// 月度排班数据
const monthSchedule = ref([
  {
    id: 1,
    date: '2026-12-01',
    timeRange: '08:00-10:00',
    status: 'confirmed',
    statusText: '已确认',
    note: '上午配送，注意老人饮食禁忌'
  },
  {
    id: 2,
    date: '2026-12-02',
    timeRange: '14:00-16:00',
    status: 'confirmed',
    statusText: '已确认',
    note: '下午配送，需要提前联系老人'
  }
])

// 计算属性和方法
const getSelectedDayName = () => {
  const day = weekDays.value.find(d => d.value === selectedDay.value)
  return day ? day.label : ''
}

// 根据选中日期过滤排班数据
const filteredMonthSchedule = computed(() => {
  if (selectedDate.value) {
    return monthSchedule.value.filter(schedule => schedule.date === selectedDate.value)
  }
  return monthSchedule.value
})

const isSlotSelected = (slotId) => {
  return selectedSlots.value.includes(slotId)
}

const toggleSlot = (slotId) => {
  const index = selectedSlots.value.indexOf(slotId)
  if (index > -1) {
    selectedSlots.value.splice(index, 1)
  } else {
    selectedSlots.value.push(slotId)
  }
}

const selectDate = (date) => {
  selectedDate.value = date
}

const handleMonthChange = (value) => {
  if (value) {
    const [year, month] = value.split('-')
    currentYear.value = parseInt(year)
    currentMonth.value = parseInt(month)
    refreshMonthSchedule()
  }
}

const generateCalendar = () => {
  const today = new Date()
  const year = currentYear.value
  const month = currentMonth.value - 1
  
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const daysInMonth = lastDay.getDate()
  const startDay = firstDay.getDay()
  
  calendarDays.value = []
  
  // 添加上个月的日期
  for (let i = 0; i< startDay; i++) {
    const prevMonthDay = new Date(year, month, -startDay + i + 1)
    calendarDays.value.push({
      date: `${prevMonthDay.getFullYear()}-${String(prevMonthDay.getMonth() + 1).padStart(2, '0')}-${String(prevMonthDay.getDate()).padStart(2, '0')}`,
      day: prevMonthDay.getDate(),
      isCurrentMonth: false,
      isToday: false,
      hasSchedule: false
    })
  }
  
  // 添加当前月的日期
  for (let day = 1; day <= daysInMonth; day++) {
    const currentDate = new Date(year, month, day)
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    calendarDays.value.push({
      date: dateStr,
      day: day,
      isCurrentMonth: true,
      isToday: currentDate.toDateString() === today.toDateString(),
      hasSchedule: monthSchedule.value.some(s => s.date === dateStr)
    })
  }
}

const saveSchedule = async () => {
  if (selectedSlots.value.length === 0) {
    ElMessage.warning('请选择至少一个时间段')
    return
  }

  saving.value = true
  try {
    // 获取选中的星期对应的日期
    const selectedDayObj = weekDays.value.find(d => d.value === selectedDay.value)
    if (!selectedDayObj) {
      ElMessage.error('无法获取日期信息')
      return
    }
    
    // 动态计算日期：获取当前周的对应星期几的日期
    const now = new Date()
    const currentDay = now.getDay() // 0=周日, 1=周一, ..., 6=周六
    
    // 获取选中的星期几（0=周一, 1=周二, ..., 6=周日）
    const weekDayIndex = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].indexOf(selectedDay.value)
    
    // 计算本周一的日期
    const monday = new Date(now)
    monday.setDate(now.getDate() - (currentDay === 0 ? 6 : currentDay - 1))
    
    // 计算选中星期几的日期
    const targetDate = new Date(monday)
    targetDate.setDate(monday.getDate() + weekDayIndex)
    
    const scheduleDate = targetDate.toISOString().split('T')[0]
    
    // 批量创建排班记录
    for (const slotId of selectedSlots.value) {
      const slot = timeSlots.value.find(s => s.id === slotId)
      if (slot) {
        // 从staffId中提取数字部分（移除P前缀）
        const numericStaffId = parseInt(staffId.value.replace('P', ''))
        
        await adminService.createStaffSchedule({
          staff_id: numericStaffId,
          schedule_date: scheduleDate,
          time_slot: slot.time,
          note: scheduleNote.value
        })
      }
    }
    
    ElMessage.success('排班保存成功')
    // 刷新月度排班数据
    await refreshMonthSchedule()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '排班保存失败')
    console.error('保存排班失败:', error)
  } finally {
    saving.value = false
  }
}

const resetSchedule = () => {
  selectedSlots.value = []
  scheduleNote.value = ''
}

const deleteSchedule = async (scheduleItem) => {
  try {
    await adminService.deleteStaffSchedule(scheduleItem.id)
    const index = monthSchedule.value.findIndex(s => s.id === scheduleItem.id)
    if (index > -1) {
      monthSchedule.value.splice(index, 1)
    }
    ElMessage.success('排班删除成功')
    generateCalendar() // 重新生成日历
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '排班删除失败')
    console.error('删除排班失败:', error)
  }
}

const refreshMonthSchedule = async () => {
  try {
    // 使用当前选择的年份和月份
    const year = currentYear.value
    const month = currentMonth.value
    
    // 从staffId中提取数字部分（移除P前缀）
    const numericStaffId = parseInt(staffId.value.replace('P', ''))
    
    const response = await adminService.getMonthSchedules({
      staff_id: numericStaffId,
      year: year,
      month: month
    })
    
    monthSchedule.value = response.schedules.map(schedule => ({
      id: schedule.id,
      date: schedule.schedule_date,
      timeRange: schedule.time_slot,
      status: schedule.status,
      statusText: schedule.status === 'confirmed' ? '已确认' : '待确认',
      note: schedule.note
    }))
    
    // 清除选中的日期，避免显示错误的数据
    selectedDate.value = ''
    
    generateCalendar() // 重新生成日历
  } catch (error) {
    console.error('获取月度排班失败:', error)
    ElMessage.error('获取排班数据失败')
  }
}

const goBack = () => {
  router.back()
}

// 组件挂载时初始化
onMounted(async () => {
  await refreshMonthSchedule()
})
</script>

<style scoped>
.staff-schedule {
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

.schedule-tabs-container {
  background-color: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
}

.week-schedule {
  padding: var(--spacing-xl);
}

.week-header {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
  overflow-x: auto;
  padding-bottom: var(--spacing-sm);
}

.day-item {
  flex: 0 0 120px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.day-item:hover {
  background-color: var(--bg-hover);
}

.day-item.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.day-name {
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.day-date {
  font-size: 12px;
  opacity: 0.8;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
}

.time-slot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.time-slot {
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.time-slot:hover {
  background-color: var(--bg-hover);
}

.time-slot.selected {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.time-slot.available {
  border-color: var(--success-color);
}

.time-slot.rest {
  border-color: var(--danger-color);
}

.slot-time {
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.slot-status {
  font-size: 12px;
  opacity: 0.8;
}

.note-section {
  margin-bottom: var(--spacing-xl);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
}

.month-schedule {
  padding: var(--spacing-xl);
}

.month-selector {
  margin-bottom: var(--spacing-xl);
}

.calendar-grid {
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  margin-bottom: var(--spacing-md);
}

.week-day {
  font-weight: 600;
  color: var(--text-primary);
  padding: var(--spacing-sm);
}

.calendar-body {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--spacing-xs);
}

.calendar-day {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.calendar-day:hover {
  background-color: var(--bg-hover);
}

.calendar-day.other-month {
  color: var(--text-muted);
  opacity: 0.5;
}

.calendar-day.today {
  background-color: var(--primary-color);
  color: white;
}

.calendar-day.has-schedule {
  background-color: var(--success-color-light);
}

.calendar-day.selected {
  background-color: var(--primary-color);
  color: white;
}

.day-number {
  font-weight: 500;
}

.schedule-indicator {
  position: absolute;
  bottom: 4px;
  width: 6px;
  height: 6px;
  background-color: var(--success-color);
  border-radius: 50%;
}

.month-schedule-list {
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
}

.schedule-table {
  --el-table-bg-color: transparent;
}
</style>
