<template>
	<view class="profile-container">
		<!-- 用户信息区 -->
		<view class="user-info-card">
			<view class="avatar-container" @click="chooseAvatar">
				<image class="user-avatar" :src="userInfo.avatar || '/static/logo.png'" mode="aspectFill"></image>
				<view class="avatar-edit-btn">
					<text class="edit-icon">📷</text>
				</view>
			</view>
			<view class="user-info">
				<text class="user-name">{{ userInfo.name }}</text>
				<text class="user-detail">
					{{ userInfo.age ? userInfo.age + '岁' : '' }} 
					{{ userInfo.gender === 'male' || userInfo.gender === '男' ? '男' : '女' }}
				</text>
				<view class="health-tags">
				<text v-if="userInfo.health_tag" class="tag tag-warning">{{ userInfo.health_tag }}</text>
			</view>
			</view>
		</view>
		
		<!-- 功能菜单区 -->
		<view class="menu-section">
			<view class="menu-card">
				<view 
					v-for="menu in menuList" 
					:key="menu.id"
					class="menu-item"
					@click="handleMenuClick(menu)"
				>
					<view class="menu-left">
						<text class="menu-icon">{{ menu.icon }}</text>
						<text class="menu-text">{{ menu.title }}</text>
						<view class="menu-badge" v-if="menu.id === 8 && unreadAnnouncementCount > 0">
							<text class="badge-text">{{ unreadAnnouncementCount }}</text>
						</view>
					</view>
					<text class="menu-arrow">→</text>
				</view>
			</view>
		</view>
		
		<!-- 底部区域 -->
		<view class="bottom-section">
			<button class="btn-logout" @click="handleLogout">退出登录</button>
			<text class="version-info">版本 1.0.0</text>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				userInfo: {
					name: '',
					age: '',
					gender: '',
					health_tag: '',
					dietary_preference: '',
					avatar: ''
				},
				loading: false,
				unreadAnnouncementCount: 0,
				menuList: [
					{
						id: 1,
						title: '个人信息',
						icon: '👤',
						url: '/pages/profile/info'
					},
					{
						id: 2,
						title: '健康档案',
						icon: '📋',
						url: '/pages/profile/health'
					},
					{
						id: 3,
						title: '饮食偏好',
						icon: '🍽️',
						url: '/pages/profile/preference'
					},
					{
						id: 4,
						title: '我的收藏',
						icon: '❤️',
						url: '/pages/favorite/favorite'
					},
					{
						id: 10,
						title: '我的评价',
						icon: '⭐',
						url: '/pages/profile/reviews'
					},
					{
						id: 8,
						title: '我的公告',
						icon: '📢',
						url: '/pages/profile/announcements'
					},
					{
						id: 9,
						title: '健康提醒',
						icon: '💊',
						url: '/pages/profile/health-reminders'
					},
					{
						id: 6,
						title: '紧急联系人',
						icon: '📞',
						url: '/pages/profile/emergency-contacts'
					},
					{
						id: 7,
						title: '设置',
						icon: '⚙️',
						url: '/pages/profile/settings'
					}
				]
			}
		},
		onLoad() {
			this.loadUserInfo()
			this.loadUnreadAnnouncementCount()
		},
		onShow() {
			// 页面显示时重新加载用户信息和未读公告数量
			this.loadUserInfo()
			this.loadUnreadAnnouncementCount()
		},
		methods: {
			async loadUserInfo() {
				this.loading = true
				try {
					const response = await api.auth.getProfile()
					const profile = response.profile || {}
					this.userInfo = {
						name: profile.name || '未设置',
						age: profile.age || '',
						gender: profile.gender || 'female',
						health_tag: profile.health_status || '',
						dietary_preference: profile.dietary_preferences || '',
						avatar: profile.avatar || ''
					}
				} catch (error) {
					console.error('获取用户信息失败:', error)
					uni.showToast({
						title: '获取用户信息失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			// 获取未读公告数量
			async loadUnreadAnnouncementCount() {
				try {
					// 获取已读公告ID列表
					const readIds = this.getReadAnnouncementIds()
					
					// 获取公告列表
					const response = await api.older.getAnnouncements({
						page: 1,
						limit: 50
					})
					
					// 计算未读数量
					const totalCount = response.items.length
					const readCount = response.items.filter(a => readIds.includes(a.id)).length
					this.unreadAnnouncementCount = totalCount - readCount
				} catch (error) {
					console.error('获取未读公告数量失败:', error)
					this.unreadAnnouncementCount = 0
				}
			},
			// 获取已读公告ID列表
			getReadAnnouncementIds() {
				try {
					const readIds = uni.getStorageSync('olderReadAnnouncementIds')
					return readIds ? JSON.parse(readIds) : []
				} catch (error) {
					console.error('获取已读公告ID失败:', error)
					return []
				}
			},
			handleMenuClick(menu) {
				if (menu.id === 7) { // 设置按钮
					uni.showToast({
						title: '后续功能开发中...',
						icon: 'none',
						duration: 2000
					})
				} else {
					uni.navigateTo({
						url: menu.url
					})
				}
			},
			handleLogout() {
				uni.showModal({
					title: '退出登录',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							// 清除本地存储
							uni.removeStorageSync('token')
							uni.removeStorageSync('user')
							uni.showToast({
								title: '已退出登录',
								icon: 'success'
							})
							// 跳转到登录页面
							setTimeout(() => {
								uni.redirectTo({
									url: '/pages/login/login'
								})
							}, 1000)
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
						url: 'http://127.0.0.1:7678/api/v1/older/avatar',
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
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 220px, #F5F5F5 100%);
		padding-bottom: 40px;
		display: flex;
		flex-direction: column;
	}
	
	/* 用户信息区 */
	.user-info-card {
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		padding: 24px 20px 38px;
		display: flex;
		align-items: center;
		color: white;
		box-shadow: 0 10px 24px rgba(255, 122, 69, 0.22);
		border-bottom-left-radius: 26px;
		border-bottom-right-radius: 26px;
	}
	
	.avatar-container {
		position: relative;
		margin-right: 20px;
	}
	
	.user-avatar {
		width: 80px;
		height: 80px;
		border-radius: 40px;
		border: 3px solid rgba(255, 255, 255, 0.45);
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
	}
	
	.avatar-edit-btn {
		position: absolute;
		bottom: -2px;
		right: -2px;
		width: 28px;
		height: 28px;
		border-radius: 14px;
		background: linear-gradient(135deg, #FF7A45, #FF9A72);
		display: flex;
		align-items: center;
		justify-content: center;
		border: 2px solid rgba(255, 255, 255, 0.8);
		box-shadow: 0 4px 12px rgba(255, 122, 69, 0.4);
	}
	
	.edit-icon {
		font-size: 14px;
	}
	
	.user-info {
		flex: 1;
	}
	
	.user-name {
		font-size: 22px;
		font-weight: 600;
		display: block;
		margin-bottom: 4px;
	}
	
	.user-detail {
		font-size: 14px;
		opacity: 0.9;
		display: block;
		margin-bottom: 8px;
	}
	
	.health-tags {
		display: flex;
		gap: 8px;
	}
	
	.tag {
		padding: 4px 12px;
		border-radius: 14px;
		font-size: 12px;
		font-weight: 500;
		background-color: rgba(255, 255, 255, 0.24);
		color: white;
	}
	
	/* 功能菜单区 */
	.menu-section {
		padding: 20px;
		margin-top: 20px;
	}
	
	.menu-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.menu-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20px 20px;
		border-bottom: 1px solid #F0F0F0;
	}
	
	.menu-item:last-child {
		border-bottom: none;
	}
	
	.menu-left {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	
	.menu-icon {
		font-size: 24px;
		margin-right: 16px;
		width: 32px;
		text-align: center;
	}
	
	.menu-text {
		font-size: 16px;
		color: #333333;
		font-weight: 500;
	}
	
	.menu-badge {
		background-color: #FF4D4F;
		color: white;
		border-radius: 10px;
		min-width: 20px;
		height: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 12px;
		font-weight: 600;
		padding: 0 6px;
		box-shadow: 0 2px 8px rgba(255, 77, 79, 0.4);
	}
	
	.badge-text {
		
	}
	
	.menu-arrow {
		font-size: 18px;
		color: #999999;
		font-weight: 600;
	}
	
	/* 底部区域 */
	.bottom-section {
		padding: 40px 20px 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-top: auto;
	}
	
	.btn-logout {
		background: #fff;
		color: #FF6A57;
		border: 1px solid #FFD1C8;
		border-radius: 22px;
		height: 44px;
		font-size: 15px;
		font-weight: 600;
		line-height: 44px;
		text-align: center;
		display: block;
		width: 100%;
		max-width: 300px;
		margin-bottom: 24px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
	}
	
	.version-info {
		font-size: 14px;
		color: #999999;
	}
</style>