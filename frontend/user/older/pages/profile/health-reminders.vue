<template>
	<view class="health-reminders-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">健康提醒</text>
			<text class="placeholder"></text>
		</view>
		
		<!-- 分类标签 -->
		<view class="category-tabs">
			<view 
				v-for="category in categories" 
				:key="category.value"
				class="category-tab"
				:class="{ active: activeCategory === category.value }"
				@click="switchCategory(category.value)"
			>
				<text class="category-text">{{ category.label }}</text>
				<view class="category-badge" v-if="categoryUnreadCounts[category.value] > 0">
					<text class="badge-text">{{ categoryUnreadCounts[category.value] }}</text>
				</view>
			</view>
		</view>
		
		<!-- 健康提醒列表 -->
		<view class="reminders-list">
			<view 
				v-for="reminder in filteredReminders" 
				:key="reminder.id"
				class="reminder-item"
				:class="{ unread: reminder.status === 'pending' }"
				@click="viewReminder(reminder)"
			>
				<view class="reminder-header">
					<text class="reminder-sender">{{ reminder.sender_name }}</text>
					<view class="reminder-meta">
						<text class="reminder-type" :class="reminder.reminder_type">{{ getReminderTypeName(reminder.reminder_type) }}</text>
						<text class="reminder-time">{{ formatTime(reminder.created_at) }}</text>
					</view>
				</view>
				<text class="reminder-content">{{ reminder.content }}</text>
				<view class="reminder-footer">
					<view class="reminder-dot" v-if="reminder.status === 'pending'"></view>
					<text class="reminder-arrow">→</text>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-if="reminders.length === 0 && !loading" class="empty-state">
				<text class="empty-icon">💬</text>
				<text class="empty-text">暂无健康提醒</text>
				<text class="empty-desc">家属还没有给您发送健康提醒</text>
			</view>
			
			<!-- 加载状态 -->
			<view v-if="loading" class="loading-state">
				<text class="loading-text">加载中...</text>
			</view>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				reminders: [],
				loading: false,
				categories: [
					{ label: '全部', value: 'all' },
					{ label: '饮食提醒', value: 'diet' },
					{ label: '健康建议', value: 'health' },
					{ label: '体检提醒', value: 'checkup' }
				],
				activeCategory: 'all'
			}
		},
		computed: {
			filteredReminders() {
				if (this.activeCategory === 'all') {
					return this.reminders
				}
				return this.reminders.filter(reminder => reminder.reminder_type === this.activeCategory)
			},
			// 获取每个分类的未读数量
			categoryUnreadCounts() {
				const counts = {}
				counts.all = this.reminders.filter(r => r.status === 'pending').length
				counts.diet = this.reminders.filter(r => r.reminder_type === 'diet' && r.status === 'pending').length
				counts.health = this.reminders.filter(r => r.reminder_type === 'health' && r.status === 'pending').length
				counts.checkup = this.reminders.filter(r => r.reminder_type === 'checkup' && r.status === 'pending').length
				return counts
			}
		},
		onLoad() {
			this.loadReminders()
		},
		methods: {
			async loadReminders() {
				this.loading = true
				try {
					const response = await api.older.getHealthReminders()
					this.reminders = response
				} catch (error) {
					console.error('获取健康提醒列表失败:', error)
					uni.showToast({
						title: '获取健康提醒列表失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			async viewReminder(reminder) {
				// 标记为已读
				if (reminder.status === 'pending') {
					try {
						await api.older.markHealthReminderAsRead(reminder.id)
						// 更新本地状态
						reminder.status = 'read'
					} catch (error) {
						console.error('标记健康提醒为已读失败:', error)
					}
				}
				
				// 显示提醒详情
				uni.showModal({
					title: `${reminder.sender_name}的健康提醒`,
					content: reminder.content,
					showCancel: false,
					confirmText: '知道了'
				})
			},
			getReminderTypeName(type) {
				const typeMap = {
					'diet': '饮食提醒',
					'health': '健康建议',
					'checkup': '体检提醒'
				}
				return typeMap[type] || type
			},
			formatTime(time) {
				const date = new Date(time)
				const now = new Date()
				const diff = now - date
				const days = Math.floor(diff / (1000 * 60 * 60 * 24))
				
				if (days === 0) {
					return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
				} else if (days === 1) {
					return '昨天'
				} else if (days < 7) {
					return `${days}天前`
				} else {
					return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
				}
			},
			switchCategory(category) {
				this.activeCategory = category
			},
			goBack() {
				uni.navigateBack()
			}
		}
	}
</script>

<style scoped>
	.health-reminders-container {
		min-height: 100vh;
		background-color: #F5F5F5;
	}
	
	/* 顶部导航栏 */
	.top-nav {
		background-color: #FF7A45;
		color: white;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 16px 20px;
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 100;
		box-shadow: 0 2px 8px rgba(255, 122, 69, 0.3);
	}
	
	.back-btn {
		font-size: 24px;
		font-weight: 600;
	}
	
	.nav-title {
		font-size: 18px;
		font-weight: 600;
	}
	
	.placeholder {
		width: 30px;
	}
	
	/* 分类标签 */
	.category-tabs {
		display: flex;
		background-color: white;
		padding: 0 20px;
		position: fixed;
		top: 64px;
		left: 0;
		right: 0;
		z-index: 90;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		border-bottom: 1px solid #F0F0F0;
	}
	
	.category-tab {
		flex: 1;
		padding: 16px 0;
		text-align: center;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;
	}
	
	.category-tab.active .category-text {
		color: #FF7A45;
		font-weight: 600;
	}
	
	.category-tab.active::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 50%;
		transform: translateX(-50%);
		width: 30px;
		height: 3px;
		background-color: #FF7A45;
		border-radius: 2px;
	}
	
	.category-text {
		font-size: 14px;
		color: #666666;
	}
	
	.category-badge {
		background-color: #FF4D4F;
		color: white;
		border-radius: 10px;
		min-width: 20px;
		height: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 12px;
		font-weight: 600;
		padding: 0 6px;
		box-shadow: 0 2px 8px rgba(255, 77, 79, 0.4);
	}
	
	.badge-text {
		
	}
	
	/* 健康提醒列表 */
	.reminders-list {
		padding: 120px 20px 20px;
	}
	
	.reminder-item {
		background-color: white;
		border-radius: 16px;
		padding: 20px;
		margin-bottom: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		border: 1px solid #F0F0F0;
	}
	
	.reminder-item.unread {
		background-color: rgba(255, 122, 69, 0.05);
		border-color: rgba(255, 122, 69, 0.3);
	}
	
	.reminder-header {
		margin-bottom: 12px;
	}
	
	.reminder-sender {
		font-size: 17px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 8px;
	}
	
	.reminder-meta {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	
	.reminder-type {
		font-size: 12px;
		padding: 4px 12px;
		border-radius: 12px;
		font-weight: 500;
	}
	
	.reminder-type.diet {
		background-color: #E6F7FF;
		color: #1890FF;
	}
	
	.reminder-type.health {
		background-color: #F6FFED;
		color: #52C41A;
	}
	
	.reminder-type.checkup {
		background-color: #FFF2F0;
		color: #FF4D4F;
	}
	
	.reminder-time {
		font-size: 12px;
		color: #999999;
	}
	
	.reminder-content {
		font-size: 14px;
		color: #666666;
		line-height: 1.5;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
		margin-bottom: 12px;
	}
	
	.reminder-footer {
		display: flex;
		align-items: center;
		justify-content: flex-end;
		gap: 8px;
	}
	
	.reminder-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background-color: #FF4D4F;
		box-shadow: 0 2px 8px rgba(255, 77, 79, 0.4);
	}
	
	.reminder-arrow {
		font-size: 16px;
		color: #999999;
		font-weight: 600;
	}
	
	/* 空状态 */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 80px 20px;
	}
	
	.empty-icon {
		font-size: 64px;
		margin-bottom: 16px;
	}
	
	.empty-text {
		font-size: 16px;
		color: #999999;
		margin-bottom: 8px;
		font-weight: 500;
	}
	
	.empty-desc {
		font-size: 14px;
		color: #CCCCCC;
	}
	
	/* 加载状态 */
	.loading-state {
		display: flex;
		justify-content: center;
		padding: 20px;
	}
	
	.loading-text {
		font-size: 14px;
		color: #999999;
	}
</style>
