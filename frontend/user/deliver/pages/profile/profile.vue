<template>
	<view class="profile-container">
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<text class="loading-icon">⏳</text>
			<text class="loading-text">加载中...</text>
		</view>
		
		<view v-else>
			<view class="user-info-section">
				<view class="user-card">
					<view class="avatar-container" @click="chooseAvatar">
						<image class="user-avatar" :src="userInfo.avatar || '/static/logo.png'" mode="aspectFill"></image>
						<view class="avatar-edit-btn">
							<text class="edit-icon">📷</text>
						</view>
					</view>
					<view class="user-details">
						<text class="user-name">{{ userInfo.name }}</text>
						<text class="user-phone">{{ maskPhone(userInfo.phone) }}</text>
						<view class="status-badge">{{ userInfo.status }}</view>
					</view>
				</view>
			</view>
			
			<view class="stats-section">
				<view class="stat-item">
					<text class="stat-number">{{ stats.today_orders }}</text>
					<text class="stat-label">今日订单</text>
				</view>
				<view class="stat-item">
					<text class="stat-number">{{ stats.total_orders }}</text>
					<text class="stat-label">总订单</text>
				</view>
				<view class="stat-item">
					<text class="stat-number">{{ stats.rating_rate }}</text>
					<text class="stat-label">好评率</text>
				</view>
				<view class="stat-item">
					<text class="stat-number">¥{{ stats.total_income }}</text>
					<text class="stat-label">总收入</text>
				</view>
			</view>
		</view>
		
		<view class="menu-section">
			<view class="menu-group">
				<view class="menu-item" @click="goToPersonalInfo">
					<text class="menu-icon">👤</text>
					<text class="menu-label">个人信息</text>
					<text class="menu-arrow">›</text>
				</view>
				<view class="menu-item" @click="goToReviews">
					<text class="menu-icon">⭐</text>
					<text class="menu-label">我的评价</text>
					<text class="menu-arrow">›</text>
				</view>
				<view class="menu-item" @click="goToMessage">
					<text class="menu-icon">📩</text>
					<text class="menu-label">消息中心</text>
					<view class="menu-badge" v-if="unreadMessageCount > 0">
						<text class="badge-text">{{ unreadMessageCount }}</text>
					</view>
					<text class="menu-arrow">›</text>
				</view>
				<view class="menu-item" @click="goToSchedule">
					<text class="menu-icon">📅</text>
					<text class="menu-label">排班管理</text>
					<text class="menu-arrow">›</text>
				</view>
				<view class="menu-item" @click="goToIncomeDetail">
					<text class="menu-icon">💰</text>
					<text class="menu-label">收入明细</text>
					<text class="menu-arrow">›</text>
				</view>
			</view>
			
			<view class="menu-group">
				<view class="menu-item" @click="goToSettings">
					<text class="menu-icon">⚙️</text>
					<text class="menu-label">设置</text>
					<text class="menu-arrow">›</text>
				</view>

			</view>
		</view>
		
		<view class="logout-section">
			<button @click="logout" class="logout-button">退出登录</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	import { messageService } from '../../api/message.js'
	
	export default {
		data() {
			return {
				userInfo: {
					name: '',
					phone: '',
					status: '',
					avatar: ''
				},
				stats: {
					today_orders: 0,
					total_orders: 0,
					rating_rate: '0%',
					total_income: 0
				},
				loading: false,
				unreadMessageCount: 0
			}
		},
		onLoad() {
			this.loadProfile()
			this.loadUnreadMessageCount()
		},
		onShow() {
		this.loadProfile()
		this.loadUnreadMessageCount()
	},
		methods: {
			// 加载个人信息
			async loadProfile() {
				this.loading = true
				try {
					const data = await api.profile.getProfile()
					this.userInfo = {
						name: data.deliverer.name || '',
						phone: data.deliverer.phone || '',
						status: data.deliverer.status || '',
						avatar: data.deliverer.avatar || ''
					}
					this.stats = data.stats
				} catch (error) {
					console.error('加载个人信息失败:', error)
					uni.showToast({
						title: '加载失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			// 加载未读消息数量
			async loadUnreadMessageCount() {
				try {
					const count = await messageService.getUnreadCount()
					this.unreadMessageCount = count
				} catch (error) {
					console.error('获取未读消息数量失败:', error)
					this.unreadMessageCount = 0
				}
			},
			// 手机号脱敏
			maskPhone(phone) {
				if (!phone || phone.length < 11) return phone
				return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
			},
			
			goToPersonalInfo() {
				uni.navigateTo({
					url: '/pages/personal-info/personal-info'
				})
			},
			goToReviews() {
				uni.navigateTo({
					url: '/pages/reviews/reviews'
				})
			},
			goToMessage() {
				uni.navigateTo({
					url: '/pages/message/message'
				})
			},
			goToSchedule() {
				uni.navigateTo({
					url: '/pages/schedule/schedule'
				})
			},
			goToIncomeDetail() {
				uni.navigateTo({
					url: '/pages/income/income'
				})
			},
			goToSettings() {
				uni.showToast({
					title: '后续功能开发中...',
					icon: 'none',
					duration: 2000
				})
			},

			logout() {
				uni.showModal({
					title: '退出登录',
					content: '确定要退出登录吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.auth.logout()
								uni.showToast({
									title: '退出成功',
									icon: 'success'
								})
								setTimeout(() => {
									uni.redirectTo({
										url: '/pages/login/login'
									})
								}, 1000)
							} catch (error) {
								console.error('退出登录失败:', error)
								uni.showToast({
									title: '退出失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			// 选择头像
			async chooseAvatar() {
				try {
					const res = await uni.chooseImage({
						count: 1,
						sizeType: ['compressed'],
						sourceType: ['album', 'camera']
					})
					
					if (res.tempFilePaths.length > 0) {
						const tempFilePath = res.tempFilePaths[0]
						this.uploadAvatar(tempFilePath)
					}
				} catch (error) {
					console.error('选择图片失败:', error)
					uni.showToast({
						title: '选择图片失败',
						icon: 'none'
					})
				}
			},
			// 上传头像
			async uploadAvatar(filePath) {
				uni.showLoading({
					title: '上传中...'
				})
				
				try {
					const token = uni.getStorageSync('token')
					const uploadTask = uni.uploadFile({
						url: 'http://127.0.0.1:7678/api/v1/deliver/avatar',
						filePath: filePath,
						name: 'avatar',
						header: {
							'Authorization': `Bearer ${token}`
						},
						success: (uploadRes) => {
							try {
								const result = JSON.parse(uploadRes.data)
								if (uploadRes.statusCode === 200 && result.success) {
									this.userInfo.avatar = result.data.avatar_url
									uni.showToast({
										title: '头像上传成功',
										icon: 'success'
									})
								} else {
									uni.showToast({
										title: result.message || '上传失败',
										icon: 'none'
									})
								}
							} catch (parseError) {
								uni.showToast({
									title: '服务器返回数据格式错误',
									icon: 'none'
								})
							}
						},
						fail: (error) => {
							uni.showToast({
								title: '上传失败，请重试',
								icon: 'none'
							})
						},
						complete: () => {
							uni.hideLoading()
						}
					})
				} catch (error) {
					console.error('上传头像失败:', error)
					uni.showToast({
						title: '头像上传失败',
						icon: 'none'
					})
				}
			}
		}
	}
</script>

<style scoped>
	.profile-container {
		min-height: 100vh;
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
	
	.user-info-section {
		background-color: white;
		padding: 40rpx 30rpx;
		margin-bottom: 20rpx;
	}
	
	.user-card {
		display: flex;
		align-items: center;
	}
	
	.avatar-container {
		position: relative;
		margin-right: 30rpx;
	}
	
	.user-avatar {
		width: 96rpx;
		height: 96rpx;
		border-radius: 50%;
		border: 3px solid #ffffff;
		box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
	}
	
	.avatar-edit-btn {
		position: absolute;
		bottom: -2px;
		right: -2px;
		width: 28px;
		height: 28px;
		border-radius: 14px;
		background: linear-gradient(135deg, #6366f1, #8b5cf6);
		display: flex;
		align-items: center;
		justify-content: center;
		border: 2px solid rgba(255, 255, 255, 0.8);
		box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
	}
	
	.edit-icon {
		font-size: 14px;
	}
	
	.user-details {
		flex: 1;
	}
	
	.user-name {
		font-size: 40rpx;
		font-weight: 600;
		color: #1e293b;
		display: block;
		margin-bottom: 8rpx;
	}
	
	.user-phone {
		font-size: 28rpx;
		color: #64748b;
		display: block;
		margin-bottom: 12rpx;
	}
	
	.status-badge {
		display: inline-block;
		padding: 8rpx 16rpx;
		background-color: #d1fae5;
		color: #10b981;
		border-radius: 16rpx;
		font-size: 24rpx;
		font-weight: 500;
	}
	
	.stats-section {
		background-color: white;
		padding: 30rpx;
		margin-bottom: 20rpx;
		display: flex;
		justify-content: space-around;
	}
	
	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	
	.stat-number {
		font-size: 40rpx;
		font-weight: 700;
		color: #10b981;
		margin-bottom: 8rpx;
	}
	
	.stat-label {
		font-size: 24rpx;
		color: #64748b;
	}
	
	.menu-section {
		background-color: white;
		margin-bottom: 40rpx;
	}
	
	.menu-group {
		border-bottom: 1rpx solid #f1f5f9;
	}
	
	.menu-group:last-child {
		border-bottom: none;
	}
	
	.menu-item {
		display: flex;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f1f5f9;
		position: relative;
	}
	
	.menu-item:last-child {
		border-bottom: none;
	}
	
	.menu-icon {
		font-size: 32rpx;
		margin-right: 20rpx;
	}
	
	.menu-label {
		flex: 1;
		font-size: 32rpx;
		color: #1e293b;
	}
	
	.menu-arrow {
		font-size: 32rpx;
		color: #94a3b8;
	}
	
	.menu-badge {
		background-color: #ef4444;
		color: #ffffff;
		border-radius: 50%;
		min-width: 20px;
		height: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 12px;
		font-weight: 600;
		padding: 0 4px;
		box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
		margin-right: 12rpx;
	}
	
	.badge-text {
		
	}
	
	.logout-section {
		padding: 0 30rpx 40rpx;
	}
	
	.logout-button {
		width: 100%;
		height: 96rpx;
		background-color: #f1f5f9;
		color: #ef4444;
		border: none;
		border-radius: 24rpx;
		font-size: 32rpx;
		font-weight: 500;
	}
</style>