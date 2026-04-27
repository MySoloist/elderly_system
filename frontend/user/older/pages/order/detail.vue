<template>
	<view class="order-detail-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">订单详情</text>
			<text class="placeholder"></text>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 订单信息 -->
		<view v-else-if="order.id" class="order-info">
			<view class="order-header">
				<text class="order-id">订单号: {{ order.id }}</text>
				<text class="order-status" :class="getStatusClass(order.status)">
					{{ getStatusText(order.status) }}
				</text>
			</view>
			
			<view class="order-time">下单时间: {{ order.time }}</view>
		</view>
		
		<!-- 餐品列表 -->
		<view v-if="order.id" class="food-list">
			<view class="section-title">餐品清单</view>
			<view v-for="item in order.items" :key="item.id" class="food-item">
				<image v-if="item.image && item.image !== '🍱'" class="food-image" :src="item.image" mode="aspectFill"></image>
				<text v-else class="food-image">🍱</text>
				<view class="food-info">
					<text class="food-name">{{ item.name }}</text>
					<view class="food-price-row">
						<text class="food-price">¥{{ item.price }}</text>
						<text class="food-quantity">x{{ item.quantity }}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 配送信息 -->
		<view v-if="order.id && (order.status === 'delivering' || order.status === 'completed')" class="delivery-info">
			<view class="section-title">配送信息</view>
			<view class="delivery-item">
				<text class="delivery-label">配送地址:</text>
				<text class="delivery-value">{{ order.delivery_address || '暂无地址' }}</text>
			</view>
			<view v-if="order.delivery_man" class="delivery-item">
				<text class="delivery-label">配送员:</text>
				<text class="delivery-value">{{ order.delivery_man }}</text>
			</view>
			<view v-if="order.delivery_phone" class="delivery-item">
				<text class="delivery-label">联系电话:</text>
				<text class="delivery-value">{{ order.delivery_phone }}</text>
			</view>
		</view>
		
		<!-- 订单金额 -->
		<view v-if="order.id" class="order-amount">
			<view class="amount-item">
				<text class="amount-label">餐品小计:</text>
				<text class="amount-value">¥{{ order.total }}</text>
			</view>
			<view class="amount-item">
				<text class="amount-label">配送费:</text>
				<text class="amount-value">¥0</text>
			</view>
			<view class="amount-item total">
				<text class="amount-label">实付金额:</text>
				<text class="amount-value">¥{{ order.total }}</text>
			</view>
		</view>
		
		<!-- 底部按钮 -->
		<view v-if="order.id" class="bottom-actions">
			<button 
				v-if="order.status === 'pending'"
				class="action-btn cancel-btn"
				@click="cancelOrder"
			>取消订单</button>
			<button 
				v-if="order.status === 'pending'"
				class="action-btn pay-btn"
				@click="payOrder"
			>去支付</button>
			<button 
				v-if="order.status === 'completed'"
				class="action-btn review-btn"
				@click="reviewOrder"
			>评价订单</button>
			<button 
				v-if="(order.status === 'delivering' || order.status === 'completed') && order.delivery_phone"
				class="action-btn rider-btn"
				@click="contactRider"
			>联系骑手</button>
			<button 
				class="action-btn contact-btn"
				@click="contactService"
			>联系客服</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				orderId: '',
				order: {
					id: '',
					status: '',
					time: '',
					total: 0,
					items: [],
					delivery_address: '',
					delivery_man: '',
					delivery_phone: ''
				},
				loading: false
			}
		},
		onLoad(options) {
			this.orderId = options.orderId
			this.loadOrderDetail()
		},
		methods: {
			async loadOrderDetail() {
				this.loading = true
				try {
					const orderDetail = await api.older.getOrder(this.orderId)
					this.order = {
						id: orderDetail.id,
						status: orderDetail.status,
						time: new Date(orderDetail.created_at).toLocaleString('zh-CN'),
						total: orderDetail.total_amount,
						delivery_address: orderDetail.delivery_address,
						delivery_man: orderDetail.delivery ? orderDetail.delivery.deliverer_name || '' : '',
						delivery_phone: orderDetail.delivery ? orderDetail.delivery.deliverer_phone || '' : '',
						items: orderDetail.items.map(item => ({
							id: item.id,
							name: item.meal_name,
							price: item.price,
							quantity: item.quantity,
							image: item.image_url ? item.image_url : '🍱'
						}))
					}
				} catch (error) {
					console.error('获取订单详情失败:', error)
					uni.showToast({
						title: '获取订单详情失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			getStatusText(status) {
				const statusMap = {
					'pending_payment': '待支付',
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
					'pending_accept': 'status-pending',
					'delivering': 'status-delivering',
					'completed': 'status-completed',
					'cancelled': 'status-cancelled'
				}
				return classMap[status] || ''
			},
			getEstimatedTime() {
				const now = new Date()
				const hour = now.getHours()
				const minute = now.getMinutes() + 30
				const newHour = minute >= 60 ? hour + 1 : hour
				const newMinute = minute % 60
				return `${newHour.toString().padStart(2, '0')}:${newMinute.toString().padStart(2, '0')}`
			},
			goBack() {
				uni.navigateBack()
			},
			async cancelOrder() {
				uni.showModal({
					title: '取消订单',
					content: '确定要取消这个订单吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.older.cancelOrder(this.orderId)
								uni.showToast({
									title: '订单已取消',
									icon: 'success'
								})
								setTimeout(() => {
									uni.navigateBack()
								}, 1000)
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
			payOrder() {
				uni.showToast({
					title: '支付功能开发中...',
					icon: 'none'
				})
			},
			reviewOrder() {
				uni.navigateTo({
					url: `/pages/order/review?orderId=${this.orderId}`
				})
			},
			contactRider() {
				uni.showModal({
					title: '联系骑手',
					content: `是否拨打 ${this.order.delivery_man || '配送员'} 的电话？`,
					success: (res) => {
						if (res.confirm) {
							uni.makePhoneCall({
								phoneNumber: this.order.delivery_phone.replace(/\*/g, '0'),
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
			},
			contactService() {
				uni.showToast({
					title: '客服电话：400-123-4567',
					icon: 'none',
					duration: 3000
				})
			}
		}
	}
</script>

<style scoped>
	.order-detail-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 200px, #F5F5F5 100%);
		padding-bottom: 80px;
	}
	
	/* 顶部导航栏 */
	.top-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 58px;
		padding: 0 20px;
		background: rgba(255, 255, 255, 0.92);
		border-bottom: 1px solid rgba(255, 122, 69, 0.08);
		backdrop-filter: blur(8px);
	}
	
	.back-btn {
		font-size: 24px;
		color: #333333;
		width: 36px;
		text-align: center;
	}
	
	.nav-title {
		font-size: 19px;
		font-weight: 600;
		color: #333333;
		flex: 1;
		text-align: center;
	}
	
	.placeholder {
		width: 36px;
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
	
	/* 订单信息 */
	.order-info {
		background-color: #FFFFFF;
		margin: 20px;
		padding: 20px;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
	}
	
	.order-id {
		font-size: 14px;
		color: #999999;
		background: #f7f7f7;
		padding: 4px 10px;
		border-radius: 12px;
	}
	
	.order-status {
		font-size: 14px;
		font-weight: 600;
		padding: 6px 12px;
		border-radius: 12px;
	}
	
	.status-pending {
		background-color: rgba(245, 108, 108, 0.1);
		color: #F56C6C;
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
	
	.order-time {
		font-size: 13px;
		color: #999999;
	}
	
	/* 餐品列表 */
	.food-list {
		background-color: #FFFFFF;
		margin: 0 20px 20px;
		padding: 20px;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		margin-bottom: 16px;
	}
	
	.food-item {
		display: flex;
		align-items: center;
		padding: 12px 0;
		border-bottom: 1px solid #F5F5F5;
	}
	
	.food-item:last-child {
		border-bottom: none;
	}
	
	.food-image {
		font-size: 32px;
		margin-right: 12px;
		width: 40px;
		height: 40px;
		text-align: center;
		object-fit: cover;
		border-radius: 8px;
	}
	
	.food-info {
		flex: 1;
	}
	
	.food-name {
		font-size: 15px;
		color: #333333;
		font-weight: 500;
		margin-bottom: 6px;
		display: block;
	}
	
	.food-price-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.food-price {
		font-size: 14px;
		color: #FF7A45;
		font-weight: 600;
	}
	
	.food-quantity {
		font-size: 13px;
		color: #999999;
	}
	
	/* 配送信息 */
	.delivery-info {
		background-color: #FFFFFF;
		margin: 0 20px 20px;
		padding: 20px;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.delivery-item {
		display: flex;
		margin-bottom: 12px;
	}
	
	.delivery-item:last-child {
		margin-bottom: 0;
	}
	
	.delivery-label {
		width: 80px;
		font-size: 14px;
		color: #666666;
	}
	
	.delivery-value {
		flex: 1;
		font-size: 14px;
		color: #333333;
	}
	
	/* 订单金额 */
	.order-amount {
		background-color: #FFFFFF;
		margin: 0 20px 20px;
		padding: 20px;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.amount-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
	}
	
	.amount-item:last-child {
		margin-bottom: 0;
	}
	
	.amount-item.total {
		padding-top: 12px;
		border-top: 1px solid #F5F5F5;
	}
	
	.amount-label {
		font-size: 14px;
		color: #666666;
	}
	
	.amount-value {
		font-size: 14px;
		color: #333333;
		font-weight: 500;
	}
	
	.amount-item.total .amount-value {
		font-size: 18px;
		color: #FF7A45;
		font-weight: 700;
		text-shadow: 0 1px 2px rgba(255, 122, 69, 0.2);
	}
	
	/* 底部按钮 */
	.bottom-actions {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		background: rgba(255, 255, 255, 0.95);
		backdrop-filter: blur(10px);
		padding: 16px 20px;
		border-top: 1px solid rgba(255, 122, 69, 0.08);
		display: flex;
		gap: 12px;
		z-index: 100;
	}
	
	.action-btn {
		flex: 1;
		height: 44px;
		border-radius: 22px;
		font-size: 15px;
		font-weight: 600;
		border: none;
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
	
	.rider-btn {
		background-color: #409EFF;
		color: white;
	}
	
	.contact-btn {
		background-color: #67C23A;
		color: white;
	}
</style>
