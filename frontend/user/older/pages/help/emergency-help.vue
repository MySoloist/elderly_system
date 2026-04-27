<template>
	<view class="emergency-help-container">
		<!-- 导航栏 -->
		<view class="nav-bar">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">紧急求助</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 紧急求助说明 -->
		<view class="emergency-intro">
			<text class="intro-icon">🚨</text>
			<text class="intro-title">紧急求助</text>
			<text class="intro-desc">选择紧急联系人进行求助</text>
		</view>
		
		<!-- 紧急联系人列表 -->
		<view class="contacts-section">
			<view 
				v-for="contact in contacts" 
				:key="contact.id"
				class="contact-card"
				:class="{ 'primary-contact': contact.is_primary === 0 }"
			>
				<view class="contact-info">
					<view class="contact-header">
						<text class="contact-name">{{ contact.name }}</text>
						<view v-if="contact.is_primary === 0" class="primary-badge">主</view>
					</view>
					<text class="contact-phone">{{ contact.phone }}</text>
					<text class="contact-relationship">{{ contact.relationship }}</text>
				</view>
				<view class="contact-actions">
					<button class="call-btn" @click="callContact(contact)">
						<text class="call-icon">📞</text>
						<text>电话</text>
					</button>
					<button class="sms-btn" @click="sendSms(contact)">
						<text class="sms-icon">💬</text>
						<text>短信</text>
					</button>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-if="contacts.length === 0" class="empty-state">
				<text class="empty-icon">📞</text>
				<text class="empty-text">暂无紧急联系人</text>
				<button class="add-btn" @click="goToContacts">添加联系人</button>
			</view>
		</view>
		
		<!-- 底部紧急按钮 -->
		<view class="bottom-emergency">
			<button class="emergency-btn" @click="showEmergencyOptions">
				<text class="emergency-btn-icon">🚨</text>
				<text>紧急求助</text>
			</button>
		</view>
	</view>
</template>

<script>
	import api from '../../utils/api.js'
	
	export default {
		data() {
			return {
				contacts: [],
				loading: false
			}
		},
		onLoad() {
			this.loadContacts()
		},
		methods: {
			goBack() {
				uni.navigateBack()
			},
			async loadContacts() {
				this.loading = true
				try {
					const response = await api.older.getEmergencyContacts()
					this.contacts = response.data || []
				} catch (error) {
					console.error('加载紧急联系人失败:', error)
					uni.showToast({
						title: '加载失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			callContact(contact) {
				uni.makePhoneCall({
					phoneNumber: contact.phone,
					success: () => {
						console.log('拨打电话成功')
						this.addHelpRecord(contact, '电话求助')
					},
					fail: (err) => {
						console.error('拨打电话失败:', err)
						uni.showToast({
							title: '拨打电话失败',
							icon: 'none'
						})
					}
				})
			},
			sendSms(contact) {
				uni.showModal({
					title: '发送短信',
					content: `确认向${contact.name}发送求助短信吗？`,
					success: (res) => {
						if (res.confirm) {
							uni.sendSMS({
								phoneNumber: contact.phone,
								content: `紧急求助：我需要帮助，请尽快联系我。`,
								success: () => {
									console.log('发送短信成功')
									this.addHelpRecord(contact, '短信求助')
									uni.showToast({
										title: '短信发送成功',
										icon: 'success'
									})
								},
								fail: (err) => {
									console.error('发送短信失败:', err)
									uni.showToast({
										title: '发送短信失败',
										icon: 'none'
									})
								}
							})
						}
					}
				})
			},
			async addHelpRecord(contact, type) {
				try {
					let emergencyType = ''
					let message = ''
					
					if (type === '电话求助') {
						emergencyType = 'family_call'
						message = `向${contact.name}发起电话求助`
					} else if (type === '短信求助') {
						emergencyType = 'family_sms'
						message = `向${contact.name}发送求助短信`
					} else {
						emergencyType = type
						message = `拨打${contact.name}`
					}
					
					await api.older.createEmergencyCall({
						emergency_type: emergencyType,
						message: message
					})
					
					console.log('紧急求助记录保存成功')
				} catch (error) {
					console.error('保存紧急求助记录失败:', error)
				}
			},
			showEmergencyOptions() {
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
								console.log('拨打紧急电话成功')
								let emergencyType = ''
								if (phoneNumber === '110') {
									emergencyType = 'police'
								} else if (phoneNumber === '119') {
									emergencyType = 'fire'
								} else if (phoneNumber === '120') {
									emergencyType = 'medical'
								}
								this.addHelpRecord({name: phoneNumber}, emergencyType)
							},
							fail: (err) => {
								console.error('拨打紧急电话失败:', err)
								uni.showToast({
									title: '拨打电话失败',
									icon: 'none'
								})
							}
						})
					}
				})
			},
			goToContacts() {
				uni.navigateTo({
					url: '/pages/profile/emergency-contacts'
				})
			}
		}
	}
</script>

<style scoped>
	.emergency-help-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F5F5F5 100%);
		padding-bottom: 80px;
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
	
	/* 紧急求助说明 */
	.emergency-intro {
		text-align: center;
		padding: 32px 20px;
	}
	
	.intro-icon {
		font-size: 48px;
		display: block;
		margin-bottom: 16px;
	}
	
	.intro-title {
		font-size: 20px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 8px;
	}
	
	.intro-desc {
		font-size: 14px;
		color: #666666;
	}
	
	/* 紧急联系人列表 */
	.contacts-section {
		padding: 0 20px;
	}
	
	.contact-card {
		background-color: #FFFFFF;
		border-radius: 16px;
		padding: 20px;
		margin-bottom: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 2px solid transparent;
	}
	
	.contact-card.primary-contact {
		border-color: #FF7A45;
		background-color: #FFF8F4;
	}
	
	.contact-info {
		margin-bottom: 16px;
	}
	
	.contact-header {
		display: flex;
		align-items: center;
		margin-bottom: 8px;
	}
	
	.contact-name {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
		margin-right: 8px;
	}
	
	.primary-badge {
		background-color: #FF7A45;
		color: white;
		padding: 2px 8px;
		border-radius: 10px;
		font-size: 12px;
		font-weight: 500;
	}
	
	.contact-phone {
		display: block;
		font-size: 16px;
		color: #666666;
		margin-bottom: 4px;
	}
	
	.contact-relationship {
		display: block;
		font-size: 14px;
		color: #999999;
	}
	
	.contact-actions {
		display: flex;
		gap: 12px;
	}
	
	.call-btn, .sms-btn {
		flex: 1;
		padding: 12px;
		border: none;
		border-radius: 12px;
		font-size: 14px;
		font-weight: 500;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 6px;
	}
	
	.call-btn {
		background-color: #4CAF50;
		color: white;
	}
	
	.sms-btn {
		background-color: #2196F3;
		color: white;
	}
	
	.call-icon, .sms-icon {
		font-size: 18px;
	}
	
	/* 空状态 */
	.empty-state {
		text-align: center;
		padding: 60px 20px;
		background-color: #FFFFFF;
		border-radius: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
	}
	
	.empty-icon {
		font-size: 48px;
		display: block;
		margin-bottom: 16px;
	}
	
	.empty-text {
		font-size: 16px;
		color: #999999;
		display: block;
		margin-bottom: 24px;
	}
	
	.add-btn {
		padding: 12px 24px;
		background-color: #FF7A45;
		color: white;
		border: none;
		border-radius: 24px;
		font-size: 14px;
		font-weight: 500;
	}
	
	/* 底部紧急按钮 */
	.bottom-emergency {
		position: fixed;
		bottom: 20px;
		left: 20px;
		right: 20px;
		z-index: 100;
	}
	
	.emergency-btn {
		width: 100%;
		padding: 16px;
		background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
		color: white;
		border: none;
		border-radius: 24px;
		font-size: 18px;
		font-weight: 600;
		box-shadow: 0 8px 24px rgba(255, 107, 107, 0.3);
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
	}
	
	.emergency-btn-icon {
		font-size: 20px;
	}
</style>
