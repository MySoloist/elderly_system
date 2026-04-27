<template>
	<view class="container">
		<!-- 背景装饰 -->
		<view class="background-decoration">
			<view class="decoration-circle big-circle"></view>
			<view class="decoration-circle medium-circle"></view>
			<view class="decoration-circle small-circle"></view>
		</view>
		
		<!-- 顶部区域 -->
		<view class="top-section">
			<view class="logo-container">
				<view class="logo-icon">
					<view class="logo-inner"></view>
				</view>
				<text class="logo-text">颐养膳食</text>
			</view>
			<text class="subtitle">家属端</text>
		</view>
		
		<!-- 中间区域 - 注册表单 -->
		<view class="middle-section">
			<view class="login-card">
				<view class="card-header">
					<text class="card-title">创建账号</text>
					<text class="card-subtitle">请填写以下信息完成注册</text>
				</view>
				
				<view class="input-group">
					<view class="input-wrapper">
						<view class="input-icon account-icon">
							<text class="icon-text">👤</text>
						</view>
						<input 
							v-model="form.username" 
							type="text" 
							placeholder="请输入账号" 
							class="input-field"
							:disabled="isLoading"
						/>
					</view>
					
					<view class="input-wrapper">
						<view class="input-icon password-icon">
							<text class="icon-text">🔒</text>
						</view>
						<input 
							v-model="form.password" 
							:type="showPassword ? 'text' : 'password'" 
							placeholder="请输入密码" 
							class="input-field"
							:disabled="isLoading"
						/>
						<view class="toggle-icon" @click="togglePassword">
							<text class="toggle-icon-text">{{ showPassword ? '👁️' : '👁️‍🗨️' }}</text>
						</view>
					</view>
					
					<view class="input-wrapper">
						<view class="input-icon password-icon">
							<text class="icon-text">🔒</text>
						</view>
						<input 
							v-model="form.confirmPassword" 
							:type="showPassword ? 'text' : 'password'" 
							placeholder="请确认密码" 
							class="input-field"
							:disabled="isLoading"
						/>
					</view>
					
					<view class="input-wrapper">
						<view class="input-icon name-icon">
							<text class="icon-text">📝</text>
						</view>
						<input 
							v-model="form.name" 
							type="text" 
							placeholder="请输入姓名" 
							class="input-field"
							:disabled="isLoading"
						/>
					</view>
					
					<view class="input-wrapper">
						<view class="input-icon phone-icon">
							<text class="icon-text">📞</text>
						</view>
						<input 
							v-model="form.phone" 
							type="tel" 
							placeholder="请输入手机号" 
							class="input-field"
							:disabled="isLoading"
						/>
					</view>
				</view>
				
				<button class="login-btn" @click="handleRegister" :disabled="isLoading">
					<text>{{ isLoading ? '注册中...' : '注册' }}</text>
					<view class="btn-glow"></view>
				</button>
				
				<view class="links">
					<text class="link-text" @click="goToLogin">返回登录</text>
				</view>
			</view>
		</view>
		
		<!-- 底部区域 -->
		<view class="bottom-section">
			<view class="policy-links">
				<text class="policy-link" @click="showPrivacy">隐私政策</text>
				<text class="policy-separator">|</text>
				<text class="policy-link" @click="showTerms">服务条款</text>
			</view>
			<text class="copyright">© 2024 颐养膳食 版权所有</text>
		</view>
	</view>
</template>

<script>
import { authService } from '../../api/auth.js';

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
			isLoading: false
		};
	},
	methods: {
		togglePassword() {
			this.showPassword = !this.showPassword;
		},
		async handleRegister() {
			// 表单验证
			if (!this.form.username) {
				uni.showToast({
					title: '请输入账号',
					icon: 'none'
				});
				return;
			}
			if (!this.form.password) {
				uni.showToast({
					title: '请输入密码',
					icon: 'none'
				});
				return;
			}
			if (this.form.password !== this.form.confirmPassword) {
				uni.showToast({
					title: '两次输入的密码不一致',
					icon: 'none'
				});
				return;
			}
			if (!this.form.name) {
				uni.showToast({
					title: '请输入姓名',
					icon: 'none'
				});
				return;
			}
			if (!this.form.phone) {
				uni.showToast({
					title: '请输入手机号',
					icon: 'none'
				});
				return;
			}
			
			try {
				this.isLoading = true;
				uni.showLoading({
					title: '注册中...',
					mask: true
				});
				
				console.log('=== 开始注册流程 ===');
				console.log('注册信息:', this.form);
				
				// 调用注册API
				const response = await authService.register({
					username: this.form.username,
					password: this.form.password,
					user_type: 'member',
					profile: {
						name: this.form.name,
						phone: this.form.phone
					}
				});
				
				console.log('=== 注册成功 ===');
				console.log('响应数据:', response);
				
				uni.hideLoading();
				uni.showToast({
					title: '注册成功，请登录',
					icon: 'success',
					duration: 2000
				});
				
				// 跳转到登录页面
				setTimeout(() => {
					uni.navigateBack({
						delta: 1
					});
				}, 2000);
				
			} catch (error) {
				console.log('=== 注册失败 ===');
				console.error('错误详情:', error);
				
				this.isLoading = false;
				uni.hideLoading();
				
				let errorMessage = '注册失败，请稍后重试';
				if (error.response?.data?.detail) {
					errorMessage = error.response.data.detail;
				} else if (error.message) {
					errorMessage = error.message;
				}
				
				console.log('显示错误提示:', errorMessage);
				uni.showToast({
					title: errorMessage,
					icon: 'none',
					duration: 2000
				});
			}
		},
		goToLogin() {
			uni.navigateBack({
				delta: 1
			});
		},
		showPrivacy() {
			uni.showToast({
				title: '隐私政策内容',
				icon: 'none',
				duration: 2000
			});
		},
		showTerms() {
			uni.showToast({
				title: '服务条款内容',
				icon: 'none',
				duration: 2000
			});
		}
	}
};
</script>

<style scoped>
.container {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
	position: relative;
	overflow: hidden;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.background-decoration {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	pointer-events: none;
	z-index: 0;
}

.decoration-circle {
	position: absolute;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.1);
	backdrop-filter: blur(10px);
}

.big-circle {
	width: 300rpx;
	height: 300rpx;
	top: 100rpx;
	right: -100rpx;
	animation: float 6s ease-in-out infinite;
}

.medium-circle {
	width: 200rpx;
	height: 200rpx;
	bottom: 200rpx;
	left: -50rpx;
	animation: float 8s ease-in-out infinite reverse;
}

.small-circle {
	width: 100rpx;
	height: 100rpx;
	top: 50%;
	left: 20%;
	animation: float 4s ease-in-out infinite;
}

@keyframes float {
	0%, 100% {
		transform: translateY(0px);
	}
	50% {
		transform: translateY(-20px);
	}
}

.top-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding-top: 120rpx;
	z-index: 1;
}

.logo-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-bottom: 20rpx;
}

.logo-icon {
	width: 120rpx;
	height: 120rpx;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.2);
	backdrop-filter: blur(10px);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: 20rpx;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.logo-inner {
	width: 80rpx;
	height: 80rpx;
	border-radius: 50%;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.logo-text {
	font-size: 48rpx;
	font-weight: 700;
	color: #ffffff;
	text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
	font-size: 24rpx;
	color: rgba(255, 255, 255, 0.8);
	margin-bottom: 80rpx;
}

.middle-section {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 0 40rpx;
	z-index: 1;
}

.login-card {
	width: 100%;
	max-width: 350px;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	border-radius: 24px;
	padding: 40px 24px;
	box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
	box-sizing: border-box;
}

.card-header {
	text-align: center;
	margin-bottom: 32px;
}

.card-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 8px;
	display: block;
}

.card-subtitle {
	font-size: 14px;
	color: #64748b;
	display: block;
}

.input-group {
	margin-bottom: 24px;
}

.input-wrapper {
	position: relative;
	margin-bottom: 20px;
}

.input-field {
	width: 100%;
	height: 56px;
	padding: 0 16px 0 56px;
	border: 2px solid rgba(99, 102, 241, 0.3);
	border-radius: 16px;
	font-size: 16px;
	color: #1e293b;
	background: rgba(255, 255, 255, 0.8);
	outline: none;
	transition: all 0.3s ease;
	box-sizing: border-box;
	backdrop-filter: blur(10px);
}

.input-field:focus {
	border-color: #6366f1;
	box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
	background: rgba(255, 255, 255, 0.95);
	transform: translateY(-2px);
}

.input-field:disabled {
	background: #f8fafc;
	color: #94a3b8;
}

.input-icon {
	position: absolute;
	left: 16px;
	top: 50%;
	transform: translateY(-50%);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 10;
}

.icon-text {
	font-size: 24px;
	color: #64748b;
}

.toggle-icon {
	position: absolute;
	right: 16px;
	top: 50%;
	transform: translateY(-50%);
	font-size: 24px;
	cursor: pointer;
	transition: all 0.3s ease;
}

.toggle-icon-text {
	font-size: 24px;
	color: #64748b;
}

.login-btn {
	width: 100%;
	height: 56px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	color: #ffffff;
	border: none;
	border-radius: 20px;
	font-size: 18px;
	font-weight: 600;
	position: relative;
	overflow: hidden;
	cursor: pointer;
	transition: all 0.3s ease;
	margin-bottom: 24px;
	box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
	display: flex;
	align-items: center;
	justify-content: center;
}

.login-btn:active {
	transform: scale(0.98);
}

.login-btn:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.btn-glow {
	position: absolute;
	top: 0;
	left: -100%;
	width: 50%;
	height: 100%;
	background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
	transition: left 0.5s ease;
}

.login-btn:hover .btn-glow {
	left: 100%;
}

.links {
	display: flex;
	justify-content: center;
}

.link-text {
	font-size: 14px;
	color: #6366f1;
	text-decoration: underline;
	cursor: pointer;
	transition: color 0.3s ease;
}

.link-text:active {
	color: #8b5cf6;
}

.bottom-section {
	padding: 24px;
	text-align: center;
	z-index: 1;
}

.policy-links {
	display: flex;
	justify-content: center;
	align-items: center;
	margin-bottom: 12px;
}

.policy-link {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.8);
	text-decoration: underline;
	cursor: pointer;
	transition: color 0.3s ease;
}

.policy-link:active {
	color: #ffffff;
}

.policy-separator {
	margin: 0 12px;
	color: rgba(255, 255, 255, 0.5);
	font-size: 12px;
}

.copyright {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
}
</style>