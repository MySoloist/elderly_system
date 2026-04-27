<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="nav-bar">
			<button class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</button>
			<text class="nav-title">消息中心</text>
			<button class="clear-btn" @click="clearAll">
				<text class="clear-text">清除全部</text>
			</button>
		</view>
		
		<!-- 消息分类标签 -->
		<view class="category-tabs">
			<view 
				class="tab-item" 
				:class="{ active: activeTab === tab.type }"
				v-for="tab in tabs" 
				:key="tab.type"
				@click="switchTab(tab.type)"
			>
				<text class="tab-text">{{ tab.name }}</text>
				<view class="tab-badge" v-if="tab.count > 0">
					<text class="badge-text">{{ tab.count }}</text>
				</view>
			</view>
		</view>
		
		<!-- 消息列表 -->
		<view class="message-list">
			<view 
				class="message-item" 
				v-for="(message, index) in filteredMessages" 
				:key="index"
				:class="{ unread: !message.read }"
				@click="viewMessage(message)"
			>
				<view class="message-icon">
					<text class="icon-emoji">{{ message.icon }}</text>
				</view>
				<view class="message-content">
					<view class="message-header">
						<text class="message-title">{{ message.title }}</text>
						<text class="message-time">{{ message.time }}</text>
					</view>
					<text class="message-preview">{{ message.preview }}</text>
				</view>
				<view class="message-dot" v-if="!message.read"></view>
			</view>
			
			<!-- 空状态 -->
			<view class="empty-state" v-if="filteredMessages.length === 0">
				<text class="empty-icon">📭</text>
				<text class="empty-text">暂无消息</text>
			</view>
		</view>
	</view>
</template>

<script>
import { messageService } from '../../api/message.js';

export default {
	data() {
		return {
			activeTab: 'all',
			tabs: [
				{ type: 'all', name: '全部消息', count: 0 },
				{ type: 'system', name: '系统通知', count: 0 },
				{ type: 'notice', name: '一般通知', count: 0 },
				{ type: 'emergency', name: '紧急通知', count: 0 }
			],
			messages: [],
			loading: false
		};
	},
	onLoad() {
		this.loadMessages();
	},
	computed: {
		filteredMessages() {
			if (this.activeTab === 'all') {
				return this.messages;
			}
			return this.messages.filter(message => message.type === this.activeTab);
		}
	},
	methods: {
		async loadMessages() {
			this.loading = true;
			try {
				console.log('开始加载消息...');
				const messages = await messageService.getMessages();
				console.log('获取到的消息数据:', messages);
				console.log('消息数量:', messages.length);
				this.messages = messages;
				this.updateUnreadCount();
				console.log('更新后的messages:', this.messages);
				console.log('filteredMessages:', this.filteredMessages);
			} catch (error) {
				console.error('加载消息失败:', error);
				uni.showToast({
					title: '加载消息失败',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		goBack() {
			uni.navigateBack();
		},
		switchTab(tab) {
			this.activeTab = tab;
		},
		async viewMessage(message) {
			try {
				// 调用API标记为已读
				await messageService.markAsRead(message.id);
				// 更新本地状态
				message.read = true;
				// 更新未读数量
				this.updateUnreadCount();
				
				// 显示消息详情
				uni.showModal({
					title: message.title,
					content: message.content,
					showCancel: false,
					confirmText: '知道了'
				});
			} catch (error) {
				console.error('标记消息已读失败:', error);
			}
		},
		async clearAll() {
			uni.showModal({
				title: '清除消息',
				content: '确定要清除所有消息吗？',
				success: async (res) => {
					if (res.confirm) {
						try {
							await messageService.clearAll();
							this.messages = [];
							this.updateUnreadCount();
							uni.showToast({
								title: '已清除所有消息',
								icon: 'success'
							});
						} catch (error) {
							console.error('清除消息失败:', error);
							uni.showToast({
								title: '清除消息失败',
								icon: 'none'
							});
						}
					}
				}
			});
		},
		updateUnreadCount() {
			this.tabs.forEach(tab => {
				if (tab.type === 'all') {
					tab.count = this.messages.filter(m => !m.read).length;
				} else {
					tab.count = this.messages.filter(m => m.type === tab.type && !m.read).length;
				}
			});
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	position: relative;
	overflow-x: hidden;
}

/* 顶部导航 */
.nav-bar {
	height: 44px;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(10px);
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 0 16px;
	position: sticky;
	top: 0;
	z-index: 100;
	border-bottom: 1px solid rgba(226, 232, 240, 0.5);
}

.back-btn {
	width: 40px;
	height: 40px;
	background: rgba(99, 102, 241, 0.1);
	border: none;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.back-icon {
	font-size: 24px;
	color: #6366f1;
}

.nav-title {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
}

.clear-btn {
	padding: 8px 16px;
	background: transparent;
	border: none;
	border-radius: 8px;
	color: #6366f1;
	font-size: 14px;
	font-weight: 500;
}

.clear-text {
	
}

/* 消息分类标签 */
.category-tabs {
	display: flex;
	background: rgba(255, 255, 255, 0.95);
	padding: 8px 16px 8px 16px;
	margin-top: 10px;
	overflow-x: auto;
	white-space: nowrap;
	border-bottom: 1px solid rgba(226, 232, 240, 0.5);
}

.tab-item {
	display: flex;
	align-items: center;
	padding: 16px 12px;
	position: relative;
	margin-right: 20px;
	min-width: 80px;
	text-align: center;
}

.tab-item.active .tab-text {
	color: #6366f1;
	font-weight: 600;
}

.tab-text {
	font-size: 14px;
	color: #64748b;
}

.tab-badge {
	background: #ef4444;
	color: #ffffff;
	border-radius: 50%;
	min-width: 18px;
	height: 18px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 12px;
	font-weight: 600;
	padding: 0 4px;
	margin-left: 6px;
	box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
}

.badge-text {
	
}

/* 消息列表 */
.message-list {
	padding: 24px 16px 16px;
}

.message-item {
	display: flex;
	align-items: center;
	background: rgba(255, 255, 255, 0.95);
	border-radius: 12px;
	padding: 16px;
	margin-bottom: 12px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
	border: 1px solid rgba(226, 232, 240, 0.5);
}

.message-item.unread {
	background: rgba(99, 102, 241, 0.05);
	border-color: rgba(99, 102, 241, 0.3);
}

.message-icon {
	width: 48px;
	height: 48px;
	border-radius: 12px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 16px;
	box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
}

.icon-emoji {
	font-size: 24px;
}

.message-content {
	flex: 1;
}

.message-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 8px;
}

.message-title {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
	flex: 1;
}

.message-time {
	font-size: 12px;
	color: #94a3b8;
	margin-left: 12px;
}

.message-preview {
	font-size: 14px;
	color: #64748b;
	line-height: 1.5;
}

.message-dot {
	width: 8px;
	height: 8px;
	border-radius: 50%;
	background: #ef4444;
	margin-left: 12px;
	box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
}

/* 空状态 */
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 48px 0;
}

.empty-icon {
	font-size: 64px;
	margin-bottom: 16px;
}

.empty-text {
	font-size: 14px;
	color: #94a3b8;
}
</style>
