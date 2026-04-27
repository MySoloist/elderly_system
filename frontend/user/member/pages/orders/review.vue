<template>
	<view class="review-container">
		<!-- 顶部导航 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">订单评价</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 订单信息区域 -->
		<view v-else-if="orderInfo.id" class="order-info-card">
			<text class="order-id">订单号: {{ orderInfo.id }}</text>
			<view class="order-items">
				<view v-for="item in orderInfo.items" :key="item.id" class="order-item">
					<image v-if="item.image" :src="item.image" class="item-image" mode="aspectFit"></image>
					<view v-else class="item-image"></view>
					<view class="item-info">
						<text class="item-name">{{ item.name }}</text>
						<text class="item-price">¥{{ item.price }}</text>
						<text class="item-quantity">x{{ item.quantity }}</text>
					</view>
				</view>
			</view>
			<view class="order-summary">
				<text class="order-time">{{ orderInfo.time }}</text>
				<text class="order-total">合计: ¥{{ orderInfo.total }}</text>
			</view>
		</view>
		
		<!-- 评价类型选择 -->
		<view class="review-section">
			<text class="section-title">评价类型</text>
			<view class="review-type-selector">
				<view class="review-type-option" :class="{ active: reviewType === 'meal' }" @click="reviewType = 'meal'">
					<text class="review-type-name">餐品评价</text>
					<text class="review-type-desc">评价餐品的味道和质量</text>
				</view>
				<view class="review-type-option" :class="{ active: reviewType === 'deliverer' }" @click="reviewType = 'deliverer'">
					<text class="review-type-name">配送员评价</text>
					<text class="review-type-desc">评价配送员的服务和态度</text>
				</view>
			</view>
			
			<!-- 配送员信息 -->
			<view v-if="reviewType === 'deliverer' && delivererInfo.name" class="deliverer-info">
				<text class="deliverer-label">配送员：</text>
				<text class="deliverer-name">{{ delivererInfo.name }}</text>
				<text v-if="delivererInfo.phone" class="deliverer-phone">{{ delivererInfo.phone }}</text>
			</view>
		</view>
		
		<!-- 评分区域 -->
		<view class="review-section">
			<text class="section-title">评分</text>
			<view class="star-rating">
				<text 
					v-for="star in 5" 
					:key="star"
					class="star"
					:class="{ active: star <= rating }"
					@click="rating = star"
				>{{ star <= rating ? '★' : '☆' }}</text>
			</view>
			<text class="rating-desc">点击星星进行评分</text>
		</view>
		
		<!-- 评价内容区域 -->
		<view class="review-section">
			<text class="section-title">评价内容</text>
			<textarea 
				class="review-input" 
				placeholder="请输入您的评价..." 
				v-model="reviewContent"
				maxlength="200"
			></textarea>
			<text class="char-count">{{ reviewContent.length }}/200</text>
		</view>
		
		<!-- 快捷评价标签 -->
		<view class="review-section">
			<text class="section-title">快捷评价</text>
			<view class="quick-tags">
				<text 
					v-for="tag in quickTags" 
					:key="tag"
					class="quick-tag"
					:class="{ active: selectedTags.includes(tag) }"
					@click="toggleTag(tag)"
				>{{ tag }}</text>
			</view>
		</view>
		
		<!-- 图片上传区域 -->
		<view class="review-section">
			<text class="section-title">上传图片</text>
			<view class="image-upload-area">
				<view class="image-list">
					<view v-for="(image, index) in images" :key="index" class="image-item">
						<image :src="image" class="uploaded-image" mode="aspectFill"></image>
						<view class="image-delete" @click="deleteImage(index)">×</view>
					</view>
					<view v-if="images.length< 9" class="image-upload-btn" @click="chooseImage">
						<text class="upload-icon">+</text>
						<text class="upload-text">添加图片</text>
					</view>
				</view>
				<text class="image-hint">最多上传9张图片</text>
			</view>
		</view>
		
		<!-- 提交按钮 -->
		<view class="submit-section">
			<button class="btn-cancel" @click="goBack">取消</button>
			<button class="btn-submit" @click="submitReview" :disabled="rating === 0">提交评价</button>
		</view>
	</view>
</template>

<script>
	import apiClient from '../../api/axios.js'
	
	export default {
		data() {
			return {
				orderId: '',
				elderId: '',
				orderInfo: {
					id: '',
					time: '',
					total: 0,
					items: []
				},
				rating: 0,
				reviewContent: '',
				selectedTags: [],
				loading: false,
				images: [],
				quickTags: [
					'非常满意',
					'味道很好',
					'配送及时',
					'包装完好',
					'营养均衡',
					'服务周到'
				],
				reviewType: 'meal', // meal: 餐品评价, deliverer: 配送员评价
				delivererInfo: {
					name: '',
					phone: '',
					id: ''
				}
			}
		},
		onLoad(options) {
			// 获取订单ID和老人ID
			this.orderId = options.id
			this.elderId = options.elderId
			if (this.orderId && this.elderId) {
				// 根据ID获取订单信息
				this.loadOrderInfo(this.orderId)
			}
		},
		methods: {
			async loadOrderInfo(orderId) {
				this.loading = true
				try {
					const response = await uni.request({
						url: `http://127.0.0.1:7678/api/v1/member/orders/${orderId}`,
						method: 'GET',
						header: {
							'Authorization': `Bearer ${uni.getStorageSync('token')}`
						}
					})
					
					if (response.statusCode === 200) {
						const orderDetail = response.data
						this.orderInfo = {
							id: orderDetail.id,
							time: new Date(orderDetail.created_at).toLocaleString('zh-CN'),
							total: orderDetail.total_amount,
							items: orderDetail.items.map(item => ({
								id: item.meal_id,
								name: item.meal.name,
								price: item.unit_price,
								quantity: item.quantity,
								image: item.meal.image_url
							}))
						}
						
						// 获取配送员信息
						if (orderDetail.delivery) {
							this.delivererInfo = {
								id: orderDetail.delivery.deliverer_id || '',
								name: orderDetail.delivery.deliverer_name || '未知配送员',
								phone: orderDetail.delivery.deliverer_phone || ''
							}
						}
					} else {
						throw new Error(response.data?.detail || '获取订单信息失败')
					}
				} catch (error) {
					console.error('获取订单信息失败:', error)
					uni.showToast({
						title: '获取订单信息失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			goBack() {
				uni.navigateBack()
			},
			toggleTag(tag) {
				const index = this.selectedTags.indexOf(tag)
				if (index !== -1) {
					this.selectedTags.splice(index, 1)
				} else {
					this.selectedTags.push(tag)
					// 将标签添加到评价内容中
					if (this.reviewContent) {
						this.reviewContent += ' ' + tag
					} else {
						this.reviewContent = tag
					}
				}
			},
			async chooseImage() {
				const remaining = 9 - this.images.length
				if (remaining<= 0) {
					uni.showToast({
						title: '最多只能上传9张图片',
						icon: 'none'
					})
					return
				}
				
				uni.chooseImage({
					count: remaining,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success: async (res) =>{
						uni.showLoading({
							title: '上传图片中...'
						})
						
						try {
							const uploadedUrls = []
							for (const tempFilePath of res.tempFilePaths) {
								const url = await this.uploadImage(tempFilePath)
								if (url) {
									uploadedUrls.push(url)
								}
							}
							this.images = [...this.images, ...uploadedUrls]
						} catch (error) {
							console.error('上传图片失败:', error)
							uni.showToast({
								title: '上传图片失败',
								icon: 'none'
							})
						} finally {
							uni.hideLoading()
						}
					},
					fail: (err) =>{
						console.error('选择图片失败:', err)
						uni.showToast({
							title: '选择图片失败',
							icon: 'none'
						})
					}
				})
			},
			async uploadImage(filePath) {
				return new Promise((resolve, reject) => {
					const token = uni.getStorageSync('token')
					uni.uploadFile({
						url: 'http://127.0.0.1:7678/api/v1/older/upload/image',
						filePath: filePath,
						name: 'file',
						header: {
							'Authorization': `Bearer ${token}`
						},
						success: (res) => {
							try {
								const data = JSON.parse(res.data)
								if (res.statusCode === 200) {
									// 后端已经返回完整URL
									console.log('完整图片URL:', data.url)
									resolve(data.url)
								} else {
									console.error('上传失败:', data.detail)
									reject(new Error(data.detail || '上传失败'))
								}
							} catch (e) {
								console.error('解析响应失败:', e)
								reject(e)
							}
						},
						fail: (err) => {
							console.error('上传请求失败:', err)
							reject(err)
						}
					})
				})
			},
			deleteImage(index) {
				this.images.splice(index, 1)
			},
			async submitReview() {
				if (this.rating === 0) {
					uni.showToast({
						title: '请先进行评分',
						icon: 'none'
					})
					return
				}
				
				if (!this.reviewContent) {
					uni.showToast({
						title: '请输入评价内容',
						icon: 'none'
					})
					return
				}
				
				this.loading = true
				try {
					// 根据评价类型提交数据
					const reviewData = {
						order_id: this.orderId,
						rating: this.rating,
						content: this.reviewContent,
						images: this.images
					}
					
					// 如果是配送员评价，添加配送员ID
					if (this.reviewType === 'deliverer' && this.delivererInfo.id) {
						reviewData.deliverer_id = this.delivererInfo.id
					}
					
					// 直接调用老人端评价接口
					await apiClient.post('/older/reviews', reviewData)
					
					uni.showToast({
						title: '评价提交成功',
						icon: 'success'
					})
					
					// 返回订单页面
					setTimeout(() => {
						uni.navigateBack()
					}, 1000)
				} catch (error) {
					console.error('提交评价失败:', error)
					uni.showToast({
						title: error.message || '提交评价失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			}
		}
	}
</script>

<style scoped>
	.review-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 220px, #e2e8f0 100%);
		padding-bottom: 40px;
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
	
	/* 导航栏 */
	.nav-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 56px;
		padding: 0 20px;
		background: rgba(255, 255, 255, 0.95);
		border-bottom: 1px solid rgba(99, 102, 241, 0.1);
	}
	
	.back-btn {
		font-size: 22px;
		color: #6366f1;
		width: 34px;
		height: 34px;
		line-height: 34px;
		text-align: center;
		background: rgba(99, 102, 241, 0.1);
		border-radius: 17px;
	}
	
	.nav-title {
		font-size: 19px;
		font-weight: 600;
		color: #1e293b;
	}
	
	.placeholder {
		width: 24px;
	}
	
	/* 订单信息卡片 */
	.order-info-card {
		background-color: #FFFFFF;
		margin: 20px;
		padding: 20px;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(99, 102, 241, 0.08);
	}
	
	.order-id {
		font-size: 13px;
		color: #64748b;
		display: block;
		margin-bottom: 16px;
		background: #f1f5f9;
		padding: 4px 10px;
		border-radius: 12px;
		width: fit-content;
	}
	
	.order-items {
		margin-bottom: 16px;
	}
	
	.order-item {
		display: flex;
		align-items: center;
		margin-bottom: 12px;
	}
	
	.order-item:last-child {
		margin-bottom: 0;
	}
	
	.item-image {
		width: 48px;
		height: 48px;
		border-radius: 8px;
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		margin-right: 12px;
	}
	
	.item-info {
		flex: 1;
		display: flex;
		flex-direction: column;
	}
	
	.item-name {
		font-size: 15px;
		color: #1e293b;
		font-weight: 500;
		margin-bottom: 4px;
	}
	
	.item-price {
		font-size: 14px;
		color: #6366f1;
		font-weight: 600;
	}
	
	.item-quantity {
		font-size: 13px;
		color: #64748b;
	}
	
	.order-summary {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 12px;
		border-top: 1px solid #f1f5f9;
	}
	
	.order-time {
		font-size: 13px;
		color: #64748b;
	}
	
	.order-total {
		font-size: 16px;
		color: #6366f1;
		font-weight: 700;
	}
	
	/* 评价区域 */
	.review-section {
		background-color: #FFFFFF;
		margin: 0 20px 16px;
		padding: 20px;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(99, 102, 241, 0.08);
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #1e293b;
		display: block;
		margin-bottom: 16px;
	}
	
	/* 评价类型选择器 */
	.review-type-selector {
		display: flex;
		gap: 12px;
		margin-bottom: 16px;
	}
	
	.review-type-option {
		flex: 1;
		padding: 16px;
		border: 1px solid #DDDDDD;
		border-radius: 12px;
		text-align: center;
		background-color: #FFFFFF;
	}
	
	.review-type-option.active {
		border-color: #6366f1;
		background-color: rgba(99, 102, 241, 0.05);
	}
	
	.review-type-name {
		display: block;
		font-size: 15px;
		font-weight: 600;
		color: #333333;
		margin-bottom: 4px;
	}
	
	.review-type-desc {
		display: block;
		font-size: 12px;
		color: #999999;
	}
	
	/* 配送员信息 */
	.deliverer-info {
		padding: 12px;
		background-color: #f8fafc;
		border-radius: 8px;
		border-left: 3px solid #6366f1;
	}
	
	.deliverer-label {
		font-size: 13px;
		color: #666666;
	}
	
	.deliverer-name {
		font-size: 14px;
		font-weight: 600;
		color: #333333;
		margin-left: 8px;
	}
	
	.deliverer-phone {
		font-size: 13px;
		color: #999999;
		margin-left: 8px;
	}
	
	/* 星级评分 */
	.star-rating {
		display: flex;
		gap: 10px;
		margin-bottom: 12px;
	}
	
	.star {
		font-size: 42px;
		color: #cbd5e1;
	}
	
	.star.active {
		color: #f59e0b;
	}
	
	.rating-desc {
		font-size: 13px;
		color: #64748b;
	}
	
	/* 评价输入框 */
	.review-input {
		width: 100%;
		height: 120px;
		border: 1px solid #e2e8f0;
		border-radius: 12px;
		padding: 12px;
		font-size: 14px;
		color: #1e293b;
		background-color: #ffffff;
		resize: none;
		margin-bottom: 8px;
	}
	
	.char-count {
		font-size: 13px;
		color: #64748b;
		text-align: right;
		display: block;
	}
	
	/* 快捷评价标签 */
	.quick-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	
	.quick-tag {
		padding: 8px 16px;
		border: 1px solid #e2e8f0;
		border-radius: 16px;
		font-size: 14px;
		color: #64748b;
		background: #f8fafc;
	}
	
	.quick-tag.active {
		border-color: transparent;
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		box-shadow: 0 6px 14px rgba(99, 102, 241, 0.24);
	}
	
	/* 提交按钮 */
	.submit-section {
		display: flex;
		gap: 12px;
		padding: 0 20px 20px;
	}
	
	.btn-cancel {
		flex: 1;
		height: 44px;
		background-color: #f1f5f9;
		color: #64748b;
		border: 1px solid #e2e8f0;
		border-radius: 22px;
		font-size: 15px;
		font-weight: 600;
	}
	
	.btn-submit {
		flex: 2;
		height: 44px;
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		border: none;
		border-radius: 22px;
		font-size: 15px;
		font-weight: 600;
		box-shadow: 0 8px 18px rgba(99, 102, 241, 0.3);
	}
	
	.btn-submit:disabled {
		background-color: #cbd5e1;
		color: #94a3b8;
		box-shadow: none;
	}
	
	/* 图片上传区域 */
	.image-upload-area {
		margin-top: 8px;
	}
	
	.image-list {
		display: flex;
		flex-wrap: wrap;
		gap: 12px;
	}
	
	.image-item {
		position: relative;
		width: 80px;
		height: 80px;
		border-radius: 12px;
		overflow: hidden;
	}
	
	.uploaded-image {
		width: 100%;
		height: 100%;
	}
	
	.image-delete {
		position: absolute;
		top: -8px;
		right: -8px;
		width: 24px;
		height: 24px;
		background-color: rgba(0, 0, 0, 0.6);
		color: white;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 16px;
		line-height: 1;
	}
	
	.image-upload-btn {
		width: 80px;
		height: 80px;
		border: 2px dashed #e2e8f0;
		border-radius: 12px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background-color: #f8fafc;
	}
	
	.upload-icon {
		font-size: 32px;
		color: #94a3b8;
		margin-bottom: 4px;
	}
	
	.upload-text {
		font-size: 12px;
		color: #94a3b8;
	}
	
	.image-hint {
		font-size: 12px;
		color: #94a3b8;
		margin-top: 8px;
		display: block;
	}
</style>
