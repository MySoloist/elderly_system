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
				<text class="page-title">点餐</text>
			</view>
			<view class="nav-right">
				<view class="elder-selector" @click="showElderSelector" :disabled="loading">
					<view class="elder-info">
						<text class="elder-name">{{ loading ? '加载中...' : (selectedElders[0]?.name || '请选择老人') }}</text>
						<text class="elder-tag">{{ selectedElders[0]?.tag || '' }}</text>
					</view>
					<text class="selector-arrow">▼</text>
				</view>
			</view>
		</view>
		
		<!-- 餐品分类栏 -->
		<view class="category-section">
			<scroll-view class="category-scroll" scroll-x="true">
				<view class="category-item" v-for="(category, index) in categories" :key="index" 
					:class="{ active: selectedCategory === category.id }"
					@click="selectCategory(category.id)">
					<text class="category-name">{{ category.name }}</text>
				</view>
			</scroll-view>
		</view>
		
		<!-- 搜索框 -->
		<view class="search-section">
			<view class="search-box">
				<input 
					class="search-input" 
					placeholder="搜索餐品名称或标签..." 
					v-model="searchKeyword"
					@confirm="handleSearch"
				/>
				<text class="search-clear" v-if="searchKeyword" @click="searchKeyword = ''">✕</text>
			</view>
		</view>
		
		<!-- 餐品列表 -->
		<view class="food-section">
			<view class="food-grid">
				<view class="food-card" v-for="(food, index) in filteredFoods" :key="index">
					<view class="food-header">
						<image 
							class="food-image" 
							:src="food.image_url" 
							mode="aspectFill"
							@error="(e) => {
								console.error('图片加载失败:', e);
								food.image_url = `https://via.placeholder.com/300x200/6366f1/FFFFFF?text=${encodeURIComponent(food.name)}`;
							}"
						></image>
						<view class="favorite-btn" @click="toggleFavorite(food)">
							<text :class="{ 'favorited': isFavorite(food.id) }">❤</text>
						</view>
					</view>
					<view class="food-info">
						<text class="food-name">{{ food.name }}</text>
						<view class="price-action-row">
							<text class="food-price">¥{{ food.price }}</text>
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
						</view>
						<view class="nutrition-tags">
							<view class="nutrition-tag" v-for="(tag, tagIndex) in food.nutritionTags" :key="tagIndex">
								<text class="tag-text">{{ tag }}</text>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 底部固定区域 -->
		<view class="bottom-fixed">
			<view class="cart-info" @click="showCart">
				<view class="cart-icon">
					<text class="cart-symbol">🛒</text>
					<view class="cart-badge" v-if="cartTotal > 0">
						<text class="badge-text">{{ cartTotal }}</text>
					</view>
				</view>
				<view class="cart-details">
					<text class="cart-text">购物车</text>
					<text class="cart-price">¥{{ cartTotalPrice.toFixed(2) }}</text>
				</view>
			</view>
			<button class="checkout-btn" @click="goToCheckout" :disabled="cartTotal === 0">
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
						<view class="item-image"></view>
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
		
		<!-- 订单类型选择弹窗 -->
		<view class="order-type-modal" v-if="showOrderTypeModal">
			<view class="order-type-modal-content">
				<view class="order-type-modal-header">
					<text class="order-type-modal-title">选择下单方式</text>
					<text class="order-type-modal-close" @click="showOrderTypeModal = false">×</text>
				</view>
				<view class="order-type-options">
					<button class="order-type-btn" @click="handleImmediateOrder">
						<text class="order-type-icon">⚡</text>
						<text class="order-type-text">现在下单</text>
					</button>
					<button class="order-type-btn" @click="handleScheduledOrder">
						<text class="order-type-icon">⏰</text>
						<text class="order-type-text">预定下单</text>
					</button>
				</view>
			</view>
		</view>
		
		<!-- 时间选择器弹窗 -->
		<view class="time-picker-modal" v-if="showTimePicker">
			<view class="time-picker-modal-content">
				<view class="time-picker-modal-header">
					<text class="time-picker-modal-title">选择预定时间</text>
					<text class="time-picker-modal-close" @click="showTimePicker = false">×</text>
				</view>
				<view class="time-picker-content">
					<view class="time-section">
						<text class="time-label">日期:</text>
						<picker mode="date" :value="selectedDate ? selectedDate.toISOString().split('T')[0] : ''" @change="(e) => selectedDate = new Date(e.detail.value)">
							<view class="picker-view">
								<text>{{ selectedDate ? selectedDate.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit', weekday: 'short' }) : '选择日期' }}</text>
							</view>
						</picker>
					</view>
					<view class="time-section">
						<text class="time-label">时间:</text>
						<view class="time-picker-row">
							<picker :value="selectedHour - 8" :range="hours" @change="(e) => selectedHour = hours[e.detail.value]">
								<view class="picker-view">
									<text>{{ selectedHour }}时</text>
								</view>
							</picker>
							<text class="time-separator">:</text>
							<picker :value="selectedMinute" :range="minutes" @change="(e) => selectedMinute = parseInt(minutes[e.detail.value])">
								<view class="picker-view">
									<text>{{ minutes[selectedMinute] }}分</text>
								</view>
							</picker>
						</view>
					</view>
				</view>
				<view class="time-picker-footer">
					<button class="cancel-btn" @click="showTimePicker = false">取消</button>
					<button class="confirm-btn" @click="confirmTimeSelection">确定</button>
				</view>
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
						:class="{ active: isElderSelected(elder.id) }"
						@click="selectElder(elder)">
						<view class="elder-item-checkbox" :class="{ checked: isElderSelected(elder.id) }">
							<text v-if="isElderSelected(elder.id)" class="checkbox-mark">✓</text>
						</view>
						<view class="elder-item-info">
							<view class="elder-item-main">
								<text class="elder-item-name">{{ elder.name }}</text>
								<text class="elder-item-tag">{{ elder.tag }}</text>
							</view>
						</view>
					</view>
				</view>
				<view class="elder-modal-footer">
					<button class="confirm-btn" @click="confirmElderSelection" :disabled="loading || elders.length === 0">确定</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
				return {
					selectedElders: [],
			elders: [],
			loading: false,
			categories: [],
			selectedCategory: 0,
			foods: [],
			cart: {},
			showCartModal: false,
			showElderModal: false,
			searchKeyword: '',
			favoriteMeals: [],
			// 预定下单相关
			showOrderTypeModal: false,
			showTimePicker: false,
			selectedDate: null,
			selectedHour: 12,
			selectedMinute: 0,
			hours: Array.from({length: 13}, (_, i) => i + 8), // 8:00-20:00
			minutes: Array.from({length: 60}, (_, i) => i.toString().padStart(2, '0')) // 显示所有分钟
				};
			},
	computed: {
		filteredFoods() {
			let filtered = [...this.foods];
			
			// 先应用分类过滤
			if (this.selectedCategory !== 0) {
				filtered = filtered.filter(food => food.category === this.selectedCategory);
			}
			
			// 然后应用搜索过滤
			if (this.searchKeyword) {
				const keyword = this.searchKeyword.toLowerCase();
				filtered = filtered.filter(food => 
					food.name.toLowerCase().includes(keyword) ||
					food.nutritionTags.some(tag => tag.toLowerCase().includes(keyword))
				);
			}
			
			return filtered;
		},
		cartItems() {
			return Object.keys(this.cart).map(id => {
				const food = this.foods.find(f => f.id == id);
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
				const food = this.foods.find(f => f.id == id);
				if (food) {
					return total + (food.price * this.cart[id]);
				}
				return total;
			}, 0);
		}
	},
	onLoad() {
		this.loadElders();
		this.loadCategories();
		this.loadFoods();
		this.loadFavorites();
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
					// 转换数据格式，添加标签信息和地址
					this.elders = response.data.map(elder => ({
						id: elder.elderly_id,
						name: elder.elderly_name,
						tag: this.getElderTag(elder.elderly_age, elder.elderly_gender),
						address: elder.elderly_address || ''
					}));
					
					// 默认选择第一个老人
					if (this.elders.length > 0) {
						this.selectedElders = [this.elders[0]];
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
		async loadCategories() {
			try {
				this.loading = true;
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/categories',
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					// 添加"全部"选项，然后添加从API获取的分类
					this.categories = [
						{ id: 0, name: '全部' },
						...response.data.categories
					];
				} else {
					throw new Error(response.data?.detail || '加载分类列表失败');
				}
			} catch (error) {
				console.error('加载分类列表失败:', error);
				// 如果获取分类失败，使用默认分类
				this.categories = [
					{ id: 0, name: '全部' },
					{ id: 4, name: '主食' },
					{ id: 6, name: '荤菜' },
					{ id: 5, name: '凉菜' },
					{ id: 7, name: '辅食' },
					{ id: 10, name: '营养套餐' }
				];
			} finally {
				this.loading = false;
			}
		},
		async loadFoods() {
			try {
				this.loading = true;
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/older/meals',
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					// 转换数据格式以匹配前端使用的格式
					this.foods = response.data.items.map(food => {
						const foodData = {
							id: food.id,
							name: food.name,
							price: food.price,
							category: food.category_id,
							nutritionTags: food.special_tag ? [food.special_tag] : ['营养'],
							image_url: food.image_url || `https://via.placeholder.com/300x200/6366f1/FFFFFF?text=${encodeURIComponent(food.name)}`
						};
						return foodData;
					});
				} else {
					throw new Error(response.data?.detail || '加载餐品列表失败');
				}
			} catch (error) {
				console.error('加载餐品列表失败:', error);
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
			}
			if (gender === '男') {
				return '爷爷';
			} else {
				return '奶奶';
			}
		},

		goBack() {
			// 获取当前页面栈
			const pages = getCurrentPages();
			if (pages.length <= 1) {
				// 如果是第一个页面，返回首页
				uni.switchTab({
					url: '/pages/health/health'
				});
			} else {
				// 否则正常返回上一页
				uni.navigateBack();
			}
		},
		selectCategory(categoryId) {
			this.selectedCategory = categoryId;
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
		showCart() {
			if (this.cartTotal > 0) {
				this.showCartModal = true;
			} else {
				uni.showToast({
					title: '购物车为空',
					icon: 'none'
				});
			}
		},
		goToCheckout() {
			if (this.cartTotal > 0) {
				// 显示订单类型选择弹窗
				this.showOrderTypeModal = true;
			} else {
				uni.showToast({
					title: '请先添加餐品',
					icon: 'none'
				});
			}
		},
		async confirmOrder() {
			if (this.selectedElders.length === 0) {
				uni.showToast({
					title: '请选择老人',
					icon: 'none'
				});
				return;
			}
			
			uni.showLoading({
				title: '提交订单中...'
			});
			
			try {
				// 准备订单数据
				const orderData = {
					elder_id: this.selectedElders[0].id,
					items: Object.keys(this.cart).map(foodId => ({
						meal_id: parseInt(foodId),
						quantity: this.cart[foodId]
					})),
					delivery_address: this.selectedElders[0].address || '暂无地址',
					special_notes: ''
				};
				
				// 如果选择了预定时间，添加预定相关字段
				if (this.selectedDate) {
					const scheduledDate = new Date(this.selectedDate);
					scheduledDate.setHours(this.selectedHour, this.selectedMinute, 0, 0);
					orderData.scheduled_time = scheduledDate.toISOString();
					orderData.order_type = 'scheduled';
				} else {
					orderData.order_type = 'immediate';
				}
				
				// 调用后端API创建订单
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/orders',
					method: 'POST',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`,
						'Content-Type': 'application/json'
					},
					data: orderData
				});
				
				if (response.statusCode === 200) {
					uni.hideLoading();
					uni.showToast({
						title: '订单提交成功',
						icon: 'success'
					});
					this.cart = {};
					this.showCartModal = false;
					// 重置预定时间
					this.selectedDate = null;
					this.selectedHour = 12;
					this.selectedMinute = 0;
					// 发送刷新订单列表的事件
					uni.$emit('refreshOrderList');
					// 跳转到订单页面
					uni.switchTab({
						url: '/pages/orders/orders'
					});
				} else {
					throw new Error(response.data?.detail || '订单创建失败');
				}
			} catch (error) {
				console.error('订单创建失败:', error);
				uni.hideLoading();
				uni.showToast({
					title: error.message || '订单创建失败',
					icon: 'none'
				});
			}
		},
		showElderSelector() {
			this.showElderModal = true;
		},
		handleSearch() {
			// 搜索已经在computed中实时过滤了
		},
		isElderSelected(elderId) {
			return this.selectedElders.length > 0 && this.selectedElders[0].id === elderId;
		},
		selectElder(elder) {
			this.selectedElders = [elder];
		},
		confirmElderSelection() {
			if (this.selectedElders.length === 0) {
				uni.showToast({
					title: '请至少选择一位老人',
					icon: 'none'
				});
				return;
			}
			this.showElderModal = false;
		},
		// 处理现在下单
		handleImmediateOrder() {
			this.showOrderTypeModal = false;
			this.showCartModal = true;
		},
		// 处理预定下单
		handleScheduledOrder() {
			this.showOrderTypeModal = false;
			this.showTimePicker = true;
		},
		// 确认时间选择
		async confirmTimeSelection() {
			if (!this.selectedDate) {
				uni.showToast({
					title: '请选择日期',
					icon: 'none'
				});
				return;
			}
			
			this.showTimePicker = false;
			this.showCartModal = true;
		},
		
		// 加载收藏列表
		async loadFavorites() {
			try {
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/favorites',
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					this.favoriteMeals = response.data.items.map(item => item.id);
				}
			} catch (error) {
				console.error('加载收藏列表失败:', error);
			}
		},
		
		// 检查餐品是否已收藏
		isFavorite(mealId) {
			return this.favoriteMeals.includes(mealId);
		},
		
		// 切换收藏状态
		async toggleFavorite(food) {
			if (this.isFavorite(food.id)) {
				await this.removeFavorite(food.id);
			} else {
				await this.addFavorite(food.id);
			}
		},
		
		// 添加收藏
		async addFavorite(mealId) {
			try {
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/favorites',
					method: 'POST',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`,
						'Content-Type': 'application/json'
					},
					data: {
						meal_id: mealId
					}
				});
				
				if (response.statusCode === 200) {
					this.favoriteMeals.push(mealId);
					uni.showToast({
						title: '已添加到收藏',
						icon: 'success'
					});
				}
			} catch (error) {
				console.error('添加收藏失败:', error);
				uni.showToast({
					title: '添加收藏失败',
					icon: 'none'
				});
			}
		},
		
		// 删除收藏
		async removeFavorite(mealId) {
			try {
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/favorites/${mealId}`,
					method: 'DELETE',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					const index = this.favoriteMeals.indexOf(mealId);
					if (index > -1) {
						this.favoriteMeals.splice(index, 1);
					}
					uni.showToast({
						title: '已取消收藏',
						icon: 'success'
					});
				}
			} catch (error) {
				console.error('删除收藏失败:', error);
				uni.showToast({
					title: '删除收藏失败',
					icon: 'none'
				});
			}
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	padding-bottom: 80px;
	background: linear-gradient(180deg, #F8FAFF 0%, #F0F4FF 100%);
}

/* 顶部导航 */
.top-nav {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 20px 24px;
	background: #ffffff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
	min-height: 80px;
}

.nav-left {
	width: 60px;
}

.nav-center {
	flex: 1;
	text-align: left;
	margin-left: 8px;
}

/* 搜索框样式 */
.search-section {
	background: rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(10px);
	padding: 12px 20px;
	box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
}

.search-box {
	position: relative;
}

.search-input {
	width: 100%;
	height: 40px;
	border: 2px solid rgba(99, 102, 241, 0.2);
	border-radius: 20px;
	padding: 0 44px 0 18px;
	font-size: 15px;
	background: rgba(255, 255, 255, 0.8);
	outline: none;
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-input:focus {
	border-color: #6366f1;
	background: #ffffff;
	box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.search-clear {
	position: absolute;
	right: 14px;
	top: 50%;
	transform: translateY(-50%);
	font-size: 14px;
	color: #64748b;
	padding: 6px;
	border-radius: 50%;
	transition: all 0.3s ease;
}

.search-clear:active {
	background: rgba(100, 116, 139, 0.1);
}



.back-btn {
	width: 40px;
	height: 40px;
	border-radius: 50%;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 100;
}

.back-icon {
	font-size: 24px;
	color: #6366f1;
}

.page-title {
	font-size: 24px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
	text-align: left;
}

.elder-selector {
	display: flex;
	align-items: center;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	padding: 8px 16px;
	border-radius: 16px;
	color: #ffffff;
	max-width: 200px;
	white-space: nowrap;
}

.elder-info {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	margin-right: 8px;
	overflow: hidden;
}

.elder-name {
	font-size: 14px;
	font-weight: 500;
	margin-bottom: 2px;
	max-width: 120px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.elder-tag {
	font-size: 12px;
	background: rgba(255, 255, 255, 0.2);
	padding: 2px 8px;
	border-radius: 10px;
	max-width: 120px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.selector-arrow {
	font-size: 12px;
}

/* 餐品分类栏 */
.category-section {
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(10px);
	padding: 12px 0;
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.category-scroll {
	white-space: nowrap;
	padding: 0 20px;
}

.category-item {
	display: inline-block;
	padding: 10px 20px;
	margin-right: 8px;
	background: rgba(99, 102, 241, 0.05);
	border-radius: 18px;
	font-size: 15px;
	color: #64748b;
	font-weight: 500;
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	border: 1px solid rgba(99, 102, 241, 0.1);
}

.category-item.active {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	color: #ffffff;
	box-shadow: 0 6px 24px rgba(99, 102, 241, 0.4);
	border-color: #6366f1;
}

/* 餐品列表 */
.food-section {
	padding: 20px 16px;
}

.food-grid {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 16px;
}

.food-card {
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 255, 0.9) 100%);
		border-radius: 20px;
		padding: 16px;
		box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
		position: relative;
		transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
		border: 1px solid rgba(99, 102, 241, 0.1);
		backdrop-filter: blur(10px);
		overflow: hidden;
	}
	
	.food-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 3px;
		background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
		opacity: 0;
		transition: opacity 0.3s ease;
	}
	
	.food-card:active::before {
		opacity: 1;
	}
	
	.food-header {
		position: relative;
		margin-bottom: 12px;
	}
	
	.favorite-btn {
		position: absolute;
		top: 12px;
		right: 12px;
		width: 36px;
		height: 36px;
		border-radius: 12px;
		background: rgba(255, 255, 255, 0.9);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 20px;
		color: #94a3b8;
		transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
		z-index: 10;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		border: 1px solid rgba(255, 255, 255, 0.3);
	}
	
	.favorite-btn:active {
		transform: scale(0.95);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}
	
	.favorite-btn .favorited {
		color: #ef4444;
		background: linear-gradient(135deg, #ef4444, #dc2626);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		text-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
	}
	
	.food-info {
		margin-bottom: 12px;
	}
	
	.price-action-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 8px;
	}

.food-card:active {
	transform: scale(0.95);
	box-shadow: 0 6px 24px rgba(99, 102, 241, 0.15);
}

.food-image {
	width: 100%;
	height: 120px;
	border-radius: 16px;
	background: linear-gradient(135deg, #f8faff 0%, #e0e7ff 100%);
	margin-bottom: 12px;
	object-fit: cover;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.6);
}

.food-name {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 6px;
	display: block;
	line-height: 1.2;
	letter-spacing: 0.3px;
}

.food-price {
	font-size: 20px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
	margin-bottom: 8px;
	display: block;
	text-shadow: 0 1px 4px rgba(99, 102, 241, 0.2);
}

.nutrition-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 6px;
	margin-bottom: 12px;
}

.nutrition-tag {
	padding: 3px 10px;
	background: rgba(99, 102, 241, 0.1);
	border-radius: 10px;
	border: 1px solid rgba(99, 102, 241, 0.2);
	box-shadow: 0 1px 4px rgba(99, 102, 241, 0.1);
}

.tag-text {
	font-size: 11px;
	color: #6366f1;
	font-weight: 500;
}

.food-actions {
	display: flex;
	align-items: center;
}

.add-btn {
	width: 40px;
	height: 40px;
	border-radius: 50%;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	color: #ffffff;
	font-size: 24px;
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	border: 1px solid rgba(255, 255, 255, 0.3);
}

.add-btn:active {
	transform: scale(0.95);
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.quantity-control {
	display: flex;
	align-items: center;
	gap: 12px;
}

.quantity-btn {
	width: 36px;
	height: 36px;
	border-radius: 50%;
	background: linear-gradient(135deg, #f8faff 0%, #e0e7ff 100%);
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 20px;
	color: #6366f1;
	font-weight: 700;
	border: 1px solid rgba(99, 102, 241, 0.3);
	box-shadow: 0 2px 8px rgba(99, 102, 241, 0.15);
	transition: all 0.3s ease;
}

.quantity-btn:active {
	transform: scale(0.9);
	background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
}

.quantity {
	font-size: 18px;
	font-weight: 700;
	color: #1e293b;
	min-width: 24px;
	text-align: center;
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 底部固定区域 */
.bottom-fixed {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	height: 80px;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 255, 0.98) 100%);
	backdrop-filter: blur(30px);
	border-top: 1px solid rgba(99, 102, 241, 0.2);
	display: flex;
	align-items: center;
	padding: 0 24px;
	box-shadow: 0 -8px 32px rgba(99, 102, 241, 0.15);
}

.cart-info {
	flex: 1;
	display: flex;
	align-items: center;
}

.cart-icon {
	position: relative;
	margin-right: 12px;
}

.cart-symbol {
	font-size: 36px;
	text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cart-badge {
	position: absolute;
	top: -10px;
	right: -10px;
	background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
	color: #ffffff;
	border-radius: 50%;
	min-width: 24px;
	height: 24px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 14px;
	font-weight: 700;
	padding: 0 6px;
	box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
	border: 2px solid rgba(255, 255, 255, 0.9);
}

.badge-text {
	
}

.cart-details {
	
}

.cart-text {
	font-size: 15px;
	color: #64748b;
	display: block;
	font-weight: 500;
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.cart-price {
	font-size: 22px;
	font-weight: 700;
	color: #6366f1;
	display: block;
	text-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.checkout-btn {
	width: 120px;
	height: 52px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 24px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 700;
	box-shadow: 0 12px 32px rgba(99, 102, 241, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
	border: 2px solid rgba(255, 255, 255, 0.3);
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.checkout-btn:active {
	transform: scale(0.9);
	box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3);
}

.checkout-btn:disabled {
	background: linear-gradient(135deg, rgba(203, 213, 225, 0.5) 0%, rgba(148, 163, 184, 0.5) 100%);
	opacity: 0.6;
	cursor: not-allowed;
	border-color: rgba(255, 255, 255, 0.1);
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
	max-height: 85vh;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 255, 0.95) 100%);
	backdrop-filter: blur(30px);
	border-radius: 32px 32px 0 0;
	padding: 24px;
	display: flex;
	flex-direction: column;
	border-top: 1px solid rgba(99, 102, 241, 0.2);
	box-shadow: 0 -8px 32px rgba(99, 102, 241, 0.15);
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
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
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
	font-weight: 700;
	box-shadow: 0 8px 28px rgba(99, 102, 241, 0.5);
	transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
	display: flex;
	align-items: center;
	justify-content: center;
	border: 2px solid rgba(255, 255, 255, 0.3);
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.confirm-btn:active {
	transform: scale(0.9);
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
}

.confirm-btn:disabled {
	background: linear-gradient(135deg, rgba(203, 213, 225, 0.5) 0%, rgba(148, 163, 184, 0.5) 100%);
	opacity: 0.6;
	cursor: not-allowed;
	border-color: rgba(255, 255, 255, 0.1);
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
	max-height: 80vh;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 255, 0.95) 100%);
	border-radius: 28px;
	padding: 28px;
	display: flex;
	flex-direction: column;
	backdrop-filter: blur(30px);
	border: 1px solid rgba(99, 102, 241, 0.2);
	box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
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
	flex: 1;
	overflow-y: auto;
	max-height: calc(80vh - 160px);
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

.elder-item-checkbox {
	width: 24px;
	height: 24px;
	border: 2px solid #e2e8f0;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 16px;
	transition: all 0.3s ease;
}

.elder-item-checkbox.checked {
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border-color: #6366f1;
}

.checkbox-mark {
	color: #ffffff;
	font-size: 14px;
	font-weight: bold;
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

.elder-modal-footer {
	margin-top: 24px;
	padding-top: 24px;
	border-top: 1px solid #f1f5f9;
}

.elder-modal-footer .confirm-btn {
	width: 100%;
	height: 48px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 20px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 500;
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

/* 订单类型选择弹窗 */
.order-type-modal {
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

.order-type-modal-content {
	width: 90%;
	max-width: 400px;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 255, 0.95) 100%);
	border-radius: 28px;
	padding: 28px;
	backdrop-filter: blur(30px);
	border: 1px solid rgba(99, 102, 241, 0.2);
	box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
}

.order-type-modal-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 24px;
}

.order-type-modal-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
}

.order-type-modal-close {
	font-size: 24px;
	color: #64748b;
}

.order-type-options {
	display: flex;
	flex-direction: column;
	gap: 16px;
}

.order-type-btn {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 12px;
	padding: 20px;
	background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 255, 0.8) 100%);
	border: 2px solid rgba(99, 102, 241, 0.2);
	border-radius: 20px;
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	transition: all 0.3s ease;
}

.order-type-btn:active {
	transform: scale(0.95);
	background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
	border-color: #6366f1;
}

.order-type-icon {
	font-size: 24px;
}

/* 时间选择器弹窗 */
.time-picker-modal {
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

.time-picker-modal-content {
	width: 100%;
	max-height: 85vh;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 255, 0.95) 100%);
	border-radius: 32px 32px 0 0;
	padding: 24px;
	display: flex;
	flex-direction: column;
	backdrop-filter: blur(30px);
	border-top: 1px solid rgba(99, 102, 241, 0.2);
	box-shadow: 0 -8px 32px rgba(99, 102, 241, 0.15);
}

.time-picker-modal-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 24px;
}

.time-picker-modal-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
}

.time-picker-modal-close {
	font-size: 24px;
	color: #64748b;
}

.time-picker-content {
	flex: 1;
}

.time-section {
	margin-bottom: 24px;
}

.time-label {
	font-size: 16px;
	font-weight: 600;
	color: #64748b;
	display: block;
	margin-bottom: 12px;
}

.picker-view {
	background: rgba(255, 255, 255, 0.9);
	border: 2px solid rgba(99, 102, 241, 0.2);
	border-radius: 16px;
	padding: 12px 16px;
	font-size: 16px;
	color: #1e293b;
	text-align: center;
}

.time-picker-row {
	display: flex;
	align-items: center;
	gap: 12px;
}

.time-separator {
	font-size: 20px;
	font-weight: 600;
	color: #64748b;
}

.time-picker-footer {
	display: flex;
	gap: 16px;
	margin-top: 24px;
	padding-top: 24px;
	border-top: 1px solid #f1f5f9;
}

.time-picker-footer .cancel-btn {
	flex: 1;
	height: 48px;
	background: rgba(203, 213, 225, 0.3);
	border: none;
	border-radius: 20px;
	color: #64748b;
	font-size: 16px;
	font-weight: 500;
}

.time-picker-footer .confirm-btn {
	flex: 1;
	height: 48px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 20px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 600;
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