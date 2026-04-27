<template>
	<view class="reviews-container">
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<text class="loading-icon">⏳</text>
			<text class="loading-text">加载中...</text>
		</view>
		
		<view v-else>
			<!-- 评分统计卡片 -->
			<view class="stats-card">
				<view class="stats-header">
					<text class="stats-title">我的评分</text>
				</view>
				<view class="stats-content">
					<view class="average-rating">
						<text class="rating-number">{{ averageRating }}</text>
						<text class="rating-unit">分</text>
					</view>
					<view class="rating-stars">
						<text class="star-icon" v-for="i in 5" :key="i" :class="{ active: i <= averageRating }">★</text>
					</view>
					<text class="rating-count">{{ totalReviews }}条评价</text>
				</view>
				<view class="stats-details">
					<view class="stat-item" v-for="stat in ratingStats" :key="stat.rating">
						<text class="stat-rating">{{ stat.rating }}星</text>
						<view class="stat-bar">
							<view class="stat-progress" :style="{ width: stat.percentage + '%' }"></view>
						</view>
						<text class="stat-count">{{ stat.count }}</text>
					</view>
				</view>
			</view>
			
			<!-- 评价列表 -->
			<view class="reviews-list">
				<view class="reviews-header">
					<text class="reviews-title">评价详情</text>
				</view>
				
				<view v-if="reviews.length > 0">
					<view class="review-item" v-for="(review, index) in reviews" :key="index">
						<view class="review-header">
							<view class="review-info">
								<text class="review-name">{{ review.reviewerName }}</text>
								<text class="review-time">{{ review.createdAt }}</text>
							</view>
							<view class="review-rating">
								<text class="star-icon" v-for="i in 5" :key="i" :class="{ active: i <= review.rating }">★</text>
							</view>
						</view>
						<text class="review-content">{{ review.content }}</text>
						<view class="review-images" v-if="review.images && review.images.length > 0">
							<image class="review-image" v-for="(image, imgIndex) in review.images" :key="imgIndex" :src="image" mode="aspectFill"></image>
						</view>
						<view class="review-reply" v-if="review.reply">
							<text class="reply-label">回复：</text>
							<text class="reply-content">{{ review.reply }}</text>
						</view>
					</view>
				</view>
				
				<!-- 空状态 -->
				<view v-else class="empty-state">
					<text class="empty-icon">⭐</text>
					<text class="empty-text">暂无评价</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js';
	
	export default {
		data() {
			return {
				loading: false,
				averageRating: 0,
				totalReviews: 0,
				ratingStats: [
					{ rating: 5, count: 0, percentage: 0 },
					{ rating: 4, count: 0, percentage: 0 },
					{ rating: 3, count: 0, percentage: 0 },
					{ rating: 2, count: 0, percentage: 0 },
					{ rating: 1, count: 0, percentage: 0 }
				],
				reviews: []
			};
		},
		onLoad() {
			this.loadReviews();
		},
		methods: {
			async loadReviews() {
				this.loading = true;
				try {
					const data = await api.reviews.getReviews();
					
					this.averageRating = data.average_rating;
					this.totalReviews = data.total_reviews;
					this.ratingStats = data.rating_stats;
					this.reviews = data.reviews.map(review => ({
						reviewerName: review.reviewer_name,
						createdAt: review.created_at,
						rating: review.rating,
						content: review.content,
						images: review.images,
						reply: review.reply
					}));
				} catch (error) {
					console.error('加载评价失败:', error);
					uni.showToast({
						title: '加载失败',
						icon: 'none'
					});
				} finally {
					this.loading = false;
				}
			}
		}
	};
</script>

<style scoped>
	.reviews-container {
		min-height: 100vh;
		background-color: #f8fafc;
	}
	
	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 100rpx 0;
	}
	
	.loading-icon {
		font-size: 120rpx;
		margin-bottom: 20rpx;
	}
	
	.loading-text {
		font-size: 32rpx;
		color: #64748b;
	}
	
	.stats-card {
		background-color: white;
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 40rpx;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
	}
	
	.stats-header {
		text-align: center;
		margin-bottom: 30rpx;
	}
	
	.stats-title {
		font-size: 36rpx;
		font-weight: 600;
		color: #1e293b;
	}
	
	.stats-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 40rpx;
	}
	
	.average-rating {
		display: flex;
		align-items: baseline;
		margin-bottom: 20rpx;
	}
	
	.rating-number {
		font-size: 80rpx;
		font-weight: 700;
		color: #10b981;
	}
	
	.rating-unit {
		font-size: 32rpx;
		color: #64748b;
		margin-left: 10rpx;
	}
	
	.rating-stars {
		display: flex;
		margin-bottom: 10rpx;
	}
	
	.star-icon {
		font-size: 32rpx;
		color: #e5e7eb;
		margin: 0 4rpx;
	}
	
	.star-icon.active {
		color: #f59e0b;
	}
	
	.rating-count {
		font-size: 28rpx;
		color: #64748b;
	}
	
	.stats-details {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}
	
	.stat-item {
		display: flex;
		align-items: center;
		gap: 20rpx;
	}
	
	.stat-rating {
		width: 80rpx;
		font-size: 28rpx;
		color: #64748b;
	}
	
	.stat-bar {
		flex: 1;
		height: 12rpx;
		background-color: #e5e7eb;
		border-radius: 6rpx;
		overflow: hidden;
	}
	
	.stat-progress {
		height: 100%;
		background-color: #10b981;
		border-radius: 6rpx;
	}
	
	.stat-count {
		width: 60rpx;
		font-size: 28rpx;
		color: #64748b;
		text-align: right;
	}
	
	.reviews-list {
		background-color: white;
		margin: 20rpx;
		border-radius: 20rpx;
		padding: 30rpx;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
	}
	
	.reviews-header {
		margin-bottom: 30rpx;
	}
	
	.reviews-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #1e293b;
	}
	
	.review-item {
		padding: 30rpx 0;
		border-bottom: 1rpx solid #f1f5f9;
	}
	
	.review-item:last-child {
		border-bottom: none;
	}
	
	.review-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
	}
	
	.review-info {
		display: flex;
		flex-direction: column;
	}
	
	.review-name {
		font-size: 30rpx;
		font-weight: 500;
		color: #1e293b;
		margin-bottom: 8rpx;
	}
	
	.review-time {
		font-size: 24rpx;
		color: #94a3b8;
	}
	
	.review-content {
		font-size: 28rpx;
		color: #475569;
		line-height: 1.6;
		margin-bottom: 20rpx;
	}
	
	.review-images {
		display: flex;
		gap: 20rpx;
		margin-bottom: 20rpx;
	}
	
	.review-image {
		width: 120rpx;
		height: 120rpx;
		border-radius: 12rpx;
	}
	
	.review-reply {
		background-color: #f8fafc;
		padding: 20rpx;
		border-radius: 12rpx;
		display: flex;
		gap: 10rpx;
	}
	
	.reply-label {
		font-size: 26rpx;
		color: #64748b;
		font-weight: 500;
	}
	
	.reply-content {
		flex: 1;
		font-size: 26rpx;
		color: #475569;
		line-height: 1.5;
	}
	
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60rpx 0;
	}
	
	.empty-icon {
		font-size: 100rpx;
		margin-bottom: 20rpx;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #94a3b8;
	}
</style>