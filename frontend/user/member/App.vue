<template>
	<view class="app-container">
		<slot></slot>
	</view>
</template>

<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	.app-container {
		position: relative;
		width: 100%;
		height: 100%;
	}

	/*每个页面公共css */
	
	/* 全局字体设置 */
	body, text, input, button, textarea {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
		font-size: 16px;
		line-height: 1.6;
		color: #1e293b;
	}
	
	/* 全局背景色 */
	page:not([data-page="login"]) {
		background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
		min-height: 100vh;
		position: relative;
		overflow-x: hidden;
	}
	
	page:not([data-page="login"])::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		background-image: 
			radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
			radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
			radial-gradient(circle at 40% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%);
	}
	
	/* 全局按钮样式 */
	button {
		border: none;
		outline: none;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.3s ease;
	}
	
	button:active {
		transform: scale(0.98);
	}
	
	/* 全局输入框样式 */
	input, textarea {
		border: 2px solid #e2e8f0;
		outline: none;
		transition: all 0.3s ease;
	}
	
	input:focus, textarea:focus {
		border-color: #6366f1;
		box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
	}
	
	/* 全局文本样式 */
	text {
		display: block;
	}
	
	/* 全局标题样式 */
	.page-title {
		font-size: 28px;
		font-weight: 700;
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}
	
	.section-title {
		font-size: 24px;
		font-weight: 600;
		color: #1e293b;
		margin-bottom: 24px;
	}
	
	/* 全局卡片样式 */
	.card {
		background: #ffffff;
		border-radius: 24px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
		padding: 24px;
	}
	
	/* 全局按钮样式 */
	.btn-primary {
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		border-radius: 20px;
		padding: 16px 32px;
		font-size: 16px;
		font-weight: 500;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
	}
	
	.btn-secondary {
		background: #ffffff;
		color: #64748b;
		border: 2px solid #e2e8f0;
		border-radius: 20px;
		padding: 16px 32px;
		font-size: 16px;
		font-weight: 500;
	}
	
	/* 全局状态标签样式 */
	.status-tag {
		padding: 4px 16px;
		border-radius: 12px;
		font-size: 14px;
		font-weight: 500;
	}
	
	.status-tag.success {
		background: rgba(16, 185, 129, 0.1);
		color: #10b981;
	}
	
	.status-tag.warning {
		background: rgba(245, 158, 11, 0.1);
		color: #f59e0b;
	}
	
	.status-tag.danger {
		background: rgba(239, 68, 68, 0.1);
		color: #ef4444;
	}
	
	/* 全局动画效果 */
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	
	@keyframes slideIn {
		from {
			transform: translateX(-100%);
		}
		to {
			transform: translateX(0);
		}
	}
	
	@keyframes pulse {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
		100% {
			transform: scale(1);
		}
	}
	
	.fade-in {
		animation: fadeIn 0.3s ease;
	}
	
	.slide-in {
		animation: slideIn 0.3s ease;
	}
	
	.pulse {
		animation: pulse 2s infinite;
	}
	
	/* 全局工具类 */
	.text-center {
		text-align: center;
	}
	
	.text-primary {
		color: #1e293b;
	}
	
	.text-secondary {
		color: #64748b;
	}
	
	.text-light {
		color: #94a3b8;
	}
	
	.text-success {
		color: #10b981;
	}
	
	.text-warning {
		color: #f59e0b;
	}
	
	.text-danger {
		color: #ef4444;
	}
	
	.bg-primary {
		background: #f8fafc;
	}
	
	.bg-secondary {
		background: #ffffff;
	}
	
	.flex {
		display: flex;
	}
	
	.flex-column {
		flex-direction: column;
	}
	
	.items-center {
		align-items: center;
	}
	
	.justify-center {
		justify-content: center;
	}
	
	.justify-between {
		justify-content: space-between;
	}
	
	.gap-sm {
		gap: 16px;
	}
	
	.gap-md {
		gap: 20px;
	}
	
	.p-0 {
		padding: 0;
	}
	
	.p-sm {
		padding: 16px;
	}
	
	.p-md {
		padding: 20px;
	}
	
	.p-lg {
		padding: 24px;
	}
	
	.m-0 {
		margin: 0;
	}
	
	.m-sm {
		margin: 16px;
	}
	
	.m-md {
		margin: 20px;
	}
	
	.m-lg {
		margin: 24px;
	}
	
	.mb-sm {
		margin-bottom: 16px;
	}
	
	.mb-md {
		margin-bottom: 20px;
	}
	
	.mb-lg {
		margin-bottom: 24px;
	}
</style>
