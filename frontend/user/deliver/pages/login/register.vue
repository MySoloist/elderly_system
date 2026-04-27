<template>
	<view class="register-container">
		<view class="top-section">
			<view class="logo">
				<view class="logo-button">
					<view class="icon-circle">
						<text class="delivery-icon">🚴‍♂️</text>
					</view>
					<text class="logo-text">颐养膳食</text>
				</view>
			</view>
			<text class="subtitle">配送员注册</text>
		</view>
		
		<view class="form-section">
			<view class="form-card">
				<view class="input-group">
					<view class="input-icon">
						<text class="icon">📱</text>
					</view>
					<input v-model="form.username" type="text" placeholder="请输入账号" class="input-field" :disabled="loading" />
				</view>
				
				<view class="input-group">
					<view class="input-icon">
						<text class="icon">🔒</text>
					</view>
					<input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码" class="input-field" :disabled="loading" />
					<view class="eye-icon" @click="togglePassword">
						<text class="icon">{{ showPassword ? '👁️' : '👁️‍🗨️' }}</text>
					</view>
				</view>
				
				<view class="input-group">
					<view class="input-icon">
						<text class="icon">🔒</text>
					</view>
					<input v-model="form.confirmPassword" :type="showPassword ? 'text' : 'password'" placeholder="请确认密码" class="input-field" :disabled="loading" />
				</view>
				
				<view class="input-group">
					<view class="input-icon">
						<text class="icon">📝</text>
					</view>
					<input v-model="form.name" type="text" placeholder="请输入姓名" class="input-field" :disabled="loading" />
				</view>
				
				<view class="input-group">
					<view class="input-icon">
						<text class="icon">📞</text>
					</view>
					<input v-model="form.phone" type="tel" placeholder="请输入手机号" class="input-field" :disabled="loading" />
				</view>
				
				<button @click="register" class="register-button" :disabled="loading">
					{{ loading ? '注册中...' : '注册' }}
				</button>
			</view>
		</view>
		
		<view class="animation-section">
			<view class="delivery-animation">
				<!-- 云朵装饰 -->
				<view class="cloud cloud-1"></view>
				<view class="cloud cloud-2"></view>
				<view class="cloud cloud-3"></view>
				
				<!-- 餐品图标 -->
				<view class="food food-1">🍱</view>
				<view class="food food-2">🍜</view>
				<view class="food food-3">🍎</view>
				
				<view class="scooter">
					<view class="scooter-body">
						<view class="scooter-headlight"></view>
					</view>
					<view class="scooter-wheel front-wheel"></view>
					<view class="scooter-wheel back-wheel"></view>
					<view class="delivery-box">
						<text class="box-label">颐养膳食</text>
					</view>
					<view class="delivery-person">
						<view class="person-head"></view>
						<view class="person-body"></view>
					</view>
				</view>
			</view>
		</view>
		
		<view class="bottom-section">
			<view class="links">
				<text class="link" @click="goToLogin">返回登录</text>
				<text class="link" @click="goToForgot">找回密码</text>
			</view>
			<text class="copyright">© 2026 颐养膳食 版权所有</text>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				form: {
					username: '',
					password: '',
					confirmPassword: '',
					name: '',
					phone: ''
				},
				showPassword: false,
				loading: false
			}
		},
		methods: {
			togglePassword() {
				this.showPassword = !this.showPassword
			},
			async register() {
				// 表单验证
				if (!this.form.username) {
					uni.showToast({
						title: '请输入账号',
						icon: 'none'
					})
					return
				}
				if (!this.form.password) {
					uni.showToast({
						title: '请输入密码',
						icon: 'none'
					})
					return
				}
				if (this.form.password !== this.form.confirmPassword) {
					uni.showToast({
						title: '两次输入的密码不一致',
						icon: 'none'
					})
					return
				}
				if (!this.form.name) {
					uni.showToast({
						title: '请输入姓名',
						icon: 'none'
					})
					return
				}
				if (!this.form.phone) {
					uni.showToast({
						title: '请输入手机号',
						icon: 'none'
					})
					return
				}
				
				console.log('配送员注册开始:', this.form)
				this.loading = true
				uni.showLoading({
					title: '注册中...',
					mask: true
				})
				
				try {
					// 调用后端注册API
					const response = await api.auth.register({
						username: this.form.username,
						password: this.form.password,
						user_type: 'deliverer',
						profile: {
							name: this.form.name,
							phone: this.form.phone
						}
					})
					console.log('注册API调用成功:', response)
					
					uni.hideLoading()
					uni.showToast({
						title: '注册成功，请登录',
						icon: 'success',
						duration: 2000
					})
					
					setTimeout(() => {
						uni.navigateBack({
							delta: 1
						})
					}, 2000)
				} catch (error) {
					console.error('注册失败:', error)
					this.loading = false
					uni.hideLoading()
					
					let errorMessage = '注册失败，请稍后重试'
					if (error.message) {
						errorMessage = error.message
					} else if (error.response?.data?.detail) {
						errorMessage = error.response.data.detail
					}
					
					uni.showToast({
						title: errorMessage,
						icon: 'none',
						duration: 2000
					})
				}
			},
			goToLogin() {
				uni.navigateBack({
					delta: 1
				})
			},
			goToForgot() {
				uni.showToast({
					title: '找回密码功能开发中',
					icon: 'none'
				})
			}
		}
	}
</script>

<style scoped>
	.register-container {
		height: 100vh;
		display: flex;
		flex-direction: column;
		background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
	}

	.top-section {
		flex: 0.3;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: flex-end;
		padding-top: 100rpx;
		padding-bottom: 0rpx;
	}

	.logo {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 20rpx;
	}

	.logo-button {
		display: flex;
		align-items: center;
		gap: 30rpx;
		padding: 45rpx 40rpx;
		background-color: #10b981;
		border-radius: 20rpx;
		box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
	}

	.icon-circle {
		width: 80rpx;
		height: 80rpx;
		background-color: white;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.delivery-icon {
		font-size: 56rpx;
		color: #10b981;
	}

	.logo-text {
		font-size: 56rpx;
		font-weight: 700;
		color: white;
		letter-spacing: 2rpx;
	}

	.subtitle {
		font-size: 55rpx;
		color: #10b981;
		font-weight: 700;
		letter-spacing: 2rpx;
		margin-top: 40rpx;	
	}

	.form-section {
		flex: 0.4;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding: 40rpx 0 0 0;
	}

	.animation-section {
		flex: 0.15;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding: 40rpx 40rpx 0 40rpx;
	}

	.delivery-animation {
		width: 100%;
		height: 160rpx;
		position: relative;
		overflow: hidden;
	}

	/* 云朵动画 */
	.cloud {
		position: absolute;
		background-color: white;
		border-radius: 50%;
		opacity: 0.8;
	}

	.cloud-1 {
		width: 60rpx;
		height: 30rpx;
		top: 20rpx;
		left: 50rpx;
		animation: floatCloud 8s ease-in-out infinite;
	}

	.cloud-2 {
		width: 80rpx;
		height: 40rpx;
		top: 40rpx;
		right: 80rpx;
		animation: floatCloud 10s ease-in-out infinite 2s;
	}

	.cloud-3 {
		width: 40rpx;
		height: 20rpx;
		top: 60rpx;
		left: 150rpx;
		animation: floatCloud 12s ease-in-out infinite 4s;
	}

	/* 餐品图标动画 */
	.food {
		position: absolute;
		font-size: 32rpx;
		animation: floatFood 3s ease-in-out infinite;
	}

	.food-1 {
		top: 30rpx;
		left: 100rpx;
		animation-delay: 0s;
	}

	.food-2 {
		top: 50rpx;
		right: 120rpx;
		animation-delay: 1s;
	}

	.food-3 {
		top: 70rpx;
		left: 200rpx;
		animation-delay: 2s;
	}

	.scooter {
		position: absolute;
		left: -200rpx;
		top: 60rpx;
		animation: moveScooter 4s linear infinite;
	}

	.scooter-body {
		width: 140rpx;
		height: 45rpx;
		background-color: #10b981;
		border-radius: 25rpx;
		position: relative;
	}

	.scooter-headlight {
		width: 15rpx;
		height: 15rpx;
		background-color: #fbbf24;
		border-radius: 50%;
		position: absolute;
		left: 10rpx;
		top: 15rpx;
		box-shadow: 0 0 20rpx #fbbf24;
	}

	.scooter-wheel {
		width: 35rpx;
		height: 35rpx;
		background-color: #333;
		border-radius: 50%;
		position: absolute;
		bottom: -17rpx;
		animation: rotateWheel 1s linear infinite;
	}

	.front-wheel {
		left: 15rpx;
	}

	.back-wheel {
		right: 15rpx;
	}

	.delivery-box {
		width: 70rpx;
		height: 45rpx;
		background-color: #ef4444;
		border-radius: 10rpx;
		position: absolute;
		top: -50rpx;
		left: 35rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.box-label {
		color: white;
		font-size: 14rpx;
		font-weight: bold;
	}

	.delivery-person {
		position: absolute;
		top: -65rpx;
		left: 50rpx;
	}

	.person-head {
		width: 25rpx;
		height: 25rpx;
		background-color: #ff6b6b;
		border-radius: 50%;
		position: absolute;
		top: -10rpx;
		left: 10rpx;
	}

	.person-body {
		width: 30rpx;
		height: 40rpx;
		background-color: #3b82f6;
		border-radius: 15rpx;
	}

	/* 动画定义 */
	@keyframes moveScooter {
		0% {
			left: -200rpx;
			transform: translateY(0);
		}
		25% {
			transform: translateY(-5rpx);
		}
		75% {
			transform: translateY(5rpx);
		}
		100% {
			left: calc(100% + 200rpx);
			transform: translateY(0);
		}
	}

	@keyframes rotateWheel {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	@keyframes floatCloud {
		0%, 100% {
			transform: translateX(0) translateY(0);
		}
		50% {
			transform: translateX(20rpx) translateY(-10rpx);
		}
	}

	@keyframes floatFood {
		0%, 100% {
			transform: translateY(0) rotate(0deg);
		}
		50% {
			transform: translateY(-10rpx) rotate(10deg);
		}
	}

	.form-card {
		width: 100%;
		max-width: 420px;
		background-color: white;
		border-radius: 32rpx;
		padding: 60rpx 40rpx;
		box-shadow: 0 4px 16px rgba(0,0,0,0.12);
		box-sizing: border-box;
	}

	.input-group {
		display: flex;
		align-items: center;
		height: 96rpx;
		border: 1rpx solid #10b981;
		border-radius: 16rpx;
		padding: 0 30rpx;
		margin-bottom: 30rpx;
		background-color: white;
		box-sizing: border-box;
	}

	.input-field::placeholder {
		color: #94a3b8;
		font-weight: 400;
	}

	.input-icon {
		margin-right: 20rpx;
	}

	.icon {
		font-size: 32rpx;
	}

	.input-field {
		flex: 1;
		height: 100%;
		font-size: 34rpx;
		color: #1e293b;
		font-weight: 500;
		letter-spacing: 1rpx;
		border: none;
		outline: none;
	}

	.eye-icon {
		margin-left: 20rpx;
	}

	.register-button {
		width: 100%;
		height: 96rpx;
		background-color: #10b981;
		color: white;
		border: none;
		border-radius: 16rpx;
		font-size: 36rpx;
		font-weight: 600;
		letter-spacing: 2rpx;
		margin-top: 20rpx;
		box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
	}

	.register-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.bottom-section {
		flex: 0.2;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding-bottom: 60rpx;
	}

	.links {
		display: flex;
		gap: 80rpx;
		margin-bottom: 40rpx;
		padding: 25rpx 60rpx;
		background-color: white;
		border-radius: 25rpx;
		box-shadow: 0 2px 8px rgba(0,0,0,0.08);
	}

	.link {
		font-size: 42rpx;
		color: #7699d1ff;
		font-weight: 500;
	}

	.copyright {
		font-size: 28rpx;
		color: #64748b;
		font-weight: 400;
		margin-bottom: 60rpx;
	}
</style>
