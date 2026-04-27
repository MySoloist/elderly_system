<template>
	<view class="income-container">
		<view class="time-tabs">
			<view 
				v-for="tab in timeTabs" 
				:key="tab.value"
				:class="['tab-item', { active: activeTab === tab.value }]"
				@click="switchTab(tab.value)"
			>
				{{ tab.label }}
			</view>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<text class="loading-icon">⏳</text>
			<text class="loading-text">加载中...</text>
		</view>
		
		<view v-else>
			<view class="stats-section">
				<view class="stat-card">
					<text class="stat-label">今日收入</text>
					<text class="stat-value">¥{{ incomeStats.today_income }}</text>
				</view>
				<view class="stat-card">
					<text class="stat-label">本月收入</text>
					<text class="stat-value">¥{{ incomeStats.month_income }}</text>
				</view>
				<view class="stat-card">
					<text class="stat-label">总累计收入</text>
					<text class="stat-value">¥{{ incomeStats.total_income }}</text>
				</view>
			</view>
			
			<view class="detail-section">
				<view class="detail-header">
					<text class="detail-title">收入明细</text>
				</view>
				
				<view v-if="incomeDetails.length > 0" class="detail-list">
					<view v-for="item in incomeDetails" :key="item.id" class="detail-item">
						<view class="item-header">
							<text class="order-number">{{ item.order_no }}</text>
							<text class="income-time">{{ item.time }}</text>
						</view>
						<view class="item-content">
							<text class="meal-name">{{ item.meal_name }}</text>
							<text class="income-amount">+¥{{ item.amount }}</text>
						</view>
					</view>
				</view>
				
				<view v-else class="empty-state">
					<text class="empty-icon">📊</text>
					<text class="empty-text">暂无收入记录</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				activeTab: 'today',
				timeTabs: [
					{ label: '今日', value: 'today' },
					{ label: '本周', value: 'week' },
					{ label: '本月', value: 'month' },
					{ label: '自定义', value: 'custom' }
				],
				incomeStats: {
					today_income: 0,
					month_income: 0,
					total_income: 0,
					balance: 0
				},
				incomeDetails: [],
				loading: false
			}
		},
		onLoad() {
			this.loadIncomeData()
		},
		methods: {
			// 加载收入数据
			async loadIncomeData(timeRange = 'today') {
				this.loading = true
				try {
					const data = await api.profile.getIncomeStatistics(timeRange)
					this.incomeStats = {
						today_income: data.today_income,
						month_income: data.month_income,
						total_income: data.total_income,
						balance: data.balance
					}
					this.incomeDetails = data.income_details
				} catch (error) {
					console.error('加载收入数据失败:', error)
					uni.showToast({
						title: '加载失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			
			// 切换标签页
			switchTab(tabValue) {
				this.activeTab = tabValue
				// 根据标签页筛选数据
				this.loadIncomeData(tabValue)
			},
			

		}
	}
</script>

<style scoped>
	.income-container {
		min-height: 100vh;
	}
	
	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 100rpx 0;
	}
	
	.loading-icon {
		font-size: 120rpx;
		margin-bottom: 20rpx;
	}
	
	.loading-text {
		font-size: 32rpx;
		color: #64748b;
	}
	
	.time-tabs {
		background-color: white;
		display: flex;
		padding: 0 30rpx;
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
	
	.stats-section {
		display: flex;
		background-color: white;
		padding: 30rpx;
		margin-bottom: 20rpx;
		gap: 20rpx;
	}
	
	.stat-card {
		flex: 1;
		background-color: #f8fafc;
		border-radius: 16rpx;
		padding: 24rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	
	.stat-label {
		font-size: 24rpx;
		color: #64748b;
		margin-bottom: 8rpx;
	}
	
	.stat-value {
		font-size: 32rpx;
		font-weight: 700;
		color: #10b981;
	}
	
	.detail-section {
		background-color: white;
		padding: 30rpx;
	}
	
	.detail-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 30rpx;
	}
	
	.detail-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #1e293b;
	}
	
	
	
	.detail-list {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}
	
	.detail-item {
		padding: 24rpx;
		background-color: #f8fafc;
		border-radius: 16rpx;
	}
	
	.item-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12rpx;
	}
	
	.order-number {
		font-size: 24rpx;
		color: #94a3b8;
	}
	
	.income-time {
		font-size: 24rpx;
		color: #64748b;
	}
	
	.item-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.meal-name {
		font-size: 28rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.income-amount {
		font-size: 32rpx;
		color: #10b981;
		font-weight: 700;
	}
	
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60rpx 0;
	}
	
	.empty-icon {
		font-size: 100rpx;
		margin-bottom: 20rpx;
	}
	
	.empty-text {
		font-size: 32rpx;
		color: #94a3b8;
	}
</style>