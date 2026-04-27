<template>
	<view class="food-detail-container">
		<!-- 顶部导航 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">餐品详情</text>
			<text class="favorite-btn" :class="{ active: isFavorite }" @click="addToCart">
				{{ isFavorite ? '❤️' : '🤍' }}
			</text>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 餐品展示区 -->
		<view v-else-if="foodDetail.id" class="food-showcase">
			<image :src="foodDetail.image_url || '/static/logo.png'" class="food-image" mode="aspectFill"></image>
			<view class="food-info">
				<text class="food-name">{{ foodDetail.name }}</text>
				<text class="food-price">¥{{ foodDetail.price }}</text>
			</view>
		</view>
		
		<!-- 详情信息区 -->
		<view v-if="foodDetail.id" class="detail-section">
			<view class="detail-card">
				<view class="detail-header">
					<text class="detail-title">餐品描述</text>
				</view>
				<text class="food-description">{{ foodDetail.description || '暂无描述' }}</text>
			</view>
			
			<view class="detail-card">
				<view class="detail-header">
					<text class="detail-title">营养成分</text>
				</view>
				<view class="nutrition-tags">
					<text 
						v-for="tag in foodDetail.tags" 
						:key="tag"
						class="tag"
						:class="getTagClass(tag)"
					>{{ tag }}</text>
				</view>
			</view>
			
			
		</view>
		
		<!-- 底部固定操作区 -->
		<view v-if="foodDetail.id" class="bottom-actions">
			<view class="quantity-control">
				<text class="quantity-btn" @click="decreaseQuantity">-</text>
				<text class="quantity-text">{{ quantity }}</text>
				<text class="quantity-btn" @click="increaseQuantity">+</text>
			</view>
			<button class="buy-btn" @click="buyNow">立即购买</button>
		</view>
		
		<!-- 日期时间选择器弹窗 -->
		<view v-if="showTimePicker" class="time-picker-overlay">
			<view class="time-picker-container">
				<view class="time-picker-header">
					<text class="time-picker-title">选择配送时间</text>
				</view>
				<view class="time-picker-content">
					<view class="time-picker-row">
						<text class="time-label">日期:</text>
						<picker mode="date" :value="selectedDate ? selectedDate.toISOString().split('T')[0] : ''" @change="(e) => selectedDate = new Date(e.detail.value)">
							<view class="picker-display">{{ selectedDate ? selectedDate.toLocaleDateString('zh-CN') : '选择日期' }}</view>
						</picker>
					</view>
					<view class="time-picker-row">
						<text class="time-label">小时:</text>
						<picker :value="selectedHour - 8" :range="hours" @change="(e) => selectedHour = hours[e.detail.value]">
							<view class="picker-display">{{ selectedHour }}时</view>
						</picker>
					</view>
					<view class="time-picker-row">
						<text class="time-label">分钟:</text>
						<picker :value="selectedMinute === 0 ? 0 : 1" :range="minutes" @change="(e) => selectedMinute = parseInt(minutes[e.detail.value])">
							<view class="picker-display">{{ selectedMinute.toString().padStart(2, '0') }}分</view>
						</picker>
					</view>
				</view>
				<view class="time-picker-footer">
					<button class="cancel-btn" @click="cancelTimeSelection">取消</button>
					<button class="confirm-btn" @click="confirmTimeSelection">确认</button>
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
				foodDetail: {},
				quantity: 1,
				loading: false,
				isFavorite: false,
				// 时间选择器相关
				showTimePicker: false,
				selectedDate: null,
				selectedHour: 12,
				selectedMinute: 0,
				hours: Array.from({length: 13}, (_, i) => i + 8), // 8:00-20:00
				minutes: Array.from({length: 60}, (_, i) => i.toString().padStart(2, '0')) // 显示所有分钟
			}
		},
		onLoad(options) {
			// 获取餐品ID
			const foodId = options.id
			if (foodId) {
				// 根据ID获取餐品详情
				this.loadFoodDetail(foodId)
			}
		},
		methods: {
			async loadFoodDetail(foodId) {
			this.loading = true
			try {
				console.log('开始获取餐品详情，ID:', foodId)
				const mealDetail = await api.older.getMeals({ id: foodId })
				console.log('获取到的餐品数据:', mealDetail)
				console.log('餐品数据类型:', typeof mealDetail)
				console.log('餐品数据是否有items属性:', 'items' in mealDetail)
				if (mealDetail && mealDetail.items && mealDetail.items.length > 0) {
					// 根据ID过滤出对应餐品
					const selectedMeal = mealDetail.items.find(item => item.id == foodId)
					if (selectedMeal) {
						this.foodDetail = selectedMeal
						console.log('根据ID过滤后的餐品详情:', this.foodDetail)
						console.log('是否有 special_tag 字段:', 'special_tag' in this.foodDetail)
						console.log('special_tag 值:', this.foodDetail.special_tag)
						// 处理 special_tag 字段，转换为 tags 数组
						if (this.foodDetail.special_tag) {
							this.foodDetail.tags = this.foodDetail.special_tag.split(',')
							console.log('转换后的 tags 数组:', this.foodDetail.tags)
						} else {
							this.foodDetail.tags = []
							console.log('没有 special_tag 字段，设置空 tags 数组')
						}
						// 设置适合人群信息
						if (!this.foodDetail.suitable_people) {
							// 根据 special_tag 生成适合人群信息
							if (this.foodDetail.tags.length > 0) {
								this.foodDetail.suitable_people = '适合需要' + this.foodDetail.tags.join('、') + '的人群'
							} else {
								this.foodDetail.suitable_people = '一般人群'
							}
							console.log('生成的适合人群信息:', this.foodDetail.suitable_people)
						}
						console.log('设置的餐品详情:', this.foodDetail)
					} else {
						console.error('未找到ID为', foodId, '的餐品')
						this.foodDetail = {
							tags: [],
							suitable_people: '一般人群'
						}
						uni.showToast({
							title: '餐品信息不存在',
							icon: 'none'
						})
					}
				} else {
					console.error('餐品数据结构不正确:', mealDetail)
					this.foodDetail = {
						tags: [],
						suitable_people: '一般人群'
					}
					uni.showToast({
						title: '餐品信息不存在',
						icon: 'none'
					})
				}
				// 获取收藏状态
				this.checkFavoriteStatus(foodId)
			} catch (error) {
				console.error('获取餐品详情失败:', error)
				uni.showToast({
					title: '获取餐品详情失败',
					icon: 'none'
				})
			} finally {
				this.loading = false
			}
		},
			async checkFavoriteStatus(foodId) {
				try {
					const favorites = await api.older.getFavorites()
					console.log('获取到的收藏数据:', favorites)
					const favoriteItems = favorites.items || favorites
					this.isFavorite = favoriteItems.some(fav => {
						// 检查 fav.meal.id 或 fav.id
						if (fav.meal && fav.meal.id) {
							return fav.meal.id === parseInt(foodId)
						} else {
							return fav.id === parseInt(foodId)
						}
					})
					console.log('收藏状态:', this.isFavorite)
				} catch (error) {
					console.error('获取收藏状态失败:', error)
				}
			},
			goBack() {
				uni.navigateBack()
			},
			handleShare() {
				uni.showToast({
					title: '分享功能开发中...',
					icon: 'none'
				})
			},
			getTagClass(tag) {
				const tagMap = {
					'适合高血压': 'tag-warning',
					'清淡口味': 'tag-primary',
					'易消化': 'tag-success',
					'营养均衡': 'tag-success',
					'高蛋白': 'tag-success',
					'低盐': 'tag-primary',
					'低脂': 'tag-success',
					'高纤维': 'tag-primary',
					'软食': 'tag-warning',
					'清淡': 'tag-primary',
					'营养': 'tag-success'
				}
				return tagMap[tag] || 'tag-primary'
			},
			decreaseQuantity() {
				if (this.quantity > 1) {
					this.quantity--
				}
			},
			increaseQuantity() {
				this.quantity++
			},
			async addToCart() {
				// 加入购物车功能（这里实现为收藏）
				try {
					if (this.isFavorite) {
						await api.older.removeFavorite(this.foodDetail.id)
						this.isFavorite = false
						uni.showToast({
							title: '已取消收藏',
							icon: 'success'
						})
					} else {
						await api.older.addFavorite(this.foodDetail.id)
						this.isFavorite = true
						uni.showToast({
							title: '已添加到收藏',
							icon: 'success'
						})
					}
				} catch (error) {
					console.error('操作失败:', error)
					uni.showToast({
						title: '操作失败',
						icon: 'none'
					})
				}
			},
			async buyNow() {
				try {
					console.log('开始下单流程')
					// 显示下单方式选择框
					uni.showActionSheet({
						itemList: ['现在下单', '预定下单'],
						success: async (res) => {
							console.log('用户选择:', res.tapIndex)
							if (res.tapIndex === 0) {
								// 现在下单
								console.log('用户选择现在下单')
								await this.createOrder('immediate', null)
							} else {
								// 预定下单，直接显示自定义日期时间选择器
								console.log('用户选择预定下单')
								this.selectedDate = new Date()
								this.showTimePicker = true
							}
						},
						fail: (err) => {
							console.error('showActionSheet失败:', err)
						}
					})
				} catch (error) {
					console.error('点餐失败:', error)
					uni.showToast({
						title: '点餐失败，请重试',
						icon: 'none'
					})
				}
			},
			async createOrder(orderType, scheduledTime) {
				try {
					const orderData = {
						items: [{
							meal_id: this.foodDetail.id,
							quantity: this.quantity
						}],
						delivery_address: '幸福小区3号楼2单元501室',
						special_notes: '',
						order_type: orderType
					}
					
					// 如果是预定订单，添加预定时间
					if (orderType === 'scheduled' && scheduledTime) {
						orderData.scheduled_time = scheduledTime
					}
					
					await api.older.createOrder(orderData)
					
					const message = orderType === 'immediate' 
						? '点餐成功'
						: '预定成功'
					
					uni.showToast({
						title: message,
						icon: 'success'
					})
					// 跳转到订单页面并强制刷新
					setTimeout(() => {
						uni.navigateTo({
							url: '/pages/order/order',
							success: () => {
								// 跳转成功后，通知订单页面刷新数据
								uni.$emit('refreshOrderList')
							}
						})
					}, 1500)
				} catch (error) {
					console.error('点餐失败:', error)
					uni.showToast({
						title: '点餐失败',
						icon: 'none'
					})
				}
			},
			confirmTimeSelection() {
				console.log('确认时间选择:', this.selectedHour, this.selectedMinute)
				
				if (this.selectedDate) {
					const scheduledDate = new Date(this.selectedDate)
					scheduledDate.setHours(this.selectedHour, this.selectedMinute, 0, 0)
					const scheduledTime = scheduledDate.toISOString()
					console.log('最终预定时间:', scheduledTime)
					
					this.createOrder('scheduled', scheduledTime)
					this.showTimePicker = false
				}
			},
			cancelTimeSelection() {
				console.log('取消时间选择')
				this.showTimePicker = false
			}
		}
	}
</script>

<style scoped>
	.food-detail-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 200px, #F5F5F5 100%);
		padding-bottom: 80px;
	}
	
	/* 导航栏 */
	.nav-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 56px;
		padding: 0 20px;
		background: rgba(255, 255, 255, 0.95);
		border-bottom: 1px solid rgba(255, 122, 69, 0.1);
	}
	
	.back-btn {
		font-size: 22px;
		color: #FF7A45;
		width: 34px;
		height: 34px;
		line-height: 34px;
		text-align: center;
		background: rgba(255, 122, 69, 0.1);
		border-radius: 17px;
	}
	
	.nav-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
	}
	
	.favorite-btn {
		font-size: 24px;
		width: 34px;
		height: 34px;
		line-height: 34px;
		text-align: center;
		background: rgba(255, 71, 87, 0.1);
		border-radius: 17px;
	}
	
	.favorite-btn.active {
		color: #FF4757;
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
	
	/* 餐品展示区 */
	.food-showcase {
		background-color: #FFFFFF;
		padding: 16px 20px 20px;
		margin: 12px 20px 0;
		border-radius: 20px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.food-image {
		width: 100%;
		height: 220px;
		border-radius: 14px;
		margin-bottom: 16px;
		box-shadow: 0 8px 18px rgba(0, 0, 0, 0.1);
	}
	
	.food-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.food-name {
		font-size: 22px;
		font-weight: 600;
		color: #333333;
		flex: 1;
	}
	
	.food-price {
		font-size: 26px;
		font-weight: 600;
		color: #FF7A45;
		text-shadow: 0 1px 2px rgba(255, 122, 69, 0.2);
	}
	
	/* 详情信息区 */
	.detail-section {
		padding: 20px;
	}
	
	.detail-card {
		background-color: #FFFFFF;
		border-radius: 16px;
		padding: 20px;
		margin-bottom: 16px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.detail-header {
		margin-bottom: 12px;
		padding-bottom: 8px;
		border-bottom: 1px solid #F0F0F0;
	}
	
	.detail-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
	}
	
	.food-description {
		font-size: 16px;
		color: #666666;
		line-height: 1.6;
	}
	
	.nutrition-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	
	.tag {
		padding: 4px 12px;
		border-radius: 12px;
		font-size: 12px;
		font-weight: 500;
	}
	
	.tag-primary {
		background-color: #E8F5E9;
		color: #2E7D32;
	}
	
	.tag-success {
		background-color: #E3F2FD;
		color: #1565C0;
	}
	
	.tag-warning {
		background-color: #FFF3CD;
		color: #856404;
	}
	
	.suitable-people {
		font-size: 16px;
		color: #666666;
		line-height: 1.6;
	}
	
	/* 底部固定操作区 */
	.bottom-actions {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		height: 72px;
		background-color: rgba(255, 255, 255, 0.96);
		display: flex;
		align-items: center;
		padding: 0 20px;
		border-top: 1px solid rgba(255, 122, 69, 0.1);
		box-shadow: 0 -6px 20px rgba(0, 0, 0, 0.05);
	}
	
	.quantity-control {
		display: flex;
		align-items: center;
		background-color: #F8F8F8;
		border-radius: 24px;
		padding: 0 12px;
		margin-right: 12px;
		border: 1px solid #ededed;
	}
	
	.quantity-btn {
		font-size: 22px;
		color: #FF7A45;
		padding: 8px;
	}
	
	.quantity-text {
		font-size: 16px;
		color: #333333;
		padding: 0 12px;
		min-width: 40px;
		text-align: center;
	}
	
	.buy-btn {
		flex: 1;
		height: 42px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border: none;
		border-radius: 21px;
		font-size: 16px;
		font-weight: 600;
		box-shadow: 0 8px 16px rgba(255, 122, 69, 0.32);
	}
	
	/* 时间选择器样式 */
	.time-picker-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 9999;
	}
	
	.time-picker-container {
		background-color: white;
		border-radius: 12px;
		width: 80%;
		max-width: 300px;
		padding: 20px;
	}
	
	.time-picker-header {
		text-align: center;
		padding-bottom: 20px;
		border-bottom: 1px solid #f0f0f0;
	}
	
	.time-picker-title {
		font-size: 18px;
		font-weight: bold;
		color: #333;
	}
	
	.time-picker-content {
		padding: 20px 0;
	}
	
	.time-picker-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 20px;
	}
	
	.time-label {
		font-size: 16px;
		color: #666;
		width: 60px;
	}
	
	.picker-display {
		flex: 1;
		text-align: center;
		padding: 10px;
		background-color: #f5f5f5;
		border-radius: 8px;
		font-size: 16px;
		color: #333;
		border: 1px solid #e0e0e0;
	}
	
	.time-picker-footer {
		display: flex;
		justify-content: space-between;
		border-top: 1px solid #f0f0f0;
		padding-top: 20px;
	}
	
	.time-picker-footer .cancel-btn {
		flex: 1;
		margin-right: 10px;
		background-color: #f5f5f5;
		color: #666;
		border: none;
		border-radius: 8px;
		padding: 12px;
		font-size: 16px;
	}
	
	.time-picker-footer .confirm-btn {
		flex: 1;
		margin-left: 10px;
		background-color: #4CAF50;
		color: white;
		border: none;
		border-radius: 8px;
		padding: 12px;
		font-size: 16px;
	}
</style>