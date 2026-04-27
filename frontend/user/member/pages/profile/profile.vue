<template>
	<view class="container">
		<!-- 用户信息区 -->
		<view class="user-section">
			<view class="user-card">
				<view class="avatar-container" @click="chooseAvatar">
					<image class="user-avatar" :src="userInfo.avatar || '/static/logo.png'" mode="aspectFill"></image>
					<view class="avatar-edit-btn">
						<text class="edit-icon">📷</text>
					</view>
				</view>
				<text class="user-name">{{ userInfo.name }}</text>
				<text class="user-phone">{{ userInfo.phone }}</text>
			</view>
		</view>
		
		<!-- 统一功能列表区 -->
		<view class="menu-section">
			<view class="menu-card">
				<!-- 我的老人 -->
				<view class="menu-item" @click="toggleElderList">
					<view class="menu-icon elder-icon"></view>
					<text class="menu-text">我的老人</text>
					<text class="menu-arrow" :style="{ transform: elderListExpanded ? 'rotate(90deg)' : 'none', transition: 'transform 0.3s ease' }">›</text>
				</view>
				
				<!-- 老人列表（展开时显示） -->
				<view class="elder-list" v-if="elderListExpanded">
					<view class="elder-item" v-for="(elder, index) in elders" :key="index">
						<view class="elder-avatar"></view>
						<view class="elder-info">
							<text class="elder-name">{{ elder.name }}</text>
							<text class="elder-details">{{ elder.age }}岁 · {{ elder.gender }}</text>
						</view>
						<view class="elder-actions">
							<button class="action-btn" @click="editTaste(elder.id)">
								<text class="btn-icon">🍽️</text>
							</button>
							<button class="action-btn" @click="editHealth(elder.id)">
								<text class="btn-icon">❤️</text>
							</button>
						</view>
					</view>
					<view class="add-elder-item" @click="addElder">
						<view class="add-icon">+</view>
						<text class="add-text">添加老人</text>
					</view>
				</view>

				<view class="menu-item" @click="goToMessage">
					<view class="menu-icon message-icon"></view>
					<text class="menu-text">消息中心</text>
					<text class="menu-arrow">›</text>
				</view>

				<view class="menu-item" @click="goToFavorites">
					<view class="menu-icon favorites-icon"></view>
					<text class="menu-text">我的收藏</text>
					<text class="menu-arrow">›</text>
				</view>

				<view class="menu-item" @click="goToReviews">
					<view class="menu-icon reviews-icon"></view>
					<text class="menu-text">我的评价</text>
					<text class="menu-arrow">›</text>
				</view>

				<view class="menu-item" @click="goToSettings">
					<view class="menu-icon settings-icon"></view>
					<text class="menu-text">设置</text>
					<text class="menu-arrow">›</text>
				</view>
			</view>
		</view>
		
		<!-- 底部区域 -->
		<view class="bottom-section">
			<view class="about-us" @click="aboutUs">
				<text class="about-text">关于我们</text>
			</view>
			<button class="logout-btn" @click="logout">
				<text class="logout-text">退出登录</text>
			</button>
		</view>
	</view>
</template>

<script>
import { bindService } from '../../api/bind.js';
import { authService } from '../../api/auth.js';
import { messageService } from '../../api/message.js';

export default {
	data() {
			return {
				userInfo: {
					name: '',
					phone: '',
					avatar: ''
				},
				elders: [],

				elderListExpanded: false,
				loading: false
			};
		},
	onLoad() {
		this.loadUserInfo();
		this.loadElders();
	},
	methods: {
		async loadUserInfo() {
			try {
				const userData = await authService.getCurrentUser();
				this.userInfo = {
					name: userData.name || '未知',
					phone: userData.phone || '',
					avatar: userData.avatar || ''
				};
			} catch (error) {
				console.error('获取用户信息失败:', error);
				// 如果获取失败，使用默认值
				this.userInfo = {
					name: '用户',
					phone: '',
					avatar: ''
				};
			}
		},
		async loadElders() {
			try {
				this.loading = true;
				const data = await bindService.getBindList();
				// 将后端返回的数据转换为前端期望的格式
				this.elders = data.map(item => ({
					id: item.elderly_id,
					name: item.elderly_name,
					age: item.elderly_age,
					gender: item.elderly_gender
				}));
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
		toggleElderList() {
			this.elderListExpanded = !this.elderListExpanded;
		},
		editTaste(elderId) {
			uni.navigateTo({
				url: `/pages/profile/taste?elderId=${elderId}`
			});
		},
		editHealth(elderId) {
			uni.navigateTo({
				url: `/pages/profile/health-edit?elderId=${elderId}`
			});
		},
		addElder() {
			uni.navigateTo({
				url: '/pages/profile/add-bind'
			});
		},
		goToMessage() {
			uni.navigateTo({
				url: '/pages/message/message'
			});
		},

		goToFavorites() {
			uni.navigateTo({
				url: '/pages/profile/favorites'
			});
		},

		goToReviews() {
			uni.navigateTo({
				url: '/pages/profile/reviews'
			});
		},

		goToSettings() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		aboutUs() {
			uni.showToast({
				title: '关于我们',
				icon: 'none'
			});
		},

		logout() {
				uni.showModal({
					title: '退出登录',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							uni.showToast({
								title: '已退出登录',
								icon: 'success'
							});
							setTimeout(() => {
								uni.reLaunch({
									url: '/pages/login/login'
								});
							}, 1500);
						}
					}
				});
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
						url: 'http://127.0.0.1:7678/api/v1/member/avatar',
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
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background: #f8fafc;
	position: relative;
	overflow-x: hidden;
}

/* 用户信息区 */
.user-section {
	padding: 40px 24px 24px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border-bottom-left-radius: 32px;
	border-bottom-right-radius: 32px;
	box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
	margin-bottom: -16px;
	position: relative;
	z-index: 2;
}

.user-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 0;
}

.avatar-container {
	position: relative;
	margin-bottom: 16px;
}

.user-avatar {
	width: 88px;
	height: 88px;
	border-radius: 50%;
	border: 4px solid rgba(255, 255, 255, 0.3);
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
	transition: all 0.3s ease;
}

.user-avatar:active {
	transform: scale(0.95);
}

.avatar-edit-btn {
	position: absolute;
	bottom: 0;
	right: 0;
	width: 32px;
	height: 32px;
	border-radius: 16px;
	background: #ffffff;
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.edit-icon {
	font-size: 16px;
}

.user-name {
	font-size: 20px;
	font-weight: 600;
	color: #ffffff;
	margin-bottom: 6px;
	text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.user-phone {
	font-size: 15px;
	color: rgba(255, 255, 255, 0.85);
}

/* 老人列表区域 */
.elder-list {
	display: flex;
	flex-direction: column;
	gap: 12px;
	padding: 0 20px 16px;
	background: #ffffff;
}

.elder-item {
	background: #f8fafc;
	border-radius: 16px;
	padding: 16px;
	display: flex;
	align-items: center;
	gap: 12px;
	border: 1px solid rgba(226, 232, 240, 0.6);
}

.elder-avatar {
	width: 48px;
	height: 48px;
	border-radius: 50%;
	background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
	display: flex;
	align-items: center;
	justify-content: center;
}
.elder-avatar::after {
	content: '👤';
	font-size: 24px;
}

.elder-info {
	flex: 1;
}

.elder-name {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
	display: block;
}

.elder-details {
	font-size: 14px;
	color: #64748b;
	display: block;
	margin-top: 4px;
}

.elder-actions {
	display: flex;
	gap: 8px;
}

.action-btn {
	width: 36px;
	height: 36px;
	background: #ffffff;
	border-radius: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.2s ease;
	padding: 0;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.action-btn:active {
	background: #f1f5f9;
	transform: scale(0.95);
}

.btn-icon {
	font-size: 18px;
}

.add-elder-item {
	background: #f8fafc;
	border: 1.5px dashed #cbd5e1;
	border-radius: 16px;
	padding: 16px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	transition: all 0.2s ease;
}

.add-elder-item:active {
	background: #e2e8f0;
}

.add-icon {
	width: 36px;
	height: 36px;
	border-radius: 18px;
	background: rgba(99, 102, 241, 0.1);
	color: #6366f1;
	font-size: 24px;
	font-weight: 300;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: 8px;
}

.add-text {
	font-size: 14px;
	color: #6366f1;
	font-weight: 500;
}

/* 功能菜单区 */
.menu-section {
	padding: 16px 20px 24px;
	position: relative;
	z-index: 1;
}

.menu-card {
	background: #ffffff;
	border-radius: 20px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	overflow: hidden;
	border: 1px solid rgba(226, 232, 240, 0.6);
}

.menu-item {
	display: flex;
	align-items: center;
	height: 64px;
	padding: 0 20px;
	background: #ffffff;
	position: relative;
	transition: all 0.2s ease;
}

.menu-item:not(:last-child)::after {
	content: '';
	position: absolute;
	bottom: 0;
	left: 68px;
	right: 20px;
	height: 1px;
	background: rgba(226, 232, 240, 0.5);
}

.menu-item:active {
	background: #f8fafc;
}

.menu-icon {
	width: 36px;
	height: 36px;
	border-radius: 10px;
	background: rgba(99, 102, 241, 0.05);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 12px;
}

.elder-icon::before {
	content: '👴';
	font-size: 20px;
}

.message-icon::before {
	content: '📩';
	font-size: 20px;
}



.favorites-icon::before {
	content: '❤️';
	font-size: 20px;
}

.reviews-icon::before {
	content: '⭐';
	font-size: 20px;
}

.settings-icon::before {
	content: '⚙️';
	font-size: 20px;
}

.menu-text {
	flex: 1;
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
}

.menu-arrow {
	font-size: 20px;
	color: #64748b;
	margin-right: 4px;
}



/* 底部区域 */
.bottom-section {
	padding: 0 24px 32px;
	display: flex;
	flex-direction: column;
	gap: 20px;
}

.about-us {
	text-align: center;
	padding: 16px;
	background: #ffffff;
	border-radius: 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	transition: all 0.2s ease;
}
.about-us:active {
	background: #f8fafc;
}

.about-text {
	font-size: 15px;
	color: #475569;
	font-weight: 500;
}

.logout-btn {
	width: 100%;
	height: 52px;
	background: rgba(239, 68, 68, 0.1);
	border: none;
	border-radius: 16px;
	color: #ef4444;
	font-size: 16px;
	font-weight: 600;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.2s ease;
}
.logout-btn:active {
	background: rgba(239, 68, 68, 0.15);
	transform: scale(0.98);
}

.logout-text {
	
}
</style>