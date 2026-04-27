<template>
	<view class="login-container">
		<!-- 主题动画元素 -->
		<view class="theme-animation">
			<view class="elderly-character grandma">👵</view>
			<view class="food-plate">🍱</view>
			<view class="elderly-character grandpa">👴</view>
			<view class="food-item food-rice">🍚</view>
			<view class="food-item food-vegetable">🥗</view>
			<view class="food-item food-soup">🍲</view>
			<view class="food-item food-dumpling">🥟</view>
			<view class="food-item food-noodle">🍜</view>
			<view class="food-item food-egg">🥚</view>
			<view class="food-item food-meat">🥩</view>
		</view>
		
		<!-- 背景装饰动画 -->
		<view class="background-animation">
			<view class="decorative-food bg-food-1">🍞</view>
			<view class="decorative-food bg-food-2">🥖</view>
			<view class="decorative-food bg-food-3">🥟</view>
			<view class="decorative-food bg-food-4">🍤</view>
			<view class="decorative-food bg-food-5">🍎</view>
			<view class="decorative-food bg-food-6">🍊</view>
			<view class="decorative-food bg-food-7">🍌</view>
			<view class="decorative-food bg-food-8">🍋</view>
		</view>
		
		<!-- 顶部区域 -->
		<view class="top-section">
			<view class="logo-container">
				<image class="logo" :src="'/static/logo.png'" mode="aspectFit"></image>
				<text class="logo-text">颐养膳食</text>
			</view>
			<text class="subtitle">老人订餐系统</text>
		</view>
		
		<!-- 中间区域 - 登录表单 -->
		<view class="form-section">
			<view class="login-card">
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">👤</text>
						<input 
							class="input-normal" 
							placeholder="请输入账号" 
							v-model="formData.username"
							type="text"
						/>
					</view>
				</view>
				
				<view class="input-group">
					<view class="input-wrapper">
						<text class="input-icon">🔒</text>
						<input 
							class="input-normal" 
							placeholder="请输入密码" 
							v-model="formData.password"
							:type="showPassword ? 'text' : 'password'"
					 />
						<text class="eye-icon" @click="togglePassword">
							{{ showPassword ? '👁️' : '🙈' }}
						</text>
					</view>
				</view>
				
				<button type="button" class="btn-primary mt-20" @click="handleLogin">登录</button>
				
				<!-- 微信一键登录按钮 -->
				<button type="button" class="btn-wechat mt-16" @click="handleWechatLogin">
					<text class="wechat-icon">💬</text>
					<text>微信一键登录</text>
				</button>
			</view>
		</view>
		
		<!-- 底部区域 -->
		<view class="bottom-section">
			<view class="links">
				<text class="link-text" @click="goToRegister">注册新账号</text>
				<text class="link-text" @click="showDevelopmentMessage">找回密码</text>
			</view>
			<text class="copyright">© 2026 颐养膳食 版权所有</text>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	import CONFIG from '../../utils/config.js'
	
	export default {
		data() {
			return {
				formData: {
					username: '',
					password: ''
				},
				showPassword: false,
				loading: false
			}
		},
		onLoad() {
			console.log('登录页面加载完成')
			console.log('API配置:', CONFIG.api)
			console.log('API对象:', api)
			console.log('auth模块:', api.auth)
			console.log('login方法:', api.auth.login)
		},
		methods: {
			togglePassword() {
				this.showPassword = !this.showPassword
			},
			async handleLogin() {
				console.log('登录按钮被点击')
				console.log('用户名:', this.formData.username)
				console.log('密码:', this.formData.password)
				
				// 登录逻辑
				if (!this.formData.username) {
					uni.showToast({
						title: '请输入账号',
						icon: 'none'
					})
					return
				}
				if (!this.formData.password) {
					uni.showToast({
						title: '请输入密码',
						icon: 'none'
					})
					return
				}
				
				console.log('表单验证通过，准备调用API')
				this.loading = true
				
				try {
					console.log('开始调用登录API...')
					console.log('API基础URL:', CONFIG.api.baseUrl)
					// 调用后端登录API
					const response = await api.auth.login({
						username: this.formData.username,
						password: this.formData.password
					})
					console.log('登录API调用成功:', response)
					
					// 验证用户类型必须是elderly
					if (response.user.user_type !== 'elderly') {
						throw new Error('请使用老人端账号登录')
					}
					
					// 保存token和用户信息
					uni.setStorageSync('token', response.access_token)
					uni.setStorageSync('user', response.user)
					console.log('Token和用户信息保存成功')
					
					uni.showToast({
						title: '登录成功',
						icon: 'success'
					})
					
					// 跳转到首页
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}, 1000)
				} catch (error) {
					console.error('登录失败:', error)
					console.error('错误类型:', typeof error)
					
					// 处理不同类型的错误
					let errorMessage = '登录失败，请检查账号密码'
					
					if (typeof error === 'object') {
						if (error.errMsg) {
							// uni.request错误
							console.error('错误消息:', error.errMsg)
							errorMessage = '网络连接失败，请检查网络'
						} else if (error.message) {
							// 标准Error对象
							console.error('错误消息:', error.message)
							console.error('错误堆栈:', error.stack)
							errorMessage = error.message
						} else {
							// 其他对象类型错误
							console.error('错误对象:', JSON.stringify(error))
						}
					} else {
						// 字符串类型错误
						console.error('错误消息:', error)
						errorMessage = String(error)
					}
					
					uni.showToast({
						title: errorMessage,
						icon: 'none',
						duration: 2000
					})
				} finally {
					this.loading = false
					console.log('登录流程结束')
				}
			},
			goToRegister() {
				uni.navigateTo({
					url: '/pages/login/register'
				})
			},
			showDevelopmentMessage() {
				uni.showToast({
					title: '功能后续开发中...',
					icon: 'none',
					duration: 2000
				})
			},
			async handleWechatLogin() {
				console.log('微信登录按钮被点击')
				this.loading = true
				
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
					const response = await api.auth.wechatLogin({
						code: loginResult.code,
						user_type: 'elderly'
					})
					console.log('微信登录API调用成功:', response)
					
					// 验证用户类型必须是elderly
					if (response.user.user_type !== 'elderly') {
						throw new Error('请使用老人端账号登录')
					}
					
					// 保存token和用户信息
					uni.setStorageSync('token', response.access_token)
					uni.setStorageSync('user', response.user)
					console.log('Token和用户信息保存成功')
					
					uni.showToast({
						title: '微信登录成功',
						icon: 'success'
					})
					
					// 跳转到首页
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}, 1000)
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
					})
				} finally {
					this.loading = false
				}
			}
		}
	}
</script>

<style scoped>
	.login-container {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		background: linear-gradient(135deg, #FFF7F3 0%, #FFFAF7 100%);
		padding: var(--padding-page);
		position: relative;
		justify-content: flex-start;
		padding-top: 100px;
	}
	
	.login-container::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-image: radial-gradient(circle at 20% 50%, rgba(255, 122, 69, 0.1) 0%, transparent 50%),
							radial-gradient(circle at 80% 20%, rgba(64, 158, 255, 0.05) 0%, transparent 50%);
		pointer-events: none;
	}
	
	/* 主题动画元素 */
	.theme-animation {
		position: absolute;
		bottom: 165px;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		align-items: center;
		gap: 40px;
		z-index: 999;
	}
	
	.elderly-character {
		font-size: 48px;
		animation: elderlyWave 3s ease-in-out infinite;
	}
	
	.food-plate {
		font-size: 40px;
		animation: plateRotate 4s linear infinite;
	}
	
	.food-item {
		font-size: 24px;
		position: absolute;
		opacity: 0.8;
	}
	
	/* 老奶奶周围的食物 */
	.food-rice {
		top: -15px;
		left: -40px;
		animation: foodFloat 3s ease-in-out infinite;
		animation-delay: 0s;
	}
	
	.food-meat {
		bottom: -20px;
		left: -20px;
		animation: foodFloat 3s ease-in-out infinite;
		animation-delay: 1s;
	}
	
	.food-dumpling {
		top: -30px;
		left: -10px;
		animation: foodFloat 3s ease-in-out infinite;
		animation-delay: 0.5s;
	}
	
	/* 老爷爷周围的食物 */
	.food-vegetable {
		top: -20px;
		right: -40px;
		animation: foodFloat 3s ease-in-out infinite;
		animation-delay: 1s;
	}
	
	.food-noodle {
		bottom: -20px;
		right: -20px;
		animation: foodFloat 3s ease-in-out infinite;
		animation-delay: 1.5s;
	}
	
	.food-egg {
		top: -25px;
		right: -10px;
		animation: foodFloat 3s ease-in-out infinite;
		animation-delay: 2.5s;
	}
	
	/* 餐盘周围的食物 */
	.food-soup {
		bottom: -10px;
		left: 10px;
		animation: foodFloat 3s ease-in-out infinite;
		animation-delay: 2s;
	}
	
	@keyframes elderlyWave {
		0%, 100% {
			transform: rotate(0deg);
		}
		25% {
			transform: rotate(-5deg);
		}
		75% {
			transform: rotate(5deg);
		}
	}
	
	@keyframes plateRotate {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
	
	@keyframes foodFloat {
		0%, 100% {
			transform: translateY(0px);
		}
		50% {
			transform: translateY(-10px);
		}
	}
	
	/* 背景装饰动画 */
	.background-animation {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: -1;
	}
	
	.decorative-food {
		position: absolute;
		font-size: 24px;
		opacity: 0.08;
		animation: bgFloatAnimation 8s ease-in-out infinite;
	}
	
	.bg-food-1 {
		top: 20%;
		left: 10%;
		animation-delay: 0s;
	}
	
	.bg-food-2 {
		top: 30%;
		right: 15%;
		animation-delay: 1s;
	}
	
	.bg-food-3 {
		top: 60%;
		left: 20%;
		animation-delay: 2s;
	}
	
	.bg-food-4 {
		top: 70%;
		right: 25%;
		animation-delay: 3s;
	}
	
	.bg-food-5 {
		top: 40%;
		left: 8%;
		animation-delay: 4s;
	}
	
	.bg-food-6 {
		top: 50%;
		right: 12%;
		animation-delay: 5s;
	}
	
	.bg-food-7 {
		top: 80%;
		left: 15%;
		animation-delay: 6s;
	}
	
	.bg-food-8 {
		top: 85%;
		right: 8%;
		animation-delay: 7s;
	}
	
	@keyframes bgFloatAnimation {
		0%, 100% {
			transform: translateY(0px) rotate(0deg);
		}
		50% {
			transform: translateY(-30px) rotate(15deg);
		}
	}
	
	/* 顶部区域 */
	.top-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		position: relative;
		z-index: 1;
		margin-bottom: 40px;
	}
	
	.logo-container {
		display: flex;
		align-items: center;
		margin-bottom: 20px;
		padding: 20px;
		background: rgba(255, 255, 255, 0.8);
		border-radius: 16px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
		backdrop-filter: blur(10px);
	}
	
	.logo {
		width: 50px;
		height: 50px;
		margin-right: 16px;
		border-radius: 12px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}
	
	.logo-text {
		font-size: 28px;
		font-weight: 700;
		color: #FF7A45;
		text-shadow: 0 2px 4px rgba(255, 122, 69, 0.2);
	}
	
	.subtitle {
		font-size: 28px;
		color: #FF7A45;
		font-weight: 600;
		text-shadow: 0 2px 8px rgba(255, 122, 69, 0.3);
		letter-spacing: 2px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
	}
	
	/* 中间区域 */
	.form-section {
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		z-index: 1;
		margin-bottom: 60px;
	}
	
	.login-card {
		width: 100%;
		max-width: 420px;
		background: rgba(255, 255, 255, 0.95);
		border-radius: 20px;
		padding: 40px 30px;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
		backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.2);
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
		color: #FF7A45;
		z-index: 1;
	}
	
	.input-normal {
		padding-left: 60px;
		padding-right: 60px;
		height: 56px;
		font-size: 18px;
		border: 2px solid #E8E8E8;
		border-radius: 12px;
		background: rgba(255, 255, 255, 0.9);
		transition: all 0.3s ease;
	}
	
	.input-normal:focus {
		border-color: #FF7A45;
		box-shadow: 0 0 0 3px rgba(255, 122, 69, 0.1);
		outline: none;
	}
	
	.eye-icon {
		position: absolute;
		right: 20px;
		font-size: 24px;
		color: #999999;
		z-index: 1;
		cursor: pointer;
		transition: color 0.3s ease;
	}
	
	.eye-icon:hover {
		color: #FF7A45;
	}
	
	.btn-primary {
		height: 56px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		color: white;
		border: none;
		border-radius: 12px;
		font-size: 18px;
		font-weight: 600;
		box-shadow: 0 8px 24px rgba(255, 122, 69, 0.3);
		transition: all 0.3s ease;
		margin-top: 16px;
		text-align: center;
		line-height: 56px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.btn-primary:active {
		transform: scale(0.98);
		box-shadow: 0 4px 16px rgba(255, 122, 69, 0.2);
	}
	
	/* 微信登录按钮 */
	.btn-wechat {
		height: 56px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		color: white;
		border: none;
		border-radius: 12px;
		font-size: 18px;
		font-weight: 600;
		box-shadow: 0 8px 24px rgba(255, 122, 69, 0.3);
		transition: all 0.3s ease;
		margin-top: 16px;
		text-align: center;
		line-height: 56px;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 12px;
	}
	
	.btn-wechat:active {
		transform: scale(0.98);
		box-shadow: 0 4px 16px rgba(255, 122, 69, 0.2);
	}
	
	.wechat-icon {
		font-size: 24px;
	}
	
	/* 底部区域 */
	.bottom-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: flex-end;
		padding-bottom: 60px;
		position: relative;
		z-index: 1;
		flex-grow: 1;
	}
	
	.links {
		display: flex;
		justify-content: center;
		margin-bottom: 24px;
		background: rgba(255, 255, 255, 0.8);
		padding: 16px 32px;
		border-radius: 24px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
	}
	
	.link-text {
		font-size: 18px;
		color: #409EFF;
		margin: 0 24px;
		font-weight: 500;
		transition: color 0.3s ease;
	}
	
	.link-text:hover {
		color: #FF7A45;
	}
	
	.copyright {
		font-size: 14px;
		color: #999999;
		background: rgba(255, 255, 255, 0.6);
		padding: 8px 16px;
		border-radius: 12px;
		backdrop-filter: blur(10px);
	}
</style>