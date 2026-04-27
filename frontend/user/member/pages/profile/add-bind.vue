<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">添加绑定</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input-wrapper">
				<text class="search-icon">🔍</text>
				<input 
					v-model="searchQuery" 
					type="text" 
					placeholder="搜索老人姓名或手机号" 
					class="search-input"
					:disabled="loading"
				/>
				<text v-if="searchQuery" class="clear-icon" @click="clearSearch">✕</text>
			</view>
		</view>
		
		<!-- 老人列表 -->
		<view class="elderly-list">
			<view 
				v-for="elderly in filteredElderlyList" 
				:key="elderly.id" 
				class="elderly-item"
				@click="selectElderly(elderly)"
			>
				<view class="elderly-icon"></view>
				<view class="elderly-info">
					<text class="elderly-name">{{ elderly.name }}</text>
					<text class="elderly-details">{{ elderly.age }}岁 · {{ elderly.gender }}</text>
				</view>
				<view class="select-btn" :class="{ selected: selectedElderlyId === elderly.id }">
					<text class="select-icon">{{ selectedElderlyId === elderly.id ? '✓' : '' }}</text>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view class="empty-state" v-if="filteredElderlyList.length === 0 && !loading">
			<view class="empty-icon"></view>
			<text class="empty-title">暂无老人数据</text>
			<text class="empty-subtitle">请联系管理员添加老人信息</text>
		</view>
		
		<!-- 加载状态 -->
		<view class="loading-state" v-if="loading">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 关系类型选择 -->
		<view class="relation-section" v-if="true">
			<text class="section-title">选择关系类型</text>
			<view class="relation-options">
				<view 
					v-for="option in relationOptions" 
					:key="option.value"
					class="relation-option"
					:class="{ active: selectedRelation === option.value }"
					@click="selectRelation(option.value)"
				>
					<text class="relation-text">{{ option.label }}</text>
				</view>
			</view>
		</view>
		
		<!-- 绑定按钮 -->
		<button 
			class="bind-btn" 
			@click="confirmBind"
			:disabled="!selectedElderlyId || !selectedRelation || loading"
		>
			<text>绑定</text>
		</button>
	</view>
</template>

<script>
export default {
	data() {
		return {
			elderlyList: [],
			filteredElderlyList: [],
			searchQuery: '',
			selectedElderlyId: null,
			selectedRelation: '',
			relationOptions: [
				{ label: '父母', value: 'parent' },
				{ label: '子女', value: 'child' },
				{ label: '配偶', value: 'spouse' },
				{ label: '兄弟姐妹', value: 'sibling' },
				{ label: '其他', value: 'other' }
			],
			loading: false
		};
	},
	onLoad() {
		this.loadElderlyList();
	},
	watch: {
		searchQuery() {
			this.filterElderlyList();
		}
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		async loadElderlyList() {
			try {
				this.loading = true;
				// 调用获取老人列表的API
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/elderly-list',
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					this.elderlyList = response.data;
					this.filterElderlyList();
				} else {
					throw new Error(response.data?.detail || '加载老人列表失败');
				}
			} catch (error) {
				console.error('加载老人列表失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		filterElderlyList() {
			if (!this.searchQuery) {
				this.filteredElderlyList = this.elderlyList;
			} else {
				this.filteredElderlyList = this.elderlyList.filter(elderly => 
					elderly.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
					(elderly.phone && elderly.phone.toLowerCase().includes(this.searchQuery.toLowerCase()))
				);
			}
		},
		clearSearch() {
			this.searchQuery = '';
			this.filterElderlyList();
		},
		selectElderly(elderly) {
			console.log('选择了老人:', elderly);
			this.selectedElderlyId = elderly.id;
			this.selectedRelation = ''; // 重置关系选择
			console.log('selectedElderlyId:', this.selectedElderlyId);
			uni.showToast({
				title: '已选择老人',
				icon: 'success'
			});
		},
		selectRelation(relation) {
			console.log('选择了关系类型:', relation);
			this.selectedRelation = relation;
			console.log('selectedRelation:', this.selectedRelation);
			uni.showToast({
				title: '已选择关系类型',
				icon: 'success'
			});
		},
		async confirmBind() {
			console.log('绑定按钮被点击了！');
			console.log('selectedElderlyId:', this.selectedElderlyId);
			console.log('selectedRelation:', this.selectedRelation);
			console.log('loading:', this.loading);
			
			uni.showToast({
				title: '点击成功！',
				icon: 'success'
			});
			
			uni.showModal({
				title: '确认绑定',
				content: `确定要绑定这位老人吗？`,
				success: async (res) => {
					console.log('用户点击了确认:', res.confirm);
					if (res.confirm) {
						try {
							this.loading = true;
							console.log('开始调用绑定API...');
							// 调用添加绑定的API
							const response = await uni.request({
								url: 'http://127.0.0.1:7678/api/v1/member/bindings',
								method: 'POST',
								header: {
									'Authorization': `Bearer ${uni.getStorageSync('token')}`,
									'Content-Type': 'application/json'
								},
								data: {
									elderly_id: this.selectedElderlyId,
									relation: this.selectedRelation
								}
							});
							
							console.log('API响应:', response);
							if (response.statusCode === 200) {
								uni.showToast({
									title: '绑定成功',
									icon: 'success'
								});
								setTimeout(() => {
									uni.navigateBack();
								}, 1500);
							} else {
								throw new Error(response.data?.detail || '绑定失败');
							}
						} catch (error) {
							console.error('绑定失败:', error);
							uni.showToast({
								title: error.message || '绑定失败，请稍后重试',
								icon: 'none'
							});
						} finally {
							this.loading = false;
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

/* 搜索栏 */
.search-bar {
	padding: 16px 20px;
	background: #ffffff;
	margin-bottom: 8px;
}

.search-input-wrapper {
	position: relative;
	display: flex;
	align-items: center;
}

.search-icon {
	position: absolute;
	left: 16px;
	font-size: 16px;
	color: #94a3b8;
	z-index: 1;
}

.search-input {
	width: 100%;
	height: 44px;
	padding: 0 40px 0 44px;
	border: 1px solid #e2e8f0;
	border-radius: 12px;
	font-size: 15px;
	color: #1e293b;
	background: #f8fafc;
	transition: all 0.3s ease;
}

.search-input:focus {
	border-color: #6366f1;
	background: #ffffff;
	box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.clear-icon {
	position: absolute;
	right: 12px;
	font-size: 16px;
	color: #94a3b8;
	padding: 4px;
}

/* 老人列表 */
.elderly-list {
	padding: 12px 20px;
}

.elderly-item {
	display: flex;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 16px;
	margin-bottom: 12px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.5);
	transition: all 0.2s ease;
}

.elderly-item:active {
	transform: scale(0.98);
	background: #f8fafc;
}

.elderly-icon {
	width: 48px;
	height: 48px;
	border-radius: 12px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-right: 16px;
	display: flex;
	align-items: center;
	justify-content: center;
}
.elderly-icon::after {
	content: '👤';
	font-size: 24px;
}

.elderly-info {
	flex: 1;
}

.elderly-name {
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
	display: block;
	margin-bottom: 4px;
}

.elderly-details {
	font-size: 13px;
	color: #64748b;
	display: block;
}

.select-btn {
	width: 22px;
	height: 22px;
	border: 2px solid #cbd5e1;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.2s ease;
}

.select-btn.selected {
	background: #6366f1;
	border-color: #6366f1;
}

.select-icon {
	font-size: 12px;
	color: white;
	font-weight: bold;
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

/* 加载状态 */
.loading-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 60px 24px;
}

.loading-spinner {
	width: 40px;
	height: 40px;
	border: 3px solid rgba(99, 102, 241, 0.3);
	border-top: 3px solid #6366f1;
	border-radius: 50%;
	animation: spin 1s linear infinite;
	margin-bottom: 16px;
}

.loading-text {
	font-size: 16px;
	color: #64748b;
}

@keyframes spin {
	0% { transform: rotate(0deg); }
	100% { transform: rotate(360deg); }
}

/* 绑定按钮 */
.bind-btn {
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
	box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
	transition: all 0.3s ease;
	z-index: 9999;
	pointer-events: auto;
	opacity: 1;
	cursor: pointer;
}

.bind-btn:active {
	transform: translateY(2px);
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.bind-btn:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

/* 关系类型选择 */
.relation-section {
	background: #ffffff;
	border-radius: 16px;
	padding: 20px;
	margin: 0 20px 24px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.5);
}

.section-title {
	font-size: 15px;
	font-weight: 600;
	color: #1e293b;
	display: block;
	margin-bottom: 16px;
}

.relation-options {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
}

.relation-option {
	padding: 10px 20px;
	border: 1px solid #e2e8f0;
	border-radius: 10px;
	font-size: 14px;
	color: #64748b;
	background: #f8fafc;
	transition: all 0.2s ease;
}

.relation-option:active {
	transform: scale(0.95);
}

.relation-option.active {
	background: #6366f1;
	border-color: #6366f1;
	color: #ffffff;
	font-weight: 500;
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.relation-text {
	display: block;
}
</style>
