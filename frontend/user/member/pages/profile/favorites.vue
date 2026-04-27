<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="nav-left">
				<view class="back-btn" @click="goBack">
					<text class="back-icon">‹</text>
				</view>
			</view>
			<view class="nav-center">
				<text class="page-title">我的收藏</text>
			</view>
			<view class="nav-right"></view>
		</view>
		
		<!-- 收藏餐品列表 -->
		<view class="favorites-section">
			<view v-if="loading" class="loading-state">
				<view class="loading-spinner"></view>
				<text class="loading-text">加载中...</text>
			</view>
			<view v-else-if="favorites.length > 0" class="favorites-grid">
				<view class="food-card" v-for="(food, index) in favorites" :key="index">
					<image 
						class="food-image" 
						:src="food.image_url" 
						mode="aspectFill"
						@error="(e) => {
							console.error('图片加载失败:', e);
							food.image_url = `https://via.placeholder.com/300x200/6366f1/FFFFFF?text=${encodeURIComponent(food.name)}`;
						}"
					></image>
					<text class="food-name">{{ food.name }}</text>
					<text class="food-price">¥{{ food.price }}</text>
					<view class="nutrition-tags">
						<view class="nutrition-tag" v-if="food.category">
							<text class="tag-text">{{ food.category }}</text>
						</view>
						<view class="nutrition-tag" v-if="food.special_tag">
							<text class="tag-text">{{ food.special_tag }}</text>
						</view>
					</view>
					<view class="food-actions">
						<view class="quantity-control" v-if="getFoodQuantity(food.id) > 0">
							<view class="quantity-btn" @click="decreaseQuantity(food.id)">-</view>
							<text class="quantity">{{ getFoodQuantity(food.id) }}</text>
							<view class="quantity-btn" @click="increaseQuantity(food.id)">+</view>
						</view>
						<button class="add-btn" v-else @click="addFood(food)">
							<text class="add-icon">+</text>
						</button>
					</view>
					<view class="favorite-btn" @click="removeFavorite(food.id)">
						<text class="favorited">❤</text>
					</view>
				</view>
			</view>
			<view v-else class="empty-state">
				<text class="empty-icon">📝</text>
				<text class="empty-title">暂无收藏</text>
				<text class="empty-subtitle">快去点餐页面收藏喜欢的餐品吧</text>
				<button class="go-shopping-btn" @click="goToOrder">去点餐</button>
			</view>
		</view>
		
		<!-- 底部固定区域 -->
		<view class="bottom-fixed" v-if="cartTotal > 0">
			<view class="cart-info" @click="showCart">
				<view class="cart-icon">
					<text class="cart-symbol">🛒</text>
					<view class="cart-badge">
						<text class="badge-text">{{ cartTotal }}</text>
					</view>
				</view>
				<view class="cart-details">
					<text class="cart-text">购物车</text>
					<text class="cart-price">¥{{ cartTotalPrice.toFixed(2) }}</text>
				</view>
			</view>
			<button class="checkout-btn" @click="goToCheckout">
				<text class="checkout-text">去结算</text>
			</button>
		</view>
		
		<!-- 购物车弹窗 -->
		<view class="cart-modal" v-if="showCartModal">
			<view class="cart-modal-content">
				<view class="cart-modal-header">
					<text class="cart-modal-title">购物车</text>
					<text class="cart-modal-close" @click="showCartModal = false">×</text>
				</view>
				<view class="cart-items">
					<view class="cart-item" v-for="(item, index) in cartItems" :key="index">
						<image class="item-image" :src="item.image_url" mode="aspectFill"></image>
						<view class="item-info">
							<text class="item-name">{{ item.name }}</text>
							<text class="item-price">¥{{ item.price }}</text>
						</view>
						<view class="item-quantity">
							<view class="quantity-btn" @click="decreaseQuantity(item.id)">-</view>
							<text class="quantity">{{ item.quantity }}</text>
							<view class="quantity-btn" @click="increaseQuantity(item.id)">+</view>
						</view>
					</view>
					<view class="empty-cart" v-if="cartItems.length === 0">
						<text class="empty-text">购物车为空</text>
					</view>
				</view>
				<view class="cart-footer">
					<view class="total-section">
						<text class="total-label">合计：</text>
						<text class="total-price">¥{{ cartTotalPrice.toFixed(2) }}</text>
					</view>
					<button class="confirm-btn" @click="confirmOrder" :disabled="cartItems.length === 0">
						<text class="confirm-text">确认订单</text>
					</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			favorites: [],
			loading: false,
			cart: {},
			showCartModal: false
		};
	},
	computed: {
		cartItems() {
			return Object.keys(this.cart).map(id => {
				const food = this.favorites.find(f => f.id == id);
				return {
					...food,
					quantity: this.cart[id]
				};
			});
		},
		cartTotal() {
			return Object.values(this.cart).reduce((total, quantity) => total + quantity, 0);
		},
		cartTotalPrice() {
			return Object.keys(this.cart).reduce((total, id) => {
				const food = this.favorites.find(f => f.id == id);
				return total + (food.price * this.cart[id]);
			}, 0);
		}
	},
	onLoad() {
		this.loadFavorites();
	},
	methods: {
		async loadFavorites() {
			try {
				this.loading = true;
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/favorites',
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					this.favorites = response.data.items;
				}
			} catch (error) {
				console.error('加载收藏列表失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		
		getFoodQuantity(foodId) {
			return this.cart[foodId] || 0;
		},
		
		addFood(food) {
			if (this.cart[food.id]) {
				this.cart[food.id]++;
			} else {
				this.cart[food.id] = 1;
			}
			uni.showToast({
				title: '已加入购物车',
				icon: 'success'
			});
		},
		
		increaseQuantity(foodId) {
			this.cart[foodId]++;
		},
		
		decreaseQuantity(foodId) {
			if (this.cart[foodId] > 1) {
				this.cart[foodId]--;
			} else {
				delete this.cart[foodId];
			}
		},
		
		async removeFavorite(mealId) {
			uni.showModal({
				title: '取消收藏',
				content: '确定要取消收藏这个餐品吗？',
				success: async (res) => {
					if (res.confirm) {
						try {
							const response = await uni.request({
								url: `http://127.0.0.1:7678/api/v1/member/favorites/${mealId}`,
								method: 'DELETE',
								header: {
									'Authorization': `Bearer ${uni.getStorageSync('token')}`
								}
							});
							
							if (response.statusCode === 200) {
								const index = this.favorites.findIndex(f => f.id === mealId);
								if (index > -1) {
									this.favorites.splice(index, 1);
								}
								uni.showToast({
									title: '已取消收藏',
									icon: 'success'
								});
							}
						} catch (error) {
							console.error('取消收藏失败:', error);
							uni.showToast({
								title: '取消收藏失败',
								icon: 'none'
							});
						}
					}
				}
			});
		},
		
		showCart() {
			if (this.cartTotal > 0) {
				this.showCartModal = true;
			}
		},
		
		goToCheckout() {
			if (this.cartTotal > 0) {
				this.showCartModal = true;
			}
		},
		
		async confirmOrder() {
			if (this.cartItems.length === 0) {
				uni.showToast({
					title: '请先添加餐品',
					icon: 'none'
				});
				return;
			}
			
			uni.showLoading({
				title: '跳转到结算页面...'
			});
			
			setTimeout(() => {
				uni.hideLoading();
				uni.switchTab({
					url: '/pages/order/order'
				});
			}, 1000);
		},
		
		goBack() {
			uni.navigateBack();
		},
		
		goToOrder() {
			uni.switchTab({
				url: '/pages/order/order'
			});
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background: #f8fafc;
	padding-bottom: 100px;
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

.nav-left {
	width: 36px;
}

.nav-center {
	flex: 1;
	text-align: center;
}

.back-btn {
	width: 36px;
	height: 36px;
	border-radius: 10px;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
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
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
}

.nav-right {
	width: 36px;
}

/* 收藏列表 */
.favorites-section {
	padding: 16px;
}

.loading-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 0;
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
	font-size: 14px;
	color: #64748b;
}

.favorites-grid {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 16px;
}

.food-card {
	background: #ffffff;
	border-radius: 20px;
	padding: 12px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	position: relative;
	transition: all 0.3s ease;
	border: 1px solid rgba(226, 232, 240, 0.5);
}

.food-card:active {
	transform: scale(0.98);
}

.food-image {
	width: 100%;
	height: 110px;
	border-radius: 16px;
	background: #f1f5f9;
	margin-bottom: 12px;
}

.food-name {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 4px;
	display: block;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.food-price {
	font-size: 18px;
	font-weight: 700;
	color: #6366f1;
	margin-bottom: 8px;
	display: block;
}

.nutrition-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 4px;
	margin-bottom: 12px;
	height: 22px;
	overflow: hidden;
}

.nutrition-tag {
	padding: 2px 8px;
	background: #f1f5f9;
	border-radius: 6px;
}

.tag-text {
	font-size: 10px;
	color: #64748b;
}

.food-actions {
	display: flex;
	justify-content: center;
	margin-top: 4px;
}

.add-btn {
	width: 36px;
	height: 36px;
	border-radius: 12px;
	background: #6366f1;
	border: none;
	color: #ffffff;
	font-size: 20px;
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.quantity-control {
	display: flex;
	align-items: center;
	gap: 12px;
}

.quantity-btn {
	width: 28px;
	height: 28px;
	border-radius: 8px;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 18px;
	color: #6366f1;
	font-weight: 600;
}

.quantity {
	font-size: 14px;
	font-weight: 600;
	color: #1e293b;
	min-width: 16px;
	text-align: center;
}

.favorite-btn {
	position: absolute;
	top: 8px;
	right: 8px;
	width: 32px;
	height: 32px;
	border-radius: 10px;
	background: rgba(255, 255, 255, 0.9);
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 18px;
	color: #ef4444;
	transition: all 0.2s ease;
	z-index: 10;
	box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.favorite-btn:active {
	transform: scale(0.9);
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
	font-size: 80px;
	margin-bottom: 24px;
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
	margin-bottom: 24px;
}

.go-shopping-btn {
	padding: 16px 40px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	color: #ffffff;
	border: none;
	border-radius: 20px;
	font-size: 16px;
	font-weight: 500;
}

/* 底部固定区域 */
.bottom-fixed {
	position: fixed;
	bottom: 20px;
	left: 20px;
	right: 20px;
	height: 64px;
	background: #1e293b;
	border-radius: 20px;
	display: flex;
	align-items: center;
	padding: 0 16px;
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
	z-index: 100;
}

.cart-info {
	flex: 1;
	display: flex;
	align-items: center;
}

.cart-icon {
	position: relative;
	margin-right: 12px;
	width: 44px;
	height: 44px;
	background: rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.cart-symbol {
	font-size: 24px;
}

.cart-badge {
	position: absolute;
	top: -6px;
	right: -6px;
	background: #ef4444;
	color: #ffffff;
	border-radius: 10px;
	min-width: 18px;
	height: 18px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 11px;
	font-weight: 600;
	padding: 0 4px;
	border: 2px solid #1e293b;
}

.cart-details {
	
}

.cart-text {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
	display: block;
}

.cart-price {
	font-size: 18px;
	font-weight: 700;
	color: #ffffff;
	display: block;
}

.checkout-btn {
	width: 100px;
	height: 40px;
	background: #6366f1;
	border: none;
	border-radius: 12px;
	color: #ffffff;
	font-size: 14px;
	font-weight: 600;
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* 购物车弹窗 */
.cart-modal {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: flex-end;
	z-index: 1000;
}

.cart-modal-content {
	width: 100%;
	max-height: 80vh;
	background: #ffffff;
	border-radius: 32px 32px 0 0;
	padding: 24px;
	display: flex;
	flex-direction: column;
}

.cart-modal-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 24px;
}

.cart-modal-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
}

.cart-modal-close {
	font-size: 24px;
	color: #64748b;
}

.cart-items {
	flex: 1;
	overflow-y: auto;
}

.cart-item {
	display: flex;
	align-items: center;
	padding: 16px 0;
	border-bottom: 1px solid #f1f5f9;
}

.item-image {
	width: 60px;
	height: 60px;
	border-radius: 16px;
	background: #f1f5f9;
	margin-right: 16px;
}

.item-info {
	flex: 1;
}

.item-name {
	font-size: 16px;
	font-weight: 500;
	color: #1e293b;
	display: block;
	margin-bottom: 4px;
}

.item-price {
	font-size: 16px;
	color: #6366f1;
	font-weight: 600;
}

.item-quantity {
	display: flex;
	align-items: center;
	gap: 16px;
}

.empty-cart {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 40px 0;
}

.empty-text {
	font-size: 16px;
	color: #64748b;
}

.cart-footer {
	margin-top: 24px;
	padding-top: 24px;
	border-top: 1px solid #f1f5f9;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.total-section {
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

.confirm-btn {
	width: 120px;
	height: 48px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 20px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 500;
}

.confirm-btn:disabled {
	background: #cbd5e1;
	opacity: 0.6;
}

@keyframes spin {
	0% { transform: rotate(0deg); }
	100% { transform: rotate(360deg); }
}
</style>
