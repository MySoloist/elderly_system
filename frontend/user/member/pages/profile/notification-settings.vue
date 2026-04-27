<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">通知设置</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 通知设置列表 -->
		<view class="settings-list">
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-title">订单状态通知</text>
					<text class="setting-desc">订单状态变更时发送通知</text>
				</view>
				<switch class="setting-switch" color="#6366f1" :checked="settings.orderStatus" @change="toggleSetting('orderStatus')"></switch>
			</view>
			
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-title">配送提醒</text>
					<text class="setting-desc">配送状态变更时发送通知</text>
				</view>
				<switch class="setting-switch" color="#6366f1" :checked="settings.delivery" @change="toggleSetting('delivery')"></switch>
			</view>
			
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-title">健康提醒</text>
					<text class="setting-desc">老人健康状况异常时发送通知</text>
				</view>
				<switch class="setting-switch" color="#6366f1" :checked="settings.health" @change="toggleSetting('health')"></switch>
			</view>
			
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-title">消费通知</text>
					<text class="setting-desc">消费记录更新时发送通知</text>
				</view>
				<switch class="setting-switch" color="#6366f1" :checked="settings.consume" @change="toggleSetting('consume')"></switch>
			</view>
			
			<view class="setting-item">
				<view class="setting-info">
					<text class="setting-title">系统通知</text>
					<text class="setting-desc">系统公告和活动通知</text>
				</view>
				<switch class="setting-switch" color="#6366f1" :checked="settings.system" @change="toggleSetting('system')"></switch>
			</view>
		</view>
		
		<!-- 通知方式设置 -->
		<view class="section">
			<text class="section-title">通知方式</text>
			<view class="setting-item">
				<text class="setting-title">微信通知</text>
				<switch class="setting-switch" color="#6366f1" :checked="settings.wechat" @change="toggleSetting('wechat')"></switch>
			</view>
			<view class="setting-item">
				<text class="setting-title">短信通知</text>
				<switch class="setting-switch" color="#6366f1" :checked="settings.sms" @change="toggleSetting('sms')"></switch>
			</view>
		</view>
		
		<!-- 保存按钮 -->
		<button class="save-btn" @click="saveSettings">
			<text class="save-text">保存设置</text>
		</button>
	</view>
</template>

<script>
export default {
	data() {
		return {
			settings: {
				orderStatus: true,
				delivery: true,
				health: true,
				consume: true,
				system: true,
				wechat: true,
				sms: false
			}
		};
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		toggleSetting(key) {
			this.settings[key] = !this.settings[key];
		},
		saveSettings() {
			uni.showLoading({
				title: '保存中...'
			});
			setTimeout(() => {
				uni.hideLoading();
				uni.showToast({
					title: '设置已保存',
					icon: 'success'
				});
			}, 1000);
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background-color: #f8fafc;
	padding-bottom: 80px;
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

/* 设置列表 */
.settings-list {
	padding: 24px;
}

.setting-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 16px;
	margin-bottom: 12px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.6);
	transition: all 0.3s ease;
}

.setting-item:active {
	background-color: #f8fafc;
}

.setting-info {
	flex: 1;
	margin-right: 16px;
}

.setting-title {
	font-size: 16px;
	font-weight: 500;
	color: #1e293b;
	display: block;
	margin-bottom: 4px;
}

.setting-desc {
	font-size: 14px;
	color: #64748b;
	display: block;
}

.setting-switch {
	transform: scale(1.2);
}

/* 章节标题 */
.section {
	padding: 0 24px 24px;
}

.section-title {
	font-size: 20px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 16px;
	display: block;
}

/* 保存按钮 */
.save-btn {
	position: fixed;
	bottom: 24px;
	left: 24px;
	right: 24px;
	height: 48px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 12px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 500;
	box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.3s ease;
}

.save-btn:active {
	transform: scale(0.98);
	box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
}

.save-text {
	
}
</style>
