<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">设置</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 设置内容 -->
		<view class="settings-content">
			<!-- 账号安全 -->
			<view class="setting-section">
				<text class="section-title">账号安全</text>
				<view class="setting-item" @click="changePassword">
					<view class="item-left">
						<view class="item-icon password-icon"></view>
						<text class="item-text">修改密码</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="changePhone">
					<view class="item-left">
						<view class="item-icon phone-icon"></view>
						<text class="item-text">修改手机号</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="bindEmail">
					<view class="item-left">
						<view class="item-icon email-icon"></view>
						<text class="item-text">绑定邮箱</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
			</view>
			
			<!-- 隐私设置 -->
			<view class="setting-section">
				<text class="section-title">隐私设置</text>
				<view class="setting-item" @click="privacyPermission">
					<view class="item-left">
						<view class="item-icon privacy-icon"></view>
						<text class="item-text">隐私权限管理</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="dataPrivacy">
					<view class="item-left">
						<view class="item-icon data-icon"></view>
						<text class="item-text">数据隐私设置</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="clearHistory">
					<view class="item-left">
						<view class="item-icon clear-icon"></view>
						<text class="item-text">清除浏览记录</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
			</view>
			
			<!-- 应用设置 -->
			<view class="setting-section">
				<text class="section-title">应用设置</text>
				<view class="setting-item" @click="clearCache">
					<view class="item-left">
						<view class="item-icon cache-icon"></view>
						<text class="item-text">清除缓存</text>
					</view>
					<text class="cache-size">12.3MB</text>
				</view>
				<view class="setting-item" @click="notificationSettings">
					<view class="item-left">
						<view class="item-icon notification-icon"></view>
						<text class="item-text">推送通知设置</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="soundSettings">
					<view class="item-left">
						<view class="item-icon sound-icon"></view>
						<text class="item-text">声音与振动</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="languageSettings">
					<view class="item-left">
						<view class="item-icon language-icon"></view>
						<text class="item-text">语言设置</text>
					</view>
					<text class="item-value">简体中文</text>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="themeSettings">
					<view class="item-left">
						<view class="item-icon theme-icon"></view>
						<text class="item-text">主题设置</text>
					</view>
					<text class="item-value">默认</text>
					<text class="item-arrow">›</text>
				</view>
			</view>
			
			<!-- 关于 -->
			<view class="setting-section">
				<text class="section-title">关于</text>
				<view class="setting-item" @click="aboutUs">
					<view class="item-left">
						<view class="item-icon about-icon"></view>
						<text class="item-text">关于我们</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="checkUpdate">
					<view class="item-left">
						<view class="item-icon update-icon"></view>
						<text class="item-text">检查更新</text>
					</view>
					<text class="item-value">v1.0.0</text>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="userAgreement">
					<view class="item-left">
						<view class="item-icon agreement-icon"></view>
						<text class="item-text">用户协议</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
				<view class="setting-item" @click="privacyPolicy">
					<view class="item-left">
						<view class="item-icon policy-icon"></view>
						<text class="item-text">隐私政策</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
			</view>
			
			<!-- 退出登录 -->
			<button class="logout-btn" @click="logout">
				<text class="logout-text">退出登录</text>
			</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			cacheSize: '12.3MB'
		};
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		changePassword() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		changePhone() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		bindEmail() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		privacyPermission() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		dataPrivacy() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		clearHistory() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		clearCache() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		notificationSettings() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		soundSettings() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		languageSettings() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		themeSettings() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		aboutUs() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		checkUpdate() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		userAgreement() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		privacyPolicy() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
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
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background-color: #f8fafc;
	position: relative;
	overflow-x: hidden;
}

/* 顶部导航 */
.top-nav {
	display: flex;
	align-items: center;
	padding: 20px 24px;
	background: #ffffff;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
	position: sticky;
	top: 0;
	z-index: 100;
}

.back-btn {
	width: 40px;
	height: 40px;
	border-radius: 50%;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 16px;
	transition: all 0.3s ease;
}

.back-btn:active {
	transform: scale(0.95);
	background: #e2e8f0;
}

.back-icon {
	font-size: 24px;
	color: #6366f1;
}

.page-title {
	flex: 1;
	font-size: 20px;
	font-weight: 600;
	color: #1e293b;
	text-align: center;
}

.nav-right {
	width: 40px;
}

/* 设置内容 */
.settings-content {
	padding: 24px 24px 40px;
}

/* 设置区域 */
.setting-section {
	background: #ffffff;
	border-radius: 16px;
	margin-bottom: 24px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.6);
	overflow: hidden;
}

.section-title {
	display: block;
	font-size: 14px;
	font-weight: 600;
	color: #64748b;
	padding: 16px 16px 8px;
}

/* 设置项 */
.setting-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	height: 60px;
	padding: 0 16px;
	border-top: 1px solid rgba(226, 232, 240, 0.4);
	transition: all 0.3s ease;
}

.setting-item:active {
	background-color: #f8fafc;
}

.setting-item:first-child {
	border-top: none;
}

.item-left {
	display: flex;
	align-items: center;
	flex: 1;
}

.item-icon {
	width: 32px;
	height: 32px;
	border-radius: 8px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 12px;
	box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
}

.password-icon::before {
	content: '🔒';
	font-size: 16px;
}

.phone-icon::before {
	content: '📱';
	font-size: 16px;
}

.email-icon::before {
	content: '📧';
	font-size: 16px;
}

.privacy-icon::before {
	content: '🔐';
	font-size: 16px;
}

.data-icon::before {
	content: '📊';
	font-size: 16px;
}

.clear-icon::before {
	content: '🗑️';
	font-size: 16px;
}

.cache-icon::before {
	content: '💾';
	font-size: 16px;
}

.notification-icon::before {
	content: '🔔';
	font-size: 16px;
}

.sound-icon::before {
	content: '🔊';
	font-size: 16px;
}

.language-icon::before {
	content: '🌐';
	font-size: 16px;
}

.theme-icon::before {
	content: '🎨';
	font-size: 16px;
}

.about-icon::before {
	content: 'ℹ️';
	font-size: 16px;
}

.update-icon::before {
	content: '🔄';
	font-size: 16px;
}

.agreement-icon::before {
	content: '📄';
	font-size: 16px;
}

.policy-icon::before {
	content: '📋';
	font-size: 16px;
}

.item-text {
	font-size: 16px;
	color: #1e293b;
	font-weight: 500;
}

.item-arrow {
	font-size: 20px;
	color: #64748b;
	margin-left: 8px;
}

.item-value {
	font-size: 14px;
	color: #64748b;
	margin-right: 8px;
}

.cache-size {
	font-size: 14px;
	color: #64748b;
}

/* 退出登录按钮 */
.logout-btn {
	width: 100%;
	height: 48px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 12px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 500;
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.3s ease;
}

.logout-btn:active {
	transform: scale(0.98);
	box-shadow: 0 2px 6px rgba(99, 102, 241, 0.2);
}

.logout-text {
	
}
</style>
