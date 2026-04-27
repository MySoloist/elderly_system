<template>
	<view class="container">
		<!-- 背景装饰 -->
		<view class="background-decoration">
			<view class="decoration-circle big-circle"></view>
			<view class="decoration-circle medium-circle"></view>
			<view class="decoration-circle small-circle"></view>
		</view>
		
		<!-- 顶部导航 -->
		<view class="top-nav">
			<text class="page-title">饮食健康</text>
			<view class="elder-selector" @click="toggleElderSelector" :disabled="loading">
				<text class="selector-text">{{ loading ? '加载中...' : (selectedElder ? selectedElder.name : '选择老人') }}</text>
				<text class="arrow-icon">▼</text>
			</view>
		</view>
		
		<!-- 老人选择器下拉列表 -->
		<view class="elder-selector-dropdown" v-if="showElderSelector">
			<!-- 加载状态 -->
			<view v-if="loading" class="loading-state">
				<view class="loading-spinner"></view>
				<text class="loading-text">加载中...</text>
			</view>
			
			<!-- 空状态 -->
			<view v-else-if="elderList.length === 0" class="empty-state">
				<text class="empty-text">暂无绑定老人，请先添加绑定</text>
			</view>
			
			<!-- 老人列表 -->
			<view v-else>
				<view class="elder-item" v-for="elder in elderList" :key="elder.id" @click="selectElder(elder)">
					<view class="elder-main-info">
						<text class="elder-name">{{ elder.name }}</text>
						<text class="elder-status" :class="elder.status">{{ elder.status === 'normal' ? '正常' : elder.status === 'attention' ? '注意' : '关注' }}</text>
					</view>
					<text class="elder-info">{{ elder.age }}岁 · {{ elder.gender }}</text>
				</view>
			</view>
		</view>
		
		<!-- 健康概览卡片 -->
		<view class="overview-section">
			<view class="overview-card nutrition-card">
				<view class="card-header">
					<text class="card-title">营养摄入</text>
					<text class="card-subtitle">今日</text>
				</view>
				<view class="nutrition-content">
					<view class="nutrition-item">
						<text class="nutrition-value">{{ nutrition.calories }}</text>
						<text class="nutrition-unit">kcal</text>
					</view>
					<text class="nutrition-label">热量</text>
				</view>
				<view class="nutrition-details">
					<view class="detail-item">
						<text class="detail-value">{{ nutrition.protein }}g</text>
						<text class="detail-label">蛋白质</text>
					</view>
					<view class="detail-item">
						<text class="detail-value">{{ nutrition.fat }}g</text>
						<text class="detail-label">脂肪</text>
					</view>
					<view class="detail-item">
						<text class="detail-value">{{ nutrition.carbs }}g</text>
						<text class="detail-label">碳水</text>
					</view>
				</view>
			</view>
			
			<view class="overview-card diet-card">
				<view class="card-header">
					<text class="card-title">饮食规律</text>
					<text class="card-subtitle">{{ dietRegularity }}</text>
				</view>
				<view class="diet-content">
					<view class="diet-item">
						<view class="diet-status" :class="{ active: dietPattern.breakfast.hasMeal }">早</view>
						<text class="diet-time">{{ dietPattern.breakfast.time || '--:--' }}</text>
					</view>
					<view class="diet-item">
						<view class="diet-status" :class="{ active: dietPattern.lunch.hasMeal }">午</view>
						<text class="diet-time">{{ dietPattern.lunch.time || '--:--' }}</text>
					</view>
					<view class="diet-item">
						<view class="diet-status" :class="{ active: dietPattern.dinner.hasMeal }">晚</view>
						<text class="diet-time">{{ dietPattern.dinner.time || '--:--' }}</text>
					</view>
				</view>
			</view>
			
			<view class="overview-card health-card">
				<view class="card-header">
					<text class="card-title">健康状态</text>
					<text class="card-subtitle">{{ healthStatus }}</text>
				</view>
				<view class="health-content">
					<view class="health-indicator">
						<text class="indicator-value">--/--</text>
						<text class="indicator-label">血压</text>
					</view>
					<view class="health-indicator">
						<text class="indicator-value">--</text>
						<text class="indicator-label">血糖</text>
					</view>
				</view>
				<!-- 健康标签显示 -->
				<view class="health-tags" v-if="healthTags.length > 0">
					<view 
						v-for="tag in healthTags" 
						:key="tag.id || tag.name"
						class="health-tag"
						:style="{ backgroundColor: tag.color ? tag.color + '20' : '#f1f5f9', borderColor: tag.color || '#e2e8f0' }"
					>
						<text 
							class="health-tag-text"
							:style="{ color: tag.color || '#475569' }"
						>{{ tag.name }}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 日期选择器 -->
		<view class="date-selector">
			<text class="date-text">{{ selectedDate }}</text>
			<view class="date-nav">
				<text class="nav-btn" @click="prevDate">‹</text>
				<text class="nav-btn" @click="nextDate">›</text>
			</view>
		</view>
		
		<!-- 饮食记录列表 -->
		<view class="diet-records">
			<view class="record-card" v-for="(record, index) in dietRecords" :key="index">
				<view class="record-header">
					<text class="record-time">{{ record.time }}</text>
					<text class="record-meal">{{ record.meal }}</text>
				</view>
				<view class="record-content">
					<view class="food-item" v-for="(food, foodIndex) in record.foods" :key="foodIndex">
							<image v-if="food.image" :src="food.image" class="food-image" mode="aspectFill"></image>
							<view v-else class="food-image"></view>
							<view class="food-info">
								<text class="food-name">{{ food.name }}</text>
								<text class="food-calories">{{ food.calories }}kcal</text>
							</view>
						</view>
				</view>
				<view class="record-footer">
					<text class="total-calories">总计: {{ record.totalCalories }}kcal</text>
					<view class="nutrition-tags">
						<view class="nutrition-tag" v-for="(tag, tagIndex) in record.nutritionTags" :key="tagIndex">
							<text class="tag-text">{{ tag }}</text>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- AI智能健康建议 -->
		<view class="advice-section">
			<view class="advice-card">
				<view class="advice-header">
					<text class="advice-title">AI健康建议</text>
					<text class="advice-badge">智能</text>
				</view>
				<text class="advice-content">
					{{ healthAdvice || '正在生成健康建议...' }}
				</text>
			</view>
		</view>
		
		<!-- 健康提醒按钮 -->
		<view class="reminder-section">
			<button class="reminder-btn" @click="showReminderModal">
				<text class="reminder-icon">💬</text>
				<text class="reminder-text">发送健康提醒</text>
			</button>
		</view>
		
		<!-- 健康提醒弹窗 -->
		<view class="modal" v-if="showModal">
			<view class="modal-content">
				<view class="modal-header">
					<text class="modal-title">发送健康提醒</text>
					<text class="modal-close" @click="showModal = false">×</text>
				</view>
				<view class="modal-body">
					<view class="reminder-type">
						<text class="type-label">提醒类型</text>
						<view class="type-options">
							<view class="type-option" :class="{ active: reminderType === 'diet' }" @click="reminderType = 'diet'">饮食提醒</view>
							<view class="type-option" :class="{ active: reminderType === 'health' }" @click="reminderType = 'health'">健康建议</view>
							<view class="type-option" :class="{ active: reminderType === 'checkup' }" @click="reminderType = 'checkup'">体检提醒</view>
						</view>
					</view>
					<view class="reminder-content">
						<text class="content-label">提醒内容</text>
						<textarea class="content-input" v-model="reminderContent" placeholder="请输入提醒内容"></textarea>
					</view>
					<view class="reminder-time">
						<text class="time-label">提醒时间</text>
						<input class="time-input" type="text" v-model="reminderTime" placeholder="请输入时间，格式：YYYY-MM-DD HH:MM" />
					</view>
				</view>
				<view class="modal-footer">
					<button class="cancel-btn" @click="showModal = false">取消</button>
					<button class="send-btn" @click="sendReminder">发送</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import { healthService } from '../../api/health.js';

export default {
	data() {
			return {
				selectedElder: null,
				elderList: [],
				loading: false,
				showElderSelector: false,
				selectedDate: new Date().toISOString().split('T')[0],
				dietRecords: [],
				nutrition: {
					calories: 0,
					protein: 0,
					fat: 0,
					carbs: 0
				},
				healthStatus: '正常',
				healthTags: [],
				dietPattern: {
					breakfast: { time: '', hasMeal: false },
					lunch: { time: '', hasMeal: false },
					dinner: { time: '', hasMeal: false }
				},
				dietRegularity: '良好',
				showModal: false,
				reminderType: 'diet',
				reminderContent: '',
				reminderTime: '',
				healthAdvice: ''
			};
		},
	onLoad() {
		this.loadElders();
		this.initDateTime();
	},
	onShow() {
		// 页面显示时重新初始化时间限制
		this.initDateTime();
	},
	methods: {
		initDateTime() {
			const now = new Date();
			const year = now.getFullYear();
			const month = String(now.getMonth() + 1).padStart(2, '0');
			const day = String(now.getDate()).padStart(2, '0');
			const hour = String(now.getHours()).padStart(2, '0');
			const minute = String(now.getMinutes()).padStart(2, '0');
			
			// 默认设置为当前时间（数字格式）
			if (!this.reminderTime) {
				this.reminderTime = `${year}-${month}-${day} ${hour}:${minute}`;
			}
		},
		async loadElders() {
			try {
				this.loading = true;
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/bindings',
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					// 转换数据格式，添加状态信息
					this.elderList = response.data.map(elder => ({
						id: elder.elderly_id,
						name: elder.elderly_name,
						age: elder.elderly_age,
						gender: elder.elderly_gender,
						status: 'normal' // 默认状态
					}));
					
					// 默认选择第一个老人
					if (this.elderList.length > 0) {
						this.selectedElder = this.elderList[0];
						this.healthAdvice = '正在生成健康建议...';
						this.loadHealthData(this.selectedElder.id);
						this.loadHealthAdvice(this.selectedElder.id);
					}
				} else {
					throw new Error(response.data?.detail || '加载老人列表失败');
				}
			} catch (error) {
				console.error('加载老人列表失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		async loadHealthData(elderId) {
			try {
				this.loading = true;
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/health/${elderId}?date=${this.selectedDate}`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					const data = response.data;
					this.nutrition = data.nutrition || { calories: 0, protein: 0, fat: 0, carbs: 0 };
					this.healthStatus = data.health_status || '正常';
					this.healthTags = data.health_tags || [];
					this.dietPattern = data.diet_pattern ? {
						breakfast: { 
							time: data.diet_pattern.breakfast.time, 
							hasMeal: data.diet_pattern.breakfast.has_meal 
						},
						lunch: { 
							time: data.diet_pattern.lunch.time, 
							hasMeal: data.diet_pattern.lunch.has_meal 
						},
						dinner: { 
							time: data.diet_pattern.dinner.time, 
							hasMeal: data.diet_pattern.dinner.has_meal 
						}
					} : {
						breakfast: { time: '', hasMeal: false },
						lunch: { time: '', hasMeal: false },
						dinner: { time: '', hasMeal: false }
					};
					this.dietRegularity = data.diet_regularity || '良好';
					this.dietRecords = data.diet_records || [];
				} else {
					throw new Error(response.data?.detail || '加载健康数据失败');
				}
			} catch (error) {
				console.error('加载健康数据失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		prevDate() {
			const date = new Date(this.selectedDate);
			date.setDate(date.getDate() - 1);
			this.selectedDate = date.toISOString().split('T')[0];
			if (this.selectedElder) {
				this.loadHealthData(this.selectedElder.id);
			}
		},
		nextDate() {
			const date = new Date(this.selectedDate);
			date.setDate(date.getDate() + 1);
			const today = new Date().toISOString().split('T')[0];
			if (date.toISOString().split('T')[0] > today) {
				uni.showToast({
					title: '不能查看未来日期',
					icon: 'none'
				});
				return;
			}
			this.selectedDate = date.toISOString().split('T')[0];
			if (this.selectedElder) {
				this.loadHealthData(this.selectedElder.id);
			}
		},
		toggleElderSelector() {
			this.showElderSelector = !this.showElderSelector;
		},
		selectElder(elder) {
			this.selectedElder = elder;
			this.showElderSelector = false;
			this.healthAdvice = '正在生成健康建议...';
			this.loadHealthData(elder.id);
			this.loadHealthAdvice(elder.id);
		},
		async loadHealthAdvice(elderId) {
			try {
				const response = await healthService.getHealthAdvice(elderId);
				this.healthAdvice = response.advice;
			} catch (error) {
				console.error('加载健康建议失败:', error);
				this.healthAdvice = '获取健康建议失败，请稍后重试';
			}
		},
		showReminderModal() {
			this.showModal = true;
		},
		async sendReminder() {
			if (!this.selectedElder) {
				uni.showToast({
					title: '请先选择老人',
					icon: 'none'
				});
				return;
			}
			if (!this.reminderContent) {
				uni.showToast({
					title: '请输入提醒内容',
					icon: 'none'
				});
				return;
			}
			if (!this.reminderTime) {
				uni.showToast({
					title: '请选择提醒时间',
					icon: 'none'
				});
				return;
			}
			
			uni.showLoading({
				title: '发送中...'
			});
			
			try {
				// 将时间格式转换为后端需要的ISO格式
				const scheduledTime = this.reminderTime ? this.reminderTime.replace(' ', 'T') + ':00' : null;
				
				const reminderData = {
					receiver_id: this.selectedElder.id,
					reminder_type: this.reminderType,
					content: this.reminderContent,
					scheduled_time: scheduledTime
				};
				
				await healthService.sendHealthReminder(reminderData);
				
				uni.hideLoading();
				uni.showToast({
					title: '提醒发送成功',
					icon: 'success'
				});
				this.showModal = false;
				this.reminderContent = '';
				this.reminderTime = '';
			} catch (error) {
				uni.hideLoading();
				uni.showToast({
					title: error.response?.data?.detail || '发送失败，请稍后重试',
					icon: 'none'
				});
			}
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	padding-bottom: 20px;
	position: relative;
	overflow-x: hidden;
	overflow-y: auto;
}



/* 顶部导航 */
.top-nav {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 20px 24px;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
	border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.page-title {
	font-size: 28px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
	text-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
}

.elder-selector {
	display: flex;
	align-items: center;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	padding: 8px 16px;
	border-radius: 16px;
	color: #ffffff;
	font-size: 16px;
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
	transition: all 0.3s ease;
}

.elder-selector:hover {
	box-shadow: 0 6px 24px rgba(99, 102, 241, 0.4);
	transform: translateY(-2px);
}

.arrow-icon {
	margin-left: 8px;
	font-size: 12px;
}

/* 老人选择器下拉列表 */
.elder-selector-dropdown {
	position: absolute;
	top: 80px;
	right: 24px;
	width: 200px;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	border-radius: 16px;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
	border: 1px solid rgba(255, 255, 255, 0.2);
	z-index: 100;
	max-height: 300px;
	overflow-y: auto;
}

.elder-item {
	padding: 16px;
	border-bottom: 1px solid rgba(226, 232, 240, 0.5);
	transition: all 0.3s ease;
}

.elder-item:last-child {
	border-bottom: none;
}

.elder-item:hover {
	background: rgba(99, 102, 241, 0.1);
}

.elder-main-info {
	display: flex;
	align-items: center;
	margin-bottom: 4px;
	gap: 8px;
}

.elder-name {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
}

.elder-info {
	display: block;
	font-size: 14px;
	color: #64748b;
}

.elder-status {
	display: inline-block;
	padding: 4px 12px;
	border-radius: 12px;
	font-size: 12px;
	font-weight: 500;
}

.elder-status.normal {
	background: rgba(34, 197, 94, 0.1);
	color: #16a34a;
}

.elder-status.attention {
	background: rgba(245, 158, 11, 0.1);
	color: #d97706;
}

.elder-status.warning {
	background: rgba(239, 68, 68, 0.1);
	color: #dc2626;
}

/* 健康概览卡片 */
.overview-section {
	display: flex;
	justify-content: space-between;
	padding: 24px 8px;
	gap: 8px;
}

.overview-card {
	flex: 1;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	border-radius: 24px;
	padding: 16px;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
	position: relative;
	overflow: hidden;
	border: 1px solid rgba(255, 255, 255, 0.2);
	transition: all 0.3s ease;
	min-height: 220px;
	min-width: 0;
}

.overview-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
}

.overview-card::before {
	content: '';
	position: absolute;
	top: -1px;
	left: -1px;
	right: -1px;
	bottom: -1px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
	border-radius: 24px;
	z-index: -1;
	filter: blur(20px);
	opacity: 0.6;
}

.card-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 16px;
}

.card-title {
	font-size: 14px;
	font-weight: 600;
	color: #1e293b;
}

.card-subtitle {
	font-size: 12px;
	color: #6366f1;
	font-weight: 500;
}

/* 营养摄入卡片 */
.nutrition-content {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-bottom: 16px;
}

.nutrition-item {
	display: flex;
	align-items: baseline;
}

.nutrition-value {
	font-size: 24px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.nutrition-unit {
	font-size: 14px;
	color: #64748b;
	margin-left: 4px;
}

.nutrition-label {
	font-size: 12px;
	color: #64748b;
	margin-top: 4px;
}

.nutrition-details {
	display: flex;
	justify-content: space-around;
}

.detail-item {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.detail-value {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
}

.detail-label {
	font-size: 12px;
	color: #64748b;
}

/* 饮食规律卡片 */
.diet-content {
	display: flex;
	justify-content: space-around;
}

.diet-item {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.diet-status {
	width: 40px;
	height: 40px;
	border-radius: 50%;
	background: #e2e8f0;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 16px;
	font-weight: 600;
	color: #64748b;
	margin-bottom: 6px;
}

.diet-status.active {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	color: #ffffff;
}

.diet-time {
	font-size: 14px;
	color: #64748b;
}

/* 健康状态卡片 */
.health-content {
	display: flex;
	justify-content: space-around;
}

.health-indicator {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.indicator-value {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
}

.indicator-label {
	font-size: 14px;
	color: #64748b;
}

/* 健康标签样式 */
.health-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 8px;
	margin-top: 16px;
	padding-top: 16px;
	border-top: 1px solid rgba(226, 232, 240, 0.5);
}

.health-tag {
	padding: 6px 12px;
	border-radius: 16px;
	border: 1px solid;
	transition: all 0.3s ease;
}

.health-tag:hover {
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.health-tag-text {
	font-size: 12px;
	font-weight: 500;
}

/* 日期选择器 */
.date-selector {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0 24px;
	margin-bottom: 20px;
}

.date-text {
	font-size: 20px;
	font-weight: 600;
	color: #1e293b;
	text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.date-nav {
	display: flex;
	gap: 16px;
}

.nav-btn {
	width: 32px;
	height: 32px;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(10px);
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 20px;
	color: #6366f1;
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
	border: 1px solid rgba(255, 255, 255, 0.2);
	transition: all 0.3s ease;
}

.nav-btn:hover {
	background: rgba(99, 102, 241, 0.1);
	transform: scale(1.1);
}

/* 饮食记录列表 */
.diet-records {
	padding: 0 24px;
}

.record-card {
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	border-radius: 24px;
	padding: 20px;
	margin-bottom: 16px;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
	border: 1px solid rgba(255, 255, 255, 0.2);
	transition: all 0.3s ease;
}

.record-card:hover {
	transform: translateY(-2px);
	box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
}

.record-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 16px;
}

.record-time {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
}

.record-meal {
	font-size: 16px;
	color: #6366f1;
	font-weight: 500;
}

.record-content {
	margin-bottom: 16px;
}

.food-item {
	display: flex;
	align-items: center;
	margin-bottom: 12px;
}

.food-image {
	width: 48px;
	height: 48px;
	border-radius: 12px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-right: 12px;
}

.food-info {
	flex: 1;
}

.food-name {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
}

.food-calories {
	font-size: 14px;
	color: #64748b;
}

.record-footer {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.total-calories {
	font-size: 16px;
	font-weight: 600;
	color: #6366f1;
}

.nutrition-tags {
	display: flex;
	gap: 8px;
}

.nutrition-tag {
	padding: 4px 12px;
	background: #f1f5f9;
	border-radius: 12px;
}

.tag-text {
	font-size: 12px;
	color: #64748b;
}

/* AI智能健康建议 */
.advice-section {
	padding: 0 24px 24px;
}

.advice-card {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
	border-radius: 24px;
	padding: 24px;
	color: #ffffff;
	box-shadow: 0 12px 48px rgba(99, 102, 241, 0.4);
	position: relative;
	overflow: hidden;
	transition: all 0.3s ease;
}

.advice-card:hover {
	box-shadow: 0 16px 64px rgba(99, 102, 241, 0.6);
	transform: translateY(-4px);
}

.advice-card::before {
	content: '';
	position: absolute;
	top: -50%;
	left: -50%;
	width: 200%;
	height: 200%;
	background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
	animation: glowPulse 3s ease-in-out infinite;
}

@keyframes glowPulse {
	0%, 100% { opacity: 0.3; transform: scale(0.8); }
	50% { opacity: 0.6; transform: scale(1); }
}

.advice-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 16px;
	position: relative;
	z-index: 10;
}

.advice-title {
	font-size: 20px;
	font-weight: 600;
	text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.advice-badge {
	background: rgba(255, 255, 255, 0.2);
	padding: 4px 12px;
	border-radius: 12px;
	font-size: 14px;
	font-weight: 500;
	backdrop-filter: blur(10px);
}

.advice-content {
	font-size: 16px;
	line-height: 1.6;
	position: relative;
	z-index: 10;
	text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

/* 健康提醒按钮 */
.reminder-section {
	padding: 0 24px 24px;
}

.reminder-btn {
	width: 100%;
	height: 56px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 24px;
	color: #ffffff;
	font-size: 18px;
	font-weight: 600;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
	transition: all 0.3s ease;
	position: relative;
	overflow: hidden;
}

.reminder-btn::before {
	content: '';
	position: absolute;
	top: 0;
	left: -100%;
	width: 100%;
	height: 100%;
	background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
	transition: left 0.6s ease;
}

.reminder-btn:hover::before {
	left: 100%;
}

.reminder-btn:hover {
	box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
	transform: translateY(-2px);
}

.reminder-icon {
	font-size: 20px;
}

/* 弹窗样式 */
.modal {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.6);
	backdrop-filter: blur(10px);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
}

.modal-content {
	width: 90%;
	max-width: 400px;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	border-radius: 24px;
	padding: 24px;
	box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
	border: 1px solid rgba(255, 255, 255, 0.2);
	position: relative;
}

.modal-content::before {
	content: '';
	position: absolute;
	top: -1px;
	left: -1px;
	right: -1px;
	bottom: -1px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
	border-radius: 24px;
	z-index: -1;
	filter: blur(20px);
	opacity: 0.6;
}

.modal-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 24px;
}

.modal-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
}

.modal-close {
	font-size: 24px;
	color: #64748b;
}

.modal-body {
	margin-bottom: 24px;
}

.reminder-type,
.reminder-content,
.reminder-time {
	margin-bottom: 20px;
}

.type-label,
.content-label,
.time-label {
	font-size: 16px;
	font-weight: 500;
	color: #1e293b;
	margin-bottom: 8px;
	display: block;
}

.type-options {
	display: flex;
	gap: 12px;
}

.type-option {
	flex: 1;
	padding: 12px;
	border: 2px solid #e2e8f0;
	border-radius: 12px;
	text-align: center;
	font-size: 14px;
	color: #64748b;
	transition: all 0.3s ease;
}

.type-option.active {
	border-color: #6366f1;
	background: rgba(99, 102, 241, 0.1);
	color: #6366f1;
}

.content-input {
	width: 100%;
	height: 120px;
	border: 2px solid #e2e8f0;
	border-radius: 16px;
	padding: 16px;
	font-size: 16px;
	color: #1e293b;
	resize: none;
}

/* 时间输入框 */
.time-input {
	width: 100%;
	height: 48px;
	border: 2px solid #e2e8f0;
	border-radius: 16px;
	padding: 0 16px;
	font-size: 16px;
	color: #1e293b;
	background: #ffffff;
	transition: all 0.3s ease;
}

.time-input:focus {
	border-color: #6366f1;
	background: rgba(99, 102, 241, 0.05);
	outline: none;
}

.modal-footer {
	display: flex;
	gap: 16px;
}

.cancel-btn,
.send-btn {
	flex: 1;
	height: 48px;
	border-radius: 16px;
	font-size: 16px;
	font-weight: 500;
	transition: all 0.3s ease;
}

.cancel-btn {
	background: rgba(241, 245, 249, 0.8);
	color: #64748b;
	border: 1px solid rgba(226, 232, 240, 0.5);
	backdrop-filter: blur(10px);
}

.cancel-btn:hover {
	background: rgba(241, 245, 249, 1);
	transform: translateY(-2px);
}

.send-btn {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	color: #ffffff;
	border: none;
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
	position: relative;
	overflow: hidden;
}

.send-btn::before {
	content: '';
	position: absolute;
	top: 0;
	left: -100%;
	width: 100%;
	height: 100%;
	background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
	transition: left 0.6s ease;
}

.send-btn:hover::before {
	left: 100%;
}

.send-btn:hover {
	box-shadow: 0 8px 24px rgba(99, 102, 241, 0.5);
	transform: translateY(-2px);
}

/* 加载状态 */
.loading-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 20px;
}

.loading-spinner {
	width: 30px;
	height: 30px;
	border: 3px solid rgba(99, 102, 241, 0.3);
	border-top: 3px solid #6366f1;
	border-radius: 50%;
	animation: spin 1s linear infinite;
	margin-bottom: 12px;
}

.loading-text {
	font-size: 14px;
	color: #64748b;
}

@keyframes spin {
	0% { transform: rotate(0deg); }
	100% { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 20px;
	text-align: center;
}

.empty-text {
	font-size: 14px;
	color: #64748b;
	line-height: 1.5;
}
</style>