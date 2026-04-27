<script>
	import { api } from './utils/api.js'
	
	export default {
		globalData: {
			currentLocation: null,
			isGettingLocation: false
		},
		
		onLaunch: function() {
			console.log('App Launch')
			// 检查用户是否已登录
			const token = uni.getStorageSync('token')
			if (token) {
				// 用户已登录，获取位置
				this.getCurrentLocation()
			}
			// 用户未登录时，不在onLaunch中获取位置
		},
		
		onShow: function() {
			console.log('App Show')
		},
		
		onHide: function() {
			console.log('App Hide')
		},
		
		methods: {
			/**
			 * 获取当前位置信息（全局方法）
			 */
			getCurrentLocation() {
				// 防止重复调用
				if (this.globalData.isGettingLocation) {
					console.log('全局位置获取已在进行中，跳过重复调用')
					return
				}
				
				this.globalData.isGettingLocation = true
				
				// 先请求位置权限
				uni.authorize({
					scope: 'scope.userLocation',
					success: () => {
						// 权限获取成功，获取位置
						uni.getLocation({
							type: 'gcj02', // 高德地图坐标系
							success: async (res) => {
								this.globalData.currentLocation = {
									latitude: res.latitude,
									longitude: res.longitude
								}
								
								// 调用API保存位置到数据库
								try {
									await api.location.updateLocation(res.latitude, res.longitude, res.accuracy || 0)
									console.log('全局位置保存成功')
								} catch (error) {
									console.error('全局位置保存失败:', error)
								}
							},
							fail: (error) => {
								console.error('全局获取位置失败:', error)
								uni.showToast({
									title: '位置获取失败',
									icon: 'none'
								})
							},
							complete: () => {
								this.globalData.isGettingLocation = false
							}
						})
					},
					fail: (error) => {
						console.error('位置权限请求失败:', error)
						// 权限被拒绝，引导用户去设置页面
						uni.showModal({
							title: '位置权限被拒绝',
							content: '配送功能需要获取您的位置信息。请在设置中开启位置权限。',
							confirmText: '去设置',
							cancelText: '取消',
							success: (res) => {
								if (res.confirm) {
									// 引导用户去设置页面
									uni.openSetting({
										success: (settingRes) => {
											console.log('设置页面返回:', settingRes)
											if (settingRes.authSetting['scope.userLocation']) {
												// 用户在设置中开启了权限，重新获取位置
												this.getCurrentLocation()
											}
										}
									})
								}
							}
						})
						this.globalData.isGettingLocation = false
					}
				})
			}
		}
	}
</script>

<style>
	/*每个页面公共css */
	
	/* 全局背景样式 - 适配所有页面（除登录页面） */
	page:not(.page-login) {
		background-color: #f0fdf4;
		background-image: 
			rgba(16, 185, 129, 0.1) 1px 0 0 0,
			rgba(16, 185, 129, 0.1) 0 1px 0 0;
		background-size: 20px 20px;
		min-height: 100vh;
	}
	
	/* 登录页面特殊背景 */
	.page-login {
		background: linear-gradient(135deg, #10b981 0%, #059669 100%);
	}
</style>
