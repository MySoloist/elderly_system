<template>
	<view class="container">
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="back-btn" @click="goBack">
				<text class="back-icon">‹</text>
			</view>
			<text class="page-title">编辑绑定</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 老人信息 -->
		<view class="elderly-info-card">
			<view class="elderly-icon"></view>
			<view class="elderly-details">
				<text class="elderly-name">{{ bindData?.elderly_name || '' }}</text>
				<text class="elderly-age">{{ bindData?.elderly_age || '' }}岁 · {{ bindData?.elderly_gender || '' }}</text>
			</view>
		</view>
		
		<!-- 表单 -->
		<view class="form-container">
			<view class="form-group">
				<text class="form-label">关系类型</text>
				<view class="relation-options">
					<view 
						v-for="relation in relationOptions" 
						:key="relation.value"
						class="relation-option"
						:class="{ active: bindData?.relation === relation.value }"
						@click="selectRelation(relation.value)"
					>
						<text class="relation-text">{{ relation.label }}</text>
					</view>
				</view>
			</view>
			
			<view class="form-group">
				<text class="form-label">备注</text>
				<textarea 
					v-model="bindData.remark" 
					class="textarea" 
					placeholder="添加备注信息（可选）"
					:disabled="loading"
				></textarea>
			</view>
		</view>
		
		<!-- 保存按钮 -->
		<button 
			class="save-btn" 
			@click="saveBind"
			:disabled="!bindData.relation || loading"
		>
			<text>保存</text>
		</button>
		
		<!-- 加载状态 -->
		<view class="loading-overlay" v-if="loading">
			<view class="loading-spinner"></view>
			<text class="loading-text">保存中...</text>
		</view>
	</view>
</template>

<script>
import { bindService } from '../../api/bind.js';

export default {
	data() {
		return {
			bindId: null,
			bindData: {
				relation: '',
				remark: ''
			},
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
	onLoad(options) {
		this.bindId = options.id;
		this.loadBindDetails();
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		async loadBindDetails() {
			try {
				this.loading = true;
				// 调用获取绑定详情的API
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/bindings/${this.bindId}`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${uni.getStorageSync('token')}`
					}
				});
				
				if (response.statusCode === 200) {
					this.bindData = response.data;
				} else {
					throw new Error(response.data?.detail || '加载绑定详情失败');
				}
			} catch (error) {
				console.error('加载绑定详情失败:', error);
				uni.showToast({
					title: '加载失败，请稍后重试',
					icon: 'none'
				});
			} finally {
				this.loading = false;
			}
		},
		selectRelation(relation) {
			this.bindData.relation = relation;
		},
		async saveBind() {
			uni.showModal({
				title: '保存修改',
				content: '确定要保存修改吗？',
				success: async (res) => {
					if (res.confirm) {
						try {
							this.loading = true;
							await bindService.updateBind(this.bindId, {
								relation: this.bindData.relation,
								remark: this.bindData.remark
							});
							uni.showToast({
								title: '保存成功',
								icon: 'success'
							});
							setTimeout(() => {
								uni.navigateBack();
							}, 1500);
						} catch (error) {
							console.error('保存失败:', error);
							uni.showToast({
								title: error.message || '保存失败，请稍后重试',
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

/* 老人信息卡片 */
.elderly-info-card {
	display: flex;
	align-items: center;
	background: #ffffff;
	border-radius: 16px;
	padding: 20px;
	margin: 20px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.5);
}

.elderly-icon {
	width: 56px;
	height: 56px;
	border-radius: 14px;
	background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
	margin-right: 16px;
	display: flex;
	align-items: center;
	justify-content: center;
}
.elderly-icon::after {
	content: '👤';
	font-size: 28px;
}

.elderly-details {
	flex: 1;
}

.elderly-name {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	display: block;
	margin-bottom: 4px;
}

.elderly-age {
	font-size: 14px;
	color: #64748b;
	display: block;
}

/* 表单容器 */
.form-container {
	padding: 0 20px;
}

.form-group {
	margin-bottom: 24px;
	background: #ffffff;
	border-radius: 16px;
	padding: 20px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
	border: 1px solid rgba(226, 232, 240, 0.5);
}

.form-label {
	font-size: 15px;
	font-weight: 600;
	color: #1e293b;
	display: block;
	margin-bottom: 16px;
}

/* 关系选项 */
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

/* 文本区域 */
.textarea {
	width: 100%;
	height: 100px;
	padding: 16px;
	border: 1px solid #e2e8f0;
	border-radius: 12px;
	font-size: 15px;
	color: #1e293b;
	background: #f8fafc;
	outline: none;
	resize: none;
	transition: all 0.3s ease;
	box-sizing: border-box;
}

.textarea:focus {
	border-color: #6366f1;
	background: #ffffff;
	box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* 保存按钮 */
.save-btn {
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
}

.save-btn:active {
	transform: translateY(2px);
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.save-btn:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

/* 加载遮罩 */
.loading-overlay {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	z-index: 9999;
}

.loading-spinner {
	width: 40px;
	height: 40px;
	border: 3px solid rgba(255, 255, 255, 0.3);
	border-top: 3px solid #ffffff;
	border-radius: 50%;
	animation: spin 1s linear infinite;
	margin-bottom: 16px;
}

.loading-text {
	font-size: 16px;
	color: #ffffff;
}

@keyframes spin {
	0% { transform: rotate(0deg); }
	100% { transform: rotate(360deg); }
}
</style>
