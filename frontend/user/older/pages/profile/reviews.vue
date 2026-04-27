<template>
	<view class="reviews-container">
		<!-- 导航栏 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">我的评价</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 评价列表 -->
		<view v-else class="reviews-list">
			<view v-for="(review, index) in reviewsList" :key="review.id" class="review-card">
				<!-- 订单信息 -->
				<view class="order-info">
					<view class="order-header">
						<text class="order-number">订单号: {{ review.order_id }}</text>
						<text class="review-time">{{ formatTime(review.created_at) }}</text>
					</view>
					<view class="food-info">
						<image v-if="review.order?.meal_image" :src="review.order.meal_image" class="food-image" mode="aspectFill"></image>
						<text v-else class="food-emoji">🍱</text>
						<text class="food-name">{{ review.order?.meal_name || '未知餐品' }}</text>
					</view>
				</view>
				
				<!-- 评价内容 -->
				<view class="review-content">
					<view class="rating">
						<text class="star" v-for="i in 5" :key="i" :class="{ 'active': i <= review.rating }">★</text>
					</view>
					<text class="review-text">{{ review.content }}</text>
					
					<!-- 评价图片 -->
					<view v-if="review.images && review.images.length > 0" class="review-images">
						<image 
							v-for="(image, index) in review.images" 
							:key="index" 
							:src="image" 
							class="review-image"
							mode="aspectFill"
						></image>
					</view>
				</view>
				
				<!-- 评价回复 -->
				<view v-if="review.reply" class="review-reply">
					<view class="reply-header">
						<text class="reply-icon">💬</text>
						<text class="reply-title">商家回复</text>
					</view>
					<view class="reply-content">
						<text>{{ review.reply }}</text>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-if="reviewsList.length === 0" class="empty-state">
				<text class="empty-icon">📝</text>
				<text class="empty-text">暂无评价记录</text>
				<text class="empty-hint">完成订单后可以进行评价哦~</text>
			</view>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				reviewsList: [],
				loading: false
			}
		},
		onLoad() {
			this.loadReviews()
		},
		methods: {
			async loadReviews() {
				this.loading = true
				try {
					const result = await api.older.getReviews()
					this.reviewsList = result.reviews || []
				} catch (error) {
					console.error('获取评价列表失败:', error)
					uni.showToast({
						title: '获取评价列表失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			goBack() {
				uni.navigateBack()
			},
			formatTime(timeStr) {
				if (!timeStr) return ''
				const date = new Date(timeStr)
				return date.toLocaleString('zh-CN')
			}
		}
	}
</script>

<style scoped>
	.reviews-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F5F5F5 100%);
		padding-bottom: 40px;
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
	
	/* 评价列表 */
	.reviews-list {
		padding: 20px;
	}
	
	.review-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		margin-bottom: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	/* 订单信息 */
	.order-info {
		border-bottom: 1px solid #F0F0F0;
		padding-bottom: 16px;
		margin-bottom: 16px;
	}
	
	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
	}
	
	.order-number {
		font-size: 14px;
		color: #666666;
	}
	
	.review-time {
		font-size: 14px;
		color: #999999;
	}
	
	.food-info {
		display: flex;
		align-items: center;
	}
	
	.food-image {
		width: 32px;
		height: 32px;
		border-radius: 8px;
		margin-right: 12px;
	}
	
	.food-emoji {
		font-size: 32px;
		margin-right: 12px;
	}
	
	.food-name {
		font-size: 16px;
		font-weight: 500;
		color: #333333;
	}
	
	/* 评价内容 */
	.review-content {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	
	.rating {
		display: flex;
		gap: 4px;
	}
	
	.star {
		font-size: 20px;
		color: #E0E0E0;
	}
	
	.star.active {
		color: #FFD700;
	}
	
	.review-text {
		font-size: 15px;
		color: #666666;
		line-height: 1.5;
		margin-bottom: 12px;
	}
	
	/* 评价图片 */
	.review-images {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		margin-top: 12px;
	}
	
	.review-image {
		width: 60px;
		height: 60px;
		border-radius: 8px;
	}
	
	/* 评价回复 */
	.review-reply {
		margin-top: 16px;
		padding-top: 16px;
		border-top: 1px solid #F0F0F0;
		background: linear-gradient(135deg, rgba(255, 122, 69, 0.05) 0%, rgba(255, 122, 69, 0.02) 100%);
		border-radius: 12px;
		padding: 16px;
	}
	
	.reply-header {
		display: flex;
		align-items: center;
		margin-bottom: 12px;
	}
	
	.reply-icon {
		font-size: 20px;
		margin-right: 8px;
	}
	
	.reply-title {
		font-size: 14px;
		font-weight: 600;
		color: #FF7A45;
	}
	
	.reply-content {
		font-size: 15px !important;
		color: #555555 !important;
		line-height: 1.6 !important;
		background-color: #FFFFFF !important;
		padding: 16px !important;
		border-radius: 8px !important;
		border: 1px solid rgba(255, 122, 69, 0.1) !important;
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
	
	/* 空状态 */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60px 20px;
		text-align: center;
	}
	
	.empty-icon {
		font-size: 64px;
		margin-bottom: 16px;
	}
	
	.empty-text {
		font-size: 16px;
		color: #666666;
		margin-bottom: 8px;
	}
	
	.empty-hint {
		font-size: 14px;
		color: #999999;
	}
</style>