<template>
	<view class="forgot-container">
		<!-- 顶部导航 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">找回密码</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 找回密码表单 -->
		<view class="form-container">
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">📱</text>
					<input 
						class="input-normal" 
						placeholder="请输入手机号" 
						v-model="formData.phone"
						type="number"
					/>
				</view>
			</view>
			
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">📧</text>
					<input 
						class="input-normal" 
						placeholder="请输入验证码" 
						v-model="formData.code"
						type="number"
					/>
					<button class="code-btn" @click="sendCode">获取验证码</button>
				</view>
			</view>
			
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">🔒</text>
					<input 
						class="input-normal" 
						placeholder="请设置新密码" 
						v-model="formData.newPassword"
						type="password"
					/>
				</view>
			</view>
			
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">🔒</text>
					<input 
						class="input-normal" 
						placeholder="请确认新密码" 
						v-model="formData.confirmPassword"
						type="password"
					/>
				</view>
			</view>
			
			<button class="btn-primary mt-20" @click="handleReset">重置密码</button>
			
			<view class="login-link">
				<text class="link-text">想起密码了？</text>
				<text class="primary-link" @click="goToLogin">立即登录</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				formData: {
					phone: '',
					code: '',
					newPassword: '',
					confirmPassword: ''
				},
				countdown: 0
			}
		},
		methods: {
			goBack() {
				uni.navigateBack()
			},
			goToLogin() {
				uni.navigateTo({
					url: '/pages/login/login'
				})
			},
			sendCode() {
				if (!this.formData.phone) {
					uni.showToast({
						title: '请输入手机号',
						icon: 'none'
					})
					return
				}
				if (!/^1[3-9]\d{9}$/.test(this.formData.phone)) {
					uni.showToast({
						title: '请输入正确的手机号',
						icon: 'none'
					})
					return
				}
				
				// 模拟发送验证码
				this.countdown = 60
				uni.showToast({
					title: '验证码已发送',
					icon: 'success'
				})
				
				// 倒计时
				let timer = setInterval(() => {
					this.countdown--
					if (this.countdown<= 0) {
						clearInterval(timer)
					}
				}, 1000)
			},
			handleReset() {
				// 表单验证
				if (!this.formData.phone) {
					uni.showToast({
						title: '请输入手机号',
						icon: 'none'
					})
					return
				}
				if (!this.formData.code) {
					uni.showToast({
						title: '请输入验证码',
						icon: 'none'
					})
					return
				}
				if (!this.formData.newPassword) {
					uni.showToast({
						title: '请设置新密码',
						icon: 'none'
					})
					return
				}
				if (this.formData.newPassword.length< 6) {
					uni.showToast({
						title: '密码至少6位',
						icon: 'none'
					})
					return
				}
				if (this.formData.newPassword !== this.formData.confirmPassword) {
					uni.showToast({
						title: '两次输入的密码不一致',
						icon: 'none'
					})
					return
				}
				
				// 模拟重置密码成功
				uni.showToast({
					title: '密码重置成功',
					icon: 'success'
				})
				
				// 跳转到登录页面
				setTimeout(() =>{
					uni.navigateTo({
						url: '/pages/login/login'
					})
				}, 1000)
			}
		}
	}
</script>

<style scoped>
	.forgot-container {
		min-height: 100vh;
		background: linear-gradient(135deg, #FFF7F3 0%, #FFFAF7 100%);
	}
	
	/* 导航栏 */
	.nav-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 56px;
		padding: 0 var(--padding-page);
		background: rgba(255, 255, 255, 0.95);
		border-bottom: 1px solid rgba(0, 0, 0, 0.05);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		backdrop-filter: blur(10px);
	}
	
	.back-btn {
		font-size: 28px;
		color: var(--text-primary);
		padding: 8px;
		border-radius: 8px;
		transition: all 0.3s ease;
	}
	
	.back-btn:hover {
		background: rgba(0, 0, 0, 0.05);
	}
	
	.nav-title {
		font-size: var(--font-medium);
		font-weight: 600;
		color: var(--text-primary);
	}
	
	.placeholder {
		width: 28px;
	}
	
	/* 表单容器 */
	.form-container {
		padding: var(--padding-page);
	}
	
	.input-group {
		margin-bottom: 24px;
	}
	
	.input-wrapper {
		position: relative;
		display: flex;
		align-items: center;
	}
	
	.input-icon {
		position: absolute;
		left: 20px;
		font-size: 24px;
		color: var(--primary-color);
		z-index: 1;
	}
	
	.input-normal {
		padding-left: 60px;
		height: 56px;
		font-size: 18px;
		border: 2px solid #E8E8E8;
		border-radius: 12px;
		background: rgba(255, 255, 255, 0.9);
		transition: all 0.3s ease;
	}
	
	.input-normal:focus {
		border-color: var(--primary-color);
		box-shadow: 0 0 0 3px rgba(255, 122, 69, 0.1);
		outline: none;
	}
	
	.btn-primary {
		height: 56px;
		background: linear-gradient(135deg, var(--primary-color) 0%, #FF8F6A 100%);
		color: white;
		border: none;
		border-radius: 12px;
		font-size: 18px;
		font-weight: 600;
		box-shadow: 0 8px 24px rgba(255, 122, 69, 0.3);
		transition: all 0.3s ease;
		margin-top: 16px;
	}
	
	.btn-primary:active {
		transform: scale(0.98);
		box-shadow: 0 4px 16px rgba(255, 122, 69, 0.2);
	}
	
	/* 验证码按钮 */
	.code-btn {
		position: absolute;
		right: 12px;
		height: 40px;
		padding: 0 20px;
		border: none;
		border-radius: 20px;
		background: linear-gradient(135deg, var(--secondary-color) 0%, #66B1FF 100%);
		color: white;
		font-size: var(--font-normal);
		font-weight: 600;
		box-shadow: 0 4px 16px rgba(64, 158, 255, 0.3);
		transition: all 0.3s ease;
	}
	
	.code-btn:active {
		transform: scale(0.98);
		box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
	}
	
	.code-btn:disabled {
		background: #CCCCCC;
		color: #999999;
		box-shadow: none;
	}
	
	/* 登录链接 */
	.login-link {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-top: 24px;
		padding: 16px;
		background: rgba(255, 255, 255, 0.8);
		border-radius: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
	}
	
	.link-text {
		font-size: var(--font-normal);
		color: var(--text-secondary);
		font-weight: 500;
	}
	
	.primary-link {
		font-size: var(--font-normal);
		color: var(--primary-color);
		font-weight: 600;
		margin-left: 8px;
		transition: color 0.3s ease;
	}
	
	.primary-link:hover {
		color: #FF8F6A;
	}
</style>