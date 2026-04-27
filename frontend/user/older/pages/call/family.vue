<template>
	<view class="family-container">
		<!-- 导航栏 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">呼叫家属</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 家属列表 -->
		<view class="family-list">
			<view 
				v-for="(family, index) in familyList" 
				:key="index"
				class="family-card"
			>
				<view class="family-info">
					<view class="family-avatar">
						<text class="avatar-text">{{ family.name.charAt(0) }}</text>
					</view>
					<view class="family-details">
						<text class="family-name">{{ family.name }}</text>
						<text class="family-relation">{{ family.relation }}</text>
					</view>
				</view>
				<view class="call-buttons">
					<button 
						class="btn-call" 
						@click="handleCall(family, 'voice')"
					>
						<text class="btn-icon">📞</text>
						<text>语音</text>
					</button>
					<button 
						class="btn-video" 
						@click="handleCall(family, 'video')"
					>
						<text class="btn-icon">📹</text>
						<text>视频</text>
					</button>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-if="familyList.length === 0" class="empty-state">
				<text class="empty-icon">👨👩👧👦</text>
				<text class="empty-text">暂无家属信息</text>
				<text class="empty-hint">请联系管理员添加家属信息</text>
			</view>
		</view>
		
		<!-- 最近通话记录 -->
		<view class="call-history">
			<text class="section-title">最近通话</text>
			<view class="history-list">
				<view 
					v-for="(record, index) in callHistory" 
					:key="index"
					class="history-item"
				>
					<view class="history-info">
						<text class="history-name">{{ record.name }}</text>
						<text class="history-time">{{ record.time }}</text>
					</view>
					<view class="history-type" :class="record.type">
						<text class="type-icon">{{ record.icon }}</text>
						<text>{{ record.duration }}</text>
					</view>
				</view>
				
				<!-- 空状态 -->
				<view v-if="callHistory.length === 0" class="empty-state">
					<text class="empty-text">暂无通话记录</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				familyList: [
					{
						name: '张小明',
						relation: '儿子',
						phone: '13800138001',
						avatar: '👦'
					},
					{
						name: '李小红',
						relation: '女儿',
						phone: '13900139002',
						avatar: '👧'
					},
					{
						name: '王芳',
						relation: '儿媳',
						phone: '13700137003',
						avatar: '👩'
					}
				],
				callHistory: [
					{
						name: '张小明',
						time: '今天 14:30',
						type: 'voice',
						icon: '📞',
						duration: '05:32'
					},
					{
						name: '李小红',
						time: '昨天 18:45',
						type: 'video',
						icon: '📹',
						duration: '12:45'
					}
				]
			}
		},
		methods: {
			handleCall(family, callType) {
				uni.showModal({
					title: '呼叫确认',
					content: `确定要${callType === 'voice' ? '语音' : '视频'}呼叫${family.name}吗？`,
					success: (res) => {
						if (res.confirm) {
							// 模拟拨打电话
							this.simulateCall(family, callType);
						}
					}
				});
			},
			simulateCall(family, callType) {
				uni.showLoading({
					title: '正在拨号...'
				});
				
				setTimeout(() => {
					uni.hideLoading();
					uni.showModal({
						title: '通话中',
						content: `正在与${family.name}${callType === 'voice' ? '语音' : '视频'}通话`,
						confirmText: '结束通话',
						showCancel: false,
						success: () => {
							// 添加到通话记录
							const now = new Date();
							const timeStr = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
							const duration = `${Math.floor(Math.random() * 10) + 1}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`;
							
							this.callHistory.unshift({
								name: family.name,
								time: '刚刚',
								type: callType,
								icon: callType === 'voice' ? '📞' : '📹',
								duration: duration
							});
							
							uni.showToast({
								title: '通话已结束',
								icon: 'success'
							});
						}
					});
				}, 1500);
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
	.family-container {
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
	
	/* 家属列表 */
	.family-list {
		padding: 20px;
	}
	
	.family-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		margin-bottom: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.family-info {
		display: flex;
		align-items: center;
		margin-bottom: 16px;
	}
	
	.family-avatar {
		width: 64px;
		height: 64px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		border-radius: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 16px;
		box-shadow: 0 4px 12px rgba(255, 122, 69, 0.2);
	}
	
	.avatar-text {
		font-size: 24px;
		font-weight: 600;
		color: white;
	}
	
	.family-details {
		flex: 1;
	}
	
	.family-name {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 4px;
	}
	
	.family-relation {
		font-size: 14px;
		color: #666666;
	}
	
	.call-buttons {
		display: flex;
		gap: 12px;
	}
	
	.btn-call, .btn-video {
		flex: 1;
		height: 48px;
		border-radius: 12px;
		font-size: 15px;
		font-weight: 500;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
	}
	
	.btn-call {
		background-color: #4CAF50;
		color: white;
		border: none;
	}
	
	.btn-video {
		background-color: #2196F3;
		color: white;
		border: none;
	}
	
	.btn-icon {
		font-size: 20px;
	}
	
	/* 最近通话记录 */
	.call-history {
		padding: 20px;
	}
	
	.section-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
		margin-bottom: 16px;
		display: block;
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
		justify-content: space-between;
		padding: 16px;
		border-bottom: 1px solid #F0F0F0;
	}
	
	.history-item:last-child {
		border-bottom: none;
	}
	
	.history-info {
		flex: 1;
	}
	
	.history-name {
		font-size: 16px;
		font-weight: 500;
		color: #333333;
		display: block;
		margin-bottom: 4px;
	}
	
	.history-time {
		font-size: 13px;
		color: #999999;
	}
	
	.history-type {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 16px;
		border-radius: 16px;
		font-size: 14px;
		font-weight: 500;
	}
	
	.history-type.voice {
		background-color: #E8F5E9;
		color: #2E7D32;
	}
	
	.history-type.video {
		background-color: #E3F2FD;
		color: #1565C0;
	}
	
	.type-icon {
		font-size: 16px;
	}
	
	/* 空状态 */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 60px 20px;
		text-align: center;
	}
	
	.empty-icon {
		font-size: 64px;
		margin-bottom: 16px;
	}
	
	.empty-text {
		font-size: 16px;
		color: #666666;
		margin-bottom: 8px;
	}
	
	.empty-hint {
		font-size: 14px;
		color: #999999;
	}
</style>