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
					const response = await uni.request({
						url: 'http://127.0.0.1:7678/api/v1/member/reviews',
						method: 'GET',
						header: {
							'Authorization': `Bearer ${uni.getStorageSync('token')}`
						}
					})
					
					if (response.statusCode === 200) {
						this.reviewsList = response.data.reviews || []
					} else {
						throw new Error(response.data?.detail || '获取评价列表失败')
					}
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
		background: #f8fafc;
		padding-bottom: 40px;
	}
	
	/* 导航栏 */
	.nav-bar {
		display: flex;
		align-items: center;
		padding: 44px 20px 12px;
		background: #ffffff;
		position: sticky;
		top: 0;
		z-index: 100;
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
	}
	
	.back-btn {
		width: 36px;
		height: 36px;
		border-radius: 10px;
		background: #f1f5f9;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 12px;
		transition: all 0.2s ease;
		font-size: 20px;
		color: #1e293b;
		font-weight: 600;
	}
	.back-btn:active {
		transform: scale(0.9);
		background: #e2e8f0;
	}
	
	.nav-title {
		flex: 1;
		font-size: 18px;
		font-weight: 600;
		color: #1e293b;
		text-align: center;
	}
	
	.placeholder {
		width: 36px;
	}
	
	/* 评价列表 */
	.reviews-list {
		padding: 16px;
	}
	
	.review-card {
		background-color: #FFFFFF;
		border-radius: 16px;
		padding: 16px;
		margin-bottom: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
		border: 1px solid rgba(226, 232, 240, 0.5);
	}
	
	/* 订单信息 */
	.order-info {
		border-bottom: 1px solid rgba(226, 232, 240, 0.5);
		padding-bottom: 12px;
		margin-bottom: 12px;
	}
	
	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
	}
	
	.order-number {
		font-size: 14px;
		color: #64748b;
	}
	
	.review-time {
		font-size: 14px;
		color: #94a3b8;
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
		color: #1e293b;
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
		color: #cbd5e1;
	}
	
	.star.active {
		color: #f59e0b;
	}
	
	.review-text {
		font-size: 15px;
		color: #475569;
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
		border-top: 1px solid #f1f5f9;
		background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(99, 102, 241, 0.02) 100%);
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
		color: #6366f1;
	}
	
	.reply-content {
		font-size: 15px;
		color: #475569;
		line-height: 1.6;
		background-color: #FFFFFF;
		padding: 16px;
		border-radius: 8px;
		border: 1px solid rgba(99, 102, 241, 0.1);
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
		border: 4px solid #6366f1;
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
		color: #64748b;
	}
	
	/* 空状态 */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 80px 20px;
		text-align: center;
	}
	
	.empty-icon {
		font-size: 80px;
		margin-bottom: 24px;
	}
	
	.empty-text {
		font-size: 16px;
		color: #64748b;
		margin-bottom: 8px;
	}
	
	.empty-hint {
		font-size: 14px;
		color: #94a3b8;
	}
</style>