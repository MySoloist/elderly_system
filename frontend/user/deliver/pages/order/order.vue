<template>
	<view class="order-container">
		<view class="status-tabs">
			<view 
				v-for="tab in tabs" 
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
		
		<view v-else-if="filteredOrders.length > 0" class="order-list">
			<view v-for="order in filteredOrders" :key="order.id" class="order-card" @click="goToDetail(order.id)">
				<view class="order-header">
					<text class="order-number">订单编号: {{ order.orderNo }}</text>
					<view :class="['status-tag', order.status]">
						{{ getStatusText(order.status) }}
					</view>
					<view v-if="order.isAssignedByAdmin" class="admin-assigned-tag">
						该订单已被管理员委派
					</view>
				</view>
				
				<view class="order-info">
						<view class="elder-info">
							<text class="avatar">👴</text>
							<view class="elder-details">
								<text class="elder-name">{{ order.elderlyName }}</text>
								<text class="elder-phone">{{ order.elderlyPhone }}</text>
							</view>
						</view>
						
						<view class="community-info">
							<text class="community-icon">🏘️</text>
							<text class="community-name">{{ order.communityName }}</text>
						</view>
						
						<view class="delivery-info">
							<text class="address-icon">📍</text>
							<text class="address">{{ order.deliveryAddress }}</text>
						</view>
						
						<view class="meal-info">
							<view class="meal-details">
								<text class="meal-name">{{ order.mealName }}</text>
								<text class="meal-price">¥{{ order.totalAmount.toFixed(2) }}</text>
							</view>
							<view class="meal-quantity">
								x{{ order.quantity }}
							</view>
						</view>
					</view>
				
				<view class="order-footer">
					<view v-if="order.status !== 'completed'" class="time-distance">
						<text class="time-label">预计送达时间</text>
						<text class="time">{{ order.deliveryTime }}</text>
						<text class="distance">{{ order.distance }}</text>
					</view>
					<view class="action-buttons">
						<button v-if="order.status === 'pending' && (!order.isAssignedByAdmin || order.assignedDelivererId === currentUserId)" @click.stop="acceptOrder(order.id)" class="accept-button">接单</button>
						<button v-if="order.status === 'delivering'" @click.stop="completeOrder(order.id)" class="complete-button">已送达</button>
						<button @click.stop="callElder(order.id)" class="call-button">联系老人</button>
						<button @click.stop="callFamily(order.id)" class="call-button">联系家属</button>
					</view>
				</view>
			</view>
		</view>
		
		<view v-else class="empty-state">
			<text class="empty-icon">📦</text>
			<text class="empty-text">暂无订单</text>
			<button @click="refreshOrders" class="refresh-button">刷新</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
import { calculateDistance, formatDistance, estimateDeliveryTime, geocode } from '../../utils/map.js'
	
	export default {
		data() {
			return {
				activeTab: 'pending',
				tabs: [
					{ label: '待接单', value: 'pending' },
					{ label: '配送中', value: 'delivering' },
					{ label: '已完成', value: 'completed' }
				],
				orders: [],
				loading: false,
				currentUserId: null,
				currentLocation: null,
				isGettingLocation: false, // 防止重复获取位置的标志
				// 模拟位置（北京中心位置，等待微信位置权限审核通过后改为真实位置）
				mockLocation: {
					latitude: 39.908722,
					longitude: 116.397477
				}
			}
		},
		computed: {
			filteredOrders() {
				return this.orders.filter(order => order.status === this.activeTab)
			}
		},
		onLoad() {
			// 获取当前用户信息
			const user = uni.getStorageSync('user')
			this.currentUserId = user ? user.id : null
			// 使用全局位置信息
			this.currentLocation = getApp().globalData.currentLocation
		},
		onShow() {
			// 页面显示时，使用全局位置信息
			this.currentLocation = getApp().globalData.currentLocation
			// 位置信息已获取才加载订单
			if (this.currentLocation) {
				this.loadOrders()
			}
		},
		methods: {
			switchTab: function(tabValue) {
				this.activeTab = tabValue
				this.loadOrders()
			},
			
			// 加载订单数据
			async loadOrders() {
				if (!this.currentLocation) {
					console.log('位置信息未获取，等待中...')
					return
				}
				
				this.loading = true
				try {
					let status = null
					if (this.activeTab === 'pending') {
						status = 'pending_accept'
					} else if (this.activeTab === 'delivering') {
						status = 'delivering'
					} else if (this.activeTab === 'completed') {
						status = 'completed'
					}
					
					const data = await api.orders.getOrders(status)
					// 异步计算每个订单的距离
					const ordersWithDistance = []
					for (const order of data.orders) {
						let distanceStr = '距离未知'
						let calcDistance = null
						try {
							// 优先使用后端提供的位置信息（地理空间数据）
							if (order.elderly_location && order.elderly_location.latitude && order.elderly_location.longitude) {
								// 使用后端返回的老人位置计算距离
								calcDistance = calculateDistance(
									this.currentLocation.latitude,
									this.currentLocation.longitude,
									order.elderly_location.latitude,
									order.elderly_location.longitude
								)
								distanceStr = formatDistance(calcDistance)
							} else {
								// 后端没有提供位置信息，使用地址解析
								const realDistance = await this.calculateRealDistance(order.delivery_address)
								if (realDistance !== '距离未知') {
									// 解析距离字符串获取数值
									const distanceMatch = realDistance.match(/距离(\d+(?:\.\d+)?)km/)
									if (distanceMatch) {
										calcDistance = parseFloat(distanceMatch[1])
									} else {
										const distanceMatchM = realDistance.match(/距离(\d+)m/)
										if (distanceMatchM) {
											calcDistance = parseInt(distanceMatchM[1]) / 1000
										}
									}
								}
								distanceStr = realDistance
							}
						} catch (error) {
							console.error('计算距离失败:', error)
						}
						
						ordersWithDistance.push({
							id: order.id,
							orderNo: order.order_number,
							elderlyName: order.elderly_name,
							elderlyPhone: this.maskPhone(order.elderly_phone),
							deliveryAddress: order.delivery_address,
							communityName: order.community_name,
							mealName: order.meal_name,
							quantity: order.quantity,
							unitPrice: order.unit_price,
							totalAmount: order.total_amount,
							deliveryTime: calcDistance ? estimateDeliveryTime(calcDistance) : '暂无预计时间',
							distance: distanceStr,
							status: this.mapOrderStatus(order.status),
							isAssignedByAdmin: order.is_assigned_by_admin || false,
							assignedDelivererId: order.assigned_deliverer_id,
							elderlyLocation: order.elderly_location
						})
					}
					this.orders = ordersWithDistance
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
			
			// 映射订单状态
			mapOrderStatus(dbStatus) {
				const statusMap = {
					'pending_accept': 'pending',
					'delivering': 'delivering',
					'completed': 'completed'
				}
				return statusMap[dbStatus] || 'pending'
			},
			

			
			// 计算真实距离
			async calculateRealDistance(address) {
				try {
					// 使用地址解析获取老人位置
					const elderlyLocation = await geocode(address)
					// 计算配送员位置到老人位置的距离
					const distance = calculateDistance(
						this.currentLocation.latitude,
						this.currentLocation.longitude,
						elderlyLocation.latitude,
						elderlyLocation.longitude
					)
					return formatDistance(distance)
				} catch (error) {
					console.error('计算距离失败:', error)
					return '距离未知'
				}
			},
			
			// 手机号脱敏
			maskPhone(phone) {
				if (!phone || phone.length< 11) return phone
				return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
			},
			
			getStatusText(status) {
				const statusMap = {
					pending: '待接单',
					delivering: '配送中',
					completed: '已完成'
				}
				return statusMap[status] || status
			},
			goToDetail(orderId) {
				uni.navigateTo({
					url: `/pages/order-detail/order-detail?id=${orderId}`
				})
			},
			async acceptOrder(orderId) {
				uni.showModal({
					title: '确认接单',
					content: '确定要接这个订单吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								const response = await api.orders.acceptOrder(orderId)
								if (response.success) {
									uni.showToast({
										title: response.message || '接单成功',
										icon: 'success'
									})
									// 接单成功后，切换到配送中标签页
									this.activeTab = 'delivering'
									// 重新加载订单（此时会加载配送中的订单）
									this.loadOrders()
								} else {
									// 处理业务错误，显示友好提示
									uni.showModal({
										title: '接单提示',
										content: response.message || '接单失败',
										showCancel: false,
										confirmText: '确定'
									})
								}
							} catch (error) {
								console.error('接单失败:', error)
								uni.showToast({
									title: '接单失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			async completeOrder(orderId) {
				uni.showModal({
					title: '确认送达',
					content: '确认餐品已送达吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.orders.completeOrder(orderId)
								uni.showToast({
									title: '送达成功',
									icon: 'success'
								})
								// 重新加载订单
								this.loadOrders()
							} catch (error) {
								console.error('完成订单失败:', error)
								uni.showToast({
									title: '完成订单失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			callElder(orderId) {
				const order = this.orders.find(o => o.id === orderId)
				if (order) {
					uni.showModal({
						title: '联系老人',
						content: `是否拨打 ${order.elderlyName} 的电话？`,
						success: (res) => {
							if (res.confirm) {
								uni.makePhoneCall({
									phoneNumber: order.elderlyPhone.replace(/\*/g, '0'),
									success: () => {
										uni.showToast({
											title: '拨打电话成功',
											icon: 'success'
										})
									},
									fail: () => {
										uni.showToast({
											title: '拨打电话失败',
											icon: 'none'
										})
									}
								})
							}
						}
					})
				}
			},
			callFamily(orderId) {
				const order = this.orders.find(o => o.id === orderId)
				if (order) {
					uni.showModal({
						title: '联系家属',
						content: `当前订单暂无家属联系方式，是否联系老人 ${order.elderlyName} 了解家属信息？`,
						success: (res) => {
							if (res.confirm) {
								uni.makePhoneCall({
									phoneNumber: order.elderlyPhone.replace(/\*/g, '0'),
									success: () => {
										uni.showToast({
											title: '拨打电话成功',
											icon: 'success'
										})
									},
									fail: () => {
										uni.showToast({
											title: '拨打电话失败',
											icon: 'none'
										})
									}
								})
							}
						}
					})
				}
			},
			refreshOrders() {
				// 刷新时使用全局位置信息加载订单
				this.currentLocation = getApp().globalData.currentLocation
				if (this.currentLocation) {
					this.loadOrders()
				} else {
					// 如果没有位置信息，调用全局位置获取
					getApp().getCurrentLocation()
				}
			}
		},
		onTabItemTap() {
			// 点击Tab时使用全局位置信息重新加载订单
			this.currentLocation = getApp().globalData.currentLocation
			if (this.currentLocation) {
				this.loadOrders()
			} else {
				// 如果没有位置信息，调用全局位置获取
				getApp().getCurrentLocation()
			}
		}
	}
</script>

<style scoped>
	.order-container {
		min-height: 100vh;
	}
	
	.status-tabs {
		display: flex;
		background-color: white;
		padding: 0 40rpx;
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
	
	.order-list {
		padding: 20rpx;
	}
	
	.order-card {
		background-color: white;
		border-radius: 24rpx;
		padding: 30rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 2px 8px rgba(0,0,0,0.08);
	}
	
	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
		padding-bottom: 20rpx;
		border-bottom: 1rpx solid #e2e8f0;
	}
	
	.order-number {
		font-size: 28rpx;
		color: #94a3b8;
	}
	
	.status-tag {
		padding: 8rpx 16rpx;
		border-radius: 16rpx;
		font-size: 24rpx;
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
		background-color: #d1fae5;
		color: #10b981;
	}

	.admin-assigned-tag {
		background-color: #fef2f2;
		color: #ef4444;
		padding: 8rpx 16rpx;
		border-radius: 16rpx;
		font-size: 24rpx;
		font-weight: 500;
		margin-left: 16rpx;
	}
	
	.order-info {
		margin-bottom: 20rpx;
	}
	
	.elder-info {
		display: flex;
		align-items: center;
		margin-bottom: 16rpx;
	}
	
	.avatar {
		font-size: 48rpx;
		margin-right: 16rpx;
	}
	
	.elder-details {
		display: flex;
		flex-direction: column;
	}
	
	.elder-name {
		font-size: 32rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.elder-phone {
		font-size: 28rpx;
		color: #64748b;
	}
	
	.community-info {
		display: flex;
		align-items: center;
		margin-bottom: 16rpx;
	}
	
	.community-icon {
		font-size: 24rpx;
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
	
	.delivery-info {
		display: flex;
		align-items: center;
		margin-bottom: 16rpx;
	}
	
	.address-icon {
		font-size: 24rpx;
		margin-right: 8rpx;
	}
	
	.address {
		font-size: 28rpx;
		color: #1e293b;
		flex: 1;
	}
	
	.meal-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.meal-details {
		display: flex;
		flex-direction: column;
		flex: 1;
	}
	
	.meal-name {
		font-size: 32rpx;
		color: #1e293b;
		font-weight: 500;
		margin-bottom: 8rpx;
	}
	
	.meal-price {
		font-size: 28rpx;
		color: #ef4444;
		font-weight: 500;
	}
	
	.meal-quantity {
		font-size: 28rpx;
		color: #64748b;
		background-color: #f8fafc;
		padding: 8rpx 16rpx;
		border-radius: 16rpx;
	}
	
	.order-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 20rpx;
		border-top: 1rpx solid #e2e8f0;
	}
	
	.time-distance {
		display: flex;
		flex-direction: column;
	}
	
	.time-label {
		font-size: 20rpx;
		color: #64748b;
		margin-bottom: 4rpx;
	}
	
	.time {
		font-size: 28rpx;
		color: #f59e0b;
		font-weight: 500;
	}
	
	.distance {
		font-size: 24rpx;
		color: #3b82f6;
		margin-top: 4rpx;
	}
	
	.action-buttons {
		display: flex;
		gap: 8rpx;
		align-items: center;
	}
	
	.accept-button, .complete-button {
		padding: 16rpx 24rpx;
		border-radius: 16rpx;
		font-size: 24rpx;
		border: none;
		height: 64rpx;
		min-width: 100rpx;
	}
	
	.accept-button {
		background-color: #10b981;
		color: white;
	}
	
	.complete-button {
		background-color: #10b981;
		color: white;
	}
	
	.call-button {
		padding: 16rpx 24rpx;
		border-radius: 16rpx;
		font-size: 24rpx;
		border: none;
		background-color: #3b82f6;
		color: white;
		height: 64rpx;
		min-width: 100rpx;
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
	
	.refresh-button {
		padding: 16rpx 40rpx;
		background-color: #10b981;
		color: white;
		border: none;
		border-radius: 20rpx;
		font-size: 28rpx;
	}
</style>