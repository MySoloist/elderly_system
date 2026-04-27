<template>
	<view class="favorite-container">
		<!-- 顶部导航 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">我的收藏</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 收藏餐品列表区域 -->
		<view class="favorite-list">
			<view v-if="favoriteFoods.length === 0" class="empty-state">
				<text class="empty-icon">❤️</text>
				<text class="empty-text">暂无收藏餐品</text>
				<button class="btn-primary mt-16" @click="goToIndex">去浏览</button>
			</view>
			
			<view class="food-grid">
				<view 
					v-for="food in favoriteFoods" 
					:key="food.id"
					class="food-card"
					@click="goToFoodDetail(food.id)"
				>
					<image 
						v-if="food.image_url" 
						:src="food.image_url" 
						class="food-image" 
						mode="aspectFill"
					/>
					<view v-else class="food-emoji">🍽️</view>
					<text class="favorite-btn active">❤️</text>
					<text class="food-name">{{ food.name }}</text>
					<text class="food-price">¥{{ food.price }}</text>

					<view class="food-actions">
						<button class="cancel-btn" @click.stop="cancelFavorite(food)">取消收藏</button>
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
				favoriteFoods: [],
				loading: false
			}
		},
		onLoad() {
			this.loadFavoriteFoods()
		},
		methods: {
			goBack() {
				uni.navigateBack()
			},
			goToIndex() {
				uni.switchTab({
					url: '/pages/index/index'
				})
			},
			getTagClass(tag) {
				const tagMap = {
					'适合高血压': 'tag-warning',
					'清淡口味': 'tag-primary',
					'易消化': 'tag-success',
					'暖胃': 'tag-warning',
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
			async loadFavoriteFoods() {
				this.loading = true
				try {
					const response = await api.older.getFavorites()
					this.favoriteFoods = response.items.map(item => ({
						id: item.meal.id,
						name: item.meal.name,
						price: item.meal.price,
						image_url: item.meal.image_url,
						tags: []
					}))
				} catch (error) {
					console.error('获取收藏列表失败:', error)
					uni.showToast({
						title: '获取收藏失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			async cancelFavorite(food) {
				uni.showModal({
					title: '取消收藏',
					content: `确定要取消收藏 ${food.name} 吗？`,
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.older.removeFavorite(food.id)
								const index = this.favoriteFoods.findIndex(item => item.id === food.id)
								if (index !== -1) {
									this.favoriteFoods.splice(index, 1)
								}
								uni.showToast({
									title: '已取消收藏',
									icon: 'success'
								})
							} catch (error) {
								console.error('取消收藏失败:', error)
								uni.showToast({
									title: '取消收藏失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			async quickOrder(food) {
				try {
					await api.older.createOrder({
						items: [
							{
								meal_id: food.id,
								quantity: 1
							}
						],
						delivery_address: '默认地址'
					})
					uni.showToast({
						title: `点餐成功`,
						icon: 'success'
					})
					// 跳转到订单页面
					uni.navigateTo({
						url: '/pages/order/order'
					})
				} catch (error) {
					console.error('点餐失败:', error)
					uni.showToast({
						title: '点餐失败',
						icon: 'none'
					})
				}
			},
			goToFoodDetail(foodId) {
				uni.navigateTo({
					url: `/pages/food/detail?id=${foodId}`
				})
			}
		}
	}
</script>

<style scoped>
	.favorite-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 200px, #F5F5F5 100%);
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
	
	.placeholder {
		width: 24px;
	}
	
	/* 收藏列表 */
	.favorite-list {
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
		font-size: 16px;
		color: #999999;
		margin-bottom: 24px;
	}
	
	/* 餐品网格 */
	.food-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 16px;
	}
	
	/* 餐品卡片 */
	.food-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
		position: relative;
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.food-image {
		width: 100%;
		height: 80px;
		border-radius: 12px;
		margin-bottom: 12px;
		object-fit: cover;
	}
	
	.food-emoji {
		font-size: 48px;
		text-align: center;
		display: block;
		margin-bottom: 12px;
	}
	
	.favorite-btn {
		position: absolute;
		top: 16px;
		right: 16px;
		font-size: 24px;
		background: rgba(255, 255, 255, 0.92);
		border-radius: 14px;
		padding: 4px 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}
	
	.favorite-btn.active {
		color: #FF4757;
	}
	
	.food-name {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 8px;
		line-height: 1.4;
		text-align: center;
	}
	
	.food-price {
		font-size: 20px;
		font-weight: 600;
		color: #FF7A45;
		display: block;
		margin-bottom: 16px;
		text-align: center;
	}
	
	.food-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		justify-content: center;
		margin-bottom: 16px;
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
	
	/* 餐品操作按钮 */
	.food-actions {
		display: flex;
		gap: 8px;
	}
	
	.cancel-btn {
		width: 100%;
		height: 36px;
		background-color: #F5F5F5;
		color: #666666;
		border: 1px solid #DDDDDD;
		border-radius: 12px;
		font-size: 14px;
		font-weight: 600;
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
</style>