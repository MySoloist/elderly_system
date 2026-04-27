<template>
	<view class="home-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="nav-title">餐品浏览</text>
			<view class="search-container" :class="{ active: searchVisible }">
				<input 
					class="search-input" 
					placeholder="搜索餐品名称或标签..." 
					v-model="searchKeyword"
					@focus="searchVisible = true"
					@confirm="handleSearch"
				/>
				<text class="search-btn" @click="toggleSearch">🔍</text>
			</view>
		</view>
		
		<!-- AI智能推荐区域 -->
		<view class="ai-recommend">
			<view class="recommend-header">
				<text class="recommend-title">AI智能推荐</text>
				<text v-if="isAiThinking" class="ai-thinking">🤖 正在思考...</text>
				<text v-else class="recommend-desc">根据您的口味偏好和健康状况推荐</text>
			</view>
			<view v-if="isAiThinking" class="ai-thinking-content">
				<text class="thinking-icon">🤖</text>
				<text class="thinking-text">AI正在分析您的健康数据和饮食偏好...</text>
			</view>
			<view v-else-if="recommendFoods.length > 0">
				<view>推荐数量: {{ recommendFoods.length }}</view>
				<swiper class="recommend-swiper" :indicator-dots="true" :autoplay="true" :interval="5000" :duration="500" :circular="true">
					<swiper-item v-for="(item, index) in recommendFoods" :key="index" class="recommend-item">
						<view class="recommend-card" @click="goToFoodDetail(item.id)">
							<image v-if="item.image && item.image.includes('http')" class="recommend-image" :src="item.image" mode="aspectFill"></image>
							<text v-else class="recommend-image">{{ item.image }}</text>
							<view class="name-price-row">
								<text class="recommend-name">{{ item.name }}</text>
								<text class="recommend-price">¥{{ item.price }}</text>
							</view>
							

						</view>
					</swiper-item>
				</swiper>
			</view>
			<view v-else>
				<view class="no-recommend">
					<text class="no-recommend-text">暂无推荐餐品</text>
				</view>
			</view>
			

		</view>
		
		<!-- 分类标签栏 -->
		<scroll-view class="category-scroll" scroll-x="true" show-scrollbar="true">
			<view class="category-list">
				<text 
					v-for="category in categories" 
					:key="category.id"
					class="category-tag"
					:class="{ active: activeCategory === category.id }"
					@click="activeCategory = category.id"
				>{{ category.name }}</text>
			</view>
		</scroll-view>
		
		<!-- 餐品内容区域 -->
		<view class="food-list">
			<view 
				v-for="food in filteredFoods" 
				:key="food.id"
				class="food-card"
				@click="goToFoodDetail(food.id)"
			>
				<image v-if="food.image && food.image.includes('http')" class="food-image" :src="food.image" mode="aspectFit"></image>
				<text v-else class="food-image">{{ food.image }}</text>
				<text 
					class="favorite-btn"
					:class="{ active: favorites.includes(food.id) }"
					@click.stop="toggleFavorite(food)"
				>{{ favorites.includes(food.id) ? '❤️' : '🤍' }}</text>
				<text class="food-name">{{ food.name }}</text>
				<text class="food-price">¥{{ food.price }}</text>
				
				
			</view>
		</view>
		
		<!-- 悬浮AI助手 -->
		<view class="ai-assistant" @click="showAiAssistant">
			<image class="ai-icon" src="/static/robot.png" mode="aspectFit"></image>
		</view>
		
		<!-- AI助手悬浮窗组件 -->
		<ai-assistant ref="aiAssistant"></ai-assistant>
		
		<!-- 日期时间选择器弹窗 -->
	<view v-if="showTimePicker" class="time-picker-overlay" style="z-index: 10000; background: rgba(0,0,0,0.7);">
		<view class="time-picker-container" style="background: white; border-radius: 12px;">
			<view class="time-picker-header">
				<text class="time-picker-title">选择配送时间</text>
			</view>
			<view class="time-picker-content">
				<view class="time-picker-row">
					<text class="time-label">日期:</text>
					<picker mode="date" :value="selectedDate ? selectedDate.toISOString().split('T')[0] : ''" @change="(e) => selectedDate = new Date(e.detail.value)">
						<view class="picker-display">{{ selectedDate ? selectedDate.toLocaleDateString('zh-CN') : '选择日期' }}</view>
					</picker>
				</view>
				<view class="time-picker-row">
					<text class="time-label">小时:</text>
					<picker :value="selectedHour - 8" :range="hours" @change="(e) => selectedHour = hours[e.detail.value]">
						<view class="picker-display">{{ selectedHour }}时</view>
					</picker>
				</view>
				<view class="time-picker-row">
					<text class="time-label">分钟:</text>
					<picker :value="selectedMinute === 0 ? 0 : 1" :range="minutes" @change="(e) => selectedMinute = parseInt(minutes[e.detail.value])">
						<view class="picker-display">{{ selectedMinute.toString().padStart(2, '0') }}分</view>
					</picker>
				</view>
			</view>
			<view class="time-picker-footer">
				<button class="cancel-btn" @click="cancelTimeSelection">取消</button>
				<button class="confirm-btn" @click="confirmTimeSelection">确认</button>
			</view>
		</view>
	</view>
	</view>
</template>

<script>
	import AiAssistant from '@/components/ai-assistant/ai-assistant.vue'
	import { api } from '../../utils/api.js'

	export default {
		components: {
			AiAssistant
		},
		data() {
			return {
				activeCategory: 1,
				categories: [],
				recommendFoods: [],
				foods: [],
				favorites: [],
				loading: false,
				searchVisible: true,
				searchKeyword: '',
				isAiThinking: false,
				// 时间选择器相关
				showTimePicker: false,
				selectedFood: null,
				selectedDate: null,
				selectedHour: 12,
				selectedMinute: 0,
				hours: Array.from({length: 13}, (_, i) => i + 8), // 8:00-20:00
				minutes: Array.from({length: 60}, (_, i) => i.toString().padStart(2, '0')) // 显示所有分钟
			}
		},
		computed: {
			filteredFoods() {
				let filtered = [...this.foods]
				
				// 先应用分类过滤
				const activeCategoryConfig = this.categories.find(cat => cat.id === this.activeCategory)
				if (activeCategoryConfig) {
					const filter = activeCategoryConfig.filter
					if (filter) {
						if (filter === 'favorite') {
							// 我的收藏
							filtered = filtered.filter(food => this.favorites.includes(food.id))
						} else if (filter.tag_id) {
							// 按标签ID过滤
							filtered = filtered.filter(food => food.tag_id === filter.tag_id)
						} else if (filter.category_id) {
							// 按分类ID过滤
							filtered = filtered.filter(food => food.category_id === filter.category_id)
						} else if (filter.tag_name) {
							// 按标签名称过滤（兼容旧逻辑）
							filtered = filtered.filter(food => food.tags.includes(filter.tag_name))
						}
					}
				}
				
				// 然后在过滤后的结果中应用搜索
				if (this.searchKeyword) {
					const keyword = this.searchKeyword.toLowerCase()
					filtered = filtered.filter(food => 
						food.name.toLowerCase().includes(keyword) ||
						food.tags.some(tag => tag.toLowerCase().includes(keyword))
					)
				}
				
				return filtered
			}
		},
		onLoad() {
			this.loadData()
		},
		onShow() {
			// 页面显示时重新加载数据
			this.loadData()
		},
		methods: {
			async loadCategories() {
				try {
					console.log('开始加载标签数据...')
					const response = await api.older.getTags()
					console.log('标签API响应:', response)
					
					if (response && response.tags) {
						// 添加"全部餐品"选项，然后添加从API获取的标签
						this.categories = [
							{ id: 1, name: '全部餐品', filter: null },
							...response.tags.map((tag, index) => ({
								id: index + 2,
								name: tag.name,
								filter: { tag_id: tag.id }
							}))
						]
						console.log('加载的标签数据:', this.categories)
					} else {
						throw new Error('标签数据为空')
					}
				} catch (error) {
					console.error('加载标签失败:', error)
					// 如果获取标签失败，使用默认标签
					this.categories = [
						{ id: 1, name: '全部餐品', filter: null },
						{ id: 2, name: '营养套餐', filter: { tag_id: 13 } },
						{ id: 3, name: '清淡餐品', filter: { tag_id: 10 } },
						{ id: 4, name: '高蛋白餐品', filter: { tag_id: 11 } },
						{ id: 5, name: '流食软食', filter: { tag_id: 12 } },
						{ id: 6, name: '素食餐品', filter: { tag_id: 9 } },
						{ id: 7, name: '低糖餐品', filter: { tag_id: 8 } }
					]
				}
			},
			async loadData() {
				this.loading = true
				try {
					console.log('开始加载餐品数据...')
					// 获取当前用户信息
					this.currentUser = uni.getStorageSync('user')
					console.log('当前登录用户:', this.currentUser)
					
					// 先加载分类数据
					await this.loadCategories()
					
					// 获取餐品列表
					const mealsResponse = await api.older.getMeals()
					console.log('餐品API响应:', mealsResponse)
					
					if (!mealsResponse || !mealsResponse.items) {
						console.error('餐品数据为空')
						this.foods = []
						// 不返回，继续执行AI推荐逻辑
					}
					
					console.log('餐品数量:', mealsResponse && mealsResponse.items ? mealsResponse.items.length : 0)
					
					// 创建标签映射表
					const tagMapping = {
						'营养': '营养',
						'低盐': '低盐',
						'清淡': '清淡',
						'易消化': '易消化',
						'高蛋白': '高蛋白',
						'低脂': '低脂',
						'低糖': '低糖'
					}
					
					this.foods = mealsResponse.items.map(meal => {
						console.log('处理餐品:', meal)
						// 处理标签映射
						let tags = []
						if (meal.special_tag) {
							const mappedTag = tagMapping[meal.special_tag] || meal.special_tag
							tags = [mappedTag]
						}
						
						return {
							id: meal.id,
							name: meal.name,
							price: meal.price,
							image: meal.image_url || '🍱',
							tags: tags,
							category_id: meal.category_id,
							tag_id: meal.tag_id,
							special_tag: meal.special_tag // 保留原始标签用于过滤
						}
					})
					
					console.log('处理后的餐品数据:', this.foods)
					
					// 获取收藏列表
				try {
					const favoritesResponse = await api.older.getFavorites()
					console.log('收藏API响应:', favoritesResponse)
					this.favorites = favoritesResponse.items.map(fav => fav.meal.id)
					console.log('收藏列表:', this.favorites)
				} catch (error) {
					console.error('获取收藏失败:', error)
					this.favorites = []
				}
				
				// 获取AI智能推荐
					try {
						console.log('开始获取AI推荐...')
						console.log('foods数据:', this.foods)
						console.log('foods数量:', this.foods.length)
						// 设置AI思考状态
						this.isAiThinking = true
						
						// 模拟AI思考延迟，让用户看到思考过程
						await new Promise(resolve => setTimeout(resolve, 1500))
						
						const recommendResponse = await api.older.getAIRecommendations()
						console.log('AI推荐API响应:', recommendResponse)
						
						if (recommendResponse && recommendResponse.recommendations) {
						this.recommendFoods = recommendResponse.recommendations.map(item => ({
							id: item.id,
							name: item.name,
							price: item.price,
							image: item.image_url || '🍱',
							tags: item.tag_name ? [item.tag_name] : ['推荐']
						}))
					} else {
						// 如果AI推荐失败，使用默认推荐
						console.log('使用默认推荐，foods数量:', this.foods.length)
						this.recommendFoods = this.foods.slice(0, 4).map(food => ({
							...food,
							tags: food.tags.length > 0 ? food.tags : ['推荐']
						}))
					}
					} catch (error) {
						console.error('获取AI推荐失败:', error)
						// 使用默认推荐
						this.recommendFoods = this.foods.slice(0, 4).map(food => ({
							...food,
							tags: food.tags.length > 0 ? food.tags : ['推荐']
						}))
					} finally {
						// 结束AI思考状态
						this.isAiThinking = false
					}
					
					console.log('AI推荐数据:', this.recommendFoods)
					console.log('推荐数量:', this.recommendFoods.length)
					
					// 如果推荐数据为空，添加模拟数据
					if (this.recommendFoods.length === 0) {
						console.log('添加模拟推荐数据')
						this.recommendFoods = [
							{
								id: 1,
								name: '蒸蛋羹',
								price: 8,
								image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=delicious%20steamed%20egg%20custard%20in%20yellow%20bowl%2C%20soft%20and%20smooth%2C%20healthy%20food&image_size=square',
								tags: ['营养']
							},
							{
								id: 2,
								name: '小米粥',
								price: 6,
								image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=millet%20porridge%20in%20blue%20bowl%2C%20warm%20and%20nutritious%2C%20traditional%20chinese%20food&image_size=square',
								tags: ['易消化']
							},
							{
								id: 3,
								name: '清炒时蔬',
								price: 12,
								image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=fresh%20stir%20fried%20vegetables%2C%20colorful%20mixed%20vegetables%2C%20healthy%20diet&image_size=square',
								tags: ['清淡']
							}
						]
					}
					
				} catch (error) {
					console.error('加载数据失败:', error)
					uni.showToast({
						title: '加载失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			toggleSearch() {
			this.searchVisible = !this.searchVisible
			if (this.searchVisible) {
				setTimeout(() => {
					// 在微信小程序中使用uni.createSelectorQuery()
					uni.createSelectorQuery().select('.search-input').node(function(res) {
						if (res && res.node) {
							res.node.focus()
						}
					}).exec()
				}, 100)
			} else {
				this.searchKeyword = ''
			}
		},
		handleSearch() {
			// 搜索已经在computed中实时过滤了
			if (!this.searchKeyword.trim()) {
				this.searchVisible = false
			}
		},
			getTagClass(tag) {
				const tagMap = {
					'低糖': 'tag-primary',
					'低盐': 'tag-primary',
					'素食': 'tag-success',
					'高蛋白': 'tag-success',
					'易消化': 'tag-warning',
					'清淡': 'tag-primary',
					'推荐': 'tag-warning'
				}
				return tagMap[tag] || 'tag-primary'
			},
			async toggleFavorite(food) {
				const isFavorite = this.favorites.includes(food.id)
				try {
					if (isFavorite) {
						await api.older.removeFavorite(food.id)
						this.favorites = this.favorites.filter(id => id !== food.id)
						uni.showToast({
							title: '已取消收藏',
							icon: 'success'
						})
					} else {
						await api.older.addFavorite(food.id)
						this.favorites.push(food.id)
						uni.showToast({
							title: '已收藏',
							icon: 'success'
						})
					}
				} catch (error) {
					uni.showToast({
						title: '操作失败',
						icon: 'none'
					})
				}
			},
			async quickOrder(food) {
				try {
					console.log('开始下单流程')
					// 显示下单方式选择框
					uni.showActionSheet({
						itemList: ['现在下单', '预定下单'],
						success: async (res) => {
							console.log('用户选择:', res.tapIndex)
							if (res.tapIndex === 0) {
								// 现在下单
								console.log('用户选择现在下单')
								await this.createOrder(food, 'immediate', null)
							} else {
								// 预定下单，直接显示自定义日期时间选择器
								console.log('用户选择预定下单')
								this.selectedFood = food
								this.selectedDate = new Date()
								this.showTimePicker = true
							}
						},
						fail: (err) => {
							console.error('showActionSheet失败:', err)
						}
					})
				} catch (error) {
					console.error('点餐失败:', error)
					uni.showToast({
						title: '点餐失败，请重试',
						icon: 'none'
					})
				}
			},
			async createOrder(food, orderType, scheduledTime) {
				try {
					// 创建订单数据
					const orderData = {
						items: [{
							meal_id: food.id,
							quantity: 1
						}],
						delivery_address: '幸福小区3号楼2单元501室',
						special_notes: '',
						order_type: orderType
					}
					
					// 如果是预定订单，添加预定时间
					if (orderType === 'scheduled' && scheduledTime) {
						orderData.scheduled_time = scheduledTime
					}
					
					// 调用创建订单API
					const response = await api.older.createOrder(orderData)
					console.log('创建订单成功:', response)
					
					const message = orderType === 'immediate' 
						? `点餐成功！订单号: ${response.id}`
						: `预定成功！订单号: ${response.id}`
					
					uni.showToast({
						title: message,
						icon: 'success'
					})
					
					// 跳转到订单页面并强制刷新
					setTimeout(() => {
						uni.switchTab({
							url: '/pages/order/order',
							success: () => {
								// 跳转成功后，通知订单页面刷新数据
								uni.$emit('refreshOrderList')
							}
						})
					}, 1500)
				} catch (error) {
					console.error('点餐失败:', error)
					uni.showToast({
						title: '点餐失败，请重试',
						icon: 'none'
					})
				}
			},
			confirmTimeSelection() {
				console.log('确认时间选择:', this.selectedHour, this.selectedMinute)
				
				if (this.selectedDate && this.selectedFood) {
					const scheduledDate = new Date(this.selectedDate)
					scheduledDate.setHours(this.selectedHour, this.selectedMinute, 0, 0)
					const scheduledTime = scheduledDate.toISOString()
					console.log('最终预定时间:', scheduledTime)
					
					this.createOrder(this.selectedFood, 'scheduled', scheduledTime)
					this.showTimePicker = false
				}
			},
			cancelTimeSelection() {
				console.log('取消时间选择')
				this.showTimePicker = false
			},
			goToFoodDetail(foodId) {
				uni.navigateTo({
					url: `/pages/food/detail?id=${foodId}`
				})
			},
			showAiAssistant() {
				this.$refs.aiAssistant.open()
			}
		}
	}
</script>

<style scoped>
	.home-container {
		min-height: 100vh;
		background: linear-gradient(180deg, #FFF8F4 0%, #F7F7F7 220px, #F5F5F5 100%);
		padding-bottom: 70px;
	}
	
	/* 顶部导航栏 */
	.top-nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 20px;
		background: rgba(255, 255, 255, 0.95);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		position: sticky;
		top: 0;
		z-index: 100;
	}
	
	.nav-title {
		font-size: 20px;
		font-weight: 600;
		color: #FF7A45;
	}
	
	.search-container {
		display: flex;
		align-items: center;
	}
	
	.search-input {
		width: 200px;
		height: 36px;
		border: 1px solid #DDDDDD;
		border-radius: 18px;
		padding: 0 16px;
		font-size: 14px;
		margin-right: 12px;
	}
	
	.search-btn {
		font-size: 24px;
		padding: 8px;
		border-radius: 50%;
		background: rgba(255, 122, 69, 0.1);
	}
	
	/* AI推荐区域 */
	.ai-recommend {
		padding: 15px;
	}
	
	.recommend-header {
		display: flex;
		flex-direction: column;
		margin-bottom: 16px;
	}
	
	.recommend-title {
		font-size: 22px;
		font-weight: 600;
		color: #333;
		margin-bottom: 8px;
	}
	
	.recommend-desc {
		font-size: 14px;
		color: #666;
	}
	
	.ai-thinking {
		font-size: 14px;
		color: #FF6B6B;
		animation: pulse 1.5s infinite;
	}
	
	.ai-thinking-content {
		flex: 0 0 100%;
		background: white;
		border-radius: 16px;
		padding: 40px 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	
	.thinking-icon {
		font-size: 48px;
		margin-bottom: 16px;
		animation: bounce 2s infinite;
	}
	
	.thinking-text {
		font-size: 16px;
		color: #666;
		line-height: 1.5;
	}
	
	.no-recommend {
		flex: 0 0 100%;
		background: white;
		border-radius: 16px;
		padding: 40px 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
		text-align: center;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.no-recommend-text {
		font-size: 16px;
		color: #999;
	}
	
	@keyframes pulse {
		0% { opacity: 0.6; }
		50% { opacity: 1; }
		100% { opacity: 0.6; }
	}
	
	@keyframes bounce {
		0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
		40% { transform: translateY(-10px); }
		60% { transform: translateY(-5px); }
	}
	

	
	/* 健康数据区域样式 */
	.health-data-section {
		margin-top: 20px;
		background: white;
		border-radius: 16px;
		padding: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
	}
	
	
	
	.recommend-swiper {
		width: 100%;
		height: 350px;
		background: transparent;
	}
	
	.recommend-item {
		width: 100%;
		padding: 0;
	}
	
	.recommend-card {
		width: 100%;
		background: white;
		border-radius: 16px;
		padding: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
		position: relative;
	}
	
	.name-price-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 8px;
	}
	
	.recommend-image {
		width: 100%;
		height: 180px;
		display: block;
		margin: 0 auto 12px;
		border-radius: 16px;
		object-fit: cover;
	}
	
	.recommend-name {
		font-size: 18px;
		font-weight: 600;
		color: #333;
		flex: 1;
	}
	
	.recommend-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		margin-bottom: 12px;
	}
	
	.recommend-price {
		font-size: 20px;
		font-weight: 600;
		color: #FF7A45;
		margin-left: 12px;
	}
	
	.quick-order-btn {
		width: 100%;
		height: 40px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 16px;
		font-weight: 600;
	}
	
	/* 分类标签栏 */
	.category-scroll {
		padding: 0 20px;
		margin-bottom: 16px;
	}
	
	.category-list {
		display: flex;
		gap: 16px;
		padding: 10px 0;
	}
	
	.category-tag {
		padding: 8px 16px;
		background: white;
		border-radius: 20px;
		font-size: 16px;
		color: #666;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		white-space: nowrap;
		display: inline-block;
	}
	
	.category-tag.active {
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		color: white;
	}
	
	/* 餐品列表 */
	.food-list {
		padding: 0 12px;
		display: flex;
		flex-wrap: wrap;
		gap: 12px;
	}

	.food-card {
		background: white;
		border-radius: 16px;
		padding: 16px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
		position: relative;
		flex: 0 0 calc(50% - 6px);
		max-width: calc(50% - 6px);
		min-width: calc(50% - 6px);
	}
	
	.food-image {
		width: 100%;
		height: 120px;
		display: block;
		border-radius: 8px;
		object-fit: cover;
		margin-bottom: 12px;
	}
	
	.favorite-btn {
		position: absolute;
		top: 16px;
		right: 16px;
		font-size: 24px;
	}
	
	.favorite-btn.active {
		color: #FF4757;
	}
	
	.food-name {
		font-size: 18px;
		font-weight: 600;
		color: #333;
		display: block;
		margin-bottom: 8px;
	}
	
	.food-price {
		font-size: 20px;
		font-weight: 600;
		color: #FF7A45;
		display: block;
		margin-bottom: 12px;
	}
	
	.food-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		margin-bottom: 16px;
	}
	
	.tag {
		padding: 4px 8px;
		border-radius: 4px;
		font-size: 12px;
	}
	
	.tag-primary {
		background: rgba(64, 158, 255, 0.1);
		color: #409EFF;
	}
	
	.tag-success {
		background: rgba(103, 194, 58, 0.1);
		color: #67C23A;
	}
	
	.tag-warning {
		background: rgba(230, 162, 60, 0.1);
		color: #E6A23C;
	}
	
	.order-btn {
		width: 100%;
		height: 40px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF8F6A 100%);
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 16px;
		font-weight: 600;
	}
	
	/* AI助手 */
	.ai-assistant {
		position: fixed;
		bottom: 100px;
		right: 20px;
		width: 60px;
		height: 60px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}
	
	.ai-icon {
		width: 40px;
		height: 40px;
	}
	
	/* 时间选择器样式 */
	.time-picker-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 9999;
	}
	
	.time-picker-container {
		background-color: white;
		border-radius: 12px;
		width: 80%;
		max-width: 300px;
		padding: 20px;
	}
	
	.time-picker-header {
		text-align: center;
		padding-bottom: 20px;
		border-bottom: 1px solid #f0f0f0;
	}
	
	.time-picker-title {
		font-size: 18px;
		font-weight: bold;
		color: #333;
	}
	
	.time-picker-content {
		padding: 20px 0;
	}
	
	.time-picker-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 20px;
	}
	
	.time-label {
		font-size: 16px;
		color: #666;
		width: 60px;
	}
	
	.picker-display {
		flex: 1;
		text-align: center;
		padding: 10px;
		background-color: #f5f5f5;
		border-radius: 8px;
		font-size: 16px;
		color: #333;
		border: 1px solid #e0e0e0;
	}
	
	.time-picker-footer {
		display: flex;
		justify-content: space-between;
		border-top: 1px solid #f0f0f0;
		padding-top: 20px;
	}
	
	.time-picker-footer .cancel-btn {
		flex: 1;
		margin-right: 10px;
		background-color: #f5f5f5;
		color: #666;
		border: none;
		border-radius: 8px;
		padding: 12px;
		font-size: 16px;
	}
	
	.time-picker-footer .confirm-btn {
		flex: 1;
		margin-left: 10px;
		background-color: #4CAF50;
		color: white;
		border: none;
		border-radius: 8px;
		padding: 12px;
		font-size: 16px;
	}
</style>