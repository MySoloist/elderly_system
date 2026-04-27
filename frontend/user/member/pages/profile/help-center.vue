<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">帮助中心</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 搜索框 -->
		<view class="search-section">
			<view class="search-box">
				<text class="search-icon">🔍</text>
				<input class="search-input" placeholder="搜索问题..." />
			</view>
		</view>
		
		<!-- 常见问题 -->
		<view class="faq-section">
			<text class="section-title">常见问题</text>
			<view class="faq-item" v-for="(faq, index) in faqs" :key="index" @click="toggleFaq(index)">
				<view class="faq-question">
					<text class="question-text">{{ faq.question }}</text>
					<text class="faq-arrow">{{ faq.expanded ? '▼' : '▶' }}</text>
				</view>
				<view class="faq-answer" v-if="faq.expanded">
					<text class="answer-text">{{ faq.answer }}</text>
				</view>
			</view>
		</view>
		
		<!-- 帮助分类 -->
		<view class="help-categories">
			<view class="category-item" @click="goToCategory('order')">
				<view class="category-icon order-icon"></view>
				<text class="category-name">订单问题</text>
			</view>
			<view class="category-item" @click="goToCategory('payment')">
				<view class="category-icon payment-icon"></view>
				<text class="category-name">支付问题</text>
			</view>
			<view class="category-item" @click="goToCategory('bind')">
				<view class="category-icon bind-icon"></view>
				<text class="category-name">绑定问题</text>
			</view>
			<view class="category-item" @click="goToCategory('health')">
				<view class="category-icon health-icon"></view>
				<text class="category-name">健康问题</text>
			</view>
		</view>
		
		<!-- 联系客服 -->
		<view class="contact-section">
			<button class="contact-btn" @click="contactService">
				<text class="contact-icon">📞</text>
				<text class="contact-text">联系客服</text>
			</button>
		</view>
		
		<!-- 使用指南 -->
		<view class="guide-section">
			<text class="section-title">使用指南</text>
			<view class="guide-item" @click="viewGuide('first')">
				<view class="guide-icon first-icon"></view>
				<text class="guide-name">首次使用指南</text>
			</view>
			<view class="guide-item" @click="viewGuide('elder')">
				<view class="guide-icon elder-icon"></view>
				<text class="guide-name">老人绑定教程</text>
			</view>
			<view class="guide-item" @click="viewGuide('order')">
				<view class="guide-icon order-guide-icon"></view>
				<text class="guide-name">订餐操作流程</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			faqs: [
				{
					question: '如何绑定老人信息？',
					answer: '在个人中心页面点击"添加老人"，按照提示填写老人信息并完成绑定。需要老人的身份证号和手机号进行验证。',
					expanded: false
				},
				{
					question: '忘记密码怎么办？',
					answer: '在登录页面点击"忘记密码"，通过手机号验证码重置密码。如果无法重置，请联系客服协助处理。',
					expanded: false
				},
				{
					question: '如何取消订单？',
					answer: '在订单详情页面点击"取消订单"按钮，订单状态为"待支付"或"处理中"时可以取消。',
					expanded: false
				},
				{
					question: '配送时间是多久？',
					answer: '通常配送时间为30-60分钟，具体时间根据距离和订单量而定。可以在订单详情页面查看实时配送状态。',
					expanded: false
				},
				{
					question: '可以修改已下单的餐品吗？',
					answer: '订单支付后无法修改餐品，如需修改请取消订单重新下单。',
					expanded: false
				}
			]
		};
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		toggleFaq(index) {
			this.faqs[index].expanded = !this.faqs[index].expanded;
		},
		goToCategory(category) {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		getCategoryName(category) {
			const names = {
				'order': '订单问题',
				'payment': '支付问题',
				'bind': '绑定问题',
				'health': '健康问题'
			};
			return names[category] || category;
		},
		contactService() {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		viewGuide(guide) {
			uni.showToast({
				title: '后续功能开发中...',
				icon: 'none',
				duration: 2000
			});
		},
		getGuideName(guide) {
			const names = {
				'first': '首次使用指南',
				'elder': '老人绑定教程',
				'order': '订餐操作流程'
			};
			return names[guide] || guide;
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background-color: #f8fafc;
	padding-bottom: 20px;
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

/* 搜索框 */
.search-section {
	padding: 24px;
}

.search-box {
	display: flex;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 12px 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.6);
}

.search-icon {
	font-size: 20px;
	color: #64748b;
	margin-right: 12px;
}

.search-input {
	flex: 1;
	font-size: 16px;
	color: #1e293b;
}

/* 常见问题 */
.faq-section {
	padding: 0 24px 24px;
}

.section-title {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 16px;
	display: block;
}

.faq-item {
	background: #ffffff;
	border-radius: 16px;
	margin-bottom: 12px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.6);
	overflow: hidden;
}

.faq-question {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 16px;
	transition: background-color 0.3s ease;
}

.faq-question:active {
	background-color: #f8fafc;
}

.question-text {
	flex: 1;
	font-size: 15px;
	font-weight: 500;
	color: #1e293b;
	margin-right: 16px;
}

.faq-arrow {
	font-size: 12px;
	color: #94a3b8;
	transition: transform 0.3s ease;
}

.faq-answer {
	padding: 0 16px 16px;
	border-top: 1px solid rgba(226, 232, 240, 0.4);
	background-color: #f8fafc;
}

.answer-text {
	font-size: 14px;
	color: #64748b;
	line-height: 1.6;
	display: block;
	padding-top: 12px;
}

/* 帮助分类 */
.help-categories {
	padding: 0 24px 24px;
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 16px;
}

.category-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 20px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.6);
	transition: all 0.3s ease;
}

.category-item:active {
	transform: scale(0.98);
	background-color: #f8fafc;
}

.category-icon {
	width: 48px;
	height: 48px;
	border-radius: 16px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: 12px;
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.order-icon::before {
	content: '📋';
	font-size: 24px;
}

.payment-icon::before {
	content: '💳';
	font-size: 24px;
}

.bind-icon::before {
	content: '🔗';
	font-size: 24px;
}

.health-icon::before {
	content: '❤️';
	font-size: 24px;
}

.category-name {
	font-size: 14px;
	font-weight: 500;
	color: #1e293b;
}

/* 联系客服 */
.contact-section {
	padding: 0 24px 24px;
}

.contact-btn {
	width: 100%;
	height: 48px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 12px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 500;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
	transition: all 0.3s ease;
}

.contact-btn:active {
	transform: scale(0.98);
	box-shadow: 0 2px 6px rgba(99, 102, 241, 0.2);
}

.contact-icon {
	font-size: 20px;
}

.contact-text {
	
}

/* 使用指南 */
.guide-section {
	padding: 0 24px 40px;
}

.guide-item {
	display: flex;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 16px;
	margin-bottom: 12px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.6);
	transition: all 0.3s ease;
}

.guide-item:active {
	background-color: #f8fafc;
	transform: scale(0.98);
}

.guide-icon {
	width: 40px;
	height: 40px;
	border-radius: 8px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 16px;
}

.first-icon::before {
	content: '🏠';
	font-size: 20px;
}

.elder-icon::before {
	content: '👴';
	font-size: 20px;
}

.order-guide-icon::before {
	content: '🍽️';
	font-size: 20px;
}

.guide-name {
	flex: 1;
	font-size: 16px;
	font-weight: 500;
	color: #1e293b;
}
</style>
