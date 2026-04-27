<template>
	<view class="category-container">
		<!-- 导航栏 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">紧急求助</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 求助分类卡片 -->
		<view class="category-section">
			<view class="category-card staff-card" @click="goToStaffHelp">
				<view class="card-icon">
					<text>👨⚕️</text>
				</view>
				<text class="card-title">工作人员求助</text>
				<text class="card-desc">向医护人员、送餐人员等工作人员发送求助信息</text>
				<view class="card-arrow">→</view>
			</view>
			
			<view class="category-card family-card" @click="goToFamilyHelp">
				<view class="card-icon">
					<text>👨👩👧👦</text>
				</view>
				<text class="card-title">家属联系</text>
				<text class="card-desc">与家人进行语音或视频通话</text>
				<view class="card-arrow">→</view>
			</view>
		</view>
		
		<!-- 紧急求助快捷按钮 -->
		<view class="emergency-quick">
			<button class="emergency-btn" @click="handleEmergencyCall">
				<text class="btn-icon">🚨</text>
				<text>紧急求助</text>
			</button>
		</view>
	</view>
</template>

<script>
	export default {
		methods: {
			goBack() {
				uni.navigateBack()
			},
			goToStaffHelp() {
				uni.navigateTo({
					url: '/pages/help/help'
				})
			},
			handleEmergencyCall() {
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
			goToFamilyHelp() {
				uni.navigateTo({
					url: '/pages/call/family'
				})
			}
		}
	}
</script>

<style scoped>
	.category-container {
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
	
	/* 分类卡片区域 */
	.category-section {
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	
	.category-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 24px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
		display: flex;
		align-items: center;
		position: relative;
	}
	
	.staff-card {
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
	}
	
	.family-card {
		background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
		color: white;
	}
	
	.card-icon {
		width: 64px;
		height: 64px;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 16px;
		font-size: 32px;
	}
	
	.card-title {
		font-size: 18px;
		font-weight: 600;
		display: block;
		margin-bottom: 4px;
	}
	
	.card-desc {
		font-size: 14px;
		opacity: 0.9;
	}
	
	.card-arrow {
		position: absolute;
		right: 24px;
		font-size: 20px;
		opacity: 0.8;
	}
	
	/* 紧急求助快捷按钮 */
	.emergency-quick {
		padding: 20px;
		margin-top: 20px;
	}
	
	.emergency-btn {
		width: 100%;
		height: 56px;
		background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
		color: white;
		border: none;
		border-radius: 28px;
		font-size: 18px;
		font-weight: 600;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 12px;
		box-shadow: 0 8px 24px rgba(255, 107, 107, 0.3);
	}
	
	.btn-icon {
		font-size: 24px;
	}
</style>