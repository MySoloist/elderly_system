<template>
	<view class="help-container">
		<view class="search-section">
			<view class="search-box">
				<text class="search-icon">🔍</text>
				<input v-model="searchKeyword" type="text" placeholder="搜索帮助问题..." class="search-input" />
			</view>
		</view>
		
		<view class="faq-section">
			<text class="section-title">常见问题</text>
			<view v-for="faq in filteredFaqs" :key="faq.id" class="faq-item" @click="toggleFaq(faq.id)">
				<view class="faq-header">
					<text class="faq-question">{{ faq.question }}</text>
					<text class="faq-toggle" :class="{ expanded: expandedFaq === faq.id }">▼</text>
				</view>
				<view v-if="expandedFaq === faq.id" class="faq-answer">
					{{ faq.answer }}
				</view>
			</view>
		</view>
		
		<view class="contact-section">
			<text class="section-title">联系客服</text>
			<view class="contact-card">
				<view class="contact-item">
					<text class="contact-icon">📞</text>
					<view class="contact-info">
						<text class="contact-label">客服电话</text>
						<text class="contact-value" @click="makePhoneCall">400-123-4567</text>
					</view>
				</view>
				<view class="contact-item">
					<text class="contact-icon">💬</text>
					<view class="contact-info">
						<text class="contact-label">在线客服</text>
						<text class="contact-action" @click="onlineService">立即咨询</text>
					</view>
				</view>
				<view class="contact-item">
					<text class="contact-icon">✉️</text>
					<view class="contact-info">
						<text class="contact-label">邮箱反馈</text>
						<text class="contact-value">service@yiyangfood.com</text>
					</view>
				</view>
			</view>
		</view>
		
		<view class="feedback-section">
			<text class="section-title">意见反馈</text>
			<view class="feedback-card">
				<textarea 
					v-model="feedbackContent" 
					placeholder="请描述您遇到的问题或建议..."
					class="feedback-input"
					:maxlength="500"
				></textarea>
				<text class="char-count">{{ feedbackContent.length }}/500</text>
				<button @click="submitFeedback" class="submit-button">提交反馈</button>
			</view>
		</view>
		
		<view class="emergency-section">
			<text class="section-title">紧急情况</text>
			<view class="emergency-card">
				<view class="emergency-item">
					<text class="emergency-icon">🚨</text>
					<view class="emergency-info">
						<text class="emergency-label">紧急求助</text>
						<text class="emergency-action" @click="emergencyHelp">立即求助</text>
					</view>
				</view>
				<view class="emergency-item">
					<text class="emergency-icon">🚑</text>
					<view class="emergency-info">
						<text class="emergency-label">医疗急救</text>
						<text class="emergency-action" @click="callEmergency">120</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				searchKeyword: '',
				expandedFaq: null,
				feedbackContent: '',
				faqs: [
					{
						id: 1,
						question: '如何接单？',
						answer: '在订单页面，点击"待接单"标签，选择订单后点击"接单"按钮即可。接单后订单状态会变为"配送中"。'
					},
					{
						id: 2,
						question: '如何确认送达？',
						answer: '在订单详情页面或导航页面，点击"确认送达"按钮，确认后订单状态会变为"已完成"。'
					},
					{
						id: 3,
						question: '如何处理异常情况？',
						answer: '在订单详情页面，点击"异常处理"按钮，选择异常类型并填写详细描述，必要时上传现场照片。'
					},
					{
						id: 4,
						question: '如何联系老人？',
						answer: '在订单详情页面或导航页面，点击"联系老人"按钮，可以直接拨打老人电话。'
					},
					{
						id: 5,
						question: '如何查看收入明细？',
						answer: '在个人中心页面，点击"收入明细"可以查看详细的收入记录，包括每笔订单的收入情况。'
					},
					{
						id: 6,
						question: '如何修改个人信息？',
						answer: '在个人中心页面，点击"个人信息"可以修改姓名、手机号、身份证号等个人信息。'
					},
					{
						id: 7,
						question: '如何设置排班？',
						answer: '在个人中心页面，点击"排班管理"可以选择本周或月度排班时间。'
					},
					{
						id: 8,
						question: '如何修改密码？',
						answer: '在设置页面，点击"修改密码"可以修改登录密码。'
					}
				]
			}
		},
		computed: {
			filteredFaqs() {
				if (!this.searchKeyword) {
					return this.faqs
				}
				return this.faqs.filter(faq => 
					faq.question.toLowerCase().includes(this.searchKeyword.toLowerCase()) ||
					faq.answer.toLowerCase().includes(this.searchKeyword.toLowerCase())
				)
			}
		},
		methods: {
			toggleFaq(faqId) {
				this.expandedFaq = this.expandedFaq === faqId ? null : faqId
			},
			makePhoneCall() {
				uni.makePhoneCall({
					phoneNumber: '4001234567',
					success: () => {
						console.log('拨打电话成功')
					},
					fail: () => {
						uni.showToast({
							title: '拨打电话失败',
							icon: 'none'
						})
					}
				})
			},
			onlineService() {
				uni.showToast({
					title: '在线客服功能开发中',
					icon: 'none'
				})
			},
			submitFeedback() {
				if (!this.feedbackContent || this.feedbackContent.trim() === '') {
					uni.showToast({
						title: '请输入反馈内容',
						icon: 'none'
					})
					return
				}
				
				uni.showToast({
					title: '反馈提交成功',
					icon: 'success'
				})
				
				this.feedbackContent = ''
			},
			emergencyHelp() {
				uni.showModal({
					title: '紧急求助',
					content: '确定要发起紧急求助吗？',
					success: (res) => {
						if (res.confirm) {
							uni.showToast({
								title: '紧急求助已发送',
								icon: 'success'
							})
						}
					}
				})
			},
			callEmergency() {
				uni.makePhoneCall({
					phoneNumber: '120',
					success: () => {
						console.log('拨打急救电话成功')
					},
					fail: () => {
						uni.showToast({
							title: '拨打电话失败',
							icon: 'none'
						})
					}
				})
			}
		}
	}
</script>

<style scoped>
	.help-container {
		min-height: 100vh;
	}
	
	.search-section {
		background-color: white;
		padding: 20rpx 30rpx;
	}
	
	.search-box {
		display: flex;
		align-items: center;
		background-color: #f8fafc;
		border-radius: 16rpx;
		padding: 0 20rpx;
	}
	
	.search-icon {
		font-size: 28rpx;
		color: #94a3b8;
		margin-right: 16rpx;
	}
	
	.search-input {
		flex: 1;
		height: 72rpx;
		font-size: 28rpx;
		color: #1e293b;
	}
	
	.faq-section {
		background-color: white;
		margin-top: 20rpx;
	}
	
	.section-title {
		display: block;
		font-size: 28rpx;
		color: #64748b;
		font-weight: 500;
		padding: 20rpx 30rpx;
	}
	
	.faq-item {
		border-bottom: 1rpx solid #f1f5f9;
	}
	
	.faq-item:last-child {
		border-bottom: none;
	}
	
	.faq-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
	}
	
	.faq-question {
		font-size: 32rpx;
		color: #1e293b;
		font-weight: 500;
		flex: 1;
	}
	
	.faq-toggle {
		font-size: 24rpx;
		color: #94a3b8;
		transition: transform 0.3s;
	}
	
	.faq-toggle.expanded {
		transform: rotate(180deg);
	}
	
	.faq-answer {
		padding: 0 30rpx 30rpx;
		font-size: 28rpx;
		color: #64748b;
		line-height: 1.5;
	}
	
	.contact-section {
		background-color: white;
		margin-top: 20rpx;
	}
	
	.contact-card {
		padding: 0 30rpx 30rpx;
	}
	
	.contact-item {
		display: flex;
		align-items: center;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f1f5f9;
	}
	
	.contact-item:last-child {
		border-bottom: none;
	}
	
	.contact-icon {
		font-size: 32rpx;
		margin-right: 20rpx;
	}
	
	.contact-info {
		flex: 1;
	}
	
	.contact-label {
		display: block;
		font-size: 28rpx;
		color: #64748b;
		margin-bottom: 8rpx;
	}
	
	.contact-value {
		display: block;
		font-size: 32rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.contact-action {
		display: block;
		font-size: 32rpx;
		color: #10b981;
		font-weight: 500;
	}
	
	.feedback-section {
		background-color: white;
		margin-top: 20rpx;
	}
	
	.feedback-card {
		padding: 0 30rpx 30rpx;
	}
	
	.feedback-input {
		width: 100%;
		height: 200rpx;
		background-color: #f8fafc;
		border: 1rpx solid #e2e8f0;
		border-radius: 16rpx;
		padding: 20rpx;
		font-size: 28rpx;
		color: #1e293b;
		resize: none;
	}
	
	.char-count {
		display: block;
		text-align: right;
		font-size: 24rpx;
		color: #94a3b8;
		margin-top: 10rpx;
		margin-bottom: 20rpx;
	}
	
	.submit-button {
		width: 100%;
		height: 88rpx;
		background-color: #10b981;
		color: white;
		border: none;
		border-radius: 20rpx;
		font-size: 32rpx;
		font-weight: 500;
	}
	
	.emergency-section {
		background-color: white;
		margin-top: 20rpx;
		margin-bottom: 40rpx;
	}
	
	.emergency-card {
		padding: 0 30rpx 30rpx;
	}
	
	.emergency-item {
		display: flex;
		align-items: center;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f1f5f9;
	}
	
	.emergency-item:last-child {
		border-bottom: none;
	}
	
	.emergency-icon {
		font-size: 32rpx;
		margin-right: 20rpx;
	}
	
	.emergency-info {
		flex: 1;
	}
	
	.emergency-label {
		display: block;
		font-size: 28rpx;
		color: #64748b;
		margin-bottom: 8rpx;
	}
	
	.emergency-action {
		display: block;
		font-size: 32rpx;
		color: #ef4444;
		font-weight: 500;
	}
</style>