<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<text class="page-title">消费管理</text>
			<view class="elder-selector" @click="showElderSelector" :disabled="loading">
				<text class="selector-text">{{ loading ? '加载中...' : (selectedElder ? selectedElder.name : '选择老人') }}</text>
				<text class="arrow-icon">▼</text>
			</view>
		</view>
		
		<!-- 时间范围选择 -->
		<view class="time-section">
			<view class="time-tabs">
				<view class="time-tab" v-for="(tab, index) in timeTabs" :key="index"
					:class="{ active: selectedTime === tab.value }"
					@click="selectTime(tab.value)">
					<text class="tab-text">{{ tab.name }}</text>
				</view>
			</view>
			<view class="date-picker" v-if="selectedTime === 'custom'">
				<input class="date-input" type="date" v-model="startDate" @change="onDateChange" />
				<text class="date-separator">至</text>
				<input class="date-input" type="date" v-model="endDate" @change="onDateChange" />
			</view>
		</view>
		
		<!-- 消费统计卡片 -->
		<view class="stats-section">
			<view class="stats-card total-card">
				<view class="card-header">
					<text class="card-title">总消费金额</text>
					<text class="card-subtitle">¥{{ totalAmount }}</text>
				</view>
				<view class="card-trend">
					<text class="trend-text">较上月</text>
					<text class="trend-value" :class="amountTrend > 0 ? 'increase' : 'decrease'">
						{{ amountTrend > 0 ? '+' : '' }}{{ amountTrend }}%
					</text>
				</view>
			</view>
			
			<view class="stats-card order-card">
				<view class="card-header">
					<text class="card-title">订单数量</text>
					<text class="card-subtitle">{{ orderCount }}</text>
				</view>
				<view class="card-trend">
					<text class="trend-text">较上月</text>
					<text class="trend-value" :class="orderTrend > 0 ? 'increase' : 'decrease'">
						{{ orderTrend > 0 ? '+' : '' }}{{ orderTrend }}%
					</text>
				</view>
			</view>
			
			<view class="stats-card avg-card">
				<view class="card-header">
					<text class="card-title">平均每餐</text>
					<text class="card-subtitle">¥{{ avgAmount }}</text>
				</view>
				<view class="card-trend">
					<text class="trend-text">较上月</text>
					<text class="trend-value" :class="avgTrend > 0 ? 'increase' : 'decrease'">
						{{ avgTrend > 0 ? '+' : '' }}{{ avgTrend }}%
					</text>
				</view>
			</view>
		</view>
		
		<!-- 账单明细列表 -->
		<view class="bills-section">
			<text class="section-title">账单明细</text>
			<view class="bill-group" v-for="(group, index) in billGroups" :key="index">
				<text class="group-date">{{ group.date }}</text>
				<view class="bill-item" v-for="(bill, billIndex) in group.bills" :key="billIndex">
					<view class="bill-info">
						<text class="bill-name">{{ bill.name }}</text>
						<text class="bill-time">{{ bill.time }}</text>
					</view>
					<text class="bill-amount">-¥{{ bill.amount }}</text>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view class="empty-state" v-if="billGroups.length === 0">
				<view class="empty-icon"></view>
				<text class="empty-title">暂无账单</text>
				<text class="empty-subtitle">快去为老人点餐吧</text>
			</view>
		</view>
		
		<!-- 老人选择器弹窗 -->
		<view class="elder-modal" v-if="showElderModal">
			<view class="elder-modal-content">
				<view class="elder-modal-header">
					<text class="elder-modal-title">选择老人</text>
					<text class="elder-modal-close" @click="showElderModal = false">×</text>
				</view>
				<view class="elder-list">
					<!-- 加载状态 -->
					<view v-if="loading" class="loading-state">
						<view class="loading-spinner"></view>
						<text class="loading-text">加载中...</text>
					</view>
					
					<!-- 空状态 -->
					<view v-else-if="elders.length === 0" class="empty-state">
						<text class="empty-text">暂无绑定老人，请先添加绑定</text>
					</view>
					
					<!-- 老人列表 -->
					<view v-else class="elder-item" v-for="(elder, index) in elders" :key="index"
						:class="{ active: selectedElder && selectedElder.id === elder.id }"
						@click="selectElder(elder)">
						<view class="elder-item-avatar"></view>
						<view class="elder-item-info">
							<view class="elder-item-main">
								<text class="elder-item-name">{{ elder.name }}</text>
								<text class="elder-item-tag">{{ elder.tag }}</text>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			selectedElder: null,
			elders: [],
			loading: false,
			timeTabs: [
				{ value: 'today', name: '今日' },
				{ value: 'week', name: '本周' },
				{ value: 'month', name: '本月' },
				{ value: 'custom', name: '自定义' }
			],
			selectedTime: 'month',
			startDate: '',
			endDate: '',
			totalAmount: 0,
			orderCount: 0,
			avgAmount: 0,
			amountTrend: 0,
			orderTrend: 0,
			avgTrend: 0,
			billGroups: [],
			showElderModal: false
		};
	},
	onLoad() {
		this.loadElders();
	},
	methods: {
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
					// 转换数据格式，添加标签信息
					this.elders = response.data.map(elder => ({
						id: elder.elderly_id,
						name: elder.elderly_name,
						tag: this.getElderTag(elder.elderly_age, elder.elderly_gender)
					}));
					
					// 默认选择第一个老人
					if (this.elders.length > 0) {
						this.selectedElder = this.elders[0];
						this.loadConsumeData(this.selectedElder.id);
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
		getElderTag(age, gender) {
			// 根据年龄和性别生成标签
			if (age && age > 80) {
				return '高龄';
			} else if (gender === '女') {
				return '奶奶';
			} else {
				return '爷爷';
			}
		},
		async loadConsumeData(elderId) {
			try {
				this.loading = true;
				
				// 根据选择的时间范围构建日期参数
				let dateParams = '';
				const today = new Date();
				
				switch (this.selectedTime) {
					case 'today':
						dateParams = `?date=${today.toISOString().split('T')[0]}`;
						break;
					case 'week':
						const weekStart = new Date(today);
						weekStart.setDate(today.getDate() - today.getDay());
						const weekEnd = today;
						dateParams = `?start_date=${weekStart.toISOString().split('T')[0]}&end_date=${weekEnd.toISOString().split('T')[0]}`;
						break;
					case 'month':
						const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
						const monthEnd = today;
						dateParams = `?start_date=${monthStart.toISOString().split('T')[0]}&end_date=${monthEnd.toISOString().split('T')[0]}`;
						break;
					case 'custom':
						if (this.startDate && this.endDate) {
							dateParams = `?start_date=${this.startDate}&end_date=${this.endDate}`;
						}
						break;
				}
				
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/consume/${elderId}${dateParams}`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					const data = response.data;
					this.totalAmount = data.total_amount || 0;
					this.orderCount = data.order_count || 0;
					this.avgAmount = data.avg_amount || 0;
					this.amountTrend = data.amount_trend || 0;
					this.orderTrend = data.order_trend || 0;
					this.avgTrend = data.avg_trend || 0;
					this.billGroups = data.bill_groups || [];
				} else {
					throw new Error(response.data?.detail || '加载消费数据失败');
				}
			} catch (error) {
				console.error('加载消费数据失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		selectTime(time) {
			this.selectedTime = time;
			if (this.selectedElder) {
				this.loadConsumeData(this.selectedElder.id);
			}
		},
		showElderSelector() {
			this.showElderModal = true;
		},
		onDateChange() {
			if (this.selectedTime === 'custom' && this.startDate && this.endDate && this.selectedElder) {
				this.loadConsumeData(this.selectedElder.id);
			}
		},
		selectElder(elder) {
			this.selectedElder = elder;
			this.showElderModal = false;
			this.loadConsumeData(elder.id);
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
}

/* 顶部导航 */
.top-nav {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 20px 24px;
	background: #ffffff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.page-title {
	font-size: 28px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.elder-selector {
	display: flex;
	align-items: center;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	padding: 8px 16px;
	border-radius: 16px;
	color: #ffffff;
	font-size: 16px;
}

.arrow-icon {
	margin-left: 8px;
	font-size: 12px;
}

/* 时间范围选择 */
.time-section {
	background: #ffffff;
	padding: 20px 24px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.time-tabs {
	display: flex;
	gap: 12px;
	margin-bottom: 20px;
}

.time-tab {
	flex: 1;
	padding: 12px;
	background: #f1f5f9;
	border-radius: 16px;
	text-align: center;
	font-size: 16px;
	color: #64748b;
	font-weight: 500;
	transition: all 0.3s ease;
}

.time-tab.active {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	color: #ffffff;
}

.date-picker {
	display: flex;
	align-items: center;
	gap: 12px;
}

.date-input {
	flex: 1;
	height: 48px;
	padding: 0 16px;
	border: 2px solid #e2e8f0;
	border-radius: 16px;
	font-size: 16px;
	color: #1e293b;
	background: #f8fafc;
}

.date-separator {
	font-size: 16px;
	color: #64748b;
}

/* 消费统计卡片 */
.stats-section {
	display: flex;
	justify-content: space-between;
	padding: 24px;
	gap: 16px;
}

.stats-card {
	flex: 1;
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
	position: relative;
	overflow: hidden;
}

.stats-card::before {
	content: '';
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 4px;
	background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
}

.card-header {
	margin-bottom: 16px;
}

.card-title {
	font-size: 16px;
	color: #64748b;
	font-weight: 500;
	display: block;
	margin-bottom: 8px;
}

.card-subtitle {
	font-size: 32px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.card-trend {
	display: flex;
	align-items: center;
	gap: 8px;
}

.trend-text {
	font-size: 14px;
	color: #64748b;
}

.trend-value {
	font-size: 14px;
	font-weight: 600;
}

.trend-value.increase {
	color: #ef4444;
}

.trend-value.decrease {
	color: #10b981;
}

.section-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 20px;
	display: block;
}

/* 账单明细列表 */
.bills-section {
	padding: 0 24px 24px;
}

.bill-group {
	background: #ffffff;
	border-radius: 24px;
	padding: 20px;
	margin-bottom: 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.group-date {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 16px;
	display: block;
	padding-bottom: 12px;
	border-bottom: 1px solid #f1f5f9;
}

.bill-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 12px 0;
	border-bottom: 1px solid #f1f5f9;
}

.bill-item:last-child {
	border-bottom: none;
}

.bill-info {
	flex: 1;
}

.bill-name {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
	display: block;
	margin-bottom: 4px;
}

.bill-time {
	font-size: 14px;
	color: #64748b;
}

.bill-amount {
	font-size: 18px;
	font-weight: 600;
	color: #ef4444;
}

/* 空状态 */
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 24px;
	text-align: center;
	background: #ffffff;
	border-radius: 24px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.empty-icon {
	width: 80px;
	height: 80px;
	border-radius: 50%;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-bottom: 24px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.empty-icon::before {
	content: '';
	width: 40px;
	height: 40px;
	background: rgba(255, 255, 255, 0.3);
	border-radius: 50%;
}

.empty-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 12px;
	display: block;
}

.empty-subtitle {
	font-size: 16px;
	color: #64748b;
	display: block;
}

/* 老人选择器弹窗 */
.elder-modal {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
}

.elder-modal-content {
	width: 90%;
	max-width: 400px;
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
}

.elder-modal-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 24px;
}

.elder-modal-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
}

.elder-modal-close {
	font-size: 24px;
	color: #64748b;
}

.elder-list {
	
}

.elder-item {
	display: flex;
	align-items: center;
	padding: 16px;
	border: 2px solid #e2e8f0;
	border-radius: 16px;
	margin-bottom: 12px;
	transition: all 0.3s ease;
}

.elder-item.active {
	border-color: #6366f1;
	background: rgba(99, 102, 241, 0.1);
}

.elder-item-avatar {
	width: 48px;
	height: 48px;
	border-radius: 50%;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-right: 16px;
}

.elder-item-info {
	
}

.elder-item-main {
	display: flex;
	align-items: center;
	gap: 8px;
}

.elder-item-name {
	font-size: 16px;
	font-weight: 500;
	color: #1e293b;
}

.elder-item-tag {
	font-size: 14px;
	color: #6366f1;
	background: rgba(99, 102, 241, 0.1);
	padding: 2px 8px;
	border-radius: 10px;
}

/* 加载状态 */
.loading-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 40px 0;
}

.loading-spinner {
	width: 40px;
	height: 40px;
	border: 3px solid rgba(99, 102, 241, 0.3);
	border-top: 3px solid #6366f1;
	border-radius: 50%;
	animation: spin 1s linear infinite;
	margin-bottom: 16px;
}

.loading-text {
	font-size: 16px;
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
	padding: 40px 0;
	text-align: center;
}

.empty-text {
	font-size: 16px;
	color: #64748b;
	line-height: 1.5;
}
</style>