<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<text class="page-title">订单管理</text>
			<view class="elder-selector" @click="showElderSelector" :disabled="loading">
				<text class="selector-text">{{ loading ? '加载中...' : (selectedElder ? selectedElder.name : '选择老人') }}</text>
				<text class="arrow-icon">▼</text>
			</view>
		</view>
		
		<!-- 状态筛选栏 -->
		<view class="status-section">
			<scroll-view class="status-scroll" scroll-x="true">
				<view class="status-item" v-for="(status, index) in statuses" :key="index" 
					:class="{ active: selectedStatus === status.value }"
					@click="selectStatus(status.value)">
					<text class="status-name">{{ status.name }}</text>
				</view>
			</scroll-view>
		</view>
		
		<!-- 订单列表 -->
		<view class="orders-section">
			<view class="order-card" v-for="(order, index) in filteredOrders" :key="index">
				<view class="order-header">
					<text class="order-number">订单号：{{ order.orderNumber }}</text>
					<view class="order-status" :class="order.status">
						<text class="status-text">{{ getStatusName(order.status) }}</text>
					</view>
				</view>
				
				<view class="order-content">
					<view class="food-items">
						<view class="food-item" v-for="(food, foodIndex) in order.foods" :key="foodIndex">
							<image v-if="food.image" :src="food.image" class="food-image" mode="aspectFill"></image>
							<view v-else class="food-image"></view>
							<view class="food-info">
								<text class="food-name">{{ food.name }}</text>
								<text class="food-quantity">×{{ food.quantity }}</text>
							</view>
							<text class="food-price">¥{{ food.price }}</text>
						</view>
					</view>
				</view>
				
				<view class="order-footer">
					<view class="order-info">
						<text class="order-time">{{ order.orderTime }}</text>
						<text v-if="order.orderType === 'scheduled' && order.scheduledTime" class="order-scheduled">
							预定时间: {{ formatScheduledTime(order.scheduledTime) }}
						</text>
						<text :class="getOrderTypeClass(order.orderType)" class="order-type-tag">
							{{ order.orderType === 'scheduled' ? '预定' : '即时' }}
						</text>
					</view>
					<view class="order-actions">
						<view class="order-total">
							<text class="total-label">合计：</text>
							<text class="total-price">¥{{ order.totalPrice }}</text>
						</view>
						<view class="action-buttons">
								<button class="action-btn primary" v-if="order.status === 'pending_payment'" @click="payOrder(order.id)">
									<text class="btn-text">支付</text>
								</button>
								<button class="action-btn" v-if="order.status === 'pending_payment' || order.status === 'pending_schedule'" @click="cancelOrder(order.id)">
									<text class="btn-text">取消</text>
								</button>
								<button class="action-btn" v-if="order.status === 'pending_accept'" @click="cancelOrder(order.id)">
									<text class="btn-text">取消</text>
								</button>
								<button class="action-btn" v-if="order.status === 'delivering'" @click="contactRider(order.id)">
									<text class="btn-text">联系骑手</text>
								</button>
								<button class="action-btn primary" v-if="order.status === 'delivering'" @click="viewOrder(order.id)">
									<text class="btn-text">详情</text>
								</button>
								<button class="action-btn" v-if="order.status === 'completed'" @click="reviewOrder(order.id)">
									<text class="btn-text">评价</text>
								</button>
								<button class="action-btn" v-if="order.status === 'completed'" @click="viewOrder(order.id)">
									<text class="btn-text">查看</text>
								</button>
							</view>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view class="empty-state" v-if="filteredOrders.length === 0">
				<view class="empty-icon"></view>
				<text class="empty-title">暂无订单</text>
				<text class="empty-subtitle">快去为老人点餐吧</text>
				<button class="go-order-btn" @click="goToOrder">
					<text class="btn-text">去点餐</text>
				</button>
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
import apiClient from '../../api/axios.js'

export default {
	data() {
		return {
			selectedElder: null,
			elders: [],
			loading: false,
			statuses: [
				{ value: 'all', name: '全部' },
				{ value: 'pending_payment', name: '待支付' },
				{ value: 'pending_accept', name: '待接单' },
				{ value: 'scheduled', name: '已预定' },
				{ value: 'delivering', name: '配送中' },
				{ value: 'completed', name: '已完成' },
				{ value: 'cancelled', name: '已取消' }
			],
			selectedStatus: 'all',
			orders: [],
			showElderModal: false
		};
	},
	computed: {
		filteredOrders() {
			if (this.selectedStatus === 'all') {
				return this.orders;
			} else if (this.selectedStatus === 'scheduled') {
				// 筛选出所有预定订单（包括等待预定时间和待支付的预定订单）
				return this.orders.filter(order => order.orderType === 'scheduled');
			}
			return this.orders.filter(order => order.status === this.selectedStatus);
		}
	},
	onLoad() {
		this.loadElders();
	},
	onShow() {
		// 监听刷新订单列表的事件
		uni.$off('refreshOrderList', this.handleRefreshOrder) // 先移除旧的监听
		uni.$on('refreshOrderList', this.handleRefreshOrder)
	},
	onUnload() {
		// 页面卸载时移除监听，避免内存泄漏
		uni.$off('refreshOrderList', this.handleRefreshOrder)
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
						this.loadOrders(this.selectedElder.id);
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
		async loadOrders(elderId) {
			try {
				this.loading = true;
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/orders?elder_id=${elderId}`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					// 转换数据格式，适配前端展示
					this.orders = response.data.items.map(order => ({
						id: order.id,
						orderNumber: order.id.toString(),
						status: order.status,
						orderTime: order.created_at,
						totalPrice: order.total_amount,
						orderType: order.order_type || 'immediate',
						scheduledTime: order.scheduled_time,
						foods: order.items.map(item => ({
							name: item.meal.name,
							price: item.unit_price,
							quantity: item.quantity,
							image: item.meal.image_url
						}))
					}));
				} else {
					throw new Error(response.data?.detail || '加载订单数据失败');
				}
			} catch (error) {
				console.error('加载订单数据失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		getStatusName(status) {
			const statusMap = {
				'pending_payment': '待支付',
				'pending_schedule': '等待预定时间',
				'pending_accept': '待接单',
				'delivering': '配送中',
				'completed': '已完成',
				'cancelled': '已取消'
			};
			return statusMap[status] || status;
		},
		getOrderTypeClass(orderType) {
			return orderType === 'scheduled' ? 'order-type-scheduled' : 'order-type-immediate';
		},
		formatScheduledTime(time) {
			if (!time) return '';
			const date = new Date(time);
			return date.toLocaleString('zh-CN', {
				year: 'numeric',
				month: '2-digit',
				day: '2-digit',
				hour: '2-digit',
				minute: '2-digit'
			});
		},
		handleRefreshOrder() {
			console.log('收到刷新订单列表事件')
			if (this.selectedElder) {
				this.loadOrders(this.selectedElder.id)
			}
		},
		selectStatus(status) {
			this.selectedStatus = status;
			// 切换标签页时重新加载订单数据
			if (this.selectedElder) {
				this.loadOrders(this.selectedElder.id);
			}
		},
		async payOrder(orderId) {
			try {
				uni.showLoading({
					title: '支付中...'
				});
				
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/orders/${orderId}/pay`,
					method: 'POST',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`,
						'Content-Type': 'application/json'
					},
					data: {
						payment_method: '微信支付'
					}
				});
				
				if (response.statusCode === 200) {
					uni.hideLoading();
					uni.showToast({
						title: '支付成功',
						icon: 'success'
					});
					// 重新加载订单
					this.loadOrders(this.selectedElder.id);
				} else {
					throw new Error(response.data?.detail || '支付失败');
				}
			} catch (error) {
				console.error('支付失败:', error);
				uni.hideLoading();
				uni.showToast({
					title: error.message || '支付失败',
					icon: 'none'
				});
			}
		},
		async cancelOrder(orderId) {
			uni.showModal({
				title: '取消订单',
				content: '确定要取消这个订单吗？',
				success: async (res) => {
					if (res.confirm) {
						try {
							const response = await uni.request({
								url: `http://127.0.0.1:7678/api/v1/member/orders/${orderId}/cancel`,
								method: 'POST',
								header: {
									'Authorization': `Bearer ${uni.getStorageSync('token')}`
								}
							});
							
							if (response.statusCode === 200) {
								uni.showToast({
									title: '钱已退、订单取消',
									icon: 'success'
								});
								// 重新加载订单列表
								this.loadOrders(this.selectedElder.id);
							} else {
								throw new Error(response.data?.detail || '取消订单失败');
							}
						} catch (error) {
							console.error('取消订单失败:', error);
							uni.showToast({
								title: error.message || '取消订单失败',
								icon: 'none'
							});
						}
					}
				}
			});
		},
		trackOrder(orderId) {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		reviewOrder(orderId) {
			console.log('评价订单ID:', orderId, '老人ID:', this.selectedElder.id)
			uni.navigateTo({
				url: `/pages/orders/review?id=${orderId}&elderId=${this.selectedElder.id}`
			});
		},
		viewOrder(orderId) {
			uni.navigateTo({
				url: `/pages/orders/order-detail?id=${orderId}`
			});
		},
		goToOrder() {
			uni.switchTab({
				url: '/pages/order/order'
			});
		},
		showElderSelector() {
			this.showElderModal = true;
		},
		selectElder(elder) {
			this.selectedElder = elder;
			this.showElderModal = false;
			this.loadOrders(elder.id);
		},
		async contactRider(orderId) {
			try {
				// 获取订单详情，获取真实的配送员电话
				const orderDetail = await apiClient.get(`/member/orders/${orderId}`)
				
				if (orderDetail.delivery_phone) {
					uni.showActionSheet({
						itemList: ['语音通话', '短信联系'],
						success: (res) => {
							if (res.tapIndex === 0) {
								// 语音通话 - 使用真实配送员电话
								uni.makePhoneCall({
									phoneNumber: orderDetail.delivery_phone,
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

/* 状态筛选栏 */
.status-section {
	background: #ffffff;
	padding: 16px 0;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.status-scroll {
	white-space: nowrap;
	padding: 0 24px;
}

.status-item {
	display: inline-block;
	padding: 12px 24px;
	margin-right: 12px;
	background: #f1f5f9;
	border-radius: 20px;
	font-size: 16px;
	color: #64748b;
	font-weight: 500;
	transition: all 0.3s ease;
}

.status-item.active {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	color: #ffffff;
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
}

/* 订单列表 */
.orders-section {
	padding: 24px;
}

.order-card {
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
	margin-bottom: 24px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
	position: relative;
}

.order-card::before {
	content: '';
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 4px;
	background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
	border-radius: 24px 24px 0 0;
}

.order-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20px;
	padding-bottom: 16px;
	border-bottom: 1px solid #f1f5f9;
}

.order-number {
	font-size: 16px;
	color: #64748b;
	font-weight: 500;
}

.order-status {
	padding: 6px 16px;
	border-radius: 12px;
	font-size: 14px;
	font-weight: 500;
}

.order-status.pending_payment {
	background: rgba(245, 158, 11, 0.1);
	color: #f59e0b;
}

.order-status.pending_accept {
	background: rgba(99, 102, 241, 0.1);
	color: #6366f1;
}

.order-status.delivering {
	background: rgba(59, 130, 246, 0.1);
	color: #3b82f6;
}

.order-status.completed {
	background: rgba(16, 185, 129, 0.1);
	color: #10b981;
}

.order-status.cancelled {
	background: rgba(239, 68, 68, 0.1);
	color: #ef4444;
}

.status-text {
	
}

.order-content {
	margin-bottom: 20px;
}

.food-items {
	
}

.food-item {
	display: flex;
	align-items: center;
	padding: 12px 0;
	border-bottom: 1px solid #f1f5f9;
}

.food-item:last-child {
	border-bottom: none;
}

.food-image {
	width: 56px;
	height: 56px;
	border-radius: 12px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-right: 16px;
}

.food-info {
	flex: 1;
}

.food-name {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
	display: block;
	margin-bottom: 4px;
}

.food-quantity {
	font-size: 14px;
	color: #64748b;
}

.food-price {
	font-size: 16px;
	font-weight: 600;
	color: #6366f1;
}

.order-footer {
	
}

.order-info {
	margin-bottom: 16px;
}

.order-time {
	font-size: 14px;
	color: #64748b;
	display: block;
	margin-bottom: 8px;
}

.order-scheduled {
	font-size: 14px;
	color: #6366f1;
	display: block;
	margin-bottom: 8px;
	font-weight: 500;
}

.order-type-tag {
	display: inline-block;
	padding: 4px 12px;
	border-radius: 12px;
	font-size: 12px;
	font-weight: 500;
	margin-top: 8px;
}

.order-type-scheduled {
	background: rgba(99, 102, 241, 0.1);
	color: #6366f1;
}

.order-type-immediate {
	background: rgba(16, 185, 129, 0.1);
	color: #10b981;
}

.order-actions {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.order-total {
	display: flex;
	align-items: baseline;
}

.total-label {
	font-size: 16px;
	color: #64748b;
	margin-right: 8px;
}

.total-price {
	font-size: 24px;
	font-weight: 700;
	color: #6366f1;
}

.action-buttons {
	display: flex;
	gap: 12px;
}

.action-btn {
	padding: 8px 20px;
	border-radius: 16px;
	font-size: 14px;
	font-weight: 500;
	border: 2px solid #e2e8f0;
	background: #ffffff;
	color: #64748b;
	transition: all 0.3s ease;
}

.action-btn.primary {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border-color: #6366f1;
	color: #ffffff;
}

.btn-text {
	
}

/* 空状态 */
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 24px;
	text-align: center;
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
	margin-bottom: 24px;
	display: block;
}

.go-order-btn {
	padding: 12px 32px;
	background: linear-gradient(135deg, #165DFF 0%, #7B61FF 100%);
	border: none;
	border-radius: 24px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 500;
	box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
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