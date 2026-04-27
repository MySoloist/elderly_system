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
			<text class="page-title">编辑健康状况</text>
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
		
		<!-- 健康信息表单 -->
		<view class="form-section">
			<!-- 血压 -->
			<view class="form-group">
				<text class="form-label">血压 (mmHg)</text>
				<view class="blood-pressure-input">
					<input class="bp-input" type="number" v-model="bloodPressure.systolic" placeholder="收缩压" />
					<text class="bp-separator">/</text>
					<input class="bp-input" type="number" v-model="bloodPressure.diastolic" placeholder="舒张压" />
				</view>
			</view>
			
			<!-- 血糖 -->
			<view class="form-group">
				<text class="form-label">血糖 (mmol/L)</text>
				<input class="form-input" type="number" v-model="bloodSugar" placeholder="请输入血糖值" step="0.1" />
			</view>
			
			<!-- 体温 -->
			<view class="form-group">
				<text class="form-label">体温 (°C)</text>
				<input class="form-input" type="number" v-model="temperature" placeholder="请输入体温" step="0.1" />
			</view>
			
			<!-- 心率 -->
			<view class="form-group">
				<text class="form-label">心率 (次/分钟)</text>
				<input class="form-input" type="number" v-model="heartRate" placeholder="请输入心率" />
			</view>
			
			<!-- 体重 -->
			<view class="form-group">
				<text class="form-label">体重 (kg)</text>
				<input class="form-input" type="number" v-model="weight" placeholder="请输入体重" step="0.1" />
			</view>
			
			<!-- 健康标签 -->
			<view class="form-group">
				<text class="form-label">健康标签</text>
				<view class="health-tags">
					<view 
						v-for="tag in healthTagOptions" 
						:key="tag.id"
						class="health-tag"
						:class="{ active: selectedHealthTags.includes(tag.id) }"
						:style="{ 
							backgroundColor: tag.color ? tag.color + '20' : '#f1f5f9', 
							borderColor: tag.color || '#e2e8f0' 
						}"
						@click="toggleHealthTag(tag.id)"
					>
						<text 
							class="tag-text"
							:style="{ color: tag.color || '#475569' }"
						>{{ tag.name }}</text>
					</view>
				</view>
			</view>
			
			<!-- 健康备注 -->
			<view class="form-group">
				<text class="form-label">健康备注</text>
				<textarea 
					class="health-textarea" 
					v-model="healthNotes"
					placeholder="请输入老人的健康状况备注..."
				></textarea>
			</view>
		</view>
		
		<!-- 保存按钮 -->
		<view class="save-section">
			<button class="save-btn" @click="saveHealth">
				<text class="save-text">保存健康信息</text>
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
				bloodPressure: {
					systolic: '',
					diastolic: ''
				},
				bloodSugar: '',
				temperature: '',
				heartRate: '',
				weight: '',
				selectedHealthTags: [],
				healthNotes: '',
				healthTagOptions: []
			};
		},
	onLoad(options) {
		this.elderId = options.elderId;
		this.loadElderInfo();
		this.loadHealthInfo();
		this.loadHealthTags();
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
		async loadHealthInfo() {
			try {
				const token = uni.getStorageSync('token');
				const response = await uni.request({
					url: `http://127.0.0.1:7678/api/v1/member/health/${this.elderId}`,
					method: 'GET',
					header: {
						'Authorization': `Bearer ${token}`
					}
				});
				
				if (response.statusCode === 200) {
					const healthData = response.data;
					if (healthData.health_records && healthData.health_records.length > 0) {
						const latestRecord = healthData.health_records[0];
						this.bloodPressure.systolic = latestRecord.blood_pressure?.split('/')[0] || '';
						this.bloodPressure.diastolic = latestRecord.blood_pressure?.split('/')[1] || '';
						this.bloodSugar = latestRecord.blood_sugar || '';
						this.temperature = latestRecord.temperature || '';
						this.heartRate = latestRecord.heart_rate || '';
						this.weight = latestRecord.weight || '';
						this.healthNotes = latestRecord.notes || '';
					}
					this.selectedHealthTags = healthData.health_tags || [];
				}
			} catch (error) {
				console.error('加载健康信息失败:', error);
			}
		},
		async loadHealthTags() {
			try {
				const token = uni.getStorageSync('token');
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/admin/health-tags',
					method: 'GET',
					header: {
						'Authorization': `Bearer ${token}`
					}
				});
				
				if (response.statusCode === 200) {
					this.healthTagOptions = response.data;
				}
			} catch (error) {
				console.error('加载健康标签失败:', error);
			}
		},
		toggleHealthTag(tag) {
			const index = this.selectedHealthTags.indexOf(tag);
			if (index > -1) {
				this.selectedHealthTags.splice(index, 1);
			} else {
				this.selectedHealthTags.push(tag);
			}
		},
		async saveHealth() {
			try {
				const token = uni.getStorageSync('token');
				
				uni.showLoading({
					title: '保存中...'
				});
				
				const healthRecordData = {
					elderly_id: this.elderId,
					blood_pressure: this.bloodPressure.systolic && this.bloodPressure.diastolic 
						? `${this.bloodPressure.systolic}/${this.bloodPressure.diastolic}` 
						: null,
					blood_sugar: this.bloodSugar ? parseFloat(this.bloodSugar) : null,
					temperature: this.temperature ? parseFloat(this.temperature) : null,
					heart_rate: this.heartRate ? parseInt(this.heartRate) : null,
					weight: this.weight ? parseFloat(this.weight) : null,
					notes: this.healthNotes,
					tags: this.selectedHealthTags
				};
				
				const response = await uni.request({
					url: 'http://127.0.0.1:7678/api/v1/member/health',
					method: 'POST',
					header: {
						'Authorization': `Bearer ${token}`,
						'Content-Type': 'application/json'
					},
					data: healthRecordData
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

/* 血压输入 */
.blood-pressure-input {
	display: flex;
	align-items: center;
	gap: 12px;
}

.bp-input {
	flex: 1;
	height: 48px;
	padding: 0 16px;
	background: #ffffff;
	border: 2px solid #e2e8f0;
	border-radius: 12px;
	font-size: 16px;
	color: #1e293b;
}

.bp-input:focus {
	border-color: #6366f1;
	outline: none;
}

.bp-separator {
	font-size: 24px;
	color: #64748b;
	font-weight: 600;
}

/* 普通输入框 */
.form-input {
	width: 100%;
	height: 48px;
	padding: 0 16px;
	background: #ffffff;
	border: 2px solid #e2e8f0;
	border-radius: 12px;
	font-size: 16px;
	color: #1e293b;
}

.form-input:focus {
	border-color: #6366f1;
	outline: none;
}

/* 健康标签 */
.health-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
}

.health-tag {
	padding: 10px 16px;
	background: #f1f5f9;
	border-radius: 20px;
	border: 2px solid transparent;
	transition: all 0.3s ease;
}

.health-tag.active {
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tag-text {
	font-size: 14px;
	color: #475569;
}

/* 健康备注文本框 */
.health-textarea {
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

.health-textarea:focus {
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
