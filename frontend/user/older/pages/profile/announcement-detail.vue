<template>
	<view class="announcement-detail-container">
		<!-- 页面标题 -->
		<view class="page-header">
			<text class="back-btn" @click="goBack">←</text>
			<text class="page-title">公告详情</text>
			<view class="placeholder"></view>
		</view>
		
		<!-- 公告详情内容 -->
		<view v-if="announcement" class="announcement-content">
			<!-- 公告头部信息 -->
			<view class="announcement-header">
				<text class="announcement-title">{{ announcement.title }}</text>
				<view class="announcement-meta">
					<text class="announcement-type" :class="announcement.type">{{ getTypeName(announcement.type) }}</text>
					<text class="announcement-priority" :class="announcement.priority">{{ getPriorityName(announcement.priority) }}</text>
					<text class="announcement-time">{{ formatTime(announcement.created_at) }}</text>
				</view>
			</view>
			
			<!-- 公告内容 -->
			<view class="announcement-body">
				<text class="content-text">{{ announcement.content }}</text>
			</view>
			
			<!-- 公告底部信息 -->
			<view class="announcement-footer">
				<text class="announcement-status" :class="announcement.status">{{ getStatusName(announcement.status) }}</text>
			</view>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-state">
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 错误状态 -->
		<view v-if="error" class="error-state">
			<text class="error-icon">❌</text>
			<text class="error-text">加载失败</text>
			<button class="retry-btn" @click="loadAnnouncement">重新加载</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				announcement: null,
				loading: false,
				error: false,
				announcementId: ''
			}
		},
		onLoad(options) {
			this.announcementId = options.id
			this.loadAnnouncement()
		},
		methods: {
			async loadAnnouncement() {
				if (!this.announcementId) {
					uni.showToast({
						title: '公告ID不能为空',
						icon: 'none'
					})
					return
				}
				
				this.loading = true
				this.error = false
				
				try {
					const response = await api.older.getAnnouncement(this.announcementId)
					this.announcement = response
				} catch (error) {
					console.error('获取公告详情失败:', error)
					this.error = true
					uni.showToast({
						title: '获取公告详情失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			getTypeName(type) {
				const typeMap = {
					'system': '系统公告',
					'notice': '通知',
					'emergency': '紧急通知'
				}
				return typeMap[type] || type
			},
			getPriorityName(priority) {
				const priorityMap = {
					'high': '高优先级',
					'normal': '普通',
					'low': '低优先级'
				}
				return priorityMap[priority] || priority
			},
			getStatusName(status) {
				const statusMap = {
					'active': '生效中',
					'inactive': '已失效'
				}
				return statusMap[status] || status
			},
			formatTime(time) {
				const date = new Date(time)
				return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
			},
			goBack() {
				uni.navigateBack()
			}
		}
	}
</script>

<style scoped>
	.announcement-detail-container {
		min-height: 100vh;
		background-color: #F5F5F5;
	}
	
	/* 页面标题 */
	.page-header {
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
	
	.page-title {
		font-size: 18px;
		font-weight: 600;
	}
	
	.placeholder {
		width: 30px;
	}
	
	/* 公告内容 */
	.announcement-content {
		padding: 70px 20px 20px;
	}
	
	/* 公告头部 */
	.announcement-header {
		background-color: white;
		border-radius: 16px;
		padding: 24px;
		margin-bottom: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		border: 1px solid #F0F0F0;
	}
	
	.announcement-title {
		font-size: 20px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 16px;
		line-height: 1.4;
	}
	
	.announcement-meta {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 12px;
	}
	
	.announcement-type {
		font-size: 12px;
		padding: 4px 12px;
		border-radius: 12px;
		font-weight: 500;
	}
	
	.announcement-type.system {
		background-color: #E6F7FF;
		color: #1890FF;
	}
	
	.announcement-type.notice {
		background-color: #F6FFED;
		color: #52C41A;
	}
	
	.announcement-type.emergency {
		background-color: #FFF2F0;
		color: #FF4D4F;
	}
	
	.announcement-priority {
		font-size: 12px;
		padding: 4px 12px;
		border-radius: 12px;
		font-weight: 500;
	}
	
	.announcement-priority.high {
		background-color: #FFF2F0;
		color: #FF4D4F;
	}
	
	.announcement-priority.normal {
		background-color: #F0F0F0;
		color: #666666;
	}
	
	.announcement-priority.low {
		background-color: #F5F5F5;
		color: #999999;
	}
	
	.announcement-time {
		font-size: 12px;
		color: #999999;
	}
	
	/* 公告正文 */
	.announcement-body {
		background-color: white;
		border-radius: 16px;
		padding: 24px;
		margin-bottom: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		border: 1px solid #F0F0F0;
	}
	
	.content-text {
		font-size: 16px;
		color: #333333;
		line-height: 1.6;
		display: block;
	}
	
	/* 公告底部 */
	.announcement-footer {
		background-color: white;
		border-radius: 16px;
		padding: 16px 24px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		border: 1px solid #F0F0F0;
		display: flex;
		justify-content: center;
	}
	
	.announcement-status {
		font-size: 12px;
		padding: 4px 16px;
		border-radius: 12px;
		font-weight: 500;
	}
	
	.announcement-status.active {
		background-color: #F6FFED;
		color: #52C41A;
	}
	
	.announcement-status.inactive {
		background-color: #F5F5F5;
		color: #999999;
	}
	
	/* 加载状态 */
	.loading-state {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}
	
	.loading-text {
		font-size: 16px;
		color: #999999;
	}
	
	/* 错误状态 */
	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		padding: 0 20px;
		text-align: center;
	}
	
	.error-icon {
		font-size: 64px;
		margin-bottom: 16px;
	}
	
	.error-text {
		font-size: 16px;
		color: #999999;
		margin-bottom: 24px;
		font-weight: 500;
	}
	
	.retry-btn {
		background-color: #FF7A45;
		color: white;
		border: none;
		border-radius: 22px;
		padding: 12px 32px;
		font-size: 15px;
		font-weight: 600;
	}
</style>
