<template>
	<view class="help-container">
		<!-- 导航栏 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">工作人员求助</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 紧急求助区域 -->
		<view class="emergency-section">
			<view class="emergency-card">
				<text class="emergency-icon">🚨</text>
				<text class="emergency-title">紧急求助</text>
				<text class="emergency-desc">点击下方按钮拨打紧急电话</text>
				<button 
					class="emergency-btn" 
					@click="handleEmergencyHelp"
				>
					立即求助
				</button>
			</view>
		</view>
		
		<!-- 常用求助选项 -->
		<view class="help-options">
			<text class="section-title">常用求助</text>
			<view class="options-grid">
				<view 
					v-for="option in helpOptions" 
					:key="option.id"
					class="option-card"
					@click="handleHelpOption(option)"
				>
					<text class="option-icon">{{ option.icon }}</text>
					<text class="option-title">{{ option.title }}</text>
				</view>
			</view>
		</view>
		
		<!-- 求助记录 -->
		<view class="help-history">
			<text class="section-title">求助记录</text>
			<view class="history-list">
				<view 
					v-for="(record, index) in helpHistory" 
					:key="index"
					class="history-item"
				>
					<view class="history-icon">
						<text>{{ record.icon }}</text>
					</view>
					<view class="history-content">
						<text class="history-title">{{ record.title }}</text>
						<text class="history-time">{{ record.time }}</text>
					</view>
					<view class="history-status" :class="record.status">
						<text>{{ record.statusText }}</text>
					</view>
				</view>
				
				<!-- 空状态 -->
				<view v-if="helpHistory.length === 0" class="empty-state">
					<text class="empty-text">暂无求助记录</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				helpOptions: [
					{
						id: 1,
						icon: '🍽️',
						title: '送餐延迟'
					},
					{
						id: 2,
						icon: '💊',
						title: '需要药物'
					},
					{
						id: 3,
						icon: '🚑',
						title: '身体不适'
					}
				],
				helpHistory: [
					{
						icon: '🍽️',
						title: '送餐延迟',
						time: '2026-03-28 12:15',
						status: 'processing',
						statusText: '处理中'
					}
				]
			}
		},
		methods: {
			handleEmergencyHelp() {
				uni.showActionSheet({
					itemList: ['110 报警', '119 消防', '120 急救'],
					success: (res) => {
						let phoneNumber = ''
						if (res.tapIndex === 0) {
							phoneNumber = '110'
						} else if (res.tapIndex === 1) {
							phoneNumber = '119'
						} else if (res.tapIndex === 2) {
							phoneNumber = '120'
						}
						
						uni.makePhoneCall({
							phoneNumber: phoneNumber,
							success: () => {
								console.log('拨打电话成功')
							},
							fail: (err) => {
								uni.showToast({
									title: '拨打电话失败',
									icon: 'none'
								})
							}
						})
					}
				})
			},
			handleHelpOption(option) {
				uni.showModal({
					title: '发送求助',
					content: `确认发送"${option.title}"求助吗？`,
					success: (res) => {
						if (res.confirm) {
							// 添加到求助记录
							this.helpHistory.unshift({
								icon: option.icon,
								title: option.title,
								time: new Date().toLocaleString('zh-CN'),
								status: 'processing',
								statusText: '处理中'
							});
							
							uni.showToast({
								title: '求助已发送',
								icon: 'success'
							});
						}
					}
				});
			}
		},
		methods: {
			goBack() {
				uni.navigateBack()
			}
		}
	}
</script>

<style scoped>
	.help-container {
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
	
	/* 紧急求助区域 */
	.emergency-section {
		padding: 20px;
	}
	
	.emergency-card {
		background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
		border-radius: 20px;
		padding: 32px 20px;
		text-align: center;
		color: white;
		box-shadow: 0 8px 24px rgba(255, 107, 107, 0.3);
	}
	
	.emergency-icon {
		font-size: 48px;
		margin-bottom: 16px;
	}
	
	.emergency-title {
		font-size: 20px;
		font-weight: 600;
		display: block;
		margin-bottom: 8px;
	}
	
	.emergency-desc {
		font-size: 14px;
		opacity: 0.9;
		display: block;
		margin-bottom: 24px;
	}
	
	.emergency-btn {
		background-color: white;
		color: #FF6B6B;
		border: none;
		border-radius: 24px;
		height: 56px;
		font-size: 18px;
		font-weight: 600;
		width: 100%;
		max-width: 240px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
	}
	
	.emergency-btn:disabled {
		opacity: 0.6;
	}
	
	/* 常用求助选项 */
	.help-options {
		padding: 20px;
	}
	
	.section-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
		margin-bottom: 16px;
		display: block;
	}
	
	.options-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 16px;
	}
	
	.option-card {
		background-color: #FFFFFF;
		border-radius: 16px;
		padding: 24px 16px;
		text-align: center;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.option-icon {
		font-size: 32px;
		margin-bottom: 8px;
		display: block;
	}
	
	.option-title {
		font-size: 15px;
		color: #333333;
		font-weight: 500;
	}
	
	/* 求助记录 */
	.help-history {
		padding: 20px;
	}
	
	.history-list {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.history-item {
		display: flex;
		align-items: center;
		padding: 16px;
		border-bottom: 1px solid #F0F0F0;
	}
	
	.history-item:last-child {
		border-bottom: none;
	}
	
	.history-icon {
		width: 48px;
		height: 48px;
		background-color: #FFF8F4;
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 16px;
	}
	
	.history-icon text {
		font-size: 24px;
	}
	
	.history-content {
		flex: 1;
	}
	
	.history-title {
		font-size: 15px;
		font-weight: 500;
		color: #333333;
		display: block;
		margin-bottom: 4px;
	}
	
	.history-time {
		font-size: 13px;
		color: #999999;
	}
	
	.history-status {
		padding: 4px 12px;
		border-radius: 12px;
		font-size: 12px;
		font-weight: 500;
	}
	
	.history-status.processing {
		background-color: #FFF3CD;
		color: #856404;
	}
	
	.history-status.completed {
		background-color: #D4EDDA;
		color: #155724;
	}
	
	
	
	/* 空状态 */
	.empty-state {
		text-align: center;
		padding: 40px 20px;
	}
	
	.empty-text {
		font-size: 14px;
		color: #999999;
	}
</style>