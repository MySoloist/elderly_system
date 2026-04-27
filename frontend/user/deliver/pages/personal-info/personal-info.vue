<template>
	<view class="info-container">
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<text class="loading-icon">⏳</text>
			<text class="loading-text">加载中...</text>
		</view>
		
		<view v-else>
			<view class="info-card">
				<view class="avatar-section">
					<view v-if="userInfo.avatar" class="user-avatar-container">
						<image :src="userInfo.avatar" class="user-avatar-image"></image>
					</view>
					<text v-else class="user-avatar">👨‍🍳</text>
					<button @click="changeAvatar" class="avatar-button">更换头像</button>
				</view>
				
				<view class="form-section">
					<view class="form-item">
						<text class="label">姓名</text>
						<view class="input-wrapper">
							<input v-model="userInfo.name" type="text" placeholder="请输入姓名" class="input-field" />
						</view>
					</view>
					
					<view class="form-item">
						<text class="label">手机号</text>
						<view class="input-wrapper">
							<input v-model="userInfo.phone" type="tel" placeholder="请输入手机号" class="input-field" />
						</view>
					</view>
					
					<view class="form-item">
						<text class="label">身份证号</text>
						<view class="input-wrapper">
							<input v-model="userInfo.idCard" type="text" placeholder="请输入身份证号" class="input-field" />
						</view>
					</view>
					
					<view class="form-item">
						<text class="label">性别</text>
						<view class="gender-options">
							<view 
								v-for="gender in genderOptions" 
								:key="gender.value"
								:class="['gender-option', { selected: userInfo.gender === gender.value }]"
								@click="userInfo.gender = gender.value"
							>
								{{ gender.label }}
							</view>
						</view>
					</view>
					
					<view class="form-item">
						<text class="label">年龄</text>
						<view class="input-wrapper">
							<input v-model="userInfo.age" type="number" placeholder="请输入年龄" class="input-field" />
						</view>
					</view>
				</view>
			</view>
			
			<view class="button-section">
				<button @click="saveInfo" class="save-button">保存信息</button>
			</view>
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
				phone: '',
				idCard: '',
				gender: 'male',
				age: '',
				avatar: ''
			},
				genderOptions: [
					{ label: '男', value: 'male' },
					{ label: '女', value: 'female' }
				],
				loading: false
			}
		},
		onLoad() {
			this.loadPersonalInfo()
		},
		methods: {
			// 加载个人信息
			async loadPersonalInfo() {
				this.loading = true
				try {
					const data = await api.profile.getPersonalInfo()
					this.userInfo = {
						name: data.name,
						phone: data.phone,
						idCard: data.idCard || '',
						gender: data.gender || 'male',
						age: data.age || '',
						avatar: data.avatar || ''
					}
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
			
			changeAvatar() {
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success: async (res) => {
						uni.showLoading({
							title: '上传中...'
						})
						try {
							// 上传图片到服务器
							const tempFilePath = res.tempFilePaths[0]
							const token = uni.getStorageSync('token')
							
							uni.uploadFile({
								url: `${api.baseUrl}/deliver/upload/avatar`,
								filePath: tempFilePath,
								name: 'file',
								header: {
									'Authorization': `Bearer ${token}`
								},
								success: (uploadRes) => {
									try {
										const data = JSON.parse(uploadRes.data)
										if (uploadRes.statusCode === 200 && data.url) {
											this.userInfo.avatar = data.url
											uni.showToast({
												title: '头像更换成功',
												icon: 'success'
											})
										} else {
											uni.showToast({
												title: '上传失败',
												icon: 'none'
											})
										}
									} catch (e) {
										console.error('解析响应失败:', e)
										uni.showToast({
											title: '上传失败',
											icon: 'none'
										})
									}
								},
								fail: (error) => {
									console.error('上传失败:', error)
									uni.showToast({
										title: '上传失败',
										icon: 'none'
									})
								}
							})
						} catch (error) {
							console.error('更换头像失败:', error)
							uni.showToast({
								title: '更换头像失败',
								icon: 'none'
							})
						} finally {
							uni.hideLoading()
						}
					},
					fail: () => {
						uni.showToast({
							title: '选择图片失败',
							icon: 'none'
						})
					}
				})
			},
			saveInfo() {
				if (!this.userInfo.name) {
					uni.showToast({
						title: '请输入姓名',
						icon: 'none'
					})
					return
				}
				
				if (!this.userInfo.phone) {
					uni.showToast({
						title: '请输入手机号',
						icon: 'none'
					})
					return
				}
				
				if (!this.userInfo.idCard) {
					uni.showToast({
						title: '请输入身份证号',
						icon: 'none'
					})
					return
				}
				
				uni.showToast({
					title: '信息保存成功',
					icon: 'success'
				})
				
				setTimeout(() => {
					uni.navigateBack()
				}, 1000)
			}
		}
	}
</script>

<style scoped>
	.info-container {
		min-height: 100vh;
		padding: 30rpx;
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
	
	.info-card {
		background-color: white;
		border-radius: 24rpx;
		padding: 40rpx;
		margin-bottom: 30rpx;
		box-shadow: 0 2px 8px rgba(0,0,0,0.08);
	}
	
	.avatar-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 40rpx;
		padding-bottom: 30rpx;
		border-bottom: 1rpx solid #e2e8f0;
	}
	
	.user-avatar {
				font-size: 120rpx;
				margin-bottom: 20rpx;
			}

			.user-avatar-container {
				width: 120rpx;
				height: 120rpx;
				border-radius: 50%;
				overflow: hidden;
				margin-bottom: 20rpx;
			}

			.user-avatar-image {
				width: 100%;
				height: 100%;
				object-fit: cover;
			}
	
	.avatar-button {
		padding: 16rpx 32rpx;
		background-color: #10b981;
		color: white;
		border: none;
		border-radius: 20rpx;
		font-size: 28rpx;
	}
	
	.form-section {
		display: flex;
		flex-direction: column;
		gap: 30rpx;
	}
	
	.form-item {
		display: flex;
		flex-direction: column;
		gap: 12rpx;
	}
	
	.label {
		font-size: 28rpx;
		color: #64748b;
		font-weight: 500;
	}
	
	.input-wrapper {
		position: relative;
	}
	
	.input-field {
		width: 100%;
		height: 88rpx;
		background-color: #f8fafc;
		border: 1rpx solid #e2e8f0;
		border-radius: 16rpx;
		padding: 0 24rpx;
		font-size: 32rpx;
		color: #1e293b;
	}
	
	.gender-options {
		display: flex;
		gap: 20rpx;
	}
	
	.gender-option {
		flex: 1;
		height: 88rpx;
		background-color: #f8fafc;
		border: 1rpx solid #e2e8f0;
		border-radius: 16rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 32rpx;
		color: #64748b;
	}
	
	.gender-option.selected {
		background-color: #d1fae5;
		border-color: #10b981;
		color: #10b981;
	}
	
	.button-section {
		padding: 0 30rpx 40rpx;
	}
	
	.save-button {
		width: 100%;
		height: 96rpx;
		background-color: #10b981;
		color: white;
		border: none;
		border-radius: 24rpx;
		font-size: 32rpx;
		font-weight: 500;
	}
</style>