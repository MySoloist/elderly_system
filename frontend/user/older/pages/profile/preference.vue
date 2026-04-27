<template>
	<view class="preference-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">饮食偏好</text>
			<text class="placeholder"></text>
		</view>
		
		<!-- 当前偏好 -->
		<view class="current-preference">
			<text class="section-title">当前偏好</text>
			<view class="preference-card">
				<view class="preference-item">
					<text class="preference-label">口味偏好</text>
					<view class="preference-tags">
						<text v-if="selectedFlavors.length > 0" v-for="flavor in selectedFlavors" :key="flavor" class="tag tag-primary">{{ flavor }}</text>
						<text v-else class="preference-value">无</text>
					</view>
				</view>
				<view class="preference-item">
					<text class="preference-label">烹饪方式</text>
					<view class="preference-tags">
						<text v-if="selectedCooks.length > 0" v-for="cook in selectedCooks" :key="cook" class="tag tag-primary">{{ cook }}</text>
						<text v-else class="preference-value">无</text>
					</view>
				</view>
				<view class="preference-item">
					<text class="preference-label">忌口食物</text>
					<view class="preference-tags">
						<text v-if="selectedAllergies.length > 0" v-for="allergy in selectedAllergies" :key="allergy" class="tag tag-primary">{{ allergy }}</text>
						<text v-else class="preference-value">无</text>
					</view>
				</view>
				<view class="preference-item">
					<text class="preference-label">特殊需求</text>
					<text class="preference-value">{{ specialNeeds || '无' }}</text>
				</view>
			</view>
		</view>
		
		<!-- 偏好设置 -->
		<view class="preference-settings">
			<text class="section-title">偏好设置</text>
			<view class="settings-card">
				<!-- 口味偏好 -->
				<view class="setting-group">
					<text class="setting-title">口味偏好</text>
					<view class="setting-options">
						<text 
							v-for="flavor in flavorOptions" 
							:key="flavor"
							class="setting-option"
							:class="{ active: selectedFlavors.includes(flavor) }"
							@click="toggleFlavor(flavor)"
						>{{ flavor }}</text>
					</view>
					<view class="custom-input-group">
						<input 
							class="custom-input" 
							v-model="customFlavor" 
							placeholder="添加自定义口味"
							@confirm="addCustomFlavor"
						/>
						<button class="add-btn" @click="addCustomFlavor">添加</button>
					</view>
				</view>
				
				<!-- 烹饪方式 -->
				<view class="setting-group">
					<text class="setting-title">烹饪方式</text>
					<view class="setting-options">
						<text 
							v-for="cook in cookOptions" 
							:key="cook"
							class="setting-option"
							:class="{ active: selectedCooks.includes(cook) }"
							@click="toggleCook(cook)"
						>{{ cook }}</text>
					</view>
					<view class="custom-input-group">
						<input 
							class="custom-input" 
							v-model="customCook" 
							placeholder="添加自定义烹饪方式"
							@confirm="addCustomCook"
						/>
						<button class="add-btn" @click="addCustomCook">添加</button>
					</view>
				</view>
				
				<!-- 忌口食物 -->
				<view class="setting-group">
					<text class="setting-title">忌口食物</text>
					<view class="setting-options">
						<text 
							v-for="allergy in allergyOptions" 
							:key="allergy"
							class="setting-option"
							:class="{ active: selectedAllergies.includes(allergy) }"
							@click="toggleAllergy(allergy)"
						>{{ allergy }}</text>
					</view>
					<view class="custom-input-group">
						<input 
							class="custom-input" 
							v-model="customAllergy" 
							placeholder="添加自定义忌口食物"
							@confirm="addCustomAllergy"
						/>
						<button class="add-btn" @click="addCustomAllergy">添加</button>
					</view>
				</view>
				
				<!-- 特殊需求 -->
				<view class="setting-group">
					<text class="setting-title">特殊需求</text>
					<textarea 
						class="textarea" 
						v-model="specialNeeds" 
						placeholder="请输入特殊需求，如低盐、少糖等"
					></textarea>
				</view>
			</view>
		</view>
		
		<!-- 保存按钮 -->
		<view class="action-section">
			<button class="btn-save" @click="savePreference" :disabled="loading">
				{{ loading ? '保存中...' : '保存偏好' }}
			</button>
		</view>
	</view>
</template>

<script>
	import api from '../../utils/api.js'
	
	export default {
		data() {
			return {
				selectedFlavors: [],
				selectedCooks: [],
				selectedAllergies: [],
				specialNeeds: '',
				flavorOptions: ['清淡', '微辣', '酸甜', '原味'],
				cookOptions: ['清蒸', '水煮', '红烧', '炖汤', '凉拌'],
				allergyOptions: ['海鲜', '花生', '鸡蛋', '牛奶', '大豆'],
				customFlavor: '',
				customCook: '',
				customAllergy: '',
				loading: false
			}
		},
		onLoad() {
			this.loadPreferences()
		},
		methods: {
			goBack() {
				uni.navigateBack()
			},
			async loadPreferences() {
				this.loading = true
				try {
					console.log('开始获取饮食偏好...')
					const result = await api.older.getPreferences()
					console.log('API返回数据:', result)
					const preferences = result.dietary_preferences || ''
					console.log('饮食偏好数据:', preferences)
					this.parsePreferences(preferences)
					console.log('解析后的数据:', {
						selectedFlavors: this.selectedFlavors,
						selectedCooks: this.selectedCooks,
						selectedAllergies: this.selectedAllergies,
						specialNeeds: this.specialNeeds
					})
				} catch (error) {
					console.error('获取饮食偏好失败:', error)
					uni.showToast({
						title: '获取饮食偏好失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			parsePreferences(preferences) {
			if (!preferences) return
			
			try {
				const preference = JSON.parse(preferences)
				const tastes = preference.tastes || []
				const allergies = preference.allergies || []
				const specialNeeds = preference.special_needs || ''
				
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
				
				// 口味偏好
				tastes.forEach(taste => {
					const chineseLabel = tasteMap[taste] || taste
					if (!this.selectedFlavors.includes(chineseLabel)) {
						this.selectedFlavors.push(chineseLabel)
						if (!this.flavorOptions.includes(chineseLabel)) {
							this.flavorOptions.push(chineseLabel)
						}
					}
				})
				
				// 过敏信息
				allergies.forEach(allergy => {
					const chineseLabel = allergyMap[allergy] || allergy
					if (!this.selectedAllergies.includes(chineseLabel)) {
						this.selectedAllergies.push(chineseLabel)
						if (!this.allergyOptions.includes(chineseLabel)) {
							this.allergyOptions.push(chineseLabel)
						}
					}
				})
				
				// 特殊需求
				this.specialNeeds = specialNeeds
			} catch (error) {
				console.error('解析饮食偏好失败:', error)
			}
		},
			buildPreferences() {
			const tasteMap = {
				'清淡': 'light',
				'酸辣': 'sour',
				'甜味': 'sweet',
				'咸味': 'salty',
				'苦味': 'bitter',
				'厚重': 'heavy',
				'微辣': 'spicy',
				'低脂': 'low_oil',
				'低糖': 'low_sugar',
				'低盐': 'low_salt'
			}
			
			const allergyMap = {
				'花生': 'nuts',
				'海鲜': 'seafood',
				'鸡蛋': 'egg',
				'牛奶': 'milk',
				'小麦': 'wheat',
				'大豆': 'soy'
			}
			
			const tastes = this.selectedFlavors.map(flavor => tasteMap[flavor] || flavor)
			const allergies = this.selectedAllergies.map(allergy => allergyMap[allergy] || allergy)
			const specialNeeds = this.specialNeeds.trim()
			
			return JSON.stringify({
				tastes,
				allergies,
				special_needs: specialNeeds
			})
		},
			toggleFlavor(flavor) {
				const index = this.selectedFlavors.indexOf(flavor)
				if (index !== -1) {
					this.selectedFlavors.splice(index, 1)
				} else {
					this.selectedFlavors.push(flavor)
				}
			},
			toggleCook(cook) {
				const index = this.selectedCooks.indexOf(cook)
				if (index !== -1) {
					this.selectedCooks.splice(index, 1)
				} else {
					this.selectedCooks.push(cook)
				}
			},
			toggleAllergy(allergy) {
				const index = this.selectedAllergies.indexOf(allergy)
				if (index !== -1) {
					this.selectedAllergies.splice(index, 1)
				} else {
					this.selectedAllergies.push(allergy)
				}
			},
			addCustomFlavor() {
				if (this.customFlavor.trim()) {
					const flavor = this.customFlavor.trim()
					if (!this.flavorOptions.includes(flavor)) {
						this.flavorOptions.push(flavor)
					}
					this.selectedFlavors.push(flavor)
					this.customFlavor = ''
				}
			},
			addCustomCook() {
				if (this.customCook.trim()) {
					const cook = this.customCook.trim()
					if (!this.cookOptions.includes(cook)) {
						this.cookOptions.push(cook)
					}
					this.selectedCooks.push(cook)
					this.customCook = ''
				}
			},
			addCustomAllergy() {
				if (this.customAllergy.trim()) {
					const allergy = this.customAllergy.trim()
					if (!this.allergyOptions.includes(allergy)) {
						this.allergyOptions.push(allergy)
					}
					this.selectedAllergies.push(allergy)
					this.customAllergy = ''
				}
			},
			async savePreference() {
				this.loading = true
				try {
					const preferences = this.buildPreferences()
					await api.older.updatePreferences({ dietary_preferences: preferences })
					
					uni.showToast({
						title: '偏好设置已保存',
						icon: 'success'
					})
					
					setTimeout(() => {
						uni.navigateBack()
					}, 1000)
				} catch (error) {
					console.error('保存饮食偏好失败:', error)
					uni.showToast({
						title: '保存失败，请重试',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			}
		}
	}
</script>

<style scoped>
	.preference-container {
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
	
	/* 当前偏好 */
	.current-preference {
		padding: 20px;
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 16px;
	}
	
	.preference-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.preference-item {
		display: flex;
		align-items: center;
		padding: 12px 0;
		border-bottom: 1px solid #F5F5F5;
	}
	
	.preference-item:last-child {
		border-bottom: none;
	}
	
	.preference-label {
		width: 80px;
		font-size: 14px;
		color: #666666;
	}
	
	.preference-value {
		flex: 1;
		font-size: 14px;
		color: #333333;
		font-weight: 500;
	}
	
	.preference-tags {
		flex: 1;
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
	}
	
	.tag {
		padding: 4px 12px;
		border-radius: 12px;
		font-size: 12px;
		font-weight: 500;
		background-color: rgba(255, 122, 69, 0.1);
		color: #FF7A45;
	}
	
	/* 偏好设置 */
	.preference-settings {
		padding: 0 20px;
	}
	
	.settings-card {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.setting-group {
		margin-bottom: 24px;
	}
	
	.setting-group:last-child {
		margin-bottom: 0;
	}
	
	.setting-title {
		font-size: 15px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 12px;
	}
	
	.setting-options {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}
	
	.setting-option {
		padding: 8px 16px;
		border: 1px solid #DDDDDD;
		border-radius: 16px;
		font-size: 14px;
		color: #666666;
		background: #fafafa;
	}
	
	.setting-option.active {
		border-color: transparent;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		box-shadow: 0 6px 14px rgba(255, 122, 69, 0.24);
	}
	
	/* 自定义输入区域 */
	.custom-input-group {
		display: flex;
		gap: 12px;
		margin-top: 16px;
		align-items: center;
	}
	
	.custom-input {
		flex: 1;
		height: 40px;
		padding: 0 16px;
		border: 1px solid #DDDDDD;
		border-radius: 20px;
		font-size: 14px;
		background: #fafafa;
	}
	
	.add-btn {
		padding: 8px 20px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border: none;
		border-radius: 20px;
		font-size: 14px;
		font-weight: 500;
		box-shadow: 0 4px 12px rgba(255, 122, 69, 0.2);
	}
	
	.textarea {
		width: 100%;
		height: 80px;
		padding: 12px 16px;
		border: 1px solid #DDDDDD;
		border-radius: 12px;
		font-size: 14px;
		color: #333333;
		background: #fafafa;
		resize: none;
		line-height: 1.5;
	}
	
	.textarea:focus {
		border-color: #FF7A45;
		outline: none;
		background: #FFFFFF;
	}
	
	/* 操作区域 */
	.action-section {
		padding: 20px;
	}
	
	.btn-save {
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
	
	.btn-save:disabled {
		background: #CCCCCC;
		box-shadow: none;
	}
</style>
