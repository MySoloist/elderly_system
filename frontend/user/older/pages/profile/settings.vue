<template>
	<view class="settings-container">
		<!-- 导航栏 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">设置</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 通知设置 -->
		<view class="settings-section">
			<text class="section-title">通知设置</text>
			<view class="settings-card">
				<view 
					v-for="(setting, index) in notificationSettings" 
					:key="index"
					class="setting-item"
				>
					<view class="setting-left">
						<text class="setting-icon">{{ setting.icon }}</text>
						<text class="setting-title">{{ setting.title }}</text>
						<text v-if="setting.description" class="setting-desc">{{ setting.description }}</text>
					</view>
					<switch 
						class="setting-switch" 
						:checked="setting.enabled"
						@change="handleNotificationChange(setting)"
					/>
				</view>
			</view>
		</view>
		
		<!-- 账号安全 -->
		<view class="settings-section">
			<text class="section-title">账号安全</text>
			<view class="settings-card">
				<view 
					v-for="(setting, index) in securitySettings" 
					:key="index"
					class="setting-item"
					@click="handleSecurityClick(setting)"
				>
					<view class="setting-left">
						<text class="setting-icon">{{ setting.icon }}</text>
						<text class="setting-title">{{ setting.title }}</text>
					</view>
					<text class="setting-arrow">→</text>
				</view>
			</view>
		</view>
		
		<!-- 通用设置 -->
		<view class="settings-section">
			<text class="section-title">通用设置</text>
			<view class="settings-card">
				<view 
					v-for="(setting, index) in generalSettings" 
					:key="index"
					class="setting-item"
					@click="handleGeneralClick(setting)"
				>
					<view class="setting-left">
						<text class="setting-icon">{{ setting.icon }}</text>
						<text class="setting-title">{{ setting.title }}</text>
					</view>
					<text class="setting-arrow">→</text>
				</view>
			</view>
		</view>
		
		<!-- 关于我们 -->
		<view class="settings-section">
			<text class="section-title">关于我们</text>
			<view class="settings-card">
				<view class="about-info">
					<text class="app-name">颐养膳食</text>
					<text class="app-version">版本 1.0.0</text>
					<text class="app-description">为老年人提供营养餐饮配送服务</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				notificationSettings: [
					{
						id: 1,
						icon: '🔔',
						title: '订单通知',
						description: '接收订单状态更新通知',
						enabled: true
					},
					{
						id: 2,
						icon: '📱',
						title: '配送提醒',
						description: '餐品配送到达提醒',
						enabled: true
					},
					{
						id: 3,
						icon: '💊',
						title: '服药提醒',
						description: '定时提醒服药',
						enabled: false
					},
					{
						id: 4,
						icon: '📞',
						title: '家属呼叫',
						description: '接收家属呼叫通知',
						enabled: true
					}
				],
				securitySettings: [
					{
						id: 1,
						icon: '🔒',
						title: '修改密码'
					},
					{
						id: 2,
						icon: '📱',
						title: '绑定手机'
					},
					{
						id: 3,
						icon: '🔑',
						title: '实名认证'
					}
				],
				generalSettings: [
					{
						id: 1,
						icon: '🎨',
						title: '字体大小'
					},
					{
						id: 2,
						icon: '🌙',
						title: '夜间模式'
					},
					{
						id: 3,
						icon: '🗑️',
						title: '清除缓存'
					},
					{
						id: 4,
						icon: '📜',
						title: '用户协议'
					},
					{
						id: 5,
						icon: '🔒',
						title: '隐私政策'
					}
				]
			}
		},
		methods: {
			handleNotificationChange(setting) {
				setting.enabled = !setting.enabled;
				uni.showToast({
					title: setting.enabled ? '已开启' : '已关闭',
					icon: 'success'
				});
			},
			handleSecurityClick(setting) {
				switch(setting.id) {
					case 1:
						uni.navigateTo({
							url: '/pages/login/forgot'
						});
						break;
					case 2:
						uni.showToast({
							title: '后续功能开发中...',
							icon: 'none'
						});
						break;
					case 3:
						uni.showToast({
							title: '后续功能开发中...',
							icon: 'none'
						});
						break;
				}
			},
			handleGeneralClick(setting) {
				switch(setting.id) {
					case 1:
						this.showFontSizeOptions();
						break;
					case 2:
						uni.showToast({
							title: '后续功能开发中...',
							icon: 'none'
						});
						break;
					case 3:
						this.clearCache();
						break;
					case 4:
						uni.showToast({
							title: '后续功能开发中...',
							icon: 'none'
						});
						break;
					case 5:
						uni.showToast({
							title: '后续功能开发中...',
							icon: 'none'
						});
						break;
				}
			},
			showFontSizeOptions() {
				uni.showActionSheet({
					itemList: ['小', '中', '大', '特大'],
					success: (res) => {
						uni.showToast({
							title: '字体大小已设置',
							icon: 'success'
						});
					}
				});
			},
			clearCache() {
				uni.showModal({
					title: '清除缓存',
					content: '确定要清除应用缓存吗？',
					success: (res) => {
						if (res.confirm) {
							uni.showLoading({
								title: '清除中...'
							});
							setTimeout(() => {
								uni.hideLoading();
								uni.showToast({
									title: '缓存已清除',
									icon: 'success'
								});
							}, 1000);
						}
					}
				});
			},
			goBack() {
				uni.navigateBack()
			}
		}
	}
</script>

<style scoped>
	.settings-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F5F5F5 100%);
		padding-bottom: 40px;
	}
	
	/* 导航栏 */
	.nav-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 56px;
		padding: 0 20px;
		background: rgba(255, 255, 255, 0.95);
		border-bottom: 1px solid rgba(255, 122, 69, 0.1);
	}
	
	.back-btn {
		font-size: 22px;
		color: #FF7A45;
		width: 34px;
		height: 34px;
		line-height: 34px;
		text-align: center;
		background: rgba(255, 122, 69, 0.1);
		border-radius: 17px;
	}
	
	.nav-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
	}
	
	.placeholder {
		width: 24px;
	}
	
	/* 设置区块 */
	.settings-section {
		padding: 20px;
	}
	
	.section-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
		margin-bottom: 16px;
		display: block;
	}
	
	.settings-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	/* 设置项 */
	.setting-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 16px 20px;
		border-bottom: 1px solid #F0F0F0;
	}
	
	.setting-item:last-child {
		border-bottom: none;
	}
	
	.setting-left {
		display: flex;
		align-items: flex-start;
		flex: 1;
	}
	
	.setting-icon {
		font-size: 24px;
		margin-right: 16px;
		width: 32px;
		text-align: center;
	}
	
	.setting-title {
		font-size: 16px;
		color: #333333;
		font-weight: 500;
		display: block;
	}
	
	.setting-desc {
		font-size: 13px;
		color: #999999;
		display: block;
		margin-top: 4px;
	}
	
	.setting-switch {
		width: 50px;
		height: 30px;
	}
	
	.setting-arrow {
		font-size: 18px;
		color: #999999;
		font-weight: 600;
	}
	
	/* 关于我们 */
	.about-info {
		padding: 24px 20px;
		text-align: center;
	}
	
	.app-name {
		font-size: 20px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 8px;
	}
	
	.app-version {
		font-size: 14px;
		color: #666666;
		display: block;
		margin-bottom: 12px;
	}
	
	.app-description {
		font-size: 14px;
		color: #999999;
		line-height: 1.4;
	}
</style>