<template>
	<view class="schedule-container">
		<view class="schedule-tabs">
			<view 
				v-for="tab in tabs" 
				:key="tab.value"
				:class="['tab-item', { active: activeTab === tab.value }]"
				@click="activeTab = tab.value"
			>
				{{ tab.label }}
			</view>
		</view>
		
		<view v-if="activeTab === 'week'" class="week-schedule">
			<view class="week-header">
				<view 
					v-for="day in weekDays" 
					:key="day.value"
					:class="['day-item', { 'selected': selectedDay === day.value }]"
					@click="selectDay(day.value)"
				>
					<text class="day-name">{{ day.label }}</text>
					<text class="day-date">{{ day.date }}</text>
					<view v-if="day.hasSchedule" class="schedule-badge">已排班</view>
				</view>
			</view>
			
			<view class="assigned-schedule">
				<view v-if="selectedDaySchedule.length > 0" class="schedule-list">
					<view v-for="item in selectedDaySchedule" :key="item.id" class="schedule-item">
						<view class="schedule-header">
							<text class="schedule-date">{{ item.date }}</text>
							<text class="schedule-status" :class="item.status">{{ item.statusText }}</text>
						</view>
						<view class="schedule-time">
							<text class="time-range">{{ item.timeRange }}</text>
						</view>
						<view class="schedule-note">
							<text v-if="item.note" class="note-text">管理员备注：{{ item.note }}</text>
						</view>
					</view>
				</view>
				<view v-else class="empty-state">
					<text class="empty-icon">📅</text>
					<text class="empty-text">该日期暂无排班安排</text>
				</view>
			</view>
		</view>
		
		<view v-else-if="activeTab === 'month'" class="month-schedule">
			<view class="month-selector">
				<view class="month-nav">
					<view @click="previousMonth" class="nav-btn">
						<text>‹</text>
					</view>
					<view class="month-display" @click="showMonthPicker = true">
						<text>{{ currentYearMonth }}</text>
					</view>
					<view @click="nextMonth" class="nav-btn">
						<text>›</text>
					</view>
				</view>
			</view>
			<view class="calendar-grid">
				<view class="calendar-header">
					<text v-for="day in weekDayNames" :key="day" class="week-day">{{ day }}</text>
				</view>
				<view class="calendar-body">
					<view 
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
						<text class="day-number">{{ day.day }}</text>
						<view v-if="day.hasSchedule" class="schedule-indicator"></view>
					</view>
				</view>
			</view>
			
			<view class="month-schedule-list">
				<view v-if="filteredMonthSchedule.length > 0" class="schedule-list">
					<view v-for="item in filteredMonthSchedule" :key="item.id" class="schedule-item">
						<view class="schedule-header">
							<text class="schedule-date">{{ item.date }}</text>
							<text class="schedule-status" :class="item.status">{{ item.statusText }}</text>
						</view>
						<view class="schedule-time">
							<text class="time-range">{{ item.timeRange }}</text>
						</view>
					</view>
				</view>
				<view v-else class="empty-state">
					<text class="empty-icon">📅</text>
					<text class="empty-text">{{ selectedDate ? '该日期暂无排班安排' : '本月暂无排班安排' }}</text>
				</view>
			</view>
		</view>
		
		<view v-if="activeTab === 'week'" class="action-section">
			<button @click="saveSchedule" class="save-button">保存排班</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js';
	
	export default {
		data() {
			return {
				activeTab: 'week',
				tabs: [
					{ label: '本周排班', value: 'week' },
					{ label: '月度排班', value: 'month' }
				],
				selectedDay: 'monday',
				weekDays: [
					{ label: '周一', value: 'monday', date: '', hasSchedule: false },
					{ label: '周二', value: 'tuesday', date: '', hasSchedule: false },
					{ label: '周三', value: 'wednesday', date: '', hasSchedule: false },
					{ label: '周四', value: 'thursday', date: '', hasSchedule: false },
					{ label: '周五', value: 'friday', date: '', hasSchedule: false },
					{ label: '周六', value: 'saturday', date: '', hasSchedule: false },
					{ label: '周日', value: 'sunday', date: '', hasSchedule: false }
				],
				weekDayNames: ['日', '一', '二', '三', '四', '五', '六'],
				calendarDays: [],
				weekSchedule: [],
				monthSchedule: [],
				selectedDaySchedule: [],
				selectedDate: '',
				currentYear: new Date().getFullYear(),
				currentMonth: new Date().getMonth() + 1,
				showMonthPicker: false,
				staffId: null,
				loading: false
			}
		},
		computed: {
			// 根据选中日期过滤月度排班数据
			filteredMonthSchedule() {
				if (this.selectedDate) {
					return this.monthSchedule.filter(schedule => schedule.date === this.selectedDate)
				}
				return this.monthSchedule
			},
			
			// 当前年月显示
			currentYearMonth() {
				return `${this.currentYear}年${this.currentMonth}月`
			}
		},
		onLoad() {
			this.initSchedule()
		},
		methods: {
			async initSchedule() {
				try {
					this.loading = true
					// 获取个人信息，获取staffId
					const profile = await api.profile.getProfile()
					console.log('个人信息:', profile)
					// 从deliverer对象中获取用户ID
					this.staffId = profile.deliverer.id
					console.log('当前配送员ID:', this.staffId)
					
					// 计算本周日期
					this.calculateWeekDays()
					console.log('计算的星期日期:', this.weekDays)
					
					// 获取排班数据
					await this.loadScheduleData()
					this.generateCalendar()
				} catch (error) {
					console.error('初始化排班数据失败:', error)
				} finally {
					this.loading = false
				}
			},
			
			async loadScheduleData() {
				try {
					const now = new Date()
					const currentYear = now.getFullYear()
					const currentMonth = now.getMonth() + 1
					
					// 计算本周日期范围，可能跨月份
					const currentDay = now.getDay()
					const startOfWeek = new Date(now)
					startOfWeek.setDate(now.getDate() - (currentDay === 0 ? 6 : currentDay - 1))
					startOfWeek.setHours(0, 0, 0, 0)
					const endOfWeek = new Date(startOfWeek)
					endOfWeek.setDate(startOfWeek.getDate() + 6)
					endOfWeek.setHours(23, 59, 59, 999)
					
					console.log('本周日期范围:', startOfWeek, endOfWeek)
					
					// 检查本周是否跨月份
					let allSchedules = []
					const startMonth = startOfWeek.getMonth() + 1
					const endMonth = endOfWeek.getMonth() + 1
					
					if (startMonth !== endMonth) {
						// 跨月份，需要获取两个月份的数据
						console.log('本周跨月份，需要获取两个月份的数据')
						
						// 获取开始月份的数据
						const startMonthData = await api.schedule.getMonthSchedules({
							staff_id: this.staffId,
							year: startOfWeek.getFullYear(),
							month: startMonth
						})
						console.log('开始月份数据:', startMonthData)
						
						// 获取结束月份的数据
						const endMonthData = await api.schedule.getMonthSchedules({
							staff_id: this.staffId,
							year: endOfWeek.getFullYear(),
							month: endMonth
						})
						console.log('结束月份数据:', endMonthData)
						
						allSchedules = [...startMonthData.schedules, ...endMonthData.schedules]
					} else {
						// 不跨月份，只获取当前月份的数据
						console.log('请求参数:', { staff_id: this.staffId, year: currentYear, month: currentMonth })
						const monthData = await api.schedule.getMonthSchedules({
							staff_id: this.staffId,
							year: currentYear,
							month: currentMonth
						})
						console.log('API返回数据:', monthData)
						allSchedules = monthData.schedules
					}
					
					this.monthSchedule = allSchedules.map(schedule => ({
						id: schedule.id,
						date: schedule.schedule_date,
						timeRange: schedule.time_slot,
						status: schedule.status,
						statusText: schedule.status === 'confirmed' ? '已确认' : '待确认',
						note: schedule.note
					}))
					console.log('处理后的月度排班数据:', this.monthSchedule)
					
					// 获取本周排班数据
					this.weekSchedule = this.monthSchedule.filter(schedule =>{
						const scheduleDate = new Date(schedule.date)
						console.log('日期范围:', startOfWeek, endOfWeek, '排班日期:', scheduleDate)
						return scheduleDate >= startOfWeek && scheduleDate <= endOfWeek
					})
					console.log('本周排班数据:', this.weekSchedule)
					
					// 更新选中日期的排班数据
					this.updateSelectedDaySchedule()
					
					// 更新星期的排班状态
					this.weekDays.forEach(day => {
						if (day.date) {
							const dayDate = `${currentYear}-${day.date}`
							day.hasSchedule = this.monthSchedule.some(schedule => schedule.date === dayDate)
						}
					})
					
					// 更新日历的排班状态
					this.updateCalendarSchedule()
				} catch (error) {
					console.error('加载排班数据失败:', error)
				}
			},
			
			generateCalendar() {
				const today = new Date()
				const year = this.currentYear
				const month = this.currentMonth - 1 // JavaScript月份从0开始
				
				const firstDay = new Date(year, month, 1)
				const lastDay = new Date(year, month + 1, 0)
				const daysInMonth = lastDay.getDate()
				const startDay = firstDay.getDay()
				
				this.calendarDays = []
				
				for (let i = 0; i < startDay; i++) {
					this.calendarDays.push({
						date: '',
						day: '',
						isCurrentMonth: false,
						isToday: false,
						hasSchedule: false
					})
				}
				
				for (let day = 1; day <= daysInMonth; day++) {
					const currentDate = new Date(year, month, day)
					const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
					this.calendarDays.push({
						date: dateStr,
						day: day,
						isCurrentMonth: true,
						isToday: currentDate.toDateString() === today.toDateString(),
						hasSchedule: this.monthSchedule.some(schedule => schedule.date === dateStr)
					})
				}
			},
			
			updateCalendarSchedule() {
				this.calendarDays.forEach(day => {
					if (day.date) {
						day.hasSchedule = this.monthSchedule.some(schedule => schedule.date === day.date)
					}
				})
			},
			
			selectDay(dayValue) {
				this.selectedDay = dayValue
				// 更新选中日期的排班数据
				this.updateSelectedDaySchedule()
			},
			
			updateSelectedDaySchedule() {
				// 根据选中的日期过滤排班数据
				const selectedDayObj = this.weekDays.find(day => day.value === this.selectedDay)
				if (selectedDayObj && selectedDayObj.date) {
					const selectedDateStr = `${new Date().getFullYear()}-${selectedDayObj.date}`
					this.selectedDaySchedule = this.weekSchedule.filter(schedule => schedule.date === selectedDateStr)
				} else {
					this.selectedDaySchedule = []
				}
			},
			
			selectDate(date) {
				this.selectedDate = date
			},
			
			// 上一个月
			previousMonth() {
				if (this.currentMonth === 1) {
					this.currentYear -= 1
					this.currentMonth = 12
				} else {
					this.currentMonth -= 1
				}
				this.generateCalendar()
			},
			
			// 下一个月
			nextMonth() {
				if (this.currentMonth === 12) {
					this.currentYear += 1
					this.currentMonth = 1
				} else {
					this.currentMonth += 1
				}
				this.generateCalendar()
			},
			
			calculateWeekDays() {
				const now = new Date()
				const currentDay = now.getDay() // 0=周日, 1=周一, ..., 6=周六
				
				// 计算本周一的日期
				const monday = new Date(now)
				monday.setDate(now.getDate() - (currentDay === 0 ? 6 : currentDay - 1))
				
				// 更新一周的日期
				for (let i = 0; i< 7; i++) {
					const day = new Date(monday)
					day.setDate(monday.getDate() + i)
					const month = day.getMonth() + 1
					const date = day.getDate()
					this.weekDays[i].date = `${String(month).padStart(2, '0')}-${String(date).padStart(2, '0')}`
				}
			}

		}
	}
</script>

<style scoped>
	.schedule-container {
		min-height: 100vh;
	}
	
	.schedule-tabs {
		display: flex;
		background-color: white;
		border-bottom: 1rpx solid #e2e8f0;
	}
	
	.tab-item {
		flex: 1;
		text-align: center;
		padding: 30rpx 0;
		font-size: 32rpx;
		color: #64748b;
		position: relative;
	}
	
	.tab-item.active {
		color: #10b981;
		font-weight: 500;
	}
	
	.tab-item.active::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 50%;
		transform: translateX(-50%);
		width: 40rpx;
		height: 4rpx;
		background-color: #10b981;
		border-radius: 2rpx;
	}
	
	.week-schedule {
		padding: 30rpx;
	}
	
	.week-header {
		display: flex;
		gap: 10rpx;
		margin-bottom: 30rpx;
		overflow-x: auto;
		padding-bottom: 20rpx;
	}
	
	.day-item {
		flex: 0 0 120rpx;
		background-color: white;
		border-radius: 16rpx;
		padding: 20rpx;
		text-align: center;
		border: 2rpx solid #e2e8f0;
		transition: all 0.3s ease;
	}
	
	.day-item.selected {
		border-color: #10b981;
		background-color: #d1fae5;
	}
	
	.day-item:active {
		transform: scale(0.95);
	}
	
	.schedule-badge {
		margin-top: 8rpx;
		padding: 4rpx 12rpx;
		background-color: #10b981;
		color: white;
		border-radius: 12rpx;
		font-size: 20rpx;
		font-weight: 500;
	}
	
	.day-name {
		display: block;
		font-size: 28rpx;
		color: #1e293b;
		font-weight: 500;
		margin-bottom: 8rpx;
	}
	
	.day-date {
		display: block;
		font-size: 24rpx;
		color: #64748b;
	}
	
	.time-slots {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}
	
	.time-slot {
		background-color: white;
		border-radius: 16rpx;
		padding: 24rpx;
	}
	
	.slot-time {
		display: block;
		font-size: 28rpx;
		color: #1e293b;
		font-weight: 500;
		margin-bottom: 16rpx;
	}
	
	.slot-status {
		display: flex;
		gap: 16rpx;
	}
	
	.status-option {
		flex: 1;
		height: 64rpx;
		border-radius: 12rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 24rpx;
		font-weight: 500;
	}
	
	.status-option.available {
		background-color: #f8fafc;
		color: #64748b;
		border: 1rpx solid #e2e8f0;
	}
	
	.status-option.selected {
		background-color: #d1fae5;
		color: #10b981;
		border: 1rpx solid #10b981;
	}
	
	.status-option.rest {
		background-color: #fef2f2;
		color: #ef4444;
		border: 1rpx solid #fecaca;
	}
	
	.month-schedule {
		padding: 30rpx;
	}
	
	.month-selector {
		background-color: white;
		border-radius: 16rpx;
		padding: 20rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
	}
	
	.month-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	
	.nav-btn {
		width: 60rpx;
		height: 60rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: #f8fafc;
		border-radius: 50%;
		font-size: 36rpx;
		color: #64748b;
	}
	
	.month-display {
		flex: 1;
		text-align: center;
		font-size: 32rpx;
		font-weight: 500;
		color: #1e293b;
		padding: 10rpx 20rpx;
		border-radius: 8rpx;
		background-color: #f8fafc;
	}
	
	.calendar-grid {
		background-color: white;
		border-radius: 20rpx;
		padding: 20rpx;
	}
	
	.calendar-header {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		text-align: center;
		margin-bottom: 20rpx;
	}
	
	.week-day {
		font-size: 24rpx;
		color: #64748b;
		font-weight: 500;
	}
	
	.calendar-body {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 8rpx;
	}
	
	.calendar-day {
		height: 80rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		border-radius: 8rpx;
		position: relative;
	}
	
	.calendar-day.other-month {
		color: #cbd5e1;
	}
	
	.calendar-day.today {
		background-color: #d1fae5;
		color: #10b981;
	}
	
	.calendar-day.selected {
		background-color: #10b981;
		color: white;
	}
	
	.day-number {
		font-size: 28rpx;
	}
	
	.schedule-indicator {
		position: absolute;
		bottom: 4rpx;
		width: 6rpx;
		height: 6rpx;
		background-color: #10b981;
		border-radius: 50%;
	}
	

	
	.schedule-list {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}
	
	.schedule-item {
		background-color: white;
		border-radius: 16rpx;
		padding: 24rpx;
	}
	
	.schedule-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12rpx;
	}
	
	.schedule-date {
		font-size: 28rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.schedule-status {
		padding: 8rpx 16rpx;
		border-radius: 12rpx;
		font-size: 24rpx;
		font-weight: 500;
	}
	
	.schedule-status.confirmed {
		background-color: #d1fae5;
		color: #10b981;
	}
	
	.schedule-time {
		margin-bottom: 8rpx;
	}
	
	.time-range {
		font-size: 26rpx;
		color: #64748b;
	}
	
	.schedule-note {
		padding-top: 12rpx;
		border-top: 1rpx solid #f1f5f9;
	}
	
	.note-text {
		font-size: 24rpx;
		color: #64748b;
	}
	
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 100rpx 0;
	}
	
	.empty-icon {
		font-size: 120rpx;
		margin-bottom: 20rpx;
	}
	
	.empty-text {
		font-size: 32rpx;
		color: #94a3b8;
		margin-bottom: 30rpx;
	}
	

	
	.action-section {
		padding: 0 30rpx 40rpx;
	}
	
	.save-button {
		width: 100%;
		height: 96rpx;
		background-color: #10b981;
		color: white;
		border: none;
		border-radius: 24rpx;
		font-size: 32rpx;
		font-weight: 500;
	}
</style>