<template>
	<view class="info-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">个人信息</text>
			<text class="placeholder"></text>
		</view>
		
		<!-- 加载状态 -->
		<view v-if="loading" class="loading-container">
			<view class="loading-spinner"></view>
			<text class="loading-text">加载中...</text>
		</view>
		
		<!-- 用户基本信息 -->
		<view v-else class="info-section">
			<view class="info-card">
				<view class="info-item">
					<text class="info-label">姓名</text>
					<text class="info-value">{{ userInfo.name }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">年龄</text>
					<text class="info-value">{{ userInfo.age ? userInfo.age + '岁' : '未设置' }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">性别</text>
					<text class="info-value">{{ userInfo.gender === 'male' || userInfo.gender === '男' ? '男' : '女' }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">联系电话</text>
					<text class="info-value">{{ userInfo.phone }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">地址</text>
					<text class="info-value">{{ userInfo.address }}</text>
				</view>
			</view>
		</view>
		
		<!-- 健康信息 -->
		<view v-if="!loading" class="info-section">
			<text class="section-title">健康信息</text>
			<view class="info-card">
				<view class="info-item">
					<text class="info-label">健康状况</text>
					<text class="info-value">{{ userInfo.health_tag }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">饮食偏好</text>
					<view class="info-tags" v-if="parsedDietaryPreference.hasData">
						<text v-if="parsedDietaryPreference.tastes" class="tag tag-primary">口味: {{ parsedDietaryPreference.tastes }}</text>
						<text v-if="parsedDietaryPreference.allergies" class="tag tag-warning">忌口: {{ parsedDietaryPreference.allergies }}</text>
						<text v-if="parsedDietaryPreference.specialNeeds" class="tag tag-info">特殊: {{ parsedDietaryPreference.specialNeeds }}</text>
					</view>
					<text v-else class="info-value">{{ userInfo.dietary_preference }}</text>
				</view>
				<view class="info-item">
					<text class="info-label">过敏史</text>
					<text class="info-value">{{ userInfo.allergies }}</text>
				</view>
			</view>
		</view>
		
		<!-- 修改按钮 -->
		<view v-if="!loading" class="action-section">
			<button class="btn-edit" @click="editInfo">修改信息</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				userInfo: {
				name: '',
				age: '',
				gender: '',
				phone: '',
				address: '',
				health_tag: '',
				dietary_preference: '',
				allergies: '无'
			},
				loading: false
			}
		},
		computed: {
			parsedDietaryPreference() {
				const result = {
					hasData: false,
					tastes: '',
					allergies: '',
					specialNeeds: ''
				}
				
				const preference = this.userInfo.dietary_preference
				if (!preference || preference === '未设置') {
					return result
				}
				
				try {
					const data = JSON.parse(preference)
					
					// 口味偏好映射
					const tasteMap = {
						'light': '清淡',
						'sour': '酸辣',
						'sweet': '甜味',
						'salty': '咸味',
						'bitter': '苦味',
						'heavy': '厚重',
						'spicy': '微辣',
						'low_oil': '低脂',
						'low_sugar': '低糖',
						'low_salt': '低盐'
					}
					
					// 过敏信息映射
					const allergyMap = {
						'nuts': '花生',
						'seafood': '海鲜',
						'egg': '鸡蛋',
						'milk': '牛奶',
						'wheat': '小麦',
						'soy': '大豆'
					}
					
					// 处理口味偏好
					if (data.tastes && data.tastes.length > 0) {
						result.tastes = data.tastes.map(t => tasteMap[t] || t).join('、')
						result.hasData = true
					}
					
					// 处理过敏信息
					if (data.allergies && data.allergies.length > 0) {
						result.allergies = data.allergies.map(a => allergyMap[a] || a).join('、')
						result.hasData = true
					}
					
					// 处理特殊需求
					if (data.special_needs && data.special_needs.trim()) {
						result.specialNeeds = data.special_needs.trim()
						result.hasData = true
					}
				} catch (e) {
					// JSON解析失败，返回原始值
					console.error('解析饮食偏好失败:', e)
				}
				
				return result
			}
		},
		onLoad() {
			this.loadUserInfo()
		},
		onShow() {
			// 页面显示时重新加载用户信息，确保显示最新数据
			this.loadUserInfo()
		},
		methods: {
			async loadUserInfo() {
				this.loading = true
				try {
					const response = await api.auth.getProfile()
					const profile = response.profile || {}
					this.userInfo = {
						name: profile.name || '未设置',
						age: profile.age || '',
						gender: profile.gender || 'female',
						phone: profile.phone || '未设置',
						address: profile.address || '未设置',
						health_tag: profile.health_status || '未设置',
						dietary_preference: profile.dietary_preferences || '未设置',
						allergies: '无'
					}
				} catch (error) {
					console.error('获取用户信息失败:', error)
					uni.showToast({
						title: '获取用户信息失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			goBack() {
				uni.navigateBack()
			},
			editInfo() {
				uni.navigateTo({
					url: '/pages/profile/edit'
				})
			}
		}
	}
</script>

<style scoped>
	.info-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 220px, #F5F5F5 100%);
		padding-bottom: 40px;
	}
	
	/* 顶部导航栏 */
	.top-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 58px;
		padding: 0 20px;
		background: rgba(255, 255, 255, 0.92);
		border-bottom: 1px solid rgba(255, 122, 69, 0.08);
		backdrop-filter: blur(8px);
	}
	
	.back-btn {
		font-size: 24px;
		color: #333333;
		width: 36px;
		text-align: center;
	}
	
	.nav-title {
		font-size: 19px;
		font-weight: 600;
		color: #333333;
		flex: 1;
		text-align: center;
	}
	
	.placeholder {
		width: 36px;
	}
	
	/* 加载状态 */
	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 400px;
	}
	
	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid #FF7A45;
		border-top-color: transparent;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 16px;
	}
	
	@keyframes spin {
		to { transform: rotate(360deg); }
	}
	
	.loading-text {
		font-size: 16px;
		color: #999999;
	}
	
	/* 信息区域 */
	.info-section {
		padding: 20px;
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 16px;
	}
	
	.info-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.info-item {
		display: flex;
		align-items: center;
		padding: 12px 0;
		border-bottom: 1px solid #F5F5F5;
	}
	
	.info-item:last-child {
		border-bottom: none;
	}
	
	.info-label {
		width: 80px;
		font-size: 14px;
		color: #666666;
	}
	
	.info-value {
		flex: 1;
		font-size: 14px;
		color: #333333;
		font-weight: 500;
	}
	
	.info-tags {
		flex: 1;
		display: flex;
		gap: 8px;
	}
	
	.tag {
		padding: 4px 12px;
		border-radius: 12px;
		font-size: 12px;
		font-weight: 500;
	}
	
	.tag-warning {
		background-color: rgba(245, 108, 108, 0.1);
		color: #F56C6C;
	}
	
	.tag-primary {
		background-color: rgba(255, 122, 69, 0.1);
		color: #FF7A45;
	}
	
	.tag-info {
		background-color: rgba(64, 158, 255, 0.1);
		color: #409EFF;
	}
	
	/* 操作区域 */
	.action-section {
		padding: 20px;
	}
	
	.btn-edit {
		width: 100%;
		height: 44px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border: none;
		border-radius: 22px;
		font-size: 15px;
		font-weight: 600;
		box-shadow: 0 6px 14px rgba(255, 122, 69, 0.24);
	}
</style>
