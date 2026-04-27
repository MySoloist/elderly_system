<template>
	<view class="detail-container">
		<view v-if="loading" class="loading-container">
			<text class="loading-text">加载中...</text>
		</view>
		
		<view v-else-if="order" class="order-content">
			<view class="order-status">
				<view :class="['status-tag', order.status]">
					{{ getStatusText(order.status) }}
				</view>
			</view>
			
			<view class="info-card">
				<view class="card-section">
					<text class="section-title">老人信息</text>
					<view class="elder-info">
							<text class="avatar">👴</text>
							<view class="elder-details">
								<text class="elder-name">{{ order.elderly_name }}</text>
								<text class="elder-phone">{{ order.elderly_phone }}</text>
							</view>
						</view>
						<view class="community-info">
							<text class="community-icon">🏘️</text>
							<text class="community-name">{{ order.community_name }}</text>
						</view>
				</view>
				
				<view class="card-section">
					<text class="section-title">配送地址</text>
					<view class="address-info">
						<text class="address-icon">📍</text>
						<text class="address">{{ order.delivery_address }}</text>
					</view>
				</view>
				
				<view class="card-section">
					<text class="section-title">餐品信息</text>
					<view class="meal-info">
						<text class="meal-name">{{ order.meal_name }}</text>
						<text class="meal-quantity">x{{ order.quantity }}</text>
					</view>
					<text v-if="order.notes" class="remark">备注：{{ order.notes }}</text>
				</view>
				
				<view class="card-section">
					<text class="section-title">订单信息</text>
					<view class="order-meta">
						<view class="meta-item">
							<text class="meta-label">订单编号</text>
							<text class="meta-value">{{ order.order_no }}</text>
						</view>
						<view class="meta-item">
							<text class="meta-label">下单时间</text>
							<text class="meta-value">{{ order.created_at }}</text>
						</view>
						<view class="meta-item">
							<text class="meta-label">预计送达时间</text>
							<text class="meta-value">{{ order.estimatedTime }}</text>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view v-if="!loading && order" class="action-section">
			<!-- 检查订单是否已被管理员指派且当前用户不是被指派的配送员 -->
			<view v-if="order.is_assigned_by_admin && order.assigned_deliverer_id !== currentUserId" class="assigned-notice">
				<text class="notice-icon">⚠️</text>
				<text class="notice-text">该订单已被管理员指派，不允许您操作</text>
			</view>
			<button v-else-if="order.status === 'pending_accept'" @click="startDelivery" class="primary-button">开始配送</button>
			<button v-else-if="order.status === 'delivering'" @click="completeDelivery" class="primary-button">确认送达</button>
			
			<view class="action-buttons">
				<button @click="callElderly" class="secondary-button">
					<text class="button-icon">📞</text>
					<text>联系老人</text>
				</button>
				<button @click="goToException" class="warning-button">
					<text class="button-icon">⚠️</text>
					<text>异常处理</text>
				</button>
			</view>
			
			<button @click="goToNavigation" class="navigation-button">
				<text class="button-icon">🧭</text>
				<text>导航前往</text>
			</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
import { calculateDistance, estimateDeliveryTime } from '../../utils/map.js'
	
	export default {
		data() {
			return {
				order: {},
				loading: true,
				currentUserId: null,
				currentLocation: {
					latitude: 0,
					longitude: 0
				}
			}
		},
		onLoad(options) {
			// 获取当前用户信息
			const user = uni.getStorageSync('user')
			this.currentUserId = user ? user.id : null
			const orderId = options.id
			this.getCurrentLocation()
			this.loadOrderDetail(orderId)
		},
		methods: {
			async loadOrderDetail(orderId) {
				try {
					this.loading = true
					const res = await api.orders.getOrderDetail(orderId)
					this.order = res.data
					// 计算距离和预计送达时间
					await this.calculateOrderDistance()
				} catch (error) {
					console.error('加载订单失败:', error)
					uni.showToast({
						title: '加载订单失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			getStatusText(status) {
				const statusMap = {
					pending: '待接单',
					delivering: '配送中',
					completed: '已完成'
				}
				return statusMap[status] || status
			},
			// 获取当前位置
			getCurrentLocation() {
				uni.getLocation({
					type: 'gcj02',
					success: (res) => {
						this.currentLocation = {
							latitude: res.latitude,
							longitude: res.longitude
						}
					},
					fail: (error) => {
						console.error('获取位置失败:', error)
					}
				})
			},
			// 计算预计送达时间
			async calculateOrderDistance() {
				if (!this.order || !this.currentLocation.latitude) return
				
				let estimatedTime = '暂无预计时间'
				
				try {
					// 优先使用后端提供的位置信息（地理空间数据）
					if (this.order.elderly_location && this.order.elderly_location.latitude && this.order.elderly_location.longitude) {
						// 使用后端返回的老人位置计算距离
						const calcDistance = calculateDistance(
							this.currentLocation.latitude,
							this.currentLocation.longitude,
							this.order.elderly_location.latitude,
							this.order.elderly_location.longitude
						)
						estimatedTime = estimateDeliveryTime(calcDistance)
					} else {
						// 后端没有提供位置信息，使用地址解析
						const realDistance = await this.calculateRealDistance(this.order.delivery_address)
						if (realDistance !== '距离未知') {
							// 解析距离字符串获取数值
							const distanceMatch = realDistance.match(/距离(\d+(?:\.\d+)?)km/)
							if (distanceMatch) {
								const calcDistance = parseFloat(distanceMatch[1])
								estimatedTime = estimateDeliveryTime(calcDistance)
							} else {
								const distanceMatchM = realDistance.match(/距离(\d+)m/)
								if (distanceMatchM) {
									const calcDistance = parseInt(distanceMatchM[1]) / 1000
									estimatedTime = estimateDeliveryTime(calcDistance)
								}
							}
						}
					}
				} catch (error) {
					console.error('计算距离失败:', error)
				}
				
				// 更新订单信息
				this.order.estimatedTime = estimatedTime
			},
			// 根据地址计算实际距离
			async calculateRealDistance(address) {
				try {
					// 这里应该调用地图API进行地址解析
					// 现在返回模拟数据
					return `距离${Math.floor(Math.random() * 500 + 100)}m`
				} catch (error) {
					console.error('地址解析失败:', error)
					return '距离未知'
				}
			},
			async startDelivery() {
				uni.showModal({
					title: '开始配送',
					content: '确定开始配送吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.orders.acceptOrder(this.order.id)
								this.order.status = 'delivering'
								uni.showToast({
									title: '开始配送',
									icon: 'success'
								})
							} catch (error) {
								console.error('开始配送失败:', error)
								uni.showToast({
									title: '开始配送失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			async completeDelivery() {
				uni.showModal({
					title: '确认送达',
					content: '确认餐品已送达吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.orders.completeOrder(this.order.id)
								this.order.status = 'completed'
								uni.showToast({
									title: '送达成功',
									icon: 'success'
								})
								setTimeout(() => {
									uni.navigateBack()
								}, 1000)
							} catch (error) {
								console.error('送达失败:', error)
								uni.showToast({
									title: '送达失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			callElderly() {
				uni.makePhoneCall({
					phoneNumber: this.order.elderly_phone.replace('****', '1234'),
					success: () => {
						console.log('拨打电话成功')
					},
					fail: () => {
						uni.showToast({
							title: '拨打电话失败',
							icon: 'none'
						})
					}
				})
			},
			goToException() {
				uni.navigateTo({
					url: '/pages/exception/exception'
				})
			},
			goToNavigation() {
				uni.navigateTo({
					url: '/pages/navigation/navigation?id=' + this.order.id
				})
			}
		}
	}
</script>

<style scoped>
	.detail-container {
		min-height: 100vh;
		padding-bottom: 40rpx;
	}
	
	.loading-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 400rpx;
	}
	
	.loading-text {
		font-size: 32rpx;
		color: #64748b;
	}
	
	.order-status {
		background-color: white;
		padding: 30rpx;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	
	.status-tag {
		padding: 16rpx 40rpx;
		border-radius: 20rpx;
		font-size: 32rpx;
		font-weight: 500;
	}
	
	.status-tag.pending {
		background-color: #fffbeb;
		color: #f59e0b;
	}
	
	.status-tag.delivering {
		background-color: #dbeafe;
		color: #3b82f6;
	}
	
	.status-tag.completed {
		background-color: #ecfdf5;
		color: #10b981;
	}
	
	.assigned-notice {
		background-color: #fef2f2;
		color: #dc2626;
		padding: 20rpx;
		border-radius: 10rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 20rpx;
	}
	
	.notice-icon {
		font-size: 32rpx;
		margin-right: 10rpx;
	}
	
	.notice-text {
		font-size: 28rpx;
		font-weight: 500;
	}
	
	.info-card {
		background-color: white;
		margin: 20rpx;
		border-radius: 24rpx;
		padding: 30rpx;
		box-shadow: 0 2px 8px rgba(0,0,0,0.08);
	}
	
	.card-section {
		margin-bottom: 30rpx;
	}
	
	.card-section:last-child {
		margin-bottom: 0;
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #1e293b;
		margin-bottom: 20rpx;
		display: block;
	}
	
	.elder-info {
		display: flex;
		align-items: center;
	}
	
	.avatar {
		font-size: 64rpx;
		margin-right: 20rpx;
	}
	
	.elder-details {
		display: flex;
		flex-direction: column;
	}
	
	.elder-name {
		font-size: 36rpx;
		color: #1e293b;
		font-weight: 500;
		margin-bottom: 8rpx;
	}
	
	.elder-phone {
		font-size: 28rpx;
		color: #64748b;
	}
	
	.community-info {
		display: flex;
		align-items: center;
		margin-top: 16rpx;
	}
	
	.community-icon {
		font-size: 28rpx;
		margin-right: 8rpx;
	}
	
	.community-name {
		font-size: 28rpx;
		color: #6366f1;
		font-weight: 500;
		background-color: rgba(99, 102, 241, 0.1);
		padding: 4rpx 12rpx;
		border-radius: 12rpx;
	}
	
	.address-info {
		display: flex;
		align-items: flex-start;
	}
	
	.address-icon {
		font-size: 28rpx;
		margin-right: 12rpx;
		margin-top: 4rpx;
	}
	
	.address {
		font-size: 32rpx;
		color: #1e293b;
		line-height: 1.5;
		flex: 1;
	}
	
	.meal-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16rpx;
	}
	
	.meal-name {
		font-size: 36rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.meal-quantity {
		font-size: 32rpx;
		color: #64748b;
	}
	
	.remark {
		font-size: 28rpx;
		color: #64748b;
		display: block;
	}
	
	.order-meta {
		display: flex;
		flex-direction: column;
		gap: 16rpx;
	}
	
	.meta-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.meta-label {
		font-size: 28rpx;
		color: #64748b;
	}
	
	.meta-value {
		font-size: 28rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.action-section {
		padding: 0 20rpx;
	}
	
	.primary-button {
		width: 100%;
		height: 96rpx;
		background-color: #10b981;
		color: white;
		border: none;
		border-radius: 24rpx;
		font-size: 32rpx;
		font-weight: 500;
		margin-bottom: 20rpx;
	}
	
	.action-buttons {
		display: flex;
		gap: 20rpx;
		margin-bottom: 20rpx;
	}
	
	.secondary-button, .warning-button {
		flex: 1;
		height: 80rpx;
		border-radius: 20rpx;
		font-size: 28rpx;
		border: none;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8rpx;
	}
	
	.secondary-button {
		background-color: #3b82f6;
		color: white;
	}
	
	.warning-button {
		background-color: #f59e0b;
		color: white;
	}
	
	.navigation-button {
		width: 100%;
		height: 80rpx;
		background-color: #3b82f6;
		color: white;
		border: none;
		border-radius: 20rpx;
		font-size: 28rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8rpx;
	}
	
	.button-icon {
		font-size: 24rpx;
	}
</style>