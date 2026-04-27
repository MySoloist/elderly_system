<template>
	<view class="exception-container">
		<view class="exception-type-section">
			<text class="section-title">异常类型</text>
			<view class="type-options">
				<view 
					v-for="type in exceptionTypes" 
					:key="type.value"
					:class="['type-option', { selected: selectedType === type.value }]"
					@click="selectedType = type.value"
				>
					<text class="type-icon">{{ type.icon }}</text>
					<text class="type-label">{{ type.label }}</text>
				</view>
			</view>
		</view>
		
		<view class="description-section">
			<text class="section-title">异常描述</text>
			<textarea 
				v-model="description" 
				placeholder="请详细描述异常情况..."
				class="description-input"
				:disabled="loading"
			></textarea>
			<text class="char-count">{{ description.length }}/500</text>
		</view>
		
		<view class="submit-section">
			<button @click="submitException" class="submit-button" :disabled="loading">{{ loading ? '提交中...' : '提交异常' }}</button>
			<button @click="goBack" class="cancel-button" :disabled="loading">取消</button>
		</view>
	</view>
</template>

<script>
	import { api } from '../../utils/api.js'
	
	export default {
		data() {
			return {
				selectedType: '',
				description: '',
				loading: false,
				orderId: null,
				exceptionTypes: [
					{ value: 'elderly_not_home', label: '老人不在家', icon: '🏠' },
					{ value: 'address_error', label: '地址错误', icon: '📍' },
					{ value: 'meal_problem', label: '餐品问题', icon: '🍱' },
					{ value: 'other', label: '其他问题', icon: '❓' }
				]
			}
		},
		onLoad(options) {
			this.orderId = options.orderId
		},
		methods: {
			async submitException() {
				if (!this.selectedType) {
					uni.showToast({
						title: '请选择异常类型',
						icon: 'none'
					})
					return
				}
				if (!this.description || this.description.trim() === '') {
					uni.showToast({
						title: '请填写异常描述',
						icon: 'none'
					})
					return
				}
				if (!this.orderId) {
					uni.showToast({
						title: '订单信息错误',
						icon: 'none'
					})
					return
				}
				
				this.loading = true
				try {
					await api.exceptions.reportException(this.orderId, this.selectedType, this.description)
					uni.showToast({
						title: '异常提交成功',
						icon: 'success'
					})
					setTimeout(() => {
						uni.navigateBack()
					}, 1000)
				} catch (error) {
					console.error('提交异常失败:', error)
					uni.showToast({
						title: error.message || '提交异常失败',
						icon: 'none'
					})
				} finally {
					this.loading = false
				}
			},
			goBack() {
				uni.navigateBack()
			}
		}
	}
</script>

<style scoped>
	.exception-container {
		min-height: 100vh;
		padding: 30rpx;
	}
	
	.section-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #1e293b;
		margin-bottom: 20rpx;
		display: block;
	}
	
	.exception-type-section {
		margin-bottom: 30rpx;
	}
	
	.type-options {
		display: flex;
		flex-wrap: wrap;
		gap: 20rpx;
	}
	
	.type-option {
		flex: 1;
		min-width: 160rpx;
		background-color: white;
		border: 2rpx solid #e2e8f0;
		border-radius: 20rpx;
		padding: 24rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12rpx;
	}
	
	.type-option.selected {
		border-color: #10b981;
		background-color: #d1fae5;
	}
	
	.type-icon {
		font-size: 48rpx;
	}
	
	.type-label {
		font-size: 28rpx;
		color: #1e293b;
		font-weight: 500;
	}
	
	.description-section {
		margin-bottom: 30rpx;
	}
	
	.description-input {
		width: 100%;
		height: 200rpx;
		background-color: white;
		border: 1rpx solid #e2e8f0;
		border-radius: 16rpx;
		padding: 20rpx;
		font-size: 32rpx;
		color: #1e293b;
		resize: none;
	}
	
	.char-count {
		font-size: 24rpx;
		color: #94a3b8;
		text-align: right;
		display: block;
		margin-top: 10rpx;
	}
	
	.submit-section {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}
	
	.submit-button, .cancel-button {
		height: 96rpx;
		border-radius: 24rpx;
		font-size: 32rpx;
		font-weight: 500;
		border: none;
	}
	
	.submit-button {
		background-color: #10b981;
		color: white;
	}
	
	.cancel-button {
		background-color: #f1f5f9;
		color: #64748b;
	}
</style>