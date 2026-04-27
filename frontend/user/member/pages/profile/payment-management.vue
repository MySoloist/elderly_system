<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">支付管理</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 支付方式列表 -->
		<view class="payment-list">
			<view class="payment-item" v-for="(payment, index) in paymentMethods" :key="index">
				<view class="payment-icon"></view>
				<view class="payment-info">
					<text class="payment-name">{{ payment.name }}</text>
					<text class="payment-desc">{{ payment.desc }}</text>
				</view>
				<view class="payment-status">
					<view class="status-dot" :class="payment.status"></view>
					<text class="status-text">{{ payment.status === 'active' ? '已启用' : '未启用' }}</text>
				</view>
			</view>
		</view>
		
		<!-- 添加支付方式 -->
		<button class="add-btn" @click="addPayment">
			<text class="add-icon">+</text>
			<text class="add-text">添加支付方式</text>
		</button>
		
		<!-- 消费记录 -->
		<view class="section">
			<text class="section-title">最近消费</text>
			<view class="record-item" v-for="(record, index) in consumptionRecords" :key="index">
				<view class="record-info">
					<text class="record-name">{{ record.name }}</text>
					<text class="record-time">{{ record.time }}</text>
				</view>
				<text class="record-amount">¥{{ record.amount }}</text>
			</view>
		</view>
		
		<!-- 余额信息 -->
		<view class="balance-card">
			<text class="balance-label">账户余额</text>
			<text class="balance-amount">¥{{ balance }}</text>
			<button class="recharge-btn" @click="recharge">充值</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			paymentMethods: [
				{
					id: 1,
					name: '微信支付',
					desc: '微信支付',
					status: 'active'
				},
				{
					id: 2,
					name: '支付宝',
					desc: '支付宝',
					status: 'inactive'
				},
				{
					id: 3,
					name: '银行卡',
					desc: '尾号 ****1234',
					status: 'active'
				}
			],
			consumptionRecords: [
				{
					id: 1,
					name: '订单支付',
					time: '2024-01-15 12:00',
					amount: 51.00
				},
				{
					id: 2,
					name: '余额充值',
					time: '2024-01-15 10:30',
					amount: 200.00
				},
				{
					id: 3,
					name: '订单支付',
					time: '2024-01-14 18:00',
					amount: 34.00
				}
			],
			balance: 125.50
		};
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		addPayment() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		recharge() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background: #f8fafc;
	padding-bottom: 180px;
}

/* 顶部导航 */
.top-nav {
	display: flex;
	align-items: center;
	padding: 44px 20px 12px;
	background: #ffffff;
	position: sticky;
	top: 0;
	z-index: 100;
	box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
}

.back-btn {
	width: 36px;
	height: 36px;
	border-radius: 10px;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 12px;
	transition: all 0.2s ease;
}
.back-btn:active {
	transform: scale(0.9);
}

.back-icon {
	font-size: 20px;
	color: #1e293b;
	font-weight: 600;
}

.page-title {
	flex: 1;
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	text-align: center;
}

.nav-right {
	width: 36px;
}

/* 支付方式列表 */
.payment-list {
	padding: 20px;
}

.payment-item {
	display: flex;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 16px;
	margin-bottom: 12px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.5);
}

.payment-icon {
	width: 48px;
	height: 48px;
	border-radius: 12px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-right: 16px;
	display: flex;
	align-items: center;
	justify-content: center;
}
.payment-icon::after {
	content: '💳';
	font-size: 24px;
}

.payment-info {
	flex: 1;
}

.payment-name {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
	display: block;
	margin-bottom: 4px;
}

.payment-desc {
	font-size: 13px;
	color: #64748b;
	display: block;
}

.payment-status {
	display: flex;
	align-items: center;
	gap: 6px;
	background: #f8fafc;
	padding: 4px 10px;
	border-radius: 20px;
}

.status-dot {
	width: 6px;
	height: 6px;
	border-radius: 50%;
	background: #cbd5e1;
}

.status-dot.active {
	background: #10b981;
}

.status-text {
	font-size: 12px;
	color: #64748b;
}

/* 添加按钮 */
.add-btn {
	position: fixed;
	bottom: 30px;
	left: 20px;
	right: 20px;
	height: 52px;
	background: #ffffff;
	border: 1.5px dashed #cbd5e1;
	border-radius: 16px;
	color: #64748b;
	font-size: 15px;
	font-weight: 500;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	transition: all 0.2s ease;
}
.add-btn:active {
	background: #f8fafc;
	transform: scale(0.98);
}

.add-icon {
	font-size: 20px;
}

.add-text {
	
}

/* 章节标题 */
.section {
	padding: 0 20px 24px;
}

.section-title {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 16px;
	display: block;
}

/* 消费记录 */
.record-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 16px;
	margin-bottom: 12px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.5);
}

.record-info {
	flex: 1;
}

.record-name {
	font-size: 15px;
	font-weight: 600;
	color: #1e293b;
	display: block;
	margin-bottom: 4px;
}

.record-time {
	font-size: 13px;
	color: #94a3b8;
	display: block;
}

.record-amount {
	font-size: 16px;
	font-weight: 700;
	color: #1e293b;
}

/* 余额卡片 */
.balance-card {
	position: fixed;
	bottom: 100px;
	left: 20px;
	right: 20px;
	background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
	border-radius: 20px;
	padding: 24px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
	z-index: 90;
}

.balance-label {
	font-size: 16px;
	color: rgba(255, 255, 255, 0.9);
	display: block;
}

.balance-amount {
	font-size: 28px;
	font-weight: 700;
	color: #ffffff;
}

.recharge-btn {
	padding: 8px 20px;
	background: rgba(255, 255, 255, 0.2);
	border: none;
	border-radius: 16px;
	color: #ffffff;
	font-size: 14px;
	font-weight: 500;
}
</style>
