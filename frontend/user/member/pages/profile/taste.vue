<template>
	<view class="container">
		<!-- 背景装饰 -->
		<view class="background-decoration">
			<view class="decoration-circle big-circle"></view>
			<view class="decoration-circle medium-circle"></view>
			<view class="decoration-circle small-circle"></view>
		</view>
		
		<!-- 顶部导航 -->
		<view class="top-nav">
			<view class="nav-left" @click="goBack">
				<text class="nav-icon">←</text>
			</view>
			<text class="page-title">编辑口味偏好</text>
			<view class="nav-right"></view>
		</view>
		
		<!-- 老人信息 -->
		<view class="elder-info-card">
			<view class="elder-avatar"></view>
			<view class="elder-details">
				<text class="elder-name">{{ elderName }}</text>
				<text class="elder-age">{{ elderAge }}岁 · {{ elderGender }}</text>
			</view>
		</view>
		
		<!-- 口味偏好表单 -->
		<view class="form-section">
			<!-- 口味选择 -->
			<view class="form-group">
				<text class="form-label">口味偏好</text>
				<view class="taste-options">
					<view 
						v-for="taste in tasteOptions" 
						:key="taste.value"
						class="taste-option"
						:class="{ active: selectedTastes.includes(taste.value) }"
						@click="toggleTaste(taste.value)"
					>
						<text class="taste-text">{{ taste.label }}</text>
					</view>
				</view>
			</view>
			
			<!-- 饮食禁忌 -->
			<view class="form-group">
				<text class="form-label">饮食禁忌</text>
				<view class="allergy-options">
					<view 
						v-for="allergy in allergyOptions" 
						:key="allergy.value"
						class="allergy-option"
						:class="{ active: selectedAllergies.includes(allergy.value) }"
						@click="toggleAllergy(allergy.value)"
					>
						<text class="allergy-text">{{ allergy.label }}</text>
					</view>
				</view>
			</view>
			
			<!-- 特殊需求 -->
			<view class="form-group">
				<text class="form-label">特殊需求</text>
				<textarea 
					class="special-textarea" 
					v-model="specialNeeds"
					placeholder="请输入老人的特殊饮食需求..."
				></textarea>
			</view>
		</view>
		
		<!-- 保存按钮 -->
		<view class="save-section">
			<button class="save-btn" @click="saveTaste">
				<text class="save-text">保存偏好</text>
			</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
			return {
				elderId: '',
				elderName: '',
				elderAge: '',
				elderGender: '',
				selectedTastes: [],
				selectedAllergies: [],
				specialNeeds: '',
				tasteOptions: [
					{ label: '清淡', value: 'light' },
					{ label: '偏甜', value: 'sweet' },
					{ label: '偏咸', value: 'salty' },
					{ label: '偏辣', value: 'spicy' },
					{ label: '偏酸', value: 'sour' },
					{ label: '少油', value: 'low_oil' },
					{ label: '少盐', value: 'low_salt' },
					{ label: '软烂', value: 'soft' }
				],
				allergyOptions: [
					{ label: '海鲜过敏', value: 'seafood' },
					{ label: '坚果过敏', value: 'nuts' },
					{ label: '乳制品过敏', value: 'dairy' },
					{ label: '鸡蛋过敏', value: 'egg' },
					{ label: '小麦过敏', value: 'wheat' },
					{ label: '豆制品过敏', value: 'soy' }
				]
			};
		},
	onLoad(options) {
		this.elderId = options.elderId;
		this.loadElderInfo();
		this.loadTastePreferences();
	},
	methods: {
		goBack() {
			uni.navigateBack();
		},
		async loadElderInfo() {
			try {
				const token = uni.getStorageSync('token');
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/bindings/${this.elderId}`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${token}`
					}
				});
				
				if (response.statusCode === 200) {
					const elder = response.data;
					this.elderName = elder.elderly_name;
					this.elderAge = elder.elderly_age;
					this.elderGender = elder.elderly_gender;
				}
			} catch (error) {
				console.error('加载老人信息失败:', error);
			}
		},
		async loadTastePreferences() {
			try {
				const token = uni.getStorageSync('token');
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/elderly/${this.elderId}/preferences`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${token}`
					}
				});
				
				if (response.statusCode === 200) {
					const preferences = response.data;
					this.selectedTastes = preferences.tastes || [];
					this.selectedAllergies = preferences.allergies || [];
					this.specialNeeds = preferences.special_needs || '';
				}
			} catch (error) {
				console.error('加载口味偏好失败:', error);
			}
		},
		toggleTaste(taste) {
			const index = this.selectedTastes.indexOf(taste);
			if (index > -1) {
				this.selectedTastes.splice(index, 1);
			} else {
				this.selectedTastes.push(taste);
			}
		},
		toggleAllergy(allergy) {
			const index = this.selectedAllergies.indexOf(allergy);
			if (index > -1) {
				this.selectedAllergies.splice(index, 1);
			} else {
				this.selectedAllergies.push(allergy);
			}
		},
		async saveTaste() {
			try {
				const token = uni.getStorageSync('token');
				
				uni.showLoading({
					title: '保存中...'
				});
				
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/elderly/${this.elderId}/preferences`,
					method: 'POST',
					header: {
						'Authorization': `Bearer ${token}`,
						'Content-Type': 'application/json'
					},
					data: {
						tastes: this.selectedTastes,
						allergies: this.selectedAllergies,
						special_needs: this.specialNeeds
					}
				});
				
				if (response.statusCode === 200) {
					uni.hideLoading();
					uni.showToast({
						title: '保存成功',
						icon: 'success'
					});
					setTimeout(() => {
						uni.navigateBack();
					}, 1500);
				} else {
					throw new Error('保存失败');
				}
			} catch (error) {
				uni.hideLoading();
				uni.showToast({
					title: error.response?.data?.detail || '保存失败，请重试',
					icon: 'none'
				});
			}
		}
	}
};
</script>

<style scoped>
.container {
	min-height: 100vh;
	background: #f8fafc;
	position: relative;
	overflow-x: hidden;
}

/* 背景装饰 */
.background-decoration {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	z-index: -1;
}

.decoration-circle {
	position: absolute;
	border-radius: 50%;
	background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
}

.big-circle {
	width: 300px;
	height: 300px;
	top: -150px;
	left: -150px;
}

.medium-circle {
	width: 200px;
	height: 200px;
	bottom: -100px;
	right: -100px;
}

.small-circle {
	width: 100px;
	height: 100px;
	top: 50%;
	right: -50px;
	transform: translateY(-50%);
}

/* 顶部导航 */
.top-nav {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 20px;
	background: rgba(255, 255, 255, 0.95);
	backdrop-filter: blur(20px);
	box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
	position: sticky;
	top: 0;
	z-index: 100;
}

.nav-left, .nav-right {
	width: 40px;
	height: 40px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.nav-icon {
	font-size: 24px;
	color: #6366f1;
}

.page-title {
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
}

/* 老人信息卡片 */
.elder-info-card {
	display: flex;
	align-items: center;
	padding: 20px;
	margin: 20px;
	background: rgba(255, 255, 255, 0.9);
	border-radius: 16px;
	box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.elder-avatar {
	width: 60px;
	height: 60px;
	border-radius: 30px;
	background: linear-gradient(135deg, #6366f1, #8b5cf6);
	display: flex;
	align-items: center;
	justify-content: center;
	margin-right: 16px;
}

.elder-avatar::after {
	content: '👤';
	font-size: 32px;
}

.elder-details {
	flex: 1;
}

.elder-name {
	display: block;
	font-size: 18px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 4px;
}

.elder-age {
	display: block;
	font-size: 14px;
	color: #64748b;
}

/* 表单区域 */
.form-section {
	padding: 0 20px 20px;
}

.form-group {
	margin-bottom: 24px;
}

.form-label {
	display: block;
	font-size: 16px;
	font-weight: 600;
	color: #1e293b;
	margin-bottom: 12px;
}

/* 口味选项 */
.taste-options, .allergy-options {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
}

.taste-option, .allergy-option {
	padding: 10px 16px;
	background: #f1f5f9;
	border-radius: 20px;
	border: 2px solid transparent;
	transition: all 0.3s ease;
}

.taste-option.active, .allergy-option.active {
	background: rgba(99, 102, 241, 0.1);
	border-color: #6366f1;
}

.taste-text, .allergy-text {
	font-size: 14px;
	color: #475569;
}

/* 特殊需求文本框 */
.special-textarea {
	width: 100%;
	height: 120px;
	padding: 16px;
	background: #ffffff;
	border: 2px solid #e2e8f0;
	border-radius: 12px;
	font-size: 14px;
	color: #1e293b;
	resize: none;
}

.special-textarea:focus {
	border-color: #6366f1;
	outline: none;
}

/* 保存按钮 */
.save-section {
	padding: 0 20px 32px;
}

.save-btn {
	width: 100%;
	height: 56px;
	background: linear-gradient(135deg, #6366f1, #8b5cf6);
	border: none;
	border-radius: 28px;
	color: #ffffff;
	font-size: 18px;
	font-weight: 600;
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
	transition: all 0.3s ease;
}

.save-btn:active {
	transform: translateY(2px);
	box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}
</style>
