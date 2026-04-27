<template>
	<view class="navigation-container">
		<view :class="['map-section', { 'focus-mode': focusMode }]">
			<view v-if="loading" class="map-placeholder">
				<text class="map-icon">🗺️</text>
				<text class="map-text">加载中...</text>
				<text class="map-subtext">正在获取订单数据</text>
			</view>
			<view v-else-if="orders.length === 0" class="map-placeholder">
				<text class="map-icon">📋</text>
				<text class="map-text">暂无配送订单</text>
				<text class="map-subtext">请稍后再试</text>
			</view>
			<map 
				v-else
				:latitude="currentLocation?.latitude || 39.908722"
				:longitude="currentLocation?.longitude || 116.397477"
				:markers="markers"
				:scale="15"
				:show-location="true"
				:enable-zoom="true"
				:enable-scroll="true"
				class="map-container"
			></map>
			<view class="focus-mode-button" @click="toggleFocusMode">
				<text class="focus-mode-icon">{{ focusMode ? '⬇️' : '🎯' }}</text>
				<text class="focus-mode-text">{{ focusMode ? '退出专注' : '专注模式' }}</text>
			</view>
		</view>
		
		<view v-if="!focusMode && orders.length > 0" class="info-section">
			<!-- 订单切换组件 -->
			<view class="order-switcher">
				<text class="switcher-title">当前配送订单</text>
				<view class="order-tabs">
					<view 
						v-for="(order, index) in orders" 
						:key="order.id"
						:class="['order-tab', { active: currentOrderIndex === index }]"
						@click="switchOrder(index)"
					>
						<text class="order-tab-number">{{ index + 1 }}</text>
						<text class="order-tab-name">{{ order.elderlyName || '未知老人' }}</text>
						<view :class="['order-tab-status', order.status || 'pending']">
							{{ (order.status === 'delivering') ? '配送中' : '待配送' }}
						</view>
						<view v-if="order.isAssignedByAdmin" class="admin-assigned-tag">
							管理员委派
						</view>
					</view>
				</view>
			</view>
			
			<view class="info-card">
				<view class="card-header">
					<text class="card-title">配送信息</text>
				</view>
				
				<view class="elder-info">
					<view class="avatar-container">
						<text class="avatar">👴</text>
					</view>
					<view class="elder-details">
						<text class="elder-name">{{ currentOrder?.elderlyName || '未知老人' }}</text>
						<text class="elder-address">{{ currentOrder?.deliveryAddress || '地址未知' }}</text>
						<text class="elder-meal">{{ currentOrder?.mealName || '餐品未知' }}</text>
					</view>
				</view>
				
				<view class="status-grid">
					<view class="status-card delivering">
						<text class="status-icon">🚚</text>
						<text class="status-label">配送状态</text>
						<text class="status-value">{{ currentOrder?.status === 'delivering' ? '配送中' : '待配送' }}</text>
					</view>
					<view class="status-card countdown">
						<text class="status-icon">⏰</text>
						<text class="status-label">预计送达</text>
						<text class="status-value">{{ currentOrder?.estimatedTime || '计算中...' }}</text>
					</view>
					<view class="status-card timer">
						<text class="status-icon">📍</text>
						<text class="status-label">距离</text>
						<text class="status-value">{{ currentOrder?.distance || '计算中...' }}</text>
					</view>
				</view>
			</view>
			
			<view class="action-buttons">
				<button @click="startNavigation" class="action-button">
					<text class="button-icon">🧭</text>
					<text>开始导航</text>
				</button>
				<button @click="handleException" class="action-button warning">
					<text class="button-icon">⚠️</text>
					<text>异常处理</text>
				</button>
				<button @click="completeDelivery" class="action-button primary">
					<text class="button-icon">✅</text>
					<text>已送达</text>
				</button>
			</view>
		</view>
	</view>
</template>

<script>
	/**
	 * 配送端导航页面组件
	 * 功能：显示配送订单、地图导航、距离计算、订单管理
	 * 技术栈：uni-app + Vue.js + 原生地图组件
	 */
	
	// 导入API模块和地图工具函数
	import { api } from '../../utils/api.js'
	import { calculateDistance, formatDistance, estimateDeliveryTime, geocode } from '../../utils/map.js'
	
	export default {
		/**
		 * 组件数据定义
		 */
		data() {
			return {
				// 计时器相关
				timer: null,          // 定时器实例
				elapsedTime: 0,       // 已用时间（秒）
				
				// 订单相关
				currentOrderIndex: 0, // 当前选中订单索引
				orders: [],           // 订单列表数据
				currentLocation: null, // 当前位置信息
				
				// 界面状态
				focusMode: false,     // 专注模式状态
				loading: false,       // 加载状态
				isGettingLocation: false, // 防止重复获取位置的标志
				
				// 模拟位置数据（北京中心位置，等待微信位置权限审核通过后改为真实位置）
				mockLocation: {
					latitude: 39.908722,
					longitude: 116.397477
				},
				
				// uni-app map组件的markers格式数据
				markers: []
			}
		},
		
		/**
		 * 计算属性
		 */
		computed: {
			// 获取当前选中的订单
			currentOrder() {
				return this.orders[this.currentOrderIndex]
			}
		},
		
		/**
		 * 生命周期钩子
		 */
		onLoad() {
			// 页面加载时启动计时器、加载订单数据
			this.startTimer()
			this.loadOrders()
			// 使用全局位置信息
			this.currentLocation = getApp().globalData.currentLocation
			if (this.currentLocation) {
				this.calculateDistance()
			}
		},
		
		onShow() {
			// 页面显示时，使用全局位置信息
			this.currentLocation = getApp().globalData.currentLocation
			// 位置信息已获取才加载订单
			if (this.currentLocation) {
				this.loadOrders()
				this.calculateDistance()
			}
		},
		
		onUnload() {
			// 页面卸载时清除计时器
			this.stopTimer()
		},
		
		/**
		 * 方法定义
		 */
		methods: {
			/**
			 * 启动计时器
			 */
			startTimer() {
				this.timer = setInterval(() => {
					this.elapsedTime++
				}, 1000)
			},
			
			/**
			 * 加载配送订单数据
			 * 从后端API获取配送中的和待接单的订单
			 */
			async loadOrders() {
				this.loading = true
				try {
					// 获取不同状态的订单
					const statuses = ['delivering', 'pending_accept']
					const allOrders = []
					
					// 遍历所有状态，获取订单数据
					for (const status of statuses) {
						const result = await api.orders.getOrders(status)
						if (result && result.orders) {
							allOrders.push(...result.orders)
						}
					}
					
					// 处理订单数据格式
					this.orders = allOrders.map(order => ({
						id: order.id,
						orderNumber: order.order_number,
						elderlyName: order.elderly_name,
						elderlyPhone: order.elderly_phone,
						deliveryAddress: order.delivery_address,
						mealName: order.meal_name,
						quantity: order.quantity,
						status: order.status === 'pending_accept' ? 'pending' : order.status,
						createdAt: order.created_at,
						distance: '计算中...',
						estimatedTime: '计算中...',
						// 保存后端提供的位置信息（地理空间数据）
						elderlyLocation: order.elderly_location,
						isAssignedByAdmin: order.is_assigned_by_admin || false
					}))
					
					// 处理空订单情况
					if (this.orders.length === 0) {
						uni.showToast({
							title: '暂无配送订单',
							icon: 'none'
						})
					}
				} catch (error) {
					console.error('加载订单失败:', error)
					uni.showToast({
						title: '加载订单失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
					// 订单加载完成后，确保位置信息已获取，然后计算距离
					if (this.currentLocation) {
						this.calculateDistance()
					}
				}
			},
			

			
			/**
			 * 计算配送距离和预计时间
			 * 为每个订单计算到当前位置的距离，并添加地图标记
			 */
			async calculateDistance() {
				console.log('开始计算距离:', { currentLocation: this.currentLocation, ordersCount: this.orders.length })
				if (!this.currentLocation || this.orders.length === 0) {
					console.log('跳过计算距离：位置或订单数据缺失')
					return
				}
				
				const newMarkers = []
				
				// 遍历所有订单，计算距离和添加标记
				for (let i = 0; i < this.orders.length; i++) {
					const order = this.orders[i]
					try {
						console.log('处理订单:', { orderId: order.id, elderlyName: order.elderlyName, elderlyLocation: order.elderlyLocation })
						let location = null
						// 优先使用后端提供的位置信息（地理空间数据）
						if (order.elderlyLocation && order.elderlyLocation.latitude && order.elderlyLocation.longitude) {
							console.log('使用后端提供的位置信息')
							location = {
								latitude: order.elderlyLocation.latitude,
								longitude: order.elderlyLocation.longitude
							}
						} else {
							// 后端没有提供位置信息，使用地址解析
							console.log('后端没有提供位置信息，使用地址解析:', order.deliveryAddress)
							location = await geocode(order.deliveryAddress)
							console.log('地址解析结果:', location)
						}
						
						if (location) {
							console.log('开始计算距离:', { 
								currentLocation: this.currentLocation, 
								destination: location 
							})
							// 计算距离（使用Haversine公式）
							const distance = calculateDistance(
								this.currentLocation.latitude,
								this.currentLocation.longitude,
								location.latitude,
								location.longitude
							)
							console.log('距离计算结果:', { distance: distance, formattedDistance: formatDistance(distance), estimatedTime: estimateDeliveryTime(distance) })
							order.distance = formatDistance(distance)
							order.estimatedTime = estimateDeliveryTime(distance)
							
							// 添加uni-app map标记（带有老人姓名标签）
							newMarkers.push({
								id: i + 1,
								latitude: location.latitude,
								longitude: location.longitude,
								label: {
									content: order.elderlyName,
									color: '#10b981',
									fontSize: 14,
									bgColor: '#ffffff',
									borderWidth: 1,
									borderColor: '#10b981',
									padding: 5,
									x: 0,
									y: -40
								}
							})
						}
					} catch (error) {
						console.error('计算距离失败:', error)
						order.distance = '距离未知'
								order.estimatedTime = '时间未知'
					}
				}
				
				this.markers = newMarkers
			},
			
			/**
			 * 切换选中的订单
			 * @param {number} index - 订单索引
			 */
			switchOrder(index) {
				this.currentOrderIndex = index
				uni.showToast({
					title: `切换到${this.orders[index]?.elderlyName || '未知老人'}的订单`,
					icon: 'success'
				})
			},
			
			/**
			 * 切换专注模式
			 * 专注模式下地图区域全屏显示，隐藏其他信息
			 */
			toggleFocusMode() {
				this.focusMode = !this.focusMode
				uni.showToast({
					title: this.focusMode ? '已进入专注模式' : '已退出专注模式',
					icon: 'success'
				})
			},
			
			/**
			 * 开始导航到目的地
			 * 优先使用后端提供的地理空间位置数据，否则使用地址解析
			 */
			async startNavigation() {
				if (!this.currentOrder) {
					uni.showToast({
						title: '请选择订单',
						icon: 'none'
					})
					return
				}
				
				try {
					uni.showLoading({
						title: '正在规划路线...'
					})
					
					// 获取目的地位置（优先使用后端提供的地理空间位置数据）
					let destination = null
					if (this.currentOrder.elderlyLocation && this.currentOrder.elderlyLocation.latitude) {
						destination = this.currentOrder.elderlyLocation
					} else {
						// 后端没有提供位置，使用地址解析
						destination = await geocode(this.currentOrder.deliveryAddress)
					}
					
					if (!destination) {
						throw new Error('无法获取目的地位置')
					}
					
					// 使用uni-app的打开位置功能（会调用系统地图应用）
					uni.openLocation({
						latitude: destination.latitude,
						longitude: destination.longitude,
						name: this.currentOrder.elderlyName,
						address: this.currentOrder.deliveryAddress,
						scale: 18,
						success: () => {
							uni.hideLoading()
							uni.showToast({
								title: '导航已启动',
								icon: 'success'
							})
						},
						fail: (error) => {
							uni.hideLoading()
							console.error('导航失败:', error)
							
							// 提供更友好的错误提示，避免出现"无法访问此网站"页面
							if (error.errMsg && (error.errMsg.includes('unknown url scheme') || error.errMsg.includes('ERR_UNKNOWN_URL_SCHEME'))) {
								uni.showModal({
									title: '导航提示',
									content: '无法打开地图应用，请手动导航到：' + this.currentOrder.deliveryAddress,
									showCancel: false
								})
							} else {
								uni.showToast({
									title: '导航失败，请重试',
									icon: 'none'
								})
							}
						}
					})
					
				} catch (error) {
					uni.hideLoading()
					console.error('导航失败:', error)
					uni.showToast({
						title: '导航失败，请重试',
						icon: 'none'
					})
				}
			},
			
			/**
			 * 停止计时器
			 */
			stopTimer() {
				if (this.timer) {
					clearInterval(this.timer)
					this.timer = null
				}
			},
			
			/**
			 * 格式化时间（秒转时分秒）
			 * @param {number} seconds - 秒数
			 * @returns {string} 格式化后的时间字符串
			 */
			formatTime(seconds) {
				const hours = Math.floor(seconds / 3600)
				const minutes = Math.floor((seconds % 3600) / 60)
				const secs = seconds % 60
				return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
			},
			

			
			/**
			 * 处理异常情况
			 * 跳转到异常处理页面
			 */
			handleException() {
				if (!this.currentOrder) {
					uni.showToast({
						title: '请选择订单',
						icon: 'none'
					})
					return
				}
				uni.navigateTo({
					url: `/pages/exception/exception?orderId=${this.currentOrder.id}`
				})
			},
			
			/**
			 * 完成配送
			 * 调用后端API更新订单状态为已完成
			 */
			async completeDelivery() {
				if (!this.currentOrder) {
					uni.showToast({
						title: '请选择订单',
						icon: 'none'
					})
					return
				}
				uni.showModal({
					title: '确认送达',
					content: `确认${this.currentOrder.elderlyName || '未知老人'}的餐品已送达吗？`,
					success: async (res) => {
						if (res.confirm) {
							try {
								const result = await api.orders.completeOrder(this.currentOrder.id)
								if (result) {
									this.currentOrder.status = 'completed'
									uni.showToast({
										title: '送达成功',
										icon: 'success'
									})
									// 检查是否还有未完成的订单
									const remainingOrders = this.orders.filter(order => order.status !== 'completed')
									if (remainingOrders.length > 0) {
										// 自动切换到下一个未完成的订单
										const nextIndex = this.orders.findIndex(order => order.status !== 'completed')
										this.switchOrder(nextIndex)
									} else {
										// 所有订单都已完成，返回订单列表
										setTimeout(() => {
											uni.switchTab({
												url: '/pages/order/order'
											})
										}, 1000)
									}
								}
							} catch (error) {
								console.error('完成配送失败:', error)
								uni.showToast({
									title: '送达失败，请重试',
									icon: 'none'
								})
							}
						}
					}
				})
			}
		}
	}
</script>

<style scoped>
	.navigation-container {
		height: 100vh;
		display: flex;
		flex-direction: column;
	}
	
	.map-section {
		flex: 0.6;
		background-color: #1e293b;
		position: relative;
		transition: flex 0.3s ease;
	}
	
	.map-section.focus-mode {
		flex: 1;
	}
	
	.map-container {
		width: 100%;
		height: 100%;
	}
	
	.map-placeholder {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		color: white;
	}
	
	.map-icon {
		font-size: 120rpx;
		margin-bottom: 20rpx;
	}
	
	.map-text {
		font-size: 36rpx;
		font-weight: 500;
		margin-bottom: 10rpx;
	}
	
	.map-subtext {
		font-size: 28rpx;
		color: #94a3b8;
	}
	
	.focus-mode-button {
		position: absolute;
		bottom: 30rpx;
		right: 30rpx;
		background-color: rgba(16, 185, 129, 0.9);
		color: white;
		padding: 16rpx 24rpx;
		border-radius: 20rpx;
		display: flex;
		align-items: center;
		gap: 8rpx;
		box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
		transition: all 0.3s ease;
	}
	
	.focus-mode-button:active {
		transform: scale(0.95);
		background-color: rgba(5, 150, 105, 0.9);
	}
	
	.focus-mode-icon {
		font-size: 24rpx;
	}
	
	.focus-mode-text {
		font-size: 24rpx;
		font-weight: 500;
	}
	
	.info-section {
		flex: 0.4;
		background-color: white;
		border-top-left-radius: 32rpx;
		border-top-right-radius: 32rpx;
		padding: 30rpx;
		box-shadow: 0 -4px 16px rgba(0,0,0,0.12);
		transition: all 0.3s ease;
		overflow-y: auto;
	}

	.info-section::-webkit-scrollbar {
		width: 4rpx;
	}

	.info-section::-webkit-scrollbar-track {
		background: #f1f1f1;
		border-radius: 2rpx;
	}

	.info-section::-webkit-scrollbar-thumb {
		background: #10b981;
		border-radius: 2rpx;
	}
	
	.order-switcher {
		margin-bottom: 30rpx;
	}
	
	.switcher-title {
		font-size: 28rpx;
		color: #64748b;
		font-weight: 500;
		margin-bottom: 16rpx;
		display: block;
	}
	
	.order-tabs {
		display: flex;
		flex-direction: column;
		gap: 12rpx;
	}
	
	.order-tab {
		background-color: #f8fafc;
		border-radius: 16rpx;
		padding: 20rpx;
		display: flex;
		align-items: center;
		transition: all 0.3s ease;
		border: 2rpx solid transparent;
	}
	
	.order-tab.active {
		background-color: #d1fae5;
		border-color: #10b981;
	}
	
	.order-tab:active {
		transform: scale(0.98);
	}
	
	.order-tab-number {
		width: 40rpx;
		height: 40rpx;
		border-radius: 50%;
		background-color: #10b981;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 24rpx;
		font-weight: 600;
		margin-right: 16rpx;
	}
	
	.order-tab-name {
		flex: 1;
		font-size: 32rpx;
		font-weight: 500;
		color: #1e293b;
	}
	
	.order-tab-status {
		padding: 8rpx 16rpx;
		border-radius: 12rpx;
		font-size: 24rpx;
		font-weight: 500;
	}
	
	.order-tab-status.delivering {
		background-color: #dbeafe;
		color: #3b82f6;
	}
	
	.order-tab-status.pending {
		background-color: #fef3c7;
		color: #f59e0b;
	}

	.admin-assigned-tag {
		background-color: #fef2f2;
		color: #ef4444;
		padding: 6rpx 12rpx;
		border-radius: 12rpx;
		font-size: 20rpx;
		font-weight: 500;
		margin-left: 12rpx;
	}
	
	.info-card {
		margin-bottom: 30rpx;
	}
	
	.card-header {
		margin-bottom: 20rpx;
	}
	
	.card-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #1e293b;
	}
	
	.elder-info {
		display: flex;
		align-items: center;
		margin-bottom: 30rpx;
		padding-bottom: 30rpx;
		border-bottom: 1rpx solid #e2e8f0;
	}
	
	.avatar-container {
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
		background: linear-gradient(135deg, #10b981, #059669);
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 24rpx;
		box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
	}
	
	.avatar {
		font-size: 48rpx;
	}
	
	.elder-details {
		flex: 1;
	}
	
	.elder-name {
		font-size: 36rpx;
		font-weight: 600;
		color: #1e293b;
		margin-bottom: 8rpx;
		display: block;
	}
	
	.elder-address {
		font-size: 28rpx;
		color: #64748b;
		line-height: 1.4;
		margin-bottom: 8rpx;
		display: block;
	}
	
	.elder-meal {
		font-size: 26rpx;
		color: #10b981;
		font-weight: 500;
		display: block;
	}
	
	.status-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 20rpx;
	}
	
	.status-card {
		background-color: white;
		border-radius: 20rpx;
		padding: 24rpx 16rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		border: 2rpx solid transparent;
		transition: all 0.3s ease;
	}
	
	.status-card:active {
		transform: scale(0.95);
	}
	
	.status-card.delivering {
		border-color: #3b82f6;
		background-color: #dbeafe;
	}
	
	.status-card.countdown {
		border-color: #f59e0b;
		background-color: #fef3c7;
	}
	
	.status-card.timer {
		border-color: #10b981;
		background-color: #d1fae5;
	}
	
	.status-icon {
		font-size: 40rpx;
		margin-bottom: 12rpx;
	}
	
	.status-label {
		font-size: 24rpx;
		color: #64748b;
		margin-bottom: 8rpx;
		text-align: center;
	}
	
	.status-value {
		font-size: 28rpx;
		font-weight: 600;
		color: #1e293b;
		text-align: center;
	}
	
	.status-card.delivering .status-value {
		color: #3b82f6;
	}
	
	.status-card.countdown .status-value {
		color: #f59e0b;
	}
	
	.status-card.timer .status-value {
		color: #10b981;
	}
	
	.action-buttons {
		display: flex;
		flex-direction: row;
		gap: 16rpx;
		align-items: center;
	}
	
	.action-button {
		height: 72rpx;
		border-radius: 20rpx;
		font-size: 24rpx;
		font-weight: 600;
		border: none;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8rpx;
		transition: all 0.3s ease;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		flex: 1;
		min-width: 100rpx;
	}
	
	.action-button:active {
		transform: translateY(2px);
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
	}
	
	.action-button:not(.primary):not(.warning) {
		background: linear-gradient(135deg, #60a5fa, #3b82f6);
		color: white;
	}
	
	.action-button.primary {
		background: linear-gradient(135deg, #10b981, #059669);
		color: white;
	}
	
	.action-button.warning {
		background: linear-gradient(135deg, #f59e0b, #d97706);
		color: white;
	}
	
	.button-icon {
		font-size: 28rpx;
	}
</style>