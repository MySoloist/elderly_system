<template>
	<view class="edit-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">编辑个人信息</text>
			<text class="save-btn" @click="saveInfo">保存</text>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 编辑表单 -->
		<view v-else class="form-section">
			<!-- 基本信息 -->
			<view class="info-card">
				<view class="form-item">
					<text class="form-label">姓名</text>
					<input class="form-input" v-model="formData.name" placeholder="请输入姓名" />
				</view>
				<view class="form-item">
					<text class="form-label">年龄</text>
					<input class="form-input" v-model="formData.age" type="number" placeholder="请输入年龄" />
				</view>
				<view class="form-item">
					<text class="form-label">性别</text>
					<view class="gender-selector">
						<text 
							class="gender-option" 
							:class="{ active: formData.gender === 'male' }"
							@click="formData.gender = 'male'"
						>男</text>
						<text 
							class="gender-option" 
							:class="{ active: formData.gender === 'female' }"
							@click="formData.gender = 'female'"
						>女</text>
					</view>
				</view>
				<view class="form-item">
					<text class="form-label">联系电话</text>
					<input class="form-input" v-model="formData.phone" placeholder="请输入联系电话" />
				</view>
				<view class="form-item">
					<text class="form-label">地址</text>
					<textarea class="form-textarea" v-model="formData.address" placeholder="请输入详细地址"></textarea>
				</view>
			</view>
			
			<!-- 健康信息 -->
			<text class="section-title">健康信息</text>
			<view class="info-card">

				<view class="form-item">
					<text class="form-label">饮食偏好</text>
					<input class="form-input" v-model="formData.dietary_preference" placeholder="请输入饮食偏好" />
				</view>
				<view class="form-item">
					<text class="form-label">过敏史</text>
					<input class="form-input" v-model="formData.allergies" placeholder="请输入过敏史" />
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
				formData: {
					name: '',
					age: '',
					gender: '',
					phone: '',
					address: '',
					dietary_preference: '',
					allergies: ''
				},
				loading: false,
				saving: false
			}
		},
		onLoad() {
			this.loadUserInfo()
		},
		methods: {
			async loadUserInfo() {
				this.loading = true
				try {
					const response = await api.auth.getProfile()
					const profile = response.profile || {}
					this.formData = {
						name: profile.name || '',
						age: profile.age || '',
						gender: profile.gender || 'male',
						phone: profile.phone || '',
						address: profile.address || '',
						dietary_preference: profile.dietary_preferences || '',
						allergies: ''
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
			async saveInfo() {
				// 表单验证
				if (!this.formData.name) {
					uni.showToast({
						title: '请输入姓名',
						icon: 'none'
					})
					return
				}
				
				if (!this.formData.age || this.formData.age <= 0) {
					uni.showToast({
						title: '请输入有效的年龄',
						icon: 'none'
					})
					return
				}
				
				this.saving = true
				try {
					const updateData = {
						name: this.formData.name,
						phone: this.formData.phone,
						address: this.formData.address,
						dietary_preferences: this.formData.dietary_preference
					}
					
					const updatedProfile = await api.auth.updateProfile(updateData)
					
					// 更新本地存储中的用户信息
					const currentUser = uni.getStorageSync('user')
					if (currentUser) {
						currentUser.profile = updatedProfile.profile
						uni.setStorageSync('user', currentUser)
					}
					
					uni.showToast({
						title: '保存成功',
						icon: 'success'
					})
					// 返回上一页
					setTimeout(() => {
						uni.navigateBack()
					}, 1500)
				} catch (error) {
					console.error('保存失败:', error)
					uni.showToast({
						title: '保存失败，请重试',
						icon: 'none'
					})
				} finally {
					this.saving = false
				}
			},
			goBack() {
				uni.navigateBack()
			}
		}
	}
</script>

<style scoped>
	.edit-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 220px, #F5F5F5 100%);
		padding-bottom: 40px;
	}
	
	/* 顶部导航栏 */
	.top-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 58px;
		padding: 0 20px;
		background: rgba(255, 255, 255, 0.92);
		border-bottom: 1px solid rgba(255, 122, 69, 0.08);
		backdrop-filter: blur(8px);
	}
	
	.back-btn {
		font-size: 24px;
		color: #333333;
		width: 36px;
		text-align: center;
	}
	
	.nav-title {
		font-size: 19px;
		font-weight: 600;
		color: #333333;
		flex: 1;
		text-align: center;
	}
	
	.save-btn {
		font-size: 15px;
		color: #FF7A45;
		font-weight: 600;
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
	
	/* 表单区域 */
	.form-section {
		padding: 20px;
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin: 24px 0 16px 0;
	}
	
	.info-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.form-item {
		display: flex;
		flex-direction: column;
		margin-bottom: 20px;
	}
	
	.form-item:last-child {
		margin-bottom: 0;
	}
	
	.form-label {
		font-size: 14px;
		color: #666666;
		margin-bottom: 8px;
	}
	
	.form-input {
		height: 44px;
		padding: 0 12px;
		border: 1px solid #E0E0E0;
		border-radius: 8px;
		font-size: 14px;
		color: #333333;
		background-color: #F9F9F9;
	}
	
	.form-input:focus {
		border-color: #FF7A45;
		background-color: #FFFFFF;
	}
	
	.form-textarea {
		min-height: 80px;
		padding: 12px;
		border: 1px solid #E0E0E0;
		border-radius: 8px;
		font-size: 14px;
		color: #333333;
		background-color: #F9F9F9;
		resize: none;
	}
	
	.form-textarea:focus {
		border-color: #FF7A45;
		background-color: #FFFFFF;
	}
	
	/* 性别选择器 */
	.gender-selector {
		display: flex;
		gap: 16px;
	}
	
	.gender-option {
		flex: 1;
		height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 1px solid #E0E0E0;
		border-radius: 8px;
		font-size: 14px;
		color: #666666;
		background-color: #F9F9F9;
	}
	
	.gender-option.active {
		border-color: #FF7A45;
		color: #FF7A45;
		background-color: rgba(255, 122, 69, 0.05);
	}
</style>
