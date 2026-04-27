<template>
	<view class="settings-container">
		<view class="settings-section">
			<text class="section-title">通知设置</text>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">🔔</text>
					<text class="setting-label">新订单通知</text>
				</view>
				<switch :checked="notificationSettings.newOrder" @change="(e) => { notificationSettings.newOrder = e.detail.value; saveSettings(); }" class="setting-switch" />
			</view>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">📞</text>
					<text class="setting-label">语音提醒</text>
				</view>
				<switch :checked="notificationSettings.voiceAlert" @change="(e) => { notificationSettings.voiceAlert = e.detail.value; saveSettings(); }" class="setting-switch" />
			</view>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">⏰</text>
					<text class="setting-label">配送提醒</text>
				</view>
				<switch :checked="notificationSettings.deliveryReminder" @change="(e) => { notificationSettings.deliveryReminder = e.detail.value; saveSettings(); }" class="setting-switch" />
			</view>
		</view>
		
		<view class="settings-section">
			<text class="section-title">账号安全</text>
			<view class="setting-item" @click="changePassword">
				<view class="setting-info">
					<text class="setting-icon">🔒</text>
					<text class="setting-label">修改密码</text>
				</view>
				<text class="setting-arrow">›</text>
			</view>
			<view class="setting-item" @click="changePhone">
				<view class="setting-info">
					<text class="setting-icon">📱</text>
					<text class="setting-label">更换手机号</text>
				</view>
				<text class="setting-arrow">›</text>
			</view>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">🔐</text>
					<text class="setting-label">实名认证</text>
				</view>
				<text class="setting-status completed">已认证</text>
			</view>
		</view>
		
		<view class="settings-section">
			<text class="section-title">隐私设置</text>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">📍</text>
					<text class="setting-label">位置权限</text>
				</view>
				<switch :checked="privacySettings.location" @change="(e) => { privacySettings.location = e.detail.value; saveSettings(); }" class="setting-switch" />
			</view>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">📸</text>
					<text class="setting-label">相机权限</text>
				</view>
				<switch :checked="privacySettings.camera" @change="(e) => { privacySettings.camera = e.detail.value; saveSettings(); }" class="setting-switch" />
			</view>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">🎤</text>
					<text class="setting-label">麦克风权限</text>
				</view>
				<switch :checked="privacySettings.microphone" @change="(e) => { privacySettings.microphone = e.detail.value; saveSettings(); }" class="setting-switch" />
			</view>
		</view>
		
		<view class="settings-section">
			<text class="section-title">其他设置</text>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">🌙</text>
					<text class="setting-label">深色模式</text>
				</view>
				<switch :checked="otherSettings.darkMode" @change="(e) => { otherSettings.darkMode = e.detail.value; saveSettings(); }" class="setting-switch" />
			</view>
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-icon">🌐</text>
					<text class="setting-label">语言设置</text>
				</view>
				<text class="setting-value">简体中文</text>
			</view>
			<view class="setting-item" @click="clearCache">
				<view class="setting-info">
					<text class="setting-icon">🗑️</text>
					<text class="setting-label">清除缓存</text>
				</view>
				<text class="setting-cache">{{ cacheSize }}</text>
			</view>
		</view>
		
		<view class="settings-section">
			<text class="section-title">关于</text>
			<view class="setting-item" @click="checkUpdate">
				<view class="setting-info">
					<text class="setting-icon">📱</text>
					<text class="setting-label">检查更新</text>
				</view>
				<text class="setting-value">v1.0.0</text>
			</view>
			<view class="setting-item" @click="userAgreement">
				<view class="setting-info">
					<text class="setting-icon">📄</text>
					<text class="setting-label">用户协议</text>
				</view>
				<text class="setting-arrow">›</text>
			</view>
			<view class="setting-item" @click="privacyPolicy">
				<view class="setting-info">
					<text class="setting-icon">🔒</text>
					<text class="setting-label">隐私政策</text>
				</view>
				<text class="setting-arrow">›</text>
			</view>
		</view>
		
		<view class="logout-section">
			<button @click="logout" class="logout-button">退出登录</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				notificationSettings: {
					newOrder: true,
					voiceAlert: true,
					deliveryReminder: true
				},
				privacySettings: {
					location: true,
					camera: true,
					microphone: false
				},
				otherSettings: {
					darkMode: false
				},
				cacheSize: '2.3MB'
			}
		},
		methods: {
			saveSettings() {
				uni.setStorageSync('settings', {
					notification: this.notificationSettings,
					privacy: this.privacySettings,
					other: this.otherSettings
				})
			},
			changePassword() {
				uni.showModal({
					title: '修改密码',
					content: '确定要修改密码吗？',
					success: (res) => {
						if (res.confirm) {
							uni.showToast({
								title: '密码修改功能开发中',
								icon: 'none'
							})
						}
					}
				})
			},
			changePhone() {
				uni.showModal({
					title: '更换手机号',
					content: '确定要更换手机号吗？',
					success: (res) => {
						if (res.confirm) {
							uni.showToast({
								title: '手机号更换功能开发中',
								icon: 'none'
							})
						}
					}
				})
			},
			clearCache() {
				uni.showModal({
					title: '清除缓存',
					content: '确定要清除缓存吗？',
					success: (res) => {
						if (res.confirm) {
							uni.clearStorage()
							this.cacheSize = '0MB'
							uni.showToast({
								title: '缓存清除成功',
								icon: 'success'
							})
						}
					}
				})
			},
			checkUpdate() {
				uni.showToast({
					title: '当前已是最新版本',
					icon: 'none'
				})
			},
			userAgreement() {
				uni.showModal({
					title: '用户协议',
					content: '用户协议内容...',
					showCancel: false
				})
			},
			privacyPolicy() {
				uni.showModal({
					title: '隐私政策',
					content: '隐私政策内容...',
					showCancel: false
				})
			},
			logout() {
				uni.showModal({
					title: '退出登录',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							uni.showToast({
								title: '退出成功',
								icon: 'success'
							})
							setTimeout(() => {
								uni.redirectTo({
									url: '/pages/login/login'
								})
							}, 1000)
						}
					}
				})
			}
		}
	}
</script>

<style scoped>
	.settings-container {
		min-height: 100vh;
	}
	
	.settings-section {
		background-color: white;
		margin-bottom: 20rpx;
	}
	
	.section-title {
		display: block;
		font-size: 28rpx;
		color: #64748b;
		font-weight: 500;
		padding: 20rpx 30rpx;
	}
	
	.setting-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f1f5f9;
	}
	
	.setting-item:last-child {
		border-bottom: none;
	}
	
	.setting-info {
		display: flex;
		align-items: center;
		gap: 20rpx;
		flex: 1;
	}
	
	.setting-icon {
		font-size: 32rpx;
	}
	
	.setting-label {
		font-size: 32rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.setting-switch {
		transform: scale(1.2);
	}
	
	.setting-arrow {
		font-size: 32rpx;
		color: #94a3b8;
	}
	
	.setting-status {
		font-size: 28rpx;
		color: #94a3b8;
		padding: 8rpx 16rpx;
		border-radius: 12rpx;
	}
	
	.setting-status.completed {
		background-color: #d1fae5;
		color: #10b981;
	}
	
	.setting-value {
		font-size: 28rpx;
		color: #64748b;
	}
	
	.setting-cache {
		font-size: 28rpx;
		color: #64748b;
	}
	
	.logout-section {
		padding: 40rpx 30rpx;
	}
	
	.logout-button {
		width: 100%;
		height: 96rpx;
		background-color: #ef4444;
		color: white;
		border: none;
		border-radius: 24rpx;
		font-size: 32rpx;
		font-weight: 500;
	}
</style>