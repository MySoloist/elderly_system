<template>
	<view class="emergency-contacts-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">紧急联系人</text>
			<text class="placeholder"></text>
		</view>
		
		<!-- 紧急求助说明 -->
		<view class="emergency-intro">
			<text class="intro-icon">🚨</text>
			<text class="intro-title">紧急求助</text>
			<text class="intro-desc">选择紧急联系人进行求助</text>
		</view>
		
		<!-- 当前紧急联系人列表 -->
		<view class="current-contacts">
			<text class="section-title">当前紧急联系人</text>
			<view v-if="emergencyContacts.length > 0" class="contacts-list">
				<view v-for="contact in emergencyContacts" :key="contact.id" class="contact-item" :class="{ 'primary-contact': contact.is_primary === 0 }">
					<view class="contact-info">
						<view class="contact-header">
							<view class="contact-name">{{ contact.name }}</view>
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
						<button class="message-btn" @click="sendMessage(contact)">
							<text class="message-icon">📩</text>
							<text>消息</text>
						</button>
						<button class="btn-primary" @click="setAsPrimary(contact.id)">置主</button>
					</view>
				</view>
			</view>
			<view v-else class="empty-state">
				<text class="empty-icon">📞</text>
				<text class="empty-text">暂无紧急联系人</text>
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
				emergencyContacts: [],

				loading: false
			}
		},
		onLoad() {
			this.loadData()
		},
		methods: {
			goBack() {
				uni.navigateBack()
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
					content: `确认向${contact.name}发送求助短信吗？\n\n短信内容：紧急求助：我需要帮助，请尽快联系我。`,
					success: (res) => {
						if (res.confirm) {
							// 在微信小程序中，使用系统短信功能
							uni.showActionSheet({
								itemList: ['复制短信内容', '手动发送短信'],
								success: (res) => {
									if (res.tapIndex === 0) {
										// 复制短信内容
										uni.setClipboardData({
											data: `紧急求助：我需要帮助，请尽快联系我。`,
											success: () => {
												uni.showToast({
													title: '短信内容已复制',
													icon: 'success'
												})
												this.addHelpRecord(contact, '短信求助')
											}
										})
									} else {
										// 提示用户手动发送短信
										uni.showToast({
											title: '请手动发送短信',
											icon: 'none'
										})
										this.addHelpRecord(contact, '短信求助')
									}
								}
							})
						}
					}
				})
			},
			sendMessage(contact) {
				uni.showModal({
					title: '发送消息',
					content: `确认向${contact.name}发送消息吗？`,
					success: (res) => {
						if (res.confirm) {
							uni.showActionSheet({
								itemList: ['我饿了', '我不舒服', '我想你了', '自定义内容'],
								success: async (res) => {
									let content = ''
									switch(res.tapIndex) {
										case 0:
											content = '我饿了，想吃饭'
											break
										case 1:
											content = '我不舒服，需要帮助'
											break
										case 2:
											content = '我想你了，有空来看我'
											break
										case 3:
											uni.showModal({
												title: '自定义消息',
												content: '请输入消息内容',
												editable: true,
												success: async (res) => {
													if (res.confirm && res.content) {
														content = res.content
														await this.sendCustomMessage(contact, content)
													}
												}
											})
											return
									}
									await this.sendCustomMessage(contact, content)
								}
							})
						}
					}
				})
			},
			async sendCustomMessage(contact, content) {
				try {
					await api.older.sendMessage(contact.id, content)
					uni.showToast({
						title: '消息发送成功',
						icon: 'success'
					})
				} catch (error) {
					console.error('发送消息失败:', error)
					uni.showToast({
						title: '发送消息失败',
						icon: 'none'
					})
				}
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
					} else if (type === '消息求助') {
						emergencyType = 'in-wechat-app'
						message = `向${contact.name}发送消息求助`
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
			async loadData() {
				this.loading = true
				try {
					// 加载紧急联系人列表（自动从绑定的家属中获取）
					const contactsResult = await api.older.getEmergencyContacts()
					console.log('获取到的紧急联系人数据:', contactsResult)
					this.emergencyContacts = contactsResult.contacts || []
					console.log('处理后的紧急联系人数据:', this.emergencyContacts)
				} catch (error) {
					console.error('加载数据失败:', error)
					uni.showToast({
						title: '加载数据失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			async setAsPrimary(contactId) {
				uni.showModal({
					title: '确认设置',
					content: '确定要将该联系人设为主要联系人吗？',
					success: async (res) => {
						if (res.confirm) {
							this.loading = true
							try {
								await api.older.setEmergencyContactAsPrimary(contactId)
								uni.showToast({
									title: '设置成功',
									icon: 'success'
								})
								this.loadData() // 重新加载数据
							} catch (error) {
								console.error('设置主要联系人失败:', error)
								uni.showToast({
									title: '设置失败',
									icon: 'none'
								})
							} finally {
								this.loading = false
							}
						}
					}
				})
			}
		}
	}
</script>

<style scoped>
	.emergency-contacts-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 220px, #F5F5F5 100%);
		padding-bottom: 100px;
	}
	
	/* 顶部导航栏 */
	.top-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 58px;
		padding: 0 20px;
		background: rgba(255, 255, 255, 0.92);
		border-bottom: 1px solid rgba(255, 122, 69, 0.08);
		backdrop-filter: blur(8px);
	}
	
	.back-btn {
		font-size: 24px;
		color: #333333;
		width: 36px;
		text-align: center;
	}
	
	.nav-title {
		font-size: 19px;
		font-weight: 600;
		color: #333333;
		flex: 1;
		text-align: center;
	}
	
	.placeholder {
		width: 36px;
	}
	
	/* 紧急求助说明 */
	.emergency-intro {
		text-align: center;
		padding: 24px 20px;
	}
	
	.intro-icon {
		font-size: 40px;
		display: block;
		margin-bottom: 12px;
	}
	
	.intro-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 6px;
	}
	
	.intro-desc {
		font-size: 14px;
		color: #666666;
	}
	
	/* 当前紧急联系人列表 */
	.current-contacts {
		padding: 20px;
	}
	
	.section-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 16px;
		cursor: pointer;
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		display: block;
	}
	
	.collapse-icon {
		font-size: 14px;
		color: #666666;
		font-weight: bold;
	}
	
	.members-content {
		transition: all 0.3s ease;
	}
	
	.contacts-list {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.contact-item {
		background-color: #FFFFFF;
		border-radius: 16px;
		padding: 20px;
		margin-bottom: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 2px solid transparent;
	}
	
	.contact-item.primary-contact {
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
	
	.primary-badge {
		background-color: #FF7A45;
		color: white;
		padding: 2px 8px;
		border-radius: 10px;
		font-size: 12px;
		font-weight: 500;
	}
	
	.contact-actions {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	
	.call-btn, .sms-btn, .message-btn {
		flex: 1;
		padding: 8px 12px;
		border: none;
		border-radius: 12px;
		font-size: 14px;
		font-weight: 500;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 6px;
		min-width: 80px;
	}

	.call-btn {
		background-color: #4CAF50;
		color: white;
	}
	
	.sms-btn {
		background-color: #2196F3;
		color: white;
	}
	
	.message-btn {
		background-color: #9C27B0;
		color: white;
	}

	.call-icon, .sms-icon, .message-icon {
		font-size: 16px;
	}
	
	.btn-primary {
		padding: 6px 12px;
		background-color: #FF7A45;
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 12px;
		font-weight: 500;
		min-width: 60px;
		text-align: center;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.btn-delete {
		padding: 6px 12px;
		background-color: #FF4D4F;
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 12px;
		font-weight: 500;
		min-width: 60px;
		text-align: center;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
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
	
	/* 添加紧急联系人 */
	.add-contact-section {
		padding: 0 20px;
		margin-top: 20px;
	}
	
	.search-container {
		margin-bottom: 16px;
	}
	
	.search-input {
		width: 100%;
		height: 44px;
		padding: 0 16px;
		border: 1px solid #DDDDDD;
		border-radius: 22px;
		font-size: 14px;
		background-color: #FFFFFF;
	}
	
	.search-input:focus {
		border-color: #FF7A45;
		outline: none;
	}
	
	.members-list {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.members-container {
		max-height: 300px;
		overflow-y: auto;
	}
	
	.member-item {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 16px;
		border-bottom: 1px solid #F0F0F0;
	}
	
	.member-item:last-child {
		border-bottom: none;
	}
	
	.member-info {
		flex: 1;
	}
	
	.member-name {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		margin-bottom: 4px;
		display: block;
	}
	
	.member-phone {
		font-size: 14px;
		color: #666666;
	}
	
	.btn-add {
		padding: 8px 16px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border: none;
		border-radius: 16px;
		font-size: 14px;
		font-weight: 500;
		box-shadow: 0 4px 12px rgba(255, 122, 69, 0.2);
	}
	
	/* 空状态 */
	.empty-state {
		text-align: center;
		padding: 40px 20px;
		color: #999999;
	}
	
	.empty-text {
		font-size: 14px;
	}
	
	/* 对话框 */
	.dialog-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}
	
	.dialog-content {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 24px;
		width: 90%;
		max-width: 400px;
		box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
	}
	
	.dialog-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
		text-align: center;
		display: block;
		margin-bottom: 20px;
	}
	
	.dialog-body {
		margin-bottom: 24px;
	}
	
	.form-item {
		margin-bottom: 16px;
	}
	
	.form-label {
		font-size: 14px;
		color: #666666;
		display: block;
		margin-bottom: 8px;
	}
	
	.form-value {
		font-size: 16px;
		color: #333333;
		font-weight: 500;
	}
	
	.form-input {
		width: 100%;
		height: 44px;
		padding: 0 16px;
		border: 1px solid #DDDDDD;
		border-radius: 12px;
		font-size: 14px;
	}
	
	.form-input:focus {
		border-color: #FF7A45;
		outline: none;
	}
	
	.dialog-actions {
		display: flex;
		gap: 12px;
	}
	
	.btn-cancel, .btn-confirm {
		flex: 1;
		height: 44px;
		border-radius: 22px;
		font-size: 15px;
		font-weight: 600;
	}
	
	.btn-cancel {
		background-color: #F5F5F5;
		color: #666666;
		border: 1px solid #DDDDDD;
	}
	
	.btn-confirm {
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border: none;
		box-shadow: 0 4px 12px rgba(255, 122, 69, 0.2);
	}
</style>
