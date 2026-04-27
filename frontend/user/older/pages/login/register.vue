<template>
	<view class="register-container">
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
		

		
		<!-- 顶部导航 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">注册账号</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 注册表单 -->
		<view class="form-container">
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">👤</text>
					<input 
						class="input-normal" 
						placeholder="请输入姓名" 
						v-model="formData.name"
						type="text"
					/>
					<view class="input-decoration decoration-name">👵</view>
				</view>
			</view>
			
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">📞</text>
					<input 
						class="input-normal" 
						placeholder="请输入手机号" 
						v-model="formData.phone"
						type="number"
					/>
					<view class="input-decoration decoration-phone">📱</view>
				</view>
			</view>
			
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">🔐</text>
					<input 
						class="input-normal" 
						placeholder="请设置密码" 
						v-model="formData.password"
						type="password"
					/>
					<view class="input-decoration decoration-password">🔒</view>
				</view>
			</view>
			
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">🔐</text>
					<input 
						class="input-normal" 
						placeholder="请确认密码" 
						v-model="formData.confirmPassword"
						type="password"
					/>
					<view class="input-decoration decoration-confirm">✅</view>
				</view>
			</view>
			
			<view class="input-group">
				<view class="input-wrapper">
					<text class="input-icon">🎂</text>
					<input 
						class="input-normal" 
						placeholder="请输入年龄" 
						v-model="formData.age"
						type="number"
					/>
					<view class="input-decoration decoration-age">🎈</view>
				</view>
			</view>
			
			<view class="gender-group">
				<text class="gender-label">性别：</text>
				<view class="gender-options">
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
			
			<button class="btn-primary mt-20" @click="handleRegister">注册</button>
			
			<view class="login-link">
				<text class="link-text">已有账号？</text>
				<text class="primary-link" @click="goToLogin">立即登录</text>
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
					phone: '',
					password: '',
					confirmPassword: '',
					age: '',
					gender: 'male'
				}
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
			async handleRegister() {
				// 表单验证
				if (!this.formData.name) {
					uni.showToast({
						title: '请输入姓名',
						icon: 'none'
					})
					return
				}
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
				if (!this.formData.password) {
					uni.showToast({
						title: '请设置密码',
						icon: 'none'
					})
					return
				}
				if (this.formData.password.length< 6) {
					uni.showToast({
						title: '密码至少6位',
						icon: 'none'
					})
					return
				}
				if (this.formData.password !== this.formData.confirmPassword) {
					uni.showToast({
						title: '两次输入的密码不一致',
						icon: 'none'
					})
					return
				}
				if (!this.formData.age) {
					uni.showToast({
						title: '请输入年龄',
						icon: 'none'
					})
					return
				}
				
				try {
					// 调用后端注册API
					await api.auth.register({
						username: this.formData.phone,
						password: this.formData.password,
						user_type: 'elderly',
						profile: {
							name: this.formData.name,
							phone: this.formData.phone,
							age: this.formData.age,
							gender: this.formData.gender
						}
					})
					
					uni.showToast({
						title: '注册成功',
						icon: 'success'
					})
					
					// 跳转到登录页面
					setTimeout(() =>{
						uni.navigateTo({
							url: '/pages/login/login'
						})
					}, 1000)
				} catch (error) {
					console.error('注册失败:', error)
					uni.showToast({
						title: '注册失败，请稍后重试',
						icon: 'none'
					})
				}
			}
		}
	}
</script>

<style scoped>
	.register-container {
		min-height: 100vh;
		background: linear-gradient(135deg, #FFF7F3 0%, #FFFAF7 100%);
		position: relative;
	}

	.register-container::before {
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

	/* 导航栏 */
	.nav-bar {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		height: 120px;
		padding: 0 20px 20px 20px;
		background: rgba(255, 255, 255, 0.95);
		border-bottom: 1px solid rgba(0, 0, 0, 0.05);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		backdrop-filter: blur(10px);
	}

	.back-btn {
		font-size: 28px;
		color: #333333;
		padding: 8px;
		border-radius: 8px;
		transition: all 0.3s ease;
	}

	.back-btn:hover {
		background: rgba(0, 0, 0, 0.05);
	}

	.nav-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
	}

	.placeholder {
		width: 28px;
	}

	/* 表单容器 */
	.form-container {
		padding: 40px 20px 60px;
		position: relative;
		z-index: 1;
		max-width: 500px;
		margin: 0 auto;
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

	/* 输入框装饰元素 */
	.input-decoration {
		position: absolute;
		font-size: 20px;
		opacity: 0.6;
		animation: decorationFloat 4s ease-in-out infinite;
		z-index: 1;
	}

	.decoration-name {
		top: -10px;
		right: -15px;
		animation-delay: 0s;
	}

	.decoration-phone {
		top: -15px;
		right: -10px;
		animation-delay: 1s;
	}

	.decoration-password {
		top: -12px;
		right: -8px;
		animation-delay: 2s;
	}

	.decoration-confirm {
		top: -8px;
		right: -12px;
		animation-delay: 3s;
	}

	.decoration-age {
		top: -14px;
		right: -10px;
		animation-delay: 0.5s;
	}

	@keyframes decorationFloat {
		0%, 100% {
			transform: translateY(0px) rotate(0deg);
		}
		50% {
			transform: translateY(-15px) rotate(10deg);
		}
	}

	@keyframes shineEffect {
		0% {
			left: -100%;
		}
		100% {
			left: 100%;
		}
	}

	.input-normal {
		padding-left: 60px;
		padding-right: 60px;
		height: 56px;
		font-size: 18px;
		border: 2px solid #E8E8E8;
		border-radius: 16px;
		background: rgba(255, 255, 255, 0.95);
		transition: all 0.3s ease;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
		backdrop-filter: blur(10px);
		position: relative;
		overflow: hidden;
		width: 100%;
		box-sizing: border-box;
	}

	.input-normal:focus {
		border-color: #FF7A45;
		box-shadow: 0 0 0 3px rgba(255, 122, 69, 0.1), 0 8px 24px rgba(255, 122, 69, 0.15);
		outline: none;
		transform: translateY(-2px);
	}

	.input-normal:focus::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 122, 69, 0.1), transparent);
		animation: shineEffect 0.5s ease-in-out;
	}

	.btn-primary {
		height: 56px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		color: white;
		border: none;
		border-radius: 20px;
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
		position: relative;
		overflow: hidden;
		width: 100%;
		box-sizing: border-box;
	}

	.btn-primary:active {
		transform: scale(0.98);
		box-shadow: 0 4px 16px rgba(255, 122, 69, 0.2);
	}

	.btn-primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 12px 32px rgba(255, 122, 69, 0.4);
	}

	.btn-primary::before {
		content: '';
		position: absolute;
		top: 0;
		left: -100%;
		width: 100%;
		height: 100%;
		background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
		transition: left 0.5s ease;
	}

	.btn-primary:hover::before {
		left: 100%;
	}

	/* 性别选择 */
	.gender-group {
		display: flex;
		align-items: center;
		margin-bottom: 24px;
		padding: 24px;
		background: rgba(255, 255, 255, 0.95);
		border-radius: 20px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
		backdrop-filter: blur(10px);
		width: 100%;
		box-sizing: border-box;
	}

	.gender-label {
		font-size: 16px;
		color: #333333;
		margin-right: 20px;
		font-weight: 500;
	}

	.gender-options {
		display: flex;
		gap: 24px;
		flex: 1;
	}

	.gender-option {
		flex: 1;
		padding: 12px 24px;
		border: 2px solid #E8E8E8;
		border-radius: 24px;
		font-size: 16px;
		color: #666666;
		text-align: center;
		transition: all 0.3s ease;
		background: rgba(255, 255, 255, 0.8);
	}

	.gender-option:hover {
		border-color: #FF7A45;
		color: #FF7A45;
	}

	.gender-option.active {
		border-color: #FF7A45;
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		color: white;
		box-shadow: 0 4px 16px rgba(255, 122, 69, 0.3);
	}

	/* 登录链接 */
	.login-link {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-top: 24px;
		padding: 20px;
		background: rgba(255, 255, 255, 0.95);
		border-radius: 20px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
		backdrop-filter: blur(10px);
		width: 100%;
		box-sizing: border-box;
	}

	.link-text {
		font-size: 16px;
		color: #666666;
		font-weight: 500;
	}

	.primary-link {
		font-size: 16px;
		color: #FF7A45;
		font-weight: 600;
		margin-left: 8px;
		transition: color 0.3s ease;
	}

	.primary-link:hover {
		color: #FF8F6A;
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
</style>