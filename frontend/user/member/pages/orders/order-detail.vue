<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">订单详情</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 订单状态卡片 -->
		<view class="status-card" :class="order.status">
			<view class="status-icon"></view>
			<text class="status-title">{{ getStatusName(order.status) }}</text>
			<text class="status-desc">{{ getStatusDescription(order.status) }}</text>
		</view>
		
		<!-- 订单信息 -->
		<view class="order-info-card">
			<view class="info-item">
				<text class="info-label">订单编号</text>
				<text class="info-value">{{ order.orderNumber }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">下单时间</text>
				<text class="info-value">{{ order.orderTime }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">老人姓名</text>
				<text class="info-value">{{ order.elderName }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">配送地址</text>
				<text class="info-value">{{ order.address }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">订单类型</text>
				<text :class="getOrderTypeClass(order.orderType)" class="info-value order-type-tag">
					{{ order.orderType === 'scheduled' ? '预定' : '即时' }}
				</text>
			</view>
			<view v-if="order.orderType === 'scheduled' && order.scheduledTime" class="info-item">
				<text class="info-label">预定时间</text>
				<text class="info-value scheduled-time">{{ formatScheduledTime(order.scheduledTime) }}</text>
			</view>
		</view>
		
		<!-- 餐品列表 -->
		<view class="foods-card">
			<text class="card-title">餐品明细</text>
			<view class="food-item" v-for="(food, index) in order.foods" :key="index">
				<view class="food-image"></view>
				<view class="food-info">
					<text class="food-name">{{ food.name }}</text>
					<text class="food-price">¥{{ food.price }}</text>
				</view>
				<text class="food-quantity">×{{ food.quantity }}</text>
			</view>
		</view>
		
		<!-- 配送信息 -->
		<view class="delivery-card" v-if="order.status === 'delivering' || order.status === 'completed'">
			<text class="card-title">配送信息</text>
			<view class="delivery-info">
				<view class="delivery-item">
					<text class="delivery-label">配送员</text>
					<text class="delivery-value">{{ order.deliveryMan }}</text>
				</view>
				<view class="delivery-item">
					<text class="delivery-label">联系电话</text>
					<text class="delivery-value">{{ order.deliveryPhone }}</text>
				</view>
				<view v-if="order.status === 'delivering'" class="delivery-item">
					<text class="delivery-label">预计送达</text>
					<text class="delivery-value">{{ order.estimatedTime }}</text>
				</view>
			</view>
			<button class="contact-btn" @click="contactDelivery">
				<text class="contact-icon">📞</text>
				<text class="contact-text">联系配送员</text>
			</button>
		</view>
		
		<!-- 支付信息 -->
		<view class="payment-card">
			<text class="card-title">支付信息</text>
			<view class="payment-info">
				<view class="payment-item">
					<text class="payment-label">支付方式</text>
					<text class="payment-value">{{ order.paymentMethod }}</text>
				</view>
				<view class="payment-item">
					<text class="payment-label">支付时间</text>
					<text class="payment-value">{{ order.paymentTime || '待支付' }}</text>
				</view>
			</view>
		</view>
		
		<!-- 价格明细 -->
		<view class="price-card">
			<view class="price-item">
				<text class="price-label">商品总价</text>
				<text class="price-value">¥{{ order.subtotal }}</text>
			</view>
			<view class="price-item">
				<text class="price-label">配送费</text>
				<text class="price-value">¥{{ order.deliveryFee }}</text>
			</view>
			<view class="price-item">
				<text class="price-label">优惠金额</text>
				<text class="price-value discount">-¥{{ order.discount }}</text>
			</view>
			<view class="price-item total">
				<text class="price-label">实付金额</text>
				<text class="price-value total-price">¥{{ order.totalPrice }}</text>
			</view>
		</view>
		
		<!-- 底部操作按钮 -->
		<view class="bottom-actions" v-if="showActions">
			<button class="action-btn cancel" v-if="order.status === 'pending'" @click="cancelOrder">
				<text class="btn-text">取消订单</text>
			</button>
			<button class="action-btn primary" v-if="order.status === 'delivering'" @click="trackOrder">
				<text class="btn-text">跟踪配送</text>
			</button>
			<button class="action-btn primary" v-if="order.status === 'completed'" @click="reorder">
				<text class="btn-text">再次购买</text>
			</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			order: {
				id: '',
				orderNumber: '',
				status: '',
				orderTime: '',
				elderName: '',
				address: '',
				foods: [],
				subtotal: 0,
				deliveryFee: 0,
				discount: 0,
				totalPrice: 0,
				paymentMethod: '',
				paymentTime: '',
				deliveryMan: '',
				deliveryPhone: '',
				estimatedTime: '',
				orderType: 'immediate',
				scheduledTime: ''
			}
		};
	},
	computed: {
		showActions() {
			return ['pending', 'delivering', 'completed'].includes(this.order.status);
		}
	},
	onLoad(options) {
		const orderId = options.id;
		this.loadOrderDetail(orderId);
	},
	methods: {
		async loadOrderDetail(orderId) {
			try {
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/orders/${orderId}`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					const data = response.data;
					this.order = {
						id: data.id,
						orderNumber: data.id.toString(),
						status: data.status,
						orderTime: data.created_at,
						elderName: data.elderly_name || '未知老人',
						address: data.address || '暂无地址',
						foods: data.items.map(item => ({
							name: item.meal.name,
							price: item.unit_price,
							quantity: item.quantity
						})),
						subtotal: data.total_amount,
						deliveryFee: data.delivery_fee || 0,
						discount: data.discount || 0,
						totalPrice: data.total_amount,
						paymentMethod: data.payment_method || '微信支付',
						paymentTime: data.paid_at || '',
						deliveryMan: data.delivery_man || '',
						deliveryPhone: data.delivery_phone || '',
						estimatedTime: data.estimated_time || '',
						orderType: data.order_type || 'immediate',
						scheduledTime: data.scheduled_time || ''
					};
				} else {
					throw new Error(response.data?.detail || '加载订单详情失败');
				}
			} catch (error) {
				console.error('加载订单详情失败:', error);
				uni.showToast({
					title: '订单不存在',
					icon: 'none'
				});
				setTimeout(() => {
					this.goBack();
				}, 1000);
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
		getStatusDescription(status) {
			const descMap = {
				'pending_payment': '请尽快完成支付',
				'pending_schedule': '等待预定时间到达',
				'pending_accept': '等待商家接单',
				'delivering': '骑手正在配送中',
				'completed': '订单已完成',
				'cancelled': '订单已取消'
			};
			return descMap[status] || '';
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
		goBack() {
			const pages = getCurrentPages();
			if (pages.length <= 1) {
				uni.switchTab({
					url: '/pages/orders/orders'
				});
			} else {
				uni.navigateBack();
			}
		},
		cancelOrder() {
			uni.showModal({
				title: '取消订单',
				content: '确定要取消这个订单吗？',
				success: (res) => {
					if (res.confirm) {
						uni.showToast({
							title: '订单已取消',
							icon: 'success'
						});
						setTimeout(() => {
							this.goBack();
						}, 1000);
					}
				}
			});
		},
		trackOrder() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		reorder() {
			uni.switchTab({
				url: '/pages/order/order'
			});
		},
		contactDelivery() {
			uni.makePhoneCall({
				phoneNumber: this.order.deliveryPhone,
				success: () => {
					console.log('拨打电话成功');
				},
				fail: () => {
					uni.showToast({
						title: '拨打电话失败',
						icon: 'none'
					});
				}
			});
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	padding-bottom: 80px;
}

/* 顶部导航 */
.top-nav {
	display: flex;
	align-items: center;
	padding: 20px 24px;
	background: #ffffff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.back-btn {
	width: 40px;
	height: 40px;
	border-radius: 50%;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 16px;
}

.back-icon {
	font-size: 24px;
	color: #6366f1;
}

.page-title {
	flex: 1;
	font-size: 28px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
	text-align: center;
}

.nav-right {
	width: 40px;
}

/* 状态卡片 */
.status-card {
	margin: 24px;
	padding: 32px;
	border-radius: 24px;
	text-align: center;
	position: relative;
	overflow: hidden;
}

.status-card::before {
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

.status-card.pending {
	background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
}

.status-card.processing {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.status-card.delivering {
	background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
}

.status-card.completed {
	background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
}

.status-card.cancelled {
	background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
}

.status-icon {
	width: 80px;
	height: 80px;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.2);
	margin: 0 auto 20px;
	display: flex;
	align-items: center;
	justify-content: center;
	position: relative;
	z-index: 10;
}

.status-icon::before {
	content: '';
	width: 40px;
	height: 40px;
	background: rgba(255, 255, 255, 0.3);
	border-radius: 50%;
}

.status-title {
	font-size: 28px;
	font-weight: 700;
	color: #ffffff;
	margin-bottom: 8px;
	display: block;
	position: relative;
	z-index: 10;
}

.status-desc {
	font-size: 16px;
	color: rgba(255, 255, 255, 0.9);
	display: block;
	position: relative;
	z-index: 10;
}

/* 订单信息卡片 */
.order-info-card {
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
	margin: 0 24px 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.info-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 12px 0;
	border-bottom: 1px solid #f1f5f9;
}

.info-item:last-child {
	border-bottom: none;
}

.info-label {
	font-size: 16px;
	color: #64748b;
	font-weight: 500;
}

.info-value {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
}

.order-type-tag {
	display: inline-block;
	padding: 4px 12px;
	border-radius: 12px;
	font-size: 12px;
	font-weight: 500;
}

.order-type-scheduled {
	background: rgba(99, 102, 241, 0.1);
	color: #6366f1;
}

.order-type-immediate {
	background: rgba(16, 185, 129, 0.1);
	color: #10b981;
}

.scheduled-time {
	color: #6366f1;
	font-weight: 500;
}

/* 餐品列表卡片 */
.foods-card {
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
	margin: 0 24px 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.card-title {
	font-size: 20px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 20px;
	display: block;
}

.food-item {
	display: flex;
	align-items: center;
	padding: 16px 0;
	border-bottom: 1px solid #f1f5f9;
}

.food-item:last-child {
	border-bottom: none;
}

.food-image {
	width: 60px;
	height: 60px;
	border-radius: 16px;
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

.food-price {
	font-size: 16px;
	color: #6366f1;
	font-weight: 600;
}

.food-quantity {
	font-size: 16px;
	color: #64748b;
	font-weight: 500;
}

/* 配送信息卡片 */
.delivery-card {
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
	margin: 0 24px 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.delivery-info {
	margin-bottom: 20px;
}

.delivery-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 12px 0;
}

.delivery-label {
	font-size: 16px;
	color: #64748b;
}

.delivery-value {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
}

.contact-btn {
	width: 100%;
	height: 48px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 16px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 500;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
}

.contact-icon {
	font-size: 20px;
}

.contact-text {
	
}

/* 支付信息卡片 */
.payment-card {
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
	margin: 0 24px 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.payment-info {
	
}

.payment-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 12px 0;
}

.payment-label {
	font-size: 16px;
	color: #64748b;
}

.payment-value {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
}

/* 价格明细卡片 */
.price-card {
	background: #ffffff;
	border-radius: 24px;
	padding: 24px;
	margin: 0 24px 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.price-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 12px 0;
}

.price-item.total {
	margin-top: 8px;
	padding-top: 16px;
	border-top: 1px solid #f1f5f9;
}

.price-label {
	font-size: 16px;
	color: #64748b;
}

.price-value {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
}

.price-value.discount {
	color: #ef4444;
}

.price-value.total-price {
	font-size: 24px;
	font-weight: 700;
	color: #6366f1;
}

/* 底部操作按钮 */
.bottom-actions {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	height: 80px;
	background: #ffffff;
	border-top: 1px solid #e2e8f0;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 0 24px;
	box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.08);
}

.action-btn {
	flex: 1;
	height: 48px;
	border-radius: 16px;
	font-size: 16px;
	font-weight: 500;
	transition: all 0.3s ease;
}

.action-btn.cancel {
	background: #ffffff;
	border: 2px solid #e2e8f0;
	color: #64748b;
	margin-right: 12px;
}

.action-btn.primary {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	color: #ffffff;
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
}

.btn-text {
	
}
</style>
