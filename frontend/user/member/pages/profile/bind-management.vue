<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">老人绑定管理</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 绑定列表 -->
		<view class="bind-list">
			<view class="bind-item" v-for="(bind, index) in bindList" :key="index">
				<view class="bind-icon"></view>
				<view class="bind-info">
					<text class="bind-name">{{ bind.name }}</text>
					<text class="bind-phone">{{ bind.phone }}</text>
				</view>
				<view class="bind-actions">
					<button class="action-btn" @click="editBind(bind.id)">
						<text class="btn-icon">✏️</text>
					</button>
					<button class="action-btn delete" @click="unbind(bind.id)">
						<text class="btn-icon">🗑️</text>
					</button>
				</view>
			</view>
		</view>
		
		<!-- 添加绑定按钮 -->
		<button class="add-btn" @click="addBind">
			<text class="add-icon">+</text>
			<text class="add-text">添加绑定</text>
		</button>
		
		<!-- 空状态 -->
		<view class="empty-state" v-if="bindList.length === 0">
			<view class="empty-icon"></view>
			<text class="empty-title">暂无绑定</text>
			<text class="empty-subtitle">点击下方按钮添加绑定</text>
		</view>
	</view>
</template>

<script>
import { bindService } from '../../api/bind.js';

export default {
	data() {
		return {
			bindList: [],
			loading: false
		};
	},
	onLoad() {
		this.loadBindList();
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		async loadBindList() {
			try {
				this.loading = true;
				const data = await bindService.getBindList();
				this.bindList = data;
			} catch (error) {
				console.error('加载绑定列表失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		addBind() {
			uni.navigateTo({
				url: '/pages/profile/add-bind'
			});
		},
		editBind(bindId) {
			uni.navigateTo({
				url: `/pages/profile/edit-bind?id=${bindId}`
			});
		},
		async unbind(bindId) {
			uni.showModal({
				title: '解除绑定',
				content: '确定要解除这个绑定吗？',
				success: async (res) => {
					if (res.confirm) {
						try {
							await bindService.deleteBind(bindId);
							uni.showToast({
								title: '绑定已解除',
								icon: 'success'
							});
							// 重新加载绑定列表
							this.loadBindList();
						} catch (error) {
							console.error('解除绑定失败:', error);
							uni.showToast({
								title: '解除绑定失败，请稍后重试',
								icon: 'none'
							});
						}
					}
				}
			});
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background: #f8fafc;
	padding-bottom: 100px;
}

/* 顶部导航 */
.top-nav {
	display: flex;
	align-items: center;
	padding: 44px 20px 12px;
	background: #ffffff;
	position: sticky;
	top: 0;
	z-index: 100;
	box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
}

.back-btn {
	width: 36px;
	height: 36px;
	border-radius: 10px;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 12px;
	transition: all 0.2s ease;
}
.back-btn:active {
	transform: scale(0.9);
	background: #e2e8f0;
}

.back-icon {
	font-size: 20px;
	color: #1e293b;
	font-weight: 600;
}

.page-title {
	flex: 1;
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	text-align: center;
}

.nav-right {
	width: 36px;
}

/* 绑定列表 */
.bind-list {
	padding: 20px;
}

.bind-item {
	display: flex;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 16px;
	margin-bottom: 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.5);
	transition: all 0.3s ease;
}
.bind-item:active {
	transform: translateY(2px);
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.bind-icon {
	width: 52px;
	height: 52px;
	border-radius: 14px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-right: 16px;
	display: flex;
	align-items: center;
	justify-content: center;
}
.bind-icon::after {
	content: '👤';
	font-size: 24px;
}

.bind-info {
	flex: 1;
}

.bind-name {
	font-size: 17px;
	font-weight: 600;
	color: #1e293b;
	display: block;
	margin-bottom: 4px;
}

.bind-phone {
	font-size: 14px;
	color: #64748b;
	display: block;
}

.bind-actions {
	display: flex;
	gap: 10px;
}

.action-btn {
	width: 38px;
	height: 38px;
	background: #f8fafc;
	border: 1px solid #e2e8f0;
	border-radius: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.2s ease;
	padding: 0;
}
.action-btn:active {
	transform: scale(0.9);
}

.action-btn.delete {
	background: rgba(239, 68, 68, 0.05);
	border-color: rgba(239, 68, 68, 0.1);
}

.btn-icon {
	font-size: 18px;
}

/* 添加按钮 */
.add-btn {
	position: fixed;
	bottom: 30px;
	left: 20px;
	right: 20px;
	height: 52px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	border: none;
	border-radius: 16px;
	color: #ffffff;
	font-size: 16px;
	font-weight: 600;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
	box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
	transition: all 0.3s ease;
}
.add-btn:active {
	transform: translateY(2px);
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.add-icon {
	font-size: 20px;
}

.add-text {
	
}

/* 空状态 */
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 24px;
	text-align: center;
}

.empty-icon {
	width: 80px;
	height: 80px;
	border-radius: 50%;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-bottom: 24px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.empty-icon::before {
	content: '';
	width: 40px;
	height: 40px;
	background: rgba(255, 255, 255, 0.3);
	border-radius: 50%;
}

.empty-title {
	font-size: 24px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 12px;
	display: block;
}

.empty-subtitle {
	font-size: 16px;
	color: #64748b;
	display: block;
}
</style>
