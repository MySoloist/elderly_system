<template>
	<view class="add-health-record">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<text class="back-btn" @click="goBack">←</text>
			<text class="nav-title">添加健康记录</text>
			<text class="placeholder"></text>
		</view>
		
		<!-- 表单区域 -->
		<view class="form-container">
			<view class="form-section">
				<text class="section-title">基本信息</text>
				
				<view class="form-item">
					<text class="label">身高 (cm)</text>
					<input class="input" type="number" v-model="formData.height" placeholder="请输入身高">
				</view>
				
				<view class="form-item">
					<text class="label">体重 (kg)</text>
					<input class="input" type="number" v-model="formData.weight" placeholder="请输入体重">
				</view>
			</view>
			
			<view class="form-section">
				<text class="section-title">健康指标</text>
				
				<view class="form-item">
					<text class="label">血压</text>
					<input class="input" v-model="formData.blood_pressure" placeholder="例如：135/85">
				</view>
				
				<view class="form-item">
					<text class="label">血糖 (mmol/L)</text>
					<input class="input" type="number" step="0.1" v-model="formData.blood_sugar" placeholder="请输入血糖值">
				</view>
			</view>
			
			<view class="form-section">
				<text class="section-title">健康信息</text>
				
				<view class="form-item">
					<text class="label">过敏史</text>
					<textarea class="textarea" v-model="formData.allergies" placeholder="请输入过敏史"></textarea>
				</view>
				
				<view class="form-item">
					<text class="label">用药情况</text>
					<textarea class="textarea" v-model="formData.medications" placeholder="请输入用药情况"></textarea>
				</view>
				
				<view class="form-item">
					<text class="label">医生建议</text>
					<textarea class="textarea" v-model="formData.doctor_advice" placeholder="请输入医生建议"></textarea>
				</view>
			</view>
		</view>
		
		<!-- 保存按钮 -->
		<view class="action-section">
			<button class="btn-save" @click="saveRecord" :disabled="saving">
				{{ saving ? '保存中...' : '保存' }}
			</button>
		</view>
	</view>
</template>

<script>
	import api from '../../utils/api.js'
	
	export default {
		data() {
			return {
				formData: {
					height: '',
					weight: '',
					blood_pressure: '',
					blood_sugar: '',
					allergies: '',
					medications: '',
					doctor_advice: ''
				},
				saving: false
			}
		},
		methods: {
			goBack() {
				uni.navigateBack()
			},
			async saveRecord() {
				// 表单验证
				if (!this.formData.height && !this.formData.weight && !this.formData.blood_pressure && !this.formData.blood_sugar) {
					uni.showToast({
						title: '请至少填写一项健康数据',
						icon: 'none'
					})
					return
				}
				
				this.saving = true
				try {
					const data = {
						height: this.formData.height ? parseFloat(this.formData.height) : null,
						weight: this.formData.weight ? parseFloat(this.formData.weight) : null,
						blood_pressure: this.formData.blood_pressure || null,
						blood_sugar: this.formData.blood_sugar ? parseFloat(this.formData.blood_sugar) : null,
						allergies: this.formData.allergies || null,
						medications: this.formData.medications || null,
						doctor_advice: this.formData.doctor_advice || null
					}
					
					await api.older.createHealthRecord(data)
					
					uni.showToast({
						title: '保存成功',
						icon: 'success'
					})
					
					// 返回上一页
					setTimeout(() => {
						uni.navigateBack()
					}, 1500)
				} catch (error) {
					console.error('保存健康记录失败:', error)
					uni.showToast({
						title: '保存失败，请重试',
						icon: 'none'
					})
				} finally {
					this.saving = false
				}
			}
		}
	}
</script>

<style scoped>
	.add-health-record {
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
	
	/* 表单区域 */
	.form-container {
		padding: 20px;
	}
	
	.form-section {
		background-color: #FFFFFF;
		border-radius: 20px;
		padding: 20px;
		margin-bottom: 20px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.section-title {
		font-size: 16px;
		font-weight: 600;
		color: #333333;
		display: block;
		margin-bottom: 20px;
	}
	
	.form-item {
		margin-bottom: 20px;
	}
	
	.form-item:last-child {
		margin-bottom: 0;
	}
	
	.label {
		font-size: 14px;
		color: #666666;
		display: block;
		margin-bottom: 8px;
	}
	
	.input, .textarea {
		width: 100%;
		padding: 12px 16px;
		border: 1px solid #E5E5E5;
		border-radius: 12px;
		font-size: 14px;
		color: #333333;
		background-color: #F9F9F9;
	}
	
	.input:focus, .textarea:focus {
		border-color: #FF7A45;
		outline: none;
		background-color: #FFFFFF;
	}
	
	.textarea {
		height: 80px;
		resize: none;
		line-height: 1.5;
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
