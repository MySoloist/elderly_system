<template>
	<view class="health-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">健康档案</text>
			<text class="placeholder"></text>
		</view>
		
		<!-- 健康状况概览 -->
		<view class="health-overview">
			<view class="overview-card">
				<text class="overview-title">健康状况概览</text>
				<view class="health-status">
					<text class="status-label">当前状态:</text>
					<text class="status-value status-normal">正常</text>
				</view>
				<view class="health-tags">
					<text class="tag tag-warning">高血压</text>
					<text class="tag tag-primary">清淡饮食</text>
				</view>
			</view>
		</view>
		
		<!-- 日期选择器 -->
		<view class="date-selector">
			<text class="date-text">{{ selectedDate }}</text>
			<view class="date-nav">
				<text class="nav-btn" @click="prevDate">‹</text>
				<text class="nav-btn" @click="nextDate">›</text>
			</view>
		</view>
		
		<!-- 饮食记录列表 -->
		<view class="diet-records">
			<view class="record-card" v-for="(record, index) in dietRecords" :key="index">
				<view class="record-header">
					<text class="record-time">{{ record.time }}</text>
					<text class="record-meal">{{ record.meal }}</text>
				</view>
				<view class="record-content">
					<view class="food-item" v-for="(food, foodIndex) in record.foods" :key="foodIndex">
							<image v-if="food.image" :src="food.image" class="food-image" mode="aspectFill"></image>
							<view v-else class="food-image"></view>
							<view class="food-info">
								<text class="food-name">{{ food.name }}</text>
								<text class="food-calories">{{ food.calories }}kcal</text>
							</view>
						</view>
				</view>
				<view class="record-footer">
					<text class="total-calories">总计: {{ record.totalCalories }}kcal</text>
					<view class="nutrition-tags">
						<view class="nutrition-tag" v-for="(tag, tagIndex) in record.nutritionTags" :key="tagIndex">
							<text class="tag-text">{{ tag }}</text>
						</view>
					</view>
				</view>
			</view>
			<view v-if="dietRecords.length === 0 && !loading" class="empty-diet">
				<text class="empty-diet-text">暂无饮食记录</text>
			</view>
		</view>
		
		<!-- 健康记录 -->
		<view class="health-records">
			<text class="section-title">健康记录</text>
			<view v-if="loading" class="loading-container">
				<text class="loading-text">加载中...</text>
			</view>
			<view v-else-if="healthRecords.length === 0" class="empty-container">
				<text class="empty-text">暂无健康记录</text>
			</view>
			<view v-else class="record-card" v-for="record in healthRecords" :key="record.id">
				<view class="record-header">
					<text class="record-type">{{ record.type }}</text>
					<text class="record-date">{{ record.date }}</text>
				</view>
				<view class="record-content">
					<text class="record-item" v-for="(item, index) in record.content" :key="index">
						{{ item.label }}: {{ item.value }}
					</text>
				</view>
			</view>
		</view>
		
		<!-- 添加记录按钮 -->
		<view class="action-section">
			<button class="btn-add" @click="addRecord">添加健康记录</button>
		</view>
	</view>
</template>

<script>
	import api from '../../utils/api.js'
	
	export default {
		data() {
			return {
				healthRecords: [],
				dietRecords: [],
				loading: false,
				selectedDate: new Date().toISOString().split('T')[0]
			}
		},
		onLoad() {
			this.loadHealthRecords()
			this.loadDietRecords()
		},
		onShow() {
			// 页面显示时重新加载数据
			this.loadHealthRecords()
			this.loadDietRecords()
		},
		methods: {
			goBack() {
				uni.navigateBack()
			},
			async loadHealthRecords() {
				this.loading = true
				try {
					const records = await api.older.getHealthRecords()
					// 将后端数据转换为前端需要的格式，并根据选择的日期过滤
					this.healthRecords = records.map(record => {
						const content = []
						if (record.height) content.push({ label: '身高', value: `${record.height} cm` })
						if (record.weight) content.push({ label: '体重', value: `${record.weight} kg` })
						if (record.blood_pressure) content.push({ label: '血压', value: record.blood_pressure })
						if (record.blood_sugar) content.push({ label: '血糖', value: `${record.blood_sugar} mmol/L` })
						if (record.allergies) content.push({ label: '过敏史', value: record.allergies })
						if (record.medications) content.push({ label: '用药情况', value: record.medications })
						if (record.doctor_advice) content.push({ label: '医生建议', value: record.doctor_advice })
						
						let type = '健康记录'
						if (record.blood_pressure) type = '血压记录'
						else if (record.weight) type = '体重记录'
						else if (record.blood_sugar) type = '血糖记录'
						
						return {
							id: record.id,
							type: type,
							date: record.recorded_at.split('T')[0],
							content: content
						}
					}).filter(record => record.date === this.selectedDate)
				} catch (error) {
					console.error('获取健康记录失败:', error)
					uni.showToast({
						title: '获取健康记录失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},

			async loadDietRecords() {
				// 暂时不加载饮食记录，避免404错误
				this.dietRecords = []
			},
			prevDate() {
				const date = new Date(this.selectedDate)
				date.setDate(date.getDate() - 1)
				this.selectedDate = date.toISOString().split('T')[0]
				this.loadHealthRecords() // 根据新日期重新加载健康记录
			},
			nextDate() {
				const date = new Date(this.selectedDate)
				date.setDate(date.getDate() + 1)
				const today = new Date().toISOString().split('T')[0]
				if (date.toISOString().split('T')[0] > today) {
					uni.showToast({
						title: '不能查看未来日期',
						icon: 'none'
					})
					return
				}
				this.selectedDate = date.toISOString().split('T')[0]
				this.loadHealthRecords() // 根据新日期重新加载健康记录
			},
			addRecord() {
				// 直接跳转到添加健康记录页面
				uni.navigateTo({
					url: '/pages/profile/add-health-record'
				})
			}
		}
	}
</script>

<style scoped>
	.health-container {
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
	
	/* 健康状况概览 */
	.health-overview {
		padding: 20px;
	}
	
	.overview-card {
		background: linear-gradient(135deg, #67C23A 0%, #85CE61 100%);
		border-radius: 20px;
		padding: 24px;
		color: white;
		box-shadow: 0 8px 24px rgba(103, 194, 58, 0.3);
	}
	
	.overview-title {
		font-size: 18px;
		font-weight: 600;
		display: block;
		margin-bottom: 16px;
	}
	
	.health-status {
		display: flex;
		align-items: center;
		margin-bottom: 16px;
	}
	
	.status-label {
		font-size: 14px;
		opacity: 0.9;
		margin-right: 8px;
	}
	
	.status-value {
		font-size: 16px;
		font-weight: 600;
	}
	
	.status-normal {
		background-color: rgba(255, 255, 255, 0.2);
		padding: 4px 12px;
		border-radius: 12px;
	}
	
	.health-tags {
		display: flex;
		gap: 8px;
	}
	
	.tag {
		padding: 4px 12px;
		border-radius: 12px;
		font-size: 12px;
		font-weight: 500;
		background-color: rgba(255, 255, 255, 0.2);
	}
	
	/* 日期选择器 */
	.date-selector {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0 20px;
		margin-bottom: 16px;
	}
	
	.date-text {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
	}
	
	.date-nav {
		display: flex;
		gap: 12px;
	}
	
	.nav-btn {
		font-size: 18px;
		color: #666666;
		width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		background-color: #F5F5F5;
	}
	
	.nav-btn:active {
		background-color: #E0E0E0;
	}
	
	/* 饮食记录 */
	.diet-records {
		padding: 0 20px;
		margin-bottom: 24px;
	}
	
	.empty-diet {
		text-align: center;
		padding: 40px 0;
		color: #999999;
	}
	
	.empty-diet-text {
		font-size: 14px;
		color: #999999;
	}
	
	/* 健康记录 */
	.health-records {
		padding: 0 20px;
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 16px;
	}
	
	.record-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		margin-bottom: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.record-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 12px;
		padding-bottom: 12px;
		border-bottom: 1px solid #F5F5F5;
	}
	
	.record-type {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
	}
	
	.record-date {
		font-size: 13px;
		color: #999999;
	}
	
	.record-time {
		font-size: 14px;
		font-weight: 600;
		color: #333333;
	}
	
	.record-meal {
		font-size: 13px;
		color: #FF7A45;
		font-weight: 500;
	}
	
	.record-content {
		display: flex;
		flex-direction: column;
		gap: 12px;
		margin: 16px 0;
	}
	
	.food-item {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	
	.food-image {
		width: 48px;
		height: 48px;
		border-radius: 12px;
		background-color: #F5F5F5;
	}
	
	.food-info {
		flex: 1;
	}
	
	.food-name {
		font-size: 14px;
		font-weight: 500;
		color: #333333;
		display: block;
		margin-bottom: 4px;
	}
	
	.food-calories {
		font-size: 12px;
		color: #999999;
	}
	
	.record-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-top: 12px;
		border-top: 1px solid #F5F5F5;
	}
	
	.total-calories {
		font-size: 14px;
		font-weight: 600;
		color: #333333;
	}
	
	.nutrition-tags {
		display: flex;
		gap: 8px;
	}
	
	.nutrition-tag {
		padding: 4px 8px;
		border-radius: 8px;
		background-color: #F5F5F5;
	}
	
	.tag-text {
		font-size: 11px;
		color: #666666;
	}
	
	.record-item {
		font-size: 14px;
		color: #666666;
		line-height: 1.5;
	}
	
	/* 加载状态 */
	.loading-container {
		text-align: center;
		padding: 40px 0;
	}
	
	.loading-text {
		font-size: 14px;
		color: #999999;
	}
	
	.empty-container {
		text-align: center;
		padding: 40px 0;
	}
	
	.empty-text {
		font-size: 14px;
		color: #999999;
	}
	
	/* 操作区域 */
	.action-section {
		padding: 20px;
	}
	
	.btn-add {
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
