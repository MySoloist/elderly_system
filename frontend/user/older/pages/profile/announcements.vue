<template>
	<view class="announcements-container">
		<!-- 页面标题 -->
		<view class="page-header">
			<text class="back-btn" @click="goBack">←</text>
			<text class="page-title">我的公告</text>
			<view class="placeholder"></view>
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
		
		<!-- 公告列表 -->
		<view class="announcements-list">
			<view 
				v-for="announcement in filteredAnnouncements" 
				:key="announcement.id"
				class="announcement-item"
				:class="{ unread: !announcement.read }"
				@click="viewAnnouncement(announcement)"
			>
				<view class="announcement-header">
					<text class="announcement-title">{{ announcement.title }}</text>
					<view class="announcement-meta">
						<text class="announcement-type" :class="announcement.type">{{ getTypeName(announcement.type) }}</text>
						<text class="announcement-time">{{ formatTime(announcement.created_at) }}</text>
					</view>
				</view>
				<text class="announcement-content">{{ announcement.content }}</text>
				<view class="announcement-footer">
					<view class="announcement-dot" v-if="!announcement.read"></view>
					<text class="announcement-arrow">→</text>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-if="announcements.length === 0 && !loading" class="empty-state">
				<text class="empty-icon">📢</text>
				<text class="empty-text">暂无公告</text>
				<text class="empty-desc">管理员还没有发布公告</text>
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
				announcements: [],
				loading: false,
				page: 1,
				limit: 20,
				total: 0,
				categories: [
					{ label: '全部', value: 'all' },
					{ label: '系统公告', value: 'system' },
					{ label: '通知', value: 'notice' },
					{ label: '紧急通知', value: 'emergency' }
				],
				activeCategory: 'all'
			}
		},
		computed: {
			filteredAnnouncements() {
				if (this.activeCategory === 'all') {
					return this.announcements
				}
				return this.announcements.filter(announcement => announcement.type === this.activeCategory)
			},
			// 获取每个分类的未读数量
			categoryUnreadCounts() {
				const counts = {}
				counts.all = this.announcements.filter(a => !a.read).length
				counts.system = this.announcements.filter(a => a.type === 'system' && !a.read).length
				counts.notice = this.announcements.filter(a => a.type === 'notice' && !a.read).length
				counts.emergency = this.announcements.filter(a => a.type === 'emergency' && !a.read).length
				return counts
			}
		},
		onLoad() {
			this.loadAnnouncements()
		},
		onReachBottom() {
			if (!this.loading && this.announcements.length < this.total) {
				this.page++
				this.loadAnnouncements(true)
			}
		},
		methods: {
			// 获取已读公告ID列表
			getReadAnnouncementIds() {
				try {
					const readIds = uni.getStorageSync('olderReadAnnouncementIds')
					return readIds ? JSON.parse(readIds) : []
				} catch (error) {
					console.error('获取已读公告ID失败:', error)
					return []
				}
			},
			
			// 保存已读公告ID列表
			saveReadAnnouncementIds(readIds) {
				try {
					uni.setStorageSync('olderReadAnnouncementIds', JSON.stringify(readIds))
				} catch (error) {
					console.error('保存已读公告ID失败:', error)
				}
			},
			
			async loadAnnouncements(isLoadMore = false) {
				if (!isLoadMore) {
					this.page = 1
					this.announcements = []
				}
				
				this.loading = true
				try {
					const response = await api.older.getAnnouncements({
						page: this.page,
						limit: this.limit
					})
					
					// 获取已读公告ID列表
					const readIds = this.getReadAnnouncementIds()
					
					let newAnnouncements = response.items.map(announcement => ({
						...announcement,
						read: readIds.includes(announcement.id)
					}))
					
					if (isLoadMore) {
						this.announcements = [...this.announcements, ...newAnnouncements]
					} else {
						this.announcements = newAnnouncements
					}
					this.total = response.total
				} catch (error) {
					console.error('获取公告列表失败:', error)
					uni.showToast({
						title: '获取公告列表失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			viewAnnouncement(announcement) {
				// 标记为已读
				if (!announcement.read) {
					const readIds = this.getReadAnnouncementIds()
					if (!readIds.includes(announcement.id)) {
						readIds.push(announcement.id)
						this.saveReadAnnouncementIds(readIds)
						// 更新本地状态
						announcement.read = true
					}
				}
				
				uni.navigateTo({
					url: `/pages/profile/announcement-detail?id=${announcement.id}`
				})
			},
			getTypeName(type) {
				const typeMap = {
					'system': '系统公告',
					'notice': '通知',
					'emergency': '紧急通知'
				}
				return typeMap[type] || type
			},
			formatTime(time) {
				const date = new Date(time)
				const now = new Date()
				const diff = now - date
				const days = Math.floor(diff / (1000 * 60 * 60 * 24))
				
				if (days === 0) {
					return '今天'
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
				this.page = 1
				this.loadAnnouncements()
			},
			goBack() {
				uni.navigateBack()
			}
		}
	}
</script>

<style scoped>
	.announcements-container {
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
	
	/* 公告列表 */
	.announcements-list {
		padding: 120px 20px 20px;
	}
	
	.announcement-item {
		background-color: white;
		border-radius: 16px;
		padding: 20px;
		margin-bottom: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		border: 1px solid #F0F0F0;
	}
	
	.announcement-item.unread {
		background-color: rgba(255, 122, 69, 0.05);
		border-color: rgba(255, 122, 69, 0.3);
	}
	
	.announcement-header {
		margin-bottom: 12px;
	}
	
	.announcement-title {
		font-size: 17px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 8px;
	}
	
	.announcement-meta {
		display: flex;
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
	
	.announcement-time {
		font-size: 12px;
		color: #999999;
	}
	
	.announcement-content {
		font-size: 14px;
		color: #666666;
		line-height: 1.5;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
		margin-bottom: 12px;
	}
	
	.announcement-footer {
		display: flex;
		align-items: center;
		justify-content: flex-end;
		gap: 8px;
	}
	
	.announcement-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background-color: #FF4D4F;
		box-shadow: 0 2px 8px rgba(255, 77, 79, 0.4);
	}
	
	.announcement-arrow {
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
