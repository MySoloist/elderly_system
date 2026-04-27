<template>
	<view class="order-container">
		<!-- 顶部筛选标签 -->
		<scroll-view class="filter-tabs" scroll-x="true">
			<view class="filter-tab" 
				:class="{ active: activeTab === 'all' }"
				@click="activeTab = 'all'"
			>全部</view>
			<view class="filter-tab" 
				:class="{ active: activeTab === 'pending' }"
				@click="activeTab = 'pending'"
			>待支付</view>
			<view class="filter-tab" 
				:class="{ active: activeTab === 'pending_accept' }"
				@click="activeTab = 'pending_accept'"
			>待接单</view>
			<view class="filter-tab" 
				:class="{ active: activeTab === 'delivering' }"
				@click="activeTab = 'delivering'"
			>配送中</view>
			<view class="filter-tab" 
				:class="{ active: activeTab === 'completed' }"
				@click="activeTab = 'completed'"
			>已完成</view>
			<view class="filter-tab" 
				:class="{ active: activeTab === 'cancelled' }"
				@click="activeTab = 'cancelled'"
			>已取消</view>
			<view class="filter-tab" 
				:class="{ active: activeTab === 'scheduled' }"
				@click="activeTab = 'scheduled'"
			>已预定</view>
		</scroll-view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 订单列表 -->
		<view v-else class="order-list">
			<view v-if="filteredOrders.length === 0" class="empty-state">
				<text class="empty-icon">📦</text>
				<text class="empty-text">暂无订单</text>
				<button class="btn-primary mt-16" @click="goToIndex">去点餐</button>
			</view>
			
			<view v-for="order in filteredOrders" :key="order.id" class="order-card">
				<view class="order-header">
					<text class="order-id">订单号: {{ order.id }}</text>
					<text class="order-status" :class="getStatusClass(order.status)">
						{{ getStatusText(order.status) }}
					</text>
				</view>
				
				<view class="order-items">
					<view v-for="item in order.items" :key="item.id" class="order-item">
						<image v-if="item.image" class="item-image" :src="item.image" mode="aspectFill"></image>
						<text v-else class="item-image">🍱</text>
						<view class="item-info">
							<text class="item-name">{{ item.name }}</text>
							<text class="item-price">¥{{ item.price }}</text>
							<text class="item-quantity">x{{ item.quantity }}</text>
						</view>
					</view>
				</view>
				
				<view class="order-footer">
							<view class="order-info">
								<text class="order-time">{{ order.time }}</text>
								<text v-if="order.orderType === 'scheduled' && order.scheduledTime" class="order-scheduled">
									预定时间: {{ formatScheduledTime(order.scheduledTime) }}
								</text>
								<text :class="getOrderTypeClass(order.orderType)" class="order-type-tag">
									{{ order.orderType === 'scheduled' ? '预定' : '即时' }}
								</text>
							</view>
							<text class="order-total">合计: ¥{{ order.total }}</text>
							<view class="order-actions">
						<button 
							v-if="order.status === 'pending_payment' || order.status === 'pending_schedule'"
							class="action-btn cancel-btn"
							@click="cancelOrder(order.id)"
						>取消订单</button>
						<button 
							v-if="order.status === 'pending_payment'"
							class="action-btn pay-btn"
							@click="payOrder(order.id)"
						>去支付</button>
						<button 
							v-if="order.status === 'completed'"
							class="action-btn review-btn"
							@click="reviewOrder(order.id)"
						>评价</button>
						<button 
							v-if="order.status === 'delivering'"
							class="action-btn contact-btn"
							@click="contactRider(order.id)"
						>联系骑手</button>
						<button 
							class="action-btn detail-btn"
							@click="viewOrderDetail(order.id)"
						>查看详情</button>
					</view>
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
				activeTab: 'all',
				orders: [],
				loading: false
			}
		},
		onLoad() {
			this.loadOrders()
		},
		onShow() {
			console.log('订单页面显示')
			// 监听刷新订单列表的事件
			uni.$off('refreshOrderList', this.handleRefreshOrder) // 先移除旧的监听
			uni.$on('refreshOrderList', this.handleRefreshOrder)
		},
		onUnload() {
			// 页面卸载时移除监听，避免内存泄漏
			uni.$off('refreshOrderList', this.handleRefreshOrder)
		},
		watch: {
			activeTab() {
				this.loadOrders()
			}
		},
		computed: {
			filteredOrders() {
				if (this.activeTab === 'all') {
					return this.orders
				}
				return this.orders.filter(order => {
					switch(this.activeTab) {
						case 'pending':
							return order.status === 'pending_payment'
						case 'pending_accept':
							return order.status === 'pending_accept'
						case 'delivering':
							return order.status === 'delivering'
						case 'completed':
							return order.status === 'completed'
						case 'cancelled':
							return order.status === 'cancelled'
						case 'scheduled':
							return order.orderType === 'scheduled'
						default:
							return true
					}
				})
			}
		},
		methods: {
			async loadOrders() {
				console.log('开始加载订单...')
				this.loading = true
				try {
					console.log('调用订单API...')
					const response = await api.older.getOrders()
					console.log('订单API返回数据:', response)
					this.orders = response.items.map(order => ({
								id: order.id,
								status: order.status,
								time: new Date(order.created_at).toLocaleString('zh-CN'),
								scheduledTime: order.scheduled_time,
								orderType: order.order_type || 'immediate',
								total: order.total_amount,
								items: order.items.map(item => ({
									id: item.id,
									name: item.meal_name,
									price: item.price,
									quantity: item.quantity,
									image: item.image_url
								}))
							}))
					console.log('处理后的订单数据:', this.orders)
					console.log('过滤后的订单数据:', this.filteredOrders)
				} catch (error) {
					console.error('获取订单列表失败:', error)
					uni.showToast({
						title: '获取订单失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
					console.log('加载完成，loading状态:', this.loading)
				}
			},
			getStatusText(status) {
				const statusMap = {
					'pending_payment': '待支付',
					'pending_schedule': '等待预定时间',
					'pending_accept': '待接单',
					'delivering': '配送中',
					'completed': '已完成',
					'cancelled': '已取消'
				}
				return statusMap[status] || status
			},
			getStatusClass(status) {
				const classMap = {
					'pending_payment': 'status-pending',
					'pending_accept': 'status-pending-accept',
					'delivering': 'status-delivering',
					'completed': 'status-completed',
					'cancelled': 'status-cancelled',
					'pending_schedule': 'status-pending-schedule'
				}
				return classMap[status] || ''
			},
			getOrderTypeClass(orderType) {
				return orderType === 'scheduled' ? 'order-type-scheduled' : 'order-type-immediate'
			},
			formatScheduledTime(time) {
				if (!time) return ''
				const date = new Date(time)
				return date.toLocaleString('zh-CN', {
					year: 'numeric',
					month: '2-digit',
					day: '2-digit',
					hour: '2-digit',
					minute: '2-digit'
				})
			},
			goToIndex() {
				uni.switchTab({
					url: '/pages/index/index'
				})
			},
			handleRefreshOrder() {
				console.log('收到刷新订单列表的通知')
				this.loadOrders()
			},
			async cancelOrder(orderId) {
				uni.showModal({
					title: '取消订单',
					content: '确定要取消这个订单吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.older.cancelOrder(orderId)
								uni.showToast({
									title: '钱已退、订单取消',
									icon: 'success'
								})
								// 重新加载订单列表
								this.loadOrders()
							} catch (error) {
								console.error('取消订单失败:', error)
								uni.showToast({
									title: '取消订单失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			async payOrder(orderId) {
				try {
					uni.showLoading({
						title: '支付中...'
					})
					
					const response = await api.older.payOrder(orderId, {
						payment_method: '微信支付'
					})
					
					uni.hideLoading()
					uni.showToast({
						title: '支付成功',
						icon: 'success'
					})
					
					// 重新加载订单列表
					this.loadOrders()
				} catch (error) {
					uni.hideLoading()
					console.error('支付失败:', error)
					uni.showToast({
						title: '支付失败，请重试',
						icon: 'none'
					})
				}
			},
			async reviewOrder(orderId) {
				try {
					// 先获取订单详情，检查是否已经评价过
					const orderDetail = await api.older.getOrder(orderId)
					
					// 检查订单是否已经评价过
					if (orderDetail.reviewed) {
						uni.showToast({
							title: '该订单已评价',
							icon: 'none'
						})
						return
					}
					
					// 如果没有评价过，跳转到评价页面
					uni.navigateTo({
						url: `/pages/order/review?orderId=${orderId}`
					})
				} catch (error) {
					console.error('获取订单详情失败:', error)
					uni.showToast({
						title: '获取订单信息失败',
						icon: 'none'
					})
				}
			},
			viewOrderDetail(orderId) {
				uni.navigateTo({
					url: `/pages/order/detail?orderId=${orderId}`
				})
			},
			async contactRider(orderId) {
				try {
					// 获取订单详情，获取真实的配送员电话
					const orderDetail = await api.older.getOrder(orderId)
					
					if (orderDetail.delivery && orderDetail.delivery.deliverer_phone) {
						uni.showActionSheet({
							itemList: ['语音通话', '短信联系'],
							success: (res) => {
								if (res.tapIndex === 0) {
									// 语音通话 - 使用真实配送员电话
									uni.makePhoneCall({
										phoneNumber: orderDetail.delivery.deliverer_phone,
										success: () => {
											console.log('拨打电话成功')
										},
										fail: (err) => {
											uni.showToast({
												title: '拨打电话失败',
												icon: 'none'
											})
										}
									})
								} else if (res.tapIndex === 1) {
									// 短信联系
									uni.showToast({
										title: '短信功能开发中...',
										icon: 'none'
									})
								}
							}
						})
					} else {
						uni.showToast({
							title: '暂无配送员联系方式',
							icon: 'none'
						})
					}
				} catch (error) {
					console.error('获取配送员信息失败:', error)
					uni.showToast({
						title: '获取配送员信息失败',
						icon: 'none'
					})
				}
			}
		}
	}
</script>

<style scoped>
	.order-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 200px, #F5F5F5 100%);
	}
	
	/* 筛选标签 */
	.filter-tabs {
		white-space: nowrap;
		background-color: rgba(255, 255, 255, 0.9);
		padding: 8px 20px 10px;
		border-bottom: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.filter-tab {
		display: inline-block;
		text-align: center;
		padding: 10px 16px;
		margin-right: 8px;
		font-size: 14px;
		color: #666666;
		position: relative;
		background: #f8f8f8;
		border-radius: 18px;
		border: 1px solid #f0f0f0;
	}
	
	.filter-tab.active {
		color: #fff;
		font-weight: 600;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		box-shadow: 0 6px 14px rgba(255, 122, 69, 0.24);
		border-color: transparent;
	}
	
	/* 加载状态 */
	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 400px;
	}
	
	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid #FF7A45;
		border-top-color: transparent;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 16px;
	}
	
	@keyframes spin {
		to { transform: rotate(360deg); }
	}
	
	.loading-text {
		font-size: 16px;
		color: #999999;
	}
	
	/* 订单列表 */
	.order-list {
		padding: 20px;
	}
	
	/* 空状态 */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60px 0;
	}
	
	.empty-icon {
		font-size: 64px;
		margin-bottom: 16px;
	}
	
	.empty-text {
		font-size: 14px;
		color: #999999;
		margin-bottom: 24px;
	}
	
	.btn-primary {
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border: none;
		border-radius: 20px;
		padding: 12px 32px;
		font-size: 16px;
		font-weight: 600;
		box-shadow: 0 6px 14px rgba(255, 122, 69, 0.24);
	}
	
	.mt-16 {
		margin-top: 16px;
	}
	
	/* 订单卡片 */
	.order-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		margin-bottom: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16px;
		padding-bottom: 12px;
		border-bottom: 1px solid #F0F0F0;
	}
	
	.order-id {
		font-size: 13px;
		color: #999999;
		background: #f7f7f7;
		padding: 4px 10px;
		border-radius: 12px;
	}
	
	.order-status {
		font-size: 13px;
		font-weight: 600;
		padding: 6px 12px;
		border-radius: 12px;
	}
	
	.status-pending {
		background-color: rgba(245, 108, 108, 0.1);
		color: #F56C6C;
	}
	
	.status-pending-accept {
		background-color: rgba(250, 173, 20, 0.1);
		color: #E6A23C;
	}
	
	.status-delivering {
		background-color: rgba(64, 158, 255, 0.1);
		color: #409EFF;
	}
	
	.status-completed {
		background-color: rgba(103, 194, 58, 0.1);
		color: #67C23A;
	}
	
	.status-cancelled {
		background-color: rgba(156, 156, 156, 0.1);
		color: #9C9C9C;
	}
	
	.status-pending-schedule {
		background-color: rgba(250, 173, 20, 0.1);
		color: #E6A23C;
	}
	
	/* 订单项 */
	.order-items {
		margin-bottom: 16px;
	}
	
	.order-item {
		display: flex;
		align-items: center;
		margin-bottom: 12px;
	}
	
	.order-item:last-child {
		margin-bottom: 0;
	}
	
	.item-image {
		margin-right: 12px;
		width: 48px;
		height: 48px;
		border-radius: 8px;
		background-color: #f5f5f5;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 24px;
	}
	
	.item-info {
		flex: 1;
		display: flex;
		flex-direction: column;
	}
	
	.item-name {
		font-size: 15px;
		color: #333333;
		font-weight: 500;
		margin-bottom: 4px;
	}
	
	.item-price {
		font-size: 14px;
		color: #FF7A45;
		font-weight: 600;
	}
	
	.item-quantity {
		font-size: 13px;
		color: #999999;
	}
	
	/* 订单底部 */
	.order-footer {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		flex-wrap: wrap;
		row-gap: 10px;
		padding-top: 12px;
		border-top: 1px solid #F0F0F0;
	}
	
	.order-info {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	
	.order-time {
		font-size: 13px;
		color: #999999;
	}
	
	.order-scheduled {
		font-size: 13px;
		color: #4CAF50;
		font-weight: 500;
	}
	
	.order-type-tag {
		font-size: 12px;
		padding: 4px 8px;
		border-radius: 10px;
		font-weight: 500;
		display: inline-block;
		align-self: flex-start;
		margin-top: 4px;
	}
	
	.order-type-scheduled {
		background-color: rgba(76, 175, 80, 0.1);
		color: #4CAF50;
	}
	
	.order-type-immediate {
		background-color: rgba(64, 158, 255, 0.1);
		color: #409EFF;
	}
	
	.order-total {
		font-size: 16px;
		color: #FF7A45;
		font-weight: 700;
		margin-left: auto;
		text-shadow: 0 1px 2px rgba(255, 122, 69, 0.2);
	}
	
	.order-actions {
		display: flex;
		gap: 8px;
		width: 100%;
		justify-content: flex-end;
		flex-wrap: wrap;
	}
	
	.action-btn {
		padding: 8px 14px;
		border-radius: 16px;
		font-size: 13px;
		border: none;
		line-height: 1.2;
		font-weight: 500;
	}
	
	.cancel-btn {
		background-color: #F5F5F5;
		color: #666666;
	}
	
	.pay-btn {
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		box-shadow: 0 6px 14px rgba(255, 122, 69, 0.24);
	}
	
	.review-btn {
		background-color: #409EFF;
		color: white;
	}
	
	.detail-btn {
		background-color: #F5F5F5;
		color: #666666;
		border: 1px solid #ebebeb;
	}
	
	.contact-btn {
		background-color: #4CAF50;
		color: white;
	}
</style>