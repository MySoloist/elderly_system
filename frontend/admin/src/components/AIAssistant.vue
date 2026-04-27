<template>
  <div 
    class="ai-assistant-container"
    :class="{ 'expanded': isExpanded, 'dragging': isDragging }"
    :style="containerStyle"
    @mousedown="startDrag"
  >
    <!-- 悬浮按钮 -->
    <div class="ai-assistant-button" @click="toggleExpanded">
      <el-icon size="24" color="#fff"><Cpu /></el-icon>
      <div v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</div>
    </div>
    
    <!-- AI助手面板 -->
    <div v-if="isExpanded" class="ai-assistant-panel glass-effect">
      <!-- 面板头部 -->
      <div class="panel-header">
        <div class="header-left">
          <el-icon size="20" color="#667eea"><Cpu /></el-icon>
          <span class="header-title">AI智能助手</span>
        </div>
        <div class="header-right">
          <el-button size="small" type="text" @click="clearChat">
            <el-icon><Delete /></el-icon>
          </el-button>
          <el-button size="small" type="text" @click="toggleExpanded">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </div>
      
      <!-- 聊天内容 -->
      <div class="chat-container" ref="chatContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          class="chat-message"
          :class="{ 'user-message': message.type === 'user', 'ai-message': message.type === 'ai' }"
        >
          <div class="message-avatar">
            <el-icon :size="24" :color="message.type === 'user' ? '#667eea' : '#764ba2'">
              <User v-if="message.type === 'user'" />
              <Cpu v-else />
            </el-icon>
          </div>
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>
        <div v-if="aiThinking" class="ai-thinking">
          <div class="thinking-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span>AI正在思考...</span>
        </div>
      </div>
      
      <!-- 输入框 -->
      <div class="input-container">
        <el-input
          v-model="inputMessage"
          placeholder="请输入您的问题..."
          @keyup.enter="sendMessage"
          :disabled="aiThinking"
        >
          <template #append>
            <el-button 
              type="primary" 
              @click="sendMessage"
              :loading="aiThinking"
            >
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>
      
      <!-- 快捷问题 -->
      <div class="quick-questions">
        <el-tag 
          v-for="(question, index) in quickQuestions" 
          :key="index"
          size="small"
          effect="plain"
          @click="sendQuickQuestion(question)"
        >
          {{ question }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Cpu, User, Delete, Close, ArrowRight } from '@element-plus/icons-vue'
import apiClient from '../api/axios'

const isExpanded = ref(false)
const aiThinking = ref(false)
const unreadCount = ref(0)
const inputMessage = ref('')
const chatContainer = ref(null)

// 拖拽相关
const isDragging = ref(false)
const startX = ref(0)
const startY = ref(0)
const currentX = ref(30)
const currentY = ref(30)

const containerStyle = ref({
  left: `${currentX.value}px`,
  top: `${currentY.value}px`
})

// 消息列表
const messages = ref([
  {
    type: 'ai',
    content: '您好！我是AI智能助手，有什么可以帮助您的吗？',
    time: new Date().toLocaleTimeString()
  }
])

// 快捷问题
const quickQuestions = [
  '如何添加新的配送员？',
  '系统有哪些快捷键？',
  '如何查看订单统计？',
  '常见问题解答'
]

// 切换展开/收起
const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
  if (isExpanded.value) {
    unreadCount.value = 0
    setTimeout(() => {
      scrollToBottom()
    }, 100)
  }
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || aiThinking.value) return
  
  const message = inputMessage.value.trim()
  inputMessage.value = ''
  
  // 添加用户消息
  messages.value.push({
    type: 'user',
    content: message,
    time: new Date().toLocaleTimeString()
  })
  
  scrollToBottom()
  
  // AI回复
  aiThinking.value = true
  try {
    const response = await apiClient.post('/admin/ai/query', {
      query: message
    })
    
    messages.value.push({
      type: 'ai',
      content: response.response,
      time: new Date().toLocaleTimeString()
    })
  } catch (error) {
    console.error('AI查询失败:', error)
    messages.value.push({
      type: 'ai',
      content: '抱歉，AI服务暂时不可用，请稍后再试。',
      time: new Date().toLocaleTimeString()
    })
  } finally {
    aiThinking.value = false
    scrollToBottom()
  }
}

// 发送快捷问题
const sendQuickQuestion = (question) => {
  inputMessage.value = question
  sendMessage()
}



// 清空聊天
const clearChat = () => {
  messages.value = [
    {
      type: 'ai',
      content: '您好！我是AI智能助手，有什么可以帮助您的吗？',
      time: new Date().toLocaleTimeString()
    }
  ]
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 拖拽功能
const startDrag = (event) => {
  if (event.target.closest('.ai-assistant-button')) {
    isDragging.value = true
    startX.value = event.clientX - currentX.value
    startY.value = event.clientY - currentY.value
    
    // 添加拖动时的视觉反馈
    document.body.style.cursor = 'grabbing'
    
    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', stopDrag)
    document.addEventListener('mouseleave', stopDrag)
  }
}

const onDrag = (event) => {
  if (isDragging.value) {
    // 使用requestAnimationFrame优化性能
    requestAnimationFrame(() => {
      currentX.value = event.clientX - startX.value
      currentY.value = event.clientY - startY.value
      
      // 平滑边界限制
      const buttonWidth = 60
      const buttonHeight = 60
      
      currentX.value = Math.max(0, Math.min(currentX.value, window.innerWidth - buttonWidth))
      currentY.value = Math.max(0, Math.min(currentY.value, window.innerHeight - buttonHeight))
      
      containerStyle.value = {
        left: `${currentX.value}px`,
        top: `${currentY.value}px`,
        transition: 'none' // 拖动时禁用过渡效果
      }
    })
  }
}

const stopDrag = () => {
  isDragging.value = false
  document.body.style.cursor = 'default'
  
  // 恢复过渡效果
  setTimeout(() => {
    containerStyle.value = {
      left: `${currentX.value}px`,
      top: `${currentY.value}px`,
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
    }
  }, 50)
  
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('mouseleave', stopDrag)
}

// 监听展开状态变化
watch(isExpanded, () => {
  if (isExpanded.value) {
    scrollToBottom()
  }
})

onMounted(() => {
  // 模拟收到新消息
  setTimeout(() => {
    unreadCount.value = 1
  }, 3000)
})
</script>

<style scoped>
.ai-assistant-container {
  position: fixed;
  z-index: 9999;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.ai-assistant-container.dragging {
  transition: none;
}

.ai-assistant-container.dragging .ai-assistant-button {
  transform: scale(1.2);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.8);
}

.ai-assistant-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  position: relative;
}

.ai-assistant-button:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
}

.ai-assistant-button:active {
  transform: scale(0.95);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.unread-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.ai-assistant-panel {
  position: absolute;
  bottom: 70px;
  right: 0;
  width: 350px;
  height: 450px;
  border-radius: 20px;
  background: var(--bg-secondary);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-primary);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-title {
  font-weight: 700;
  font-size: 16px;
  color: var(--text-primary);
}

.header-right {
  display: flex;
  gap: 8px;
}

.chat-container {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-message {
  display: flex;
  gap: 12px;
  animation: fadeIn 0.3s ease;
}

.user-message {
  flex-direction: row-reverse;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.user-message .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.message-text {
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.4;
}

.user-message .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-message .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  text-align: left;
}

.user-message .message-time {
  text-align: right;
}

.user-message .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.ai-thinking {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  border-bottom-left-radius: 4px;
  font-size: 14px;
  color: white;
}

.thinking-dots {
  display: flex;
  gap: 4px;
}

.thinking-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #667eea;
  animation: bounce 1.4s infinite ease-in-out both;
}

.thinking-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.thinking-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.input-container {
  padding: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.quick-questions {
  padding: 0 16px 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-questions .el-tag {
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-questions .el-tag:hover {
  transform: translateY(-2px);
}

/* 深色模式支持 */
:global([data-theme="dark"]) .ai-assistant-panel {
  background: var(--bg-secondary) !important;
  border-color: var(--border-color) !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

:global([data-theme="dark"]) .panel-header {
  background: var(--bg-primary) !important;
  border-bottom-color: var(--border-color) !important;
}

:global([data-theme="dark"]) .header-title {
  color: var(--text-primary) !important;
}

:global([data-theme="dark"]) .chat-container {
  background: var(--bg-secondary) !important;
}

:global([data-theme="dark"]) .message-avatar {
  background: rgba(99, 102, 241, 0.1) !important;
}

:global([data-theme="dark"]) .ai-message .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white !important;
}

:global([data-theme="dark"]) .ai-thinking {
  background: var(--bg-primary) !important;
  color: white !important;
}

:global([data-theme="dark"]) .input-container {
  background: var(--bg-secondary) !important;
  border-top-color: var(--border-color) !important;
}

:global([data-theme="dark"]) .message-time {
  color: var(--text-muted) !important;
}

:global([data-theme="dark"]) .thinking-dots span {
  background: var(--primary-color) !important;
}

:global([data-theme="dark"]) .quick-questions {
  background: var(--bg-secondary) !important;
}

:global([data-theme="dark"]) .quick-questions .el-tag {
  background: var(--bg-primary) !important;
  color: var(--text-secondary) !important;
  border-color: var(--border-color) !important;
}
</style>
