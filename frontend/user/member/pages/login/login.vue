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
		
		<!-- 中间区域 - 登录表单 -->
		<view class="middle-section">
			<view class="login-card">
				<view class="card-header">
					<text class="card-title">欢迎回来</text>
					<text class="card-subtitle">请登录您的账号</text>
				</view>
				
				<view class="input-group">
					<view class="input-icon account-icon">
						<text class="icon-text">👤</text>
					</view>
					<input 
						class="input-field" 
						v-model="form.account" 
						placeholder="请输入账号"
						type="text"
					/>
				</view>
				
				<view class="input-group">
					<view class="input-icon password-icon">
						<text class="icon-text">🔒</text>
					</view>
					<input 
						class="input-field" 
						v-model="form.password" 
						placeholder="请输入密码"
						:type="showPassword ? 'text' : 'password'"
					/>
					<view class="toggle-icon" @click="togglePassword">
						<text class="toggle-icon-text">{{ showPassword ? '👁️' : '👁️‍🗨️' }}</text>
					</view>
				</view>
				
				<button class="login-btn" @click="handleLogin" :disabled="isLoading">
					<text>{{ isLoading ? '登录中...' : '登录' }}</text>
					<view class="btn-glow"></view>
				</button>
				
				<!-- 微信一键登录按钮 -->
				<button class="wechat-login-btn" @click="handleWechatLogin" :disabled="isLoading">
					<text class="wechat-icon">💬</text>
					<text>{{ isLoading ? '微信登录中...' : '微信一键登录' }}</text>
				</button>
				
				<view class="links">
					<text class="link-text" @click="goToRegister">注册新账号</text>
					<text class="link-text" @click="goToForgetPassword">找回密码</text>
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
			<text class="copyright">© 2026 颐养膳食 版权所有</text>
		</view>
	</view>
</template>

<script>
import { authService } from '../../api/auth.js';

export default {
	data() {
		return {
			form: {
				account: '',
				password: ''
			},
			showPassword: false,
			isLoading: false
		};
	},
	methods: {
		togglePassword() {
			this.showPassword = !this.showPassword;
		},
		async handleLogin() {
			// 表单验证
			if (!this.form.account) {
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
			
			try {
				this.isLoading = true;
				uni.showLoading({
					title: '登录中...',
					mask: true
				});
				
				console.log('=== 开始登录流程 ===');
				console.log('账号:', this.form.account);
				console.log('密码:', this.form.password);
				
				// 清除本地缓存，确保重新登录
				console.log('清除本地缓存...');
				uni.removeStorageSync('token');
				uni.removeStorageSync('user');
				console.log('本地缓存已清除');
				
				// 调用登录API
				console.log('调用登录API...');
				const response = await authService.login(this.form.account, this.form.password);
				
				console.log('=== 登录API调用成功 ===');
				console.log('响应数据:', response);
				
				// 验证响应数据
				if (!response || !response.access_token) {
					throw new Error('登录失败：服务器返回的数据格式不正确');
				}
				
				// 验证用户类型必须是member
				if (response.user.user_type !== 'member') {
					throw new Error('请使用家属端账号登录');
				}
				
				// 保存token和用户信息
				console.log('保存token和用户信息...');
				uni.setStorageSync('token', response.access_token);
				uni.setStorageSync('user', JSON.stringify(response.user));
				
				uni.hideLoading();
				uni.showToast({
					title: '登录成功',
					icon: 'success',
					duration: 1500
				});
				
				// 跳转到健康页面
				setTimeout(() => {
					console.log('跳转到健康页面...');
					uni.switchTab({
						url: '/pages/health/health'
					});
				}, 1500);
				
			} catch (error) {
				console.log('=== 登录失败 ===');
				console.error('错误详情:', error);
				
				this.isLoading = false;
				uni.hideLoading();
				
				let errorMessage = '登录失败，请检查网络或账号密码';
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
		goToRegister() {
			uni.navigateTo({
				url: '/pages/login/register'
			});
		},
		goToForgetPassword() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		showPrivacy() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		showTerms() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		async handleWechatLogin() {
			console.log('微信登录按钮被点击')
			this.isLoading = true;
			
			try {
				console.log('开始微信登录流程...')
				// 调用微信小程序登录API获取code
				const loginResult = await new Promise((resolve, reject) => {
					wx.login({
						success: resolve,
						fail: reject
					})
				})
				
				console.log('微信登录获取code成功:', loginResult)
				
				if (!loginResult.code) {
					throw new Error('获取微信登录code失败')
				}
				
				// 调用后端微信登录API
				const response = await authService.wechatLogin(loginResult.code, 'member')
				console.log('微信登录API调用成功:', response)
				
				// 验证用户类型必须是member
				if (response.user.user_type !== 'member') {
					throw new Error('请使用家属端账号登录')
				}
				
				// 保存token和用户信息
				console.log('保存token和用户信息...');
				uni.setStorageSync('token', response.access_token);
				uni.setStorageSync('user', JSON.stringify(response.user));
				
				uni.showToast({
					title: '微信登录成功',
					icon: 'success',
					duration: 1500
				});
				
				// 跳转到健康页面
				setTimeout(() => {
					console.log('跳转到健康页面...');
					uni.switchTab({
						url: '/pages/health/health'
					});
				}, 1500);
				
			} catch (error) {
				console.error('微信登录失败:', error)
				
				let errorMessage = '微信登录失败，请重试'
				
				if (error.message) {
					errorMessage = error.message
				}
				
				uni.showToast({
					title: errorMessage,
					icon: 'none',
					duration: 2000
				});
			} finally {
				this.isLoading = false;
			}
		}
	}
};
</script>

<style scoped>
.container {
	height: 100vh;
	background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: space-between;
	padding: 0 24px;
}

/* 背景装饰 */
.background-decoration {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	pointer-events: none;
}

.decoration-circle {
	position: absolute;
	border-radius: 50%;
	filter: blur(60px);
	opacity: 0.6;
}

.big-circle {
	width: 300px;
	height: 300px;
	background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.2) 100%);
	top: -100px;
	left: -100px;
	animation: float 6s ease-in-out infinite;
}

.medium-circle {
	width: 200px;
	height: 200px;
	background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(168, 85, 247, 0.15) 100%);
	bottom: -50px;
	right: -50px;
	animation: float 8s ease-in-out infinite reverse;
}

.small-circle {
	width: 120px;
	height: 120px;
	background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(244, 114, 182, 0.1) 100%);
	top: 60%;
	left: 70%;
	animation: float 10s ease-in-out infinite;
}

@keyframes float {
	0%, 100% { transform: translateY(0px) rotate(0deg); }
	50% { transform: translateY(-20px) rotate(180deg); }
}

/* 顶部区域 */
.top-section {
	width: 100%;
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: flex-end;
	position: relative;
	padding-top: 60px;
	padding-bottom: 30px;
}

.logo-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-bottom: 20px;
}

.logo-icon {
	width: 80px;
	height: 80px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border-radius: 20px;
	box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
	margin-bottom: 16px;
	position: relative;
	overflow: hidden;
	animation: logoGlow 3s ease-in-out infinite alternate;
}

.logo-inner {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	width: 40px;
	height: 40px;
	background: rgba(255, 255, 255, 0.2);
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.logo-icon::before {
	content: '';
	position: absolute;
	top: 0;
	left: -100%;
	width: 100%;
	height: 100%;
	background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
	animation: shine 2s infinite;
}

@keyframes shine {
	0% { left: -100%; }
	100% { left: 100%; }
}

@keyframes logoGlow {
	0% { box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4); }
	100% { box-shadow: 0 12px 48px rgba(99, 102, 241, 0.6); }
}

.logo-text {
	font-size: 40px;
	font-weight: 700;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
	text-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
	animation: textGlow 2s ease-in-out infinite alternate;
}

@keyframes textGlow {
	0% { text-shadow: 0 4px 16px rgba(99, 102, 241, 0.3); }
	100% { text-shadow: 0 6px 24px rgba(99, 102, 241, 0.5); }
}

.subtitle {
	font-size: 24px;
	color: #64748b;
	font-weight: 500;
	letter-spacing: 2px;
	text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 中间区域 - 登录表单 */
.middle-section {
	width: 100%;
	flex: 1;
	display: flex;
	align-items: flex-start;
	justify-content: center;
	padding-top: 20px;
}

.login-card {
	width: 100%;
	max-width: 400px;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	border-radius: 32px;
	padding: 32px 20px;
	box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
	position: relative;
	transform: translateY(-10px);
	transition: all 0.4s ease;
	border: 1px solid rgba(255, 255, 255, 0.2);
	box-sizing: border-box;
}

.login-card:hover {
	transform: translateY(-15px);
	box-shadow: 0 25px 80px rgba(0, 0, 0, 0.2);
}

.login-card::before {
	content: '';
	position: absolute;
	top: -1px;
	left: -1px;
	right: -1px;
	bottom: -1px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
	border-radius: 32px;
	z-index: -1;
	filter: blur(20px);
	opacity: 0.6;
}

.card-header {
	text-align: center;
	margin-bottom: 32px;
}

.card-title {
	font-size: 28px;
	font-weight: 700;
	color: #1e293b;
	margin-bottom: 8px;
	text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-subtitle {
	font-size: 16px;
	color: #64748b;
	font-weight: 400;
}

.input-group {
	position: relative;
	margin-bottom: 24px;
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
	transition: all 0.3s ease;
	backdrop-filter: blur(10px);
	box-sizing: border-box;
}

.input-field:focus {
	border-color: #6366f1;
	box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
	background: rgba(255, 255, 255, 0.95);
	transform: translateY(-2px);
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

.toggle-icon:hover {
	transform: translateY(-50%) scale(1.1);
}

.login-btn {
	width: 100%;
	height: 56px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 20px;
	color: #ffffff;
	font-size: 18px;
	font-weight: 600;
	position: relative;
	overflow: hidden;
	transition: all 0.3s ease;
	margin-bottom: 24px;
	box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
	display: flex;
	align-items: center;
	justify-content: center;
}

.login-btn::before {
	content: '';
	position: absolute;
	top: 0;
	left: -100%;
	width: 100%;
	height: 100%;
	background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
	transition: left 0.6s ease;
}

.login-btn:active {
	transform: scale(0.98);
}

.login-btn:hover::before {
	left: 100%;
}

.login-btn:hover {
	box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
	transform: translateY(-2px);
}

/* 微信登录按钮 */
.wechat-login-btn {
	width: 100%;
	height: 56px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 20px;
	color: #ffffff;
	font-size: 18px;
	font-weight: 600;
	position: relative;
	overflow: hidden;
	transition: all 0.3s ease;
	margin-bottom: 24px;
	box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 12px;
}

.wechat-login-btn:active {
	transform: scale(0.98);
}

.wechat-login-btn:hover {
	box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
	transform: translateY(-2px);
}

.wechat-icon {
	font-size: 24px;
}

.btn-glow {
	position: absolute;
	top: -50%;
	left: -50%;
	width: 200%;
	height: 200%;
	background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
	animation: glowPulse 3s ease-in-out infinite;
}

@keyframes glowPulse {
	0%, 100% { opacity: 0.3; transform: scale(0.8); }
	50% { opacity: 0.6; transform: scale(1); }
}

.links {
	display: flex;
	justify-content: space-between;
}

.link-text {
	font-size: 16px;
	color: #6366f1;
	cursor: pointer;
	transition: all 0.3s ease;
	font-weight: 500;
}

.link-text:hover {
	color: #8b5cf6;
	text-decoration: underline;
	transform: translateY(-1px);
}

/* 底部区域 */
.bottom-section {
	width: 100%;
	height: 15vh;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	position: relative;
}

.policy-links {
	display: flex;
	align-items: center;
	margin-bottom: 12px;
}

.policy-link {
	font-size: 16px;
	color: #6366f1;
	cursor: pointer;
	transition: all 0.3s ease;
	font-weight: 500;
	text-shadow: 0 1px 4px rgba(99, 102, 241, 0.2);
}

.policy-link:hover {
	color: #8b5cf6;
	text-decoration: underline;
	transform: translateY(-1px);
	text-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
}

.policy-separator {
	margin: 0 12px;
	color: #94a3b8;
	font-weight: 300;
}

.copyright {
	font-size: 14px;
	color: #94a3b8;
	font-weight: 400;
	text-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
	letter-spacing: 1px;
}
</style>