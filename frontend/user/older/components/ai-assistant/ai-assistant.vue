<template>
	<view class="ai-assistant-container" v-if="visible">
		<!-- 聊天界面 -->
		<view class="chat-window" :style="chatWindowStyle">
			<!-- 顶部栏 -->
			<view class="chat-header" @touchstart="onTouchStart" @touchmove="onTouchMove" @touchend="onTouchEnd">
				<image class="ai-avatar" src="/static/robot.png" mode="aspectFit"></image>
				<text class="ai-name">智能助手</text>
				<text class="new-chat-btn" @click.stop="newChat">🆕</text>
				<text class="history-btn" @click.stop="toggleHistory">📋</text>
				<text class="minimize-btn" @click.stop="toggleMinimize">{{ isMinimized ? '+' : '−' }}</text>
				<text class="close-btn" @click.stop="closeAssistant">✕</text>
			</view>
			
			<!-- 聊天区域 -->
			<scroll-view v-if="!isMinimized && !showHistory" class="chat-messages" scroll-y="true" show-scrollbar="false">
				<view v-if="loading" class="loading-container">
					<text class="loading-text">加载中...</text>
				</view>
				<view v-else>
					<view 
						v-for="message in messages" 
						:key="message.id"
						class="message-item"
						:class="{ 'ai-message': message.type === 'ai', 'user-message': message.type === 'user' }"
					>
						<view class="message-avatar-container">
							<text class="message-avatar">{{ message.type === 'ai' ? '🤖' : '👤' }}</text>
						</view>
						<view class="message-content">
							<text class="message-text">{{ message.content }}</text>
							<view class="message-footer">
								<text class="message-time">{{ message.time }}</text>
								<text
									v-if="message.type === 'ai'"
									class="play-voice-btn"
									@click="playVoiceWithRecord(message.content)"
								>🔊</text>
							</view>
						</view>
					</view>
					<!-- 实时识别结果显示 -->
					<view v-if="recognizingText" class="message-item user-message">
						<view class="message-avatar-container">
							<text class="message-avatar">👤</text>
						</view>
						<view class="message-content">
							<text class="message-text" style="opacity: 0.7;">{{ recognizingText }}</text>
							<view class="message-footer">
								<text class="message-time">{{ getCurrentTime() }}</text>
								<text class="recognizing-indicator">识别中...</text>
							</view>
						</view>
					</view>
				</view>
			</scroll-view>
			
			<!-- 历史记录列表 -->
			<scroll-view v-if="!isMinimized && showHistory" class="history-list" scroll-y="true" show-scrollbar="false">
				<view class="history-header">
					<text class="history-title">历史对话</text>
					<text class="history-close" @click="toggleHistory">✕</text>
				</view>
				<view v-if="historyLoading" class="history-loading">
					<text class="loading-text">加载历史记录...</text>
				</view>
				<view v-else-if="conversations.length === 0" class="history-empty">
					<text class="empty-text">暂无历史对话</text>
				</view>
				<view v-else class="history-items">
					<view 
						v-for="conv in conversations" 
						:key="conv.id"
						class="history-item"
						@click="loadConversation(conv)"
					>
						<view class="history-item-header">
							<text class="history-item-time">{{ formatConversationTime(conv.timestamp) }}</text>
						</view>
						<text class="history-item-content">{{ conv.user_query.substring(0, 30) }}{{ conv.user_query.length > 30 ? '...' : '' }}</text>
						<text class="history-item-reply">{{ conv.ai_response.substring(0, 20) }}{{ conv.ai_response.length > 20 ? '...' : '' }}</text>
					</view>
				</view>
			</scroll-view>
			
			<!-- 输入区域 -->
			<view v-if="!isMinimized" class="chat-input">
				<input 
					class="input-normal" 
					placeholder="请输入您的问题..." 
					v-model="inputText"
					@confirm="sendMessage"
				/>
				<view class="input-actions">
					<text class="voice-btn" :class="{ recording: voiceMode }" @click="toggleVoice">{{ voiceMode ? '⏹️' : '🎤' }}</text>
					<button 
						class="send-btn" 
						@click="sendMessage"
						:disabled="!inputText.trim() || sending"
					>{{ sending ? '发送中...' : '发送' }}</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import api from '../../utils/api.js'
	import CONFIG from '../../utils/config.js'
	import SpeechTranscription from '../../utils/st.js'
	import SpeechSynthesizer from '../../utils/tts.js'
	
	// 阿里云配置（从后端获取）
	let aliyunConfig = {
		token: null,
		appkey: null,
		expireTime: null
	}
	
	// 获取阿里云Token
	async function getAliyunToken() {
		// 检查Token是否过期（提前5分钟刷新）
		if (aliyunConfig.token && aliyunConfig.expireTime) {
			const expireTime = new Date(aliyunConfig.expireTime)
			const now = new Date()
			if (expireTime - now > 5 * 60 * 1000) {
				return aliyunConfig
			}
		}
		
		try {
			const result = await api.older.getAliyunToken()
			if (result.success) {
				aliyunConfig.token = result.token
				aliyunConfig.appkey = result.appkey
				aliyunConfig.expireTime = result.expire_time
				return aliyunConfig
			}
		} catch (error) {
			console.error('获取阿里云Token失败:', error)
			throw error
		}
	}
	
	export default {
		name: 'ai-assistant',
		data() {
			return {
				visible: false,
				messages: [],
				inputText: '',
				voiceMode: false,
				loading: false,
				sending: false,
				// 拖拽相关数据
				isDragging: false,
				startX: 0,
				startY: 0,
				offsetX: 0,
				offsetY: 0,
				positionX: 50,
				positionY: 150,
				// 窗口状态
				isMinimized: false,
				// 历史记录相关
				showHistory: false,
				conversations: [],
				historyLoading: false,
				// 阿里云语音识别相关
				stInstance: null,
				recognizingText: '',
				finalRecognizedText: '',
				// 阿里云语音合成相关
				ttsInstance: null,
				isPlaying: false
			}
		},
		computed: {
			chatWindowStyle() {
				if (this.isMinimized) {
					return {
						left: `${this.positionX}px`,
						top: `${this.positionY}px`,
						height: '60px',
						width: '200px',
						borderRadius: '30px'
					}
				}
				return {
					left: `${this.positionX}px`,
					top: `${this.positionY}px`
				}
			}
		},
		mounted() {
		// 初始化录音管理器（只初始化一次）
		this.initRecorderManager()
		// 加载历史对话记录
		this.loadConversationsList()
	},
		methods: {
			initRecorderManager() {
				// 初始化录音管理器
				this.recorderManager = wx.getRecorderManager()
				
				// 录音帧回调 - 实时发送音频数据
				this.recorderManager.onFrameRecorded((res) => {
					if (res.isLastFrame) {
						console.log('录音结束帧')
					}
					if (this.stInstance && this.voiceMode && res.frameBuffer) {
						// 处理音频数据
						let audioData = res.frameBuffer
						
						// 如果是 Uint8Array，转换为 ArrayBuffer
						if (audioData instanceof Uint8Array) {
							audioData = audioData.buffer
						}
						
						// 检查是否有 byteLength 属性（ArrayBuffer 的特征）
						if (audioData && typeof audioData.byteLength === 'number') {
							// 检查数据是否为空（全0）
							const view = new Uint8Array(audioData)
							let sum = 0
							for (let i = 0; i < Math.min(view.length, 100); i++) {
								sum += view[i]
							}
							console.log('发送音频数据:', audioData.byteLength, '前100字节总和:', sum)
							this.stInstance.sendAudio(audioData)
						} else {
							console.log('音频数据格式不正确:', typeof audioData, audioData)
						}
					}
				})
				
				this.recorderManager.onStart(() => {
					console.log('录音开始')
				})
				
				this.recorderManager.onStop(async (res) => {
					console.log('录音停止:', res)
					// 关闭语音识别连接
					if (this.stInstance) {
						try {
							await this.stInstance.close()
						} catch (e) {
							console.log('语音识别关闭:', e)
						}
					}
					// 清理临时文件
					if (res.tempFilePath) {
						wx.removeSavedFile({
							filePath: res.tempFilePath,
							complete: () => {}
						})
					}
				})
				
				this.recorderManager.onError((err) => {
					console.error('录音错误:', err)
					uni.showToast({
						title: '录音失败，请重试',
						icon: 'none'
					})
				})
			},
			async open() {
				this.visible = true;
				this.isMinimized = false;
				await this.loadConversations()
			},
			closeAssistant() {
			this.visible = false;
		},
		toggleMinimize() {
			this.isMinimized = !this.isMinimized
		},
		newChat() {
			// 清空当前消息
			this.messages = [
				{
					id: 1,
					type: 'ai',
					content: '我可以帮您推荐适合的餐品、解答饮食问题，或者协助您点餐。',
					time: this.getCurrentTime()
				}
			]
			// 清空输入框
			this.inputText = ''
			// 隐藏历史记录列表
			this.showHistory = false
		},
		toggleHistory() {
			this.showHistory = !this.showHistory
			if (this.showHistory) {
				this.loadConversationsList()
			}
		},
		async loadConversationsList() {
			this.historyLoading = true
			try {
				const response = await api.older.getAIConversations()
				if (response.conversations && response.conversations.length > 0) {
					this.conversations = response.conversations
				} else {
					this.conversations = []
				}
			} catch (error) {
				console.error('加载历史对话列表失败:', error)
				this.conversations = []
			} finally {
				this.historyLoading = false
			}
		},
		loadConversation(conv) {
			// 隐藏历史记录列表
			this.showHistory = false
			// 清空当前消息
			this.messages = []
			// 添加对话历史到消息列表
			const timestamp = new Date(conv.timestamp)
			// 添加用户消息
			this.messages.push({
				id: conv.id,
				type: 'user',
				content: conv.user_query,
				time: this.formatTime(timestamp)
			})
			// 添加AI回复消息
			this.messages.push({
				id: conv.id + 1,
				type: 'ai',
				content: conv.ai_response,
				time: this.formatTime(timestamp)
			})
		},
		formatConversationTime(timestamp) {
			const date = new Date(timestamp)
			const year = date.getFullYear()
			const month = (date.getMonth() + 1).toString().padStart(2, '0')
			const day = date.getDate().toString().padStart(2, '0')
			const hours = date.getHours().toString().padStart(2, '0')
			const minutes = date.getMinutes().toString().padStart(2, '0')
			return `${year}-${month}-${day} ${hours}:${minutes}`
		},
			async toggleVoice() {
				if (!this.voiceMode) {
					// 开始语音输入
					this.startVoiceRecognition()
				} else {
					// 停止语音输入
					this.stopVoiceRecognition()
				}
			},
			
			async startVoiceRecognition() {
				try {
					// 获取阿里云Token
					let config
					try {
						config = await getAliyunToken()
					} catch (error) {
						uni.showToast({
							title: '语音识别服务未配置',
							icon: 'none',
							duration: 3000
						})
						console.error('获取阿里云Token失败:', error)
						return
					}
					
					// 检查是否支持录音
					if (!wx || !wx.getRecorderManager) {
						uni.showToast({
							title: '当前环境不支持语音功能',
							icon: 'none'
						})
						return
					}
					
					uni.showLoading({
						title: '正在准备...',
						mask: true
					})
					
					// 先检查权限状态
					wx.getSetting({
						success: (res) => {
							console.log('权限设置:', res.authSetting)
							if (!res.authSetting['scope.record']) {
								// 没有权限，请求授权
								wx.authorize({
									scope: 'scope.record',
									success: () => {
										console.log('获取录音权限成功')
										this.initAliyunST()
									},
									fail: (err) => {
										console.error('获取录音权限失败:', err)
										uni.hideLoading()
										uni.showModal({
											title: '权限提示',
											content: '需要录音权限才能使用语音识别功能，请在设置中开启麦克风权限',
											showCancel: true,
											confirmText: '去设置',
											cancelText: '取消',
											success: (res) => {
												if (res.confirm) {
													wx.openSetting()
												}
											}
										})
									}
								})
							} else {
								// 已经有权限，直接开始
								console.log('已经有录音权限')
								this.initAliyunST()
							}
						},
						fail: (err) => {
							console.error('获取权限设置失败:', err)
							uni.hideLoading()
							uni.showToast({
								title: '权限检查失败',
								icon: 'none'
							})
						}
					})
				} catch (error) {
					console.error('语音识别初始化失败:', error)
					uni.hideLoading()
					uni.showToast({
						title: '语音识别功能暂时不可用',
						icon: 'none'
					})
				}
			},
			
			async initAliyunST() {
				try {
					// 获取阿里云Token
					const config = await getAliyunToken()
					console.log('获取阿里云Token成功')
					
					// 创建语音识别实例
					this.stInstance = new SpeechTranscription({
						url: 'wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1',
						token: config.token,
						appkey: config.appkey
					})
					
					// 设置事件回调
					this.stInstance.on('started', (msg) => {
						console.log('语音识别开始:', msg)
						this.voiceMode = true
						this.recognizingText = ''
						this.finalRecognizedText = ''
						uni.hideLoading()
						uni.showToast({
							title: '正在录音，请说话...',
							icon: 'none',
							duration: 2000
						})
						
						// 收到 started 事件后再开始录音
						console.log('开始录音...')
						this.recorderManager.start({
							duration: 60000,
							sampleRate: 16000,
							numberOfChannels: 1,
							encodeBitRate: 48000,
							format: 'pcm',  // 阿里云需要PCM格式
							frameSize: 4    // 每帧4KB，用于实时回调
						})
					})
					
					// 存储最终识别结果
					let finalResult = ''
					let lastRecognizedText = ''  // 用于保存最后一次识别到的文本
					
					this.stInstance.on('changed', (msg) => {
						console.log('========== changed事件 ==========')
						console.log('原始消息:', msg)
						// 解析识别结果
						try {
							const msgObj = JSON.parse(msg)
							console.log('解析后的对象:', msgObj)
							console.log('header:', msgObj.header)
							console.log('payload:', msgObj.payload)
							if (msgObj.payload && msgObj.payload.result) {
								this.recognizingText = msgObj.payload.result
								lastRecognizedText = msgObj.payload.result  // 保存最后一次识别结果
								console.log('✓ 实时识别结果:', lastRecognizedText)
							} else {
								console.log('✗ payload 或 result 不存在')
								// 尝试其他可能的路径
								if (msgObj.result) {
									console.log('找到 msgObj.result:', msgObj.result)
									lastRecognizedText = msgObj.result
								}
							}
						} catch (e) {
							console.log('✗ 解析失败:', e)
							this.recognizingText = msg
						}
						console.log('========== changed事件结束 ==========')
					})
					
					this.stInstance.on('begin', (msg) => {
						console.log('句子开始:', msg)
					})
					
					this.stInstance.on('end', (msg) => {
						console.log('========== 句子结束事件触发 ==========')
						console.log('原始消息:', msg)
						// 解析最终识别结果
						try {
							const msgObj = JSON.parse(msg)
							console.log('解析后的对象:', msgObj)
							console.log('payload:', msgObj.payload)
							if (msgObj.payload && msgObj.payload.result) {
								finalResult = msgObj.payload.result
								console.log('✓ 句子识别结果:', finalResult)
							} else {
								console.log('✗ payload 或 result 不存在')
							}
						} catch (e) {
							console.log('✗ 解析失败:', e)
						}
						console.log('========== 句子结束处理完成 ==========')
					})
					
					this.stInstance.on('completed', async (msg) => {
						console.log('识别完成:', msg)
						// 使用句子结束时的识别结果，如果没有则使用最后一次实时识别结果
						let resultToSend = finalResult || lastRecognizedText
						console.log('最终识别结果:', finalResult)
						console.log('最后一次实时识别:', lastRecognizedText)
						console.log('实际发送:', resultToSend)
						
						// 清理状态
						this.recognizingText = ''
						this.voiceMode = false
						
						// 如果有识别结果，直接发送
						if (resultToSend && resultToSend.trim()) {
							uni.showToast({
								title: '语音识别成功',
								icon: 'success'
							})
							
							// 添加用户消息到聊天记录
							const userMessage = {
								id: Date.now(),
								type: 'user',
								content: resultToSend,
								time: this.getCurrentTime()
							}
							this.messages.push(userMessage)
							
							// 发送给AI获取回复
							this.sending = true
							try {
								const response = await api.older.sendAIQuery({ query: resultToSend })
								
								const aiReply = {
									id: Date.now() + 1,
									type: 'ai',
									content: response.response,
									time: this.getCurrentTime()
								}
								this.messages.push(aiReply)
								
								// 自动播放AI回复（如果配置了TTS）
								this.playVoice(response.response)
							} catch (error) {
								console.error('发送AI查询失败:', error)
								const errorReply = {
									id: Date.now() + 1,
									type: 'ai',
									content: '抱歉，服务暂时不可用，请稍后再试。',
									time: this.getCurrentTime()
								}
								this.messages.push(errorReply)
							} finally {
								this.sending = false
							}
						} else {
							uni.showToast({
								title: '未识别到语音',
								icon: 'none'
							})
						}
						
						// 清空识别结果
						finalResult = ''
						lastRecognizedText = ''
					})
					
					this.stInstance.on('closed', () => {
						console.log('连接关闭')
						this.voiceMode = false
						this.recognizingText = ''
					})
					
					this.stInstance.on('failed', (msg) => {
						console.error('识别失败:', msg)
						this.voiceMode = false
						this.recognizingText = ''
						uni.showToast({
							title: '语音识别失败: ' + msg,
							icon: 'none',
							duration: 3000
						})
					})
					
					// 开始语音识别
					const params = this.stInstance.defaultStartParams()
					console.log('语音识别参数:', params)
					const startResult = await this.stInstance.start(params)
					console.log('语音识别启动结果:', startResult)
					
					// 注意：录音在 'started' 事件中开始
					// 确保收到 started 事件后再发送音频数据
					
				} catch (error) {
					console.error('初始化阿里云语音识别失败:', error)
					uni.hideLoading()
					uni.showToast({
						title: '语音识别初始化失败',
						icon: 'none'
					})
				}
			},
			
			async stopVoiceRecognition() {
				// 先设置标志位，防止 onStop 事件重复关闭
				this.voiceMode = false
				this.recognizingText = ''
				
				// 停止录音
				if (this.recorderManager) {
					this.recorderManager.stop()
				}
				
				// 注意：语音识别关闭在 onStop 事件中处理
				// 避免重复调用 close()
			},
			
			async playVoiceWithRecord(text) {
				// 先调用后端API创建语音合成记录
				try {
					console.log('创建语音合成记录:', text.substring(0, 50) + '...')
					await api.older.textToSpeech({
						text: text,
						voice_type: 'elderly',
						language: 'zh_CN',
						speed: 0.8
					})
					console.log('语音合成记录创建成功')
				} catch (error) {
					console.error('创建语音合成记录失败:', error)
					// 即使记录创建失败，也继续播放语音
				}

				// 然后播放语音
				await this.playVoice(text)
			},

			async playVoice(text) {
				// 获取阿里云Token
				let config
				try {
					config = await getAliyunToken()
				} catch (error) {
					console.log('TTS未配置，跳过语音播放')
					return
				}

				// 如果正在播放，先停止
				if (this.isPlaying) {
					this.stopVoice()
					return
				}

				try {
					uni.showLoading({
						title: '正在合成语音...',
						mask: true
					})

					// 创建TTS实例
					this.ttsInstance = new SpeechSynthesizer({
						url: 'wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1',
						token: config.token,
						appkey: config.appkey
					})

					// 用于存储音频数据
					const audioChunks = []

					// 设置回调
					this.ttsInstance.on('data', (msg) => {
						console.log(`接收音频数据: ${msg.byteLength} bytes`)
						audioChunks.push(msg)
					})

					this.ttsInstance.on('completed', async (msg) => {
						console.log('语音合成完成:', msg)
						uni.hideLoading()

						// 合并音频数据
						const totalLength = audioChunks.reduce((sum, chunk) => sum + chunk.byteLength, 0)
						const combinedAudio = new Uint8Array(totalLength)
						let offset = 0
						audioChunks.forEach(chunk => {
							combinedAudio.set(new Uint8Array(chunk), offset)
							offset += chunk.byteLength
						})

						// 保存为临时文件
						const fs = wx.getFileSystemManager()
						const fileName = `tts_${Date.now()}.wav`
						const filePath = `${wx.env.USER_DATA_PATH}/${fileName}`

						try {
							fs.writeFileSync(filePath, combinedAudio.buffer, 'binary')

							// 播放音频
							this.isPlaying = true
							const audio = uni.createInnerAudioContext()
							audio.src = filePath
							audio.play()

							// 监听播放完成
							audio.onEnded(() => {
								console.log('语音播放完成')
								this.isPlaying = false
								audio.destroy()
								// 删除临时文件
								fs.unlink({
									filePath: filePath,
									complete: () => {}
								})
							})

							// 监听播放错误
							audio.onError((err) => {
								console.error('语音播放错误', err)
								this.isPlaying = false
								audio.destroy()
								fs.unlink({
									filePath: filePath,
									complete: () => {}
								})
								uni.showToast({
									title: '语音播放失败',
									icon: 'none'
								})
							})
						} catch (e) {
							console.error('保存音频文件失败:', e)
							this.isPlaying = false
							uni.showToast({
								title: '语音播放失败',
								icon: 'none'
							})
						}
					})

					this.ttsInstance.on('failed', (msg) => {
						console.error('语音合成失败:', msg)
						uni.hideLoading()
						this.isPlaying = false
						uni.showToast({
							title: '语音合成失败',
							icon: 'none'
						})
					})


					const params = this.ttsInstance.defaultStartParams('zhiyuan') // 当前使用：小云（标准女声）
					params.text = text
					params.volume = 50      // 音量 0-100
					params.speech_rate = 0  // 语速 -500~500
					params.pitch_rate = 0   // 音调 -500~500

					await this.ttsInstance.start(params)

				} catch (error) {
					console.error('语音合成失败', error)
					uni.hideLoading()
					this.isPlaying = false
					uni.showToast({
						title: '语音合成失败',
						icon: 'none'
					})
				}
			},
			
			stopVoice() {
				if (this.ttsInstance) {
					this.ttsInstance.shutdown()
					this.ttsInstance = null
				}
				this.isPlaying = false
			},
			async loadConversations() {
				this.loading = true
				try {
					const response = await api.older.getAIConversations()
					if (response.conversations && response.conversations.length > 0) {
						const messageList = []
						response.conversations.forEach(conv => {
							const timestamp = new Date(conv.timestamp)
							// 添加用户消息
							messageList.push({
								id: conv.id,
								type: 'user',
								content: conv.user_query,
								time: this.formatTime(timestamp)
							})
							// 添加AI回复消息
							messageList.push({
								id: conv.id + 1,
								type: 'ai',
								content: conv.ai_response,
								time: this.formatTime(timestamp)
							})
						})
						this.messages = messageList
					} else {
						// 添加欢迎消息
						this.messages = [
							{
								id: 1,
								type: 'ai',
								content: '您好！我是您的智能助手，有什么可以帮助您的吗？',
								time: this.getCurrentTime()
							},
							{
								id: 2,
								type: 'ai',
								content: '我可以帮您推荐适合的餐品、解答饮食问题，或者协助您点餐。',
								time: this.getCurrentTime()
							}
						]
					}
				} catch (error) {
					console.error('加载对话历史失败:', error)
					// 添加欢迎消息
					this.messages = [
						{
							id: 1,
							type: 'ai',
							content: '您好！我是您的智能助手，有什么可以帮助您的吗？',
							time: this.getCurrentTime()
						},
						{
							id: 2,
							type: 'ai',
							content: '我可以帮您推荐适合的餐品、解答饮食问题，或者协助您点餐。',
							time: this.getCurrentTime()
						}
					]
				} finally {
					this.loading = false
				}
			},
			async sendMessage() {
				if (!this.inputText.trim()) {
					return
				}
				
				// 添加用户消息
				const userMessage = {
					id: Date.now(),
					type: 'user',
					content: this.inputText,
					time: this.getCurrentTime()
				}
				this.messages.push(userMessage)
				
				// 清空输入框
				const tempText = this.inputText
				this.inputText = ''
				
				this.sending = true
				try {
					// 检查是否为点餐请求
					console.log('检查点餐请求:', tempText)
					if (this.isOrderRequest(tempText)) {
						console.log('识别为点餐请求')
						// 处理点餐请求
						await this.handleOrderRequest(tempText)
					} else {
						console.log('识别为普通请求')
						// 普通AI查询
						const response = await api.older.sendAIQuery({ query: tempText })
						
						const aiReply = {
							id: Date.now() + 1,
							type: 'ai',
							content: response.response,
							time: this.getCurrentTime()
						}
						this.messages.push(aiReply)
					}
				} catch (error) {
					console.error('处理请求失败:', error)
					const errorReply = {
						id: Date.now() + 1,
						type: 'ai',
						content: '抱歉，服务暂时不可用，请稍后再试。',
						time: this.getCurrentTime()
					}
					this.messages.push(errorReply)
				} finally {
					this.sending = false
				}
			},
			// 检查是否为点餐请求
			isOrderRequest(text) {
				const orderKeywords = ['点', '要', '订', '买', '来一份', '帮我', '我要']
				const foodKeywords = ['餐', '饭', '菜', '面', '粥', '粉', '汤', '套餐', '鱼', '肉', '蛋', '蔬菜']
				
				// 不需要转换为小写，因为是中文
				const containsOrderKeyword = orderKeywords.some(keyword => text.includes(keyword))
				const containsFoodKeyword = foodKeywords.some(keyword => text.includes(keyword))
				console.log('点餐关键词检测:', { text, containsOrderKeyword, containsFoodKeyword })
				
				return containsOrderKeyword && containsFoodKeyword
			},
			// 处理点餐请求
			async handleOrderRequest(text) {
				try {
					// 解析餐品信息
					console.log('处理点餐请求:', text)
					const mealName = this.extractMealName(text)
					console.log('提取餐品名称:', mealName)
					if (!mealName) {
						const errorReply = {
							id: Date.now() + 1,
							type: 'ai',
							content: '抱歉，我没有理解您要订的餐品，请您再说一遍具体的餐品名称。',
							time: this.getCurrentTime()
						}
						this.messages.push(errorReply)
						return
					}
					
					// 搜索餐品 - 不带参数获取所有餐品，然后在前端过滤
					console.log('搜索餐品:', mealName)
					const meals = await api.older.getMeals()
					console.log('搜索结果:', meals)
					
					// 在前端过滤餐品
					const filteredMeals = meals.items.filter(meal => 
						meal.name.includes(mealName)
					)
					console.log('过滤后的餐品:', filteredMeals)
					
					if (!filteredMeals || filteredMeals.length === 0) {
						const errorReply = {
							id: Date.now() + 1,
							type: 'ai',
							content: `抱歉，没有找到"${mealName}"相关的餐品，请您尝试其他餐品。`,
							time: this.getCurrentTime()
						}
						this.messages.push(errorReply)
						return
					}
					
					// 选择第一个匹配的餐品
					const selectedMeal = filteredMeals[0]
					console.log('选择餐品:', selectedMeal)
					
					// 创建订单
					const orderData = {
						items: [{
							meal_id: selectedMeal.id,
							quantity: 1
						}],
						delivery_address: '默认地址', // 这里可以从用户信息中获取
						special_notes: ''
					}
					console.log('创建订单数据:', orderData)
					
					const order = await api.older.createOrder(orderData)
					console.log('订单创建成功:', order)
					
					// 生成AI回复
					const aiReply = {
						id: Date.now() + 1,
						type: 'ai',
						content: `已为您成功下单：${selectedMeal.name}，价格：¥${selectedMeal.price}。订单号：${order.id}。`,
						time: this.getCurrentTime()
					}
					this.messages.push(aiReply)
					
					// 自动播放AI回复
					this.playVoice(aiReply.content)
				} catch (error) {
					console.error('点餐失败:', error)
					const errorReply = {
						id: Date.now() + 1,
						type: 'ai',
						content: '抱歉，点餐失败，请稍后再试。',
						time: this.getCurrentTime()
					}
					this.messages.push(errorReply)
				}
			},
			// 提取餐品名称
			extractMealName(text) {
				// 简单的餐品名称提取逻辑
				// 这里可以根据实际情况进行更复杂的自然语言处理
				const orderKeywords = ['点', '要', '订', '买', '来一份', '帮我', '我要']
				let cleanedText = text
				
				console.log('原始文本:', text)
				
				// 移除点餐关键词
				orderKeywords.forEach(keyword => {
					if (cleanedText.includes(keyword)) {
						console.log('移除关键词:', keyword)
						cleanedText = cleanedText.replace(keyword, '')
					}
				})
				
				console.log('移除关键词后:', cleanedText)
				
				// 不移除末尾的餐品类型词，因为小米粥、清蒸鱼等都包含类型词
				// 移除多余的空格
				cleanedText = cleanedText.trim()
				
				console.log('提取的餐品名称:', cleanedText)
				return cleanedText
			},
			getCurrentTime() {
				return this.formatTime(new Date())
			},
			formatTime(date) {
				const hours = date.getHours().toString().padStart(2, '0')
				const minutes = date.getMinutes().toString().padStart(2, '0')
				return `${hours}:${minutes}`
			},
			// 拖拽功能
			onTouchStart(e) {
				this.isDragging = true
				this.startX = e.touches[0].clientX
				this.startY = e.touches[0].clientY
				this.offsetX = this.positionX
				this.offsetY = this.positionY
			},
			onTouchMove(e) {
				if (!this.isDragging) return
				
				const deltaX = e.touches[0].clientX - this.startX
				const deltaY = e.touches[0].clientY - this.startY
				
				this.positionX = this.offsetX + deltaX
				this.positionY = this.offsetY + deltaY
				
				// 限制在屏幕内
				const windowWidth = uni.getSystemInfoSync().windowWidth
				const windowHeight = uni.getSystemInfoSync().windowHeight
				const width = this.isMinimized ? 200 : 300
				const height = this.isMinimized ? 60 : 400
				
				this.positionX = Math.max(0, Math.min(this.positionX, windowWidth - width))
				this.positionY = Math.max(0, Math.min(this.positionY, windowHeight - height))
			},
			onTouchEnd() {
				this.isDragging = false
			}
		}
	}
</script>

<style scoped>
	.ai-assistant-container {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 9999;
		pointer-events: none;
	}
	
	/* 聊天窗口 */
	.chat-window {
		position: absolute;
		width: 320px;
		height: 420px;
		background: linear-gradient(180deg, #FFF8F4 0%, #FFFFFF 150px, #FFFFFF 100%);
		border-radius: 24px;
		display: flex;
		flex-direction: column;
		box-shadow: 0 20px 45px rgba(0, 0, 0, 0.18);
		border: 1px solid rgba(255, 122, 69, 0.15);
		pointer-events: auto;
		transition: width 0.3s, height 0.3s, border-radius 0.3s;
		overflow: hidden;
	}

	/* 顶部栏 */
	.chat-header {
		display: flex;
		align-items: center;
		padding: 16px 20px;
		border-bottom: 1px solid rgba(255, 122, 69, 0.1);
		background: rgba(255, 255, 255, 0.75);
		backdrop-filter: blur(8px);
		cursor: move;
	}

	.ai-avatar {
		width: 28px;
		height: 28px;
		margin-right: 12px;
	}
	
	.ai-name {
		font-size: 19px;
		font-weight: 600;
		color: #FF7A45;
		flex: 1;
		white-space: nowrap;
	}
	
	.minimize-btn {
			font-size: 20px;
			color: #666666;
			width: 28px;
			height: 28px;
			line-height: 28px;
			text-align: center;
			background: rgba(245, 245, 245, 0.9);
			border-radius: 14px;
			margin-right: 8px;
			cursor: pointer;
		}
		
		.new-chat-btn {
			font-size: 20px;
			color: #666666;
			width: 28px;
			height: 28px;
			line-height: 28px;
			text-align: center;
			background: rgba(245, 245, 245, 0.9);
			border-radius: 14px;
			margin-right: 8px;
			cursor: pointer;
		}
		
		.history-btn {
			font-size: 20px;
			color: #666666;
			width: 28px;
			height: 28px;
			line-height: 28px;
			text-align: center;
			background: rgba(245, 245, 245, 0.9);
			border-radius: 14px;
			margin-right: 8px;
			cursor: pointer;
		}
	
	.close-btn {
		font-size: 22px;
		color: #666666;
		width: 32px;
		height: 32px;
		line-height: 32px;
		text-align: center;
		background: rgba(245, 245, 245, 0.9);
		border-radius: 16px;
		cursor: pointer;
	}
	
	/* 聊天区域 */
	.chat-messages {
		flex: 1;
		padding: 24px 20px 24px 10px;
		overflow-y: auto;
		height: 0; /* 配合flex:1在scroll-view中生效 */
	}
	
	.chat-messages::-webkit-scrollbar {
		width: 6px;
	}
	
	.chat-messages::-webkit-scrollbar-track {
		background: rgba(0, 0, 0, 0.05);
		border-radius: 3px;
	}
	
	.chat-messages::-webkit-scrollbar-thumb {
		background: rgba(255, 122, 69, 0.3);
		border-radius: 3px;
	}
	
	.chat-messages::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 122, 69, 0.5);
	}
	
	.message-item {
		display: flex;
		margin-bottom: 24px;
		align-items: flex-start;
		width: 100%;
	}
	
	.message-item.ai-message {
		flex-direction: row;
	}
	
	.message-item.user-message {
		flex-direction: row-reverse;
	}
	
	.message-avatar-container {
		flex-shrink: 0;
		margin: 0 12px;
		z-index: 1;
	}
	
	.message-item.ai-message .message-avatar-container {
		margin-left: 0;
		margin-right: 12px;
	}
	
	.message-item.user-message .message-avatar-container {
		margin-left: 12px;
		margin-right: 0;
	}
	
	.message-avatar {
		font-size: 24px;
	}
	
	.message-content {
		max-width: 75%;
	}
	
	.message-text {
		display: block;
		padding: 14px 18px;
		border-radius: 18px;
		font-size: 14px;
		line-height: 1.6;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
		word-break: break-all;
	}
	
	.message-item.ai-message .message-text {
		background: #fff;
		color: #333333;
		border-top-left-radius: 8px;
		border: 1px solid rgba(255, 122, 69, 0.08);
	}
	
	.message-item.user-message .message-text {
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border-top-right-radius: 8px;
		box-shadow: 0 6px 16px rgba(255, 122, 69, 0.25);
	}
	
	.message-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: 6px;
	}
	
	.message-time {
		font-size: 11px;
		color: #999999;
	}
	
	.play-voice-btn {
		font-size: 14px;
		color: #409EFF;
		cursor: pointer;
		transition: all 0.3s;
	}
	
	.play-voice-btn:hover {
		color: #66B1FF;
		transform: scale(1.1);
	}
	
	.play-voice-btn:active {
		color: #3370B7;
		transform: scale(0.95);
	}
	
	/* 识别中指示器 */
	.recognizing-indicator {
		font-size: 11px;
		color: #FF7A45;
		animation: blink 1s infinite;
	}
	
	@keyframes blink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.5; }
	}
	
	/* 加载状态 */
	.loading-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
	}
	
	.loading-text {
		font-size: 14px;
		color: #999999;
	}
	
	/* 输入区域 */
	.chat-input {
		display: flex;
		align-items: center;
		padding: 18px 20px;
		border-top: 1px solid rgba(255, 122, 69, 0.1);
		background: rgba(255, 255, 255, 0.92);
	}
	
	.input-normal {
		flex: 1;
		height: 44px;
		margin-right: 14px;
		border-radius: 22px;
		border: 1px solid rgba(255, 122, 69, 0.2);
		background: #fff;
		padding: 0 18px;
		font-size: 14px;
	}
	
	.input-normal:focus {
		border-color: #FF7A45;
		box-shadow: 0 0 0 2px rgba(255, 122, 69, 0.1);
	}
	
	.input-actions {
		display: flex;
		align-items: center;
		gap: 14px;
	}
	
	.voice-btn {
		font-size: 24px;
		color: #409EFF;
		width: 40px;
		height: 40px;
		line-height: 40px;
		text-align: center;
		background: rgba(64, 158, 255, 0.15);
		border-radius: 20px;
		transition: all 0.3s;
	}
	
	.voice-btn:active {
		background: rgba(64, 158, 255, 0.25);
	}

	.voice-btn.recording {
		background: rgba(245, 108, 108, 0.2);
		color: #F56C6C;
		animation: pulse 1s infinite;
	}
	
	@keyframes pulse {
		0% {
			box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.7);
		}
		70% {
			box-shadow: 0 0 0 10px rgba(245, 108, 108, 0);
		}
		100% {
			box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
		}
	}
	
	.send-btn {
		padding: 0 20px;
		height: 40px;
		line-height: 40px;
		background: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		color: white;
		border: none;
		border-radius: 20px;
		font-size: 14px;
		font-weight: 600;
		box-shadow: 0 6px 16px rgba(255, 122, 69, 0.25);
		margin: 0;
	}
	
	.send-btn:active {
		box-shadow: 0 4px 12px rgba(255, 122, 69, 0.2);
	}
	
	.send-btn:disabled {
				background: #CCCCCC;
				color: #FFFFFF;
				box-shadow: none;
			}
			
			/* 历史记录列表 */
			.history-list {
				flex: 1;
				padding: 0;
				overflow-y: auto;
				height: 0; /* 配合flex:1在scroll-view中生效 */
			}
			
			.history-header {
				display: flex;
				justify-content: space-between;
				align-items: center;
				padding: 16px 20px;
				border-bottom: 1px solid rgba(255, 122, 69, 0.1);
				background: rgba(255, 255, 255, 0.75);
				backdrop-filter: blur(8px);
			}
			
			.history-title {
				font-size: 16px;
				font-weight: 600;
				color: #333333;
			}
			
			.history-close {
				font-size: 20px;
				color: #666666;
				cursor: pointer;
			}
			
			.history-loading {
				display: flex;
				justify-content: center;
				align-items: center;
				height: 200px;
			}
			
			.history-empty {
				display: flex;
				justify-content: center;
				align-items: center;
				height: 200px;
			}
			
			.empty-text {
				font-size: 14px;
				color: #999999;
			}
			
			.history-items {
				padding: 10px;
			}
			
			.history-item {
				background: #FFFFFF;
				border-radius: 12px;
				padding: 14px;
				margin-bottom: 10px;
				box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
				cursor: pointer;
				transition: all 0.3s;
			}
			
			.history-item:hover {
				box-shadow: 0 4px 12px rgba(255, 122, 69, 0.15);
				transform: translateY(-2px);
			}
			
			.history-item-header {
				margin-bottom: 8px;
			}
			
			.history-item-time {
				font-size: 12px;
				color: #999999;
			}
			
			.history-item-content {
				display: block;
				font-size: 14px;
				color: #333333;
				font-weight: 500;
				margin-bottom: 6px;
				line-height: 1.4;
			}
			
			.history-item-reply {
				display: block;
				font-size: 13px;
				color: #666666;
				line-height: 1.3;
			}
		</style>
