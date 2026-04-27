<template>
	<view class="about-container">
		<view class="header-section">
			<image class="logo" :src="logo" mode="aspectFit"></image>
			<view class="app-name">易配送</view>
			<view class="app-version">版本 {{ version }}</view>
		</view>
		
		<view class="info-section">
			<view class="info-card">
				<view class="info-item">
					<text class="info-label">开发者</text>
					<text class="info-value">易配送团队</text>
				</view>
				<view class="info-item">
					<text class="info-label">联系方式</text>
					<text class="info-value">service@epeisong.com</text>
				</view>
				<view class="info-item">
					<text class="info-label">地址</text>
					<text class="info-value">北京市朝阳区科技园区</text>
				</view>
			</view>
		</view>
		
		<view class="features-section">
			<view class="section-title">核心功能</view>
			<view class="features-list">
				<view class="feature-item">
					<view class="feature-icon">📋</view>
					<view class="feature-name">订单管理</view>
					<view class="feature-desc">实时订单接收与处理</view>
				</view>
				<view class="feature-item">
					<view class="feature-icon">🧭</view>
					<view class="feature-name">智能导航</view>
					<view class="feature-desc">精准路线规划</view>
				</view>
				<view class="feature-item">
					<view class="feature-icon">💰</view>
					<view class="feature-name">收入统计</view>
					<view class="feature-desc">详细收入数据分析</view>
				</view>
				<view class="feature-item">
					<view class="feature-icon">👤</view>
					<view class="feature-name">个人中心</view>
					<view class="feature-desc">完善的个人信息管理</view>
				</view>
			</view>
		</view>
		
		<view class="update-section">
			<view class="section-title">版本更新</view>
			<view class="update-list">
				<view class="update-item">
					<view class="update-version">v1.0.0</view>
					<view class="update-date">2024-01-15</view>
					<view class="update-content">
						<text class="update-point">• 初始版本发布</text>
						<text class="update-point">• 基础订单功能</text>
						<text class="update-point">• 个人中心管理</text>
						<text class="update-point">• 排班系统集成</text>
					</view>
				</view>
			</view>
		</view>
		
		<view class="policy-section">
			<view class="policy-links">
				<text class="policy-link" @click="openPolicy('privacy')">隐私政策</text>
				<text class="policy-divider">|</text>
				<text class="policy-link" @click="openPolicy('user')">用户协议</text>
				<text class="policy-divider">|</text>
				<text class="policy-link" @click="openPolicy('service')">服务条款</text>
			</view>
		</view>
		
		<view class="copyright">
			<text>© 2024 易配送. 保留所有权利.</text>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			logo: '/static/logo.png',
			version: '1.0.0'
		};
	},
	methods: {
		openPolicy(type) {
			let url = '';
			switch(type) {
				case 'privacy':
					url = 'https://www.epeisong.com/privacy';
					break;
				case 'user':
					url = 'https://www.epeisong.com/user-agreement';
					break;
				case 'service':
					url = 'https://www.epeisong.com/service-terms';
					break;
			}
			uni.navigateTo({
				url: `/pages/web-view/web-view?url=${encodeURIComponent(url)}`
			});
		},
		checkUpdate() {
			// 检查版本更新
			uni.showToast({
				title: '当前已是最新版本',
				icon: 'none'
			});
		}
	},
	onLoad() {
		this.checkUpdate();
	}
};
</script>

<style scoped>
.about-container {
	padding: 40rpx;
	min-height: 100vh;
}

.header-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 60rpx 0;
	background-color: #fff;
	border-radius: 20rpx;
	margin-bottom: 30rpx;
	box-shadow: 0 10rpx 20rpx rgba(0,0,0,0.1);
}

.logo {
	width: 160rpx;
	height: 160rpx;
	margin-bottom: 20rpx;
	border-radius: 20rpx;
	background-color: #f0f0f0;
}

.app-name {
	font-size: 48rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 10rpx;
}

.app-version {
	font-size: 28rpx;
	color: #666;
}

.info-section {
	margin-bottom: 30rpx;
}

.info-card {
	background-color: #fff;
	border-radius: 20rpx;
	padding: 40rpx;
	box-shadow: 0 10rpx 20rpx rgba(0,0,0,0.1);
}

.info-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #eee;
}

.info-item:last-child {
	border-bottom: none;
}

.info-label {
	font-size: 32rpx;
	color: #666;
}

.info-value {
	font-size: 32rpx;
	color: #333;
	font-weight: 500;
}

.features-section {
	margin-bottom: 30rpx;
}

.section-title {
	font-size: 36rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 20rpx;
	padding-left: 10rpx;
	border-left: 6rpx solid #4CAF50;
}

.features-list {
	background-color: #fff;
	border-radius: 20rpx;
	padding: 30rpx;
	box-shadow: 0 10rpx 20rpx rgba(0,0,0,0.1);
}

.feature-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 20rpx;
	margin: 20rpx;
	background-color: #f9f9f9;
	border-radius: 15rpx;
	transition: all 0.3s ease;
}

.feature-item:active {
	transform: scale(0.95);
	background-color: #f0f0f0;
}

.feature-icon {
	font-size: 60rpx;
	margin-bottom: 15rpx;
}

.feature-name {
	font-size: 32rpx;
	font-weight: 500;
	color: #333;
	margin-bottom: 10rpx;
}

.feature-desc {
	font-size: 28rpx;
	color: #666;
	text-align: center;
}

.update-section {
	margin-bottom: 30rpx;
}

.update-list {
	background-color: #fff;
	border-radius: 20rpx;
	padding: 30rpx;
	box-shadow: 0 10rpx 20rpx rgba(0,0,0,0.1);
}

.update-item {
	padding: 20rpx 0;
}

.update-version {
	font-size: 32rpx;
	font-weight: bold;
	color: #4CAF50;
	margin-bottom: 10rpx;
}

.update-date {
	font-size: 28rpx;
	color: #666;
	margin-bottom: 15rpx;
}

.update-content {
	display: flex;
	flex-direction: column;
}

.update-point {
	font-size: 28rpx;
	color: #333;
	line-height: 1.5;
	margin-bottom: 5rpx;
}

.policy-section {
	margin-bottom: 40rpx;
}

.policy-links {
	display: flex;
	justify-content: center;
	align-items: center;
	flex-wrap: wrap;
}

.policy-link {
	font-size: 28rpx;
	color: #4CAF50;
	margin: 0 10rpx;
}

.policy-divider {
	font-size: 28rpx;
	color: #ccc;
	margin: 0 5rpx;
}

.copyright {
	text-align: center;
	font-size: 24rpx;
	color: #999;
	padding: 40rpx 0;
}
</style>