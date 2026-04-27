<template>
  <div class="feedback-manage">
    <div class="page-header">
      <div class="header-info">
        <h1>服务评价与反馈</h1>
        <p>倾听老人的声音，持续优化社区助餐服务质量</p>
      </div>
      <div class="header-stats">
        <div class="rating-summary">
          <span class="score">{{ ((stats.positive * 4.5 + stats.neutral * 3 + stats.negative * 1.5) / stats.total).toFixed(1) || '0.0' }}</span>
          <div class="stars-info">
            <el-rate v-model="avgRate" disabled text-color="#ff9900" />
            <span class="count">共 {{ stats.total }} 条评价</span>
          </div>
        </div>
        <div class="ai-actions">
          <el-button 
            type="primary" 
            size="large" 
            class="ai-button"
            @click="startAIReview"
            :loading="aiReviewing"
          >
            <el-icon><Cpu /></el-icon>
            {{ aiReviewing ? 'AI审核中...' : 'AI智能审核' }}
          </el-button>
          <el-button 
            type="info" 
            size="large"
            @click="startAIReply"
            :loading="aiReplying"
            :disabled="unrepliedCount === 0"
          >
            <el-icon><ChatLineRound /></el-icon>
            AI智能回复 ({{ unrepliedCount }})
          </el-button>
          <el-button 
            type="success" 
            size="large"
            @click="batchApprove"
            :disabled="pendingCount === 0"
          >
            <el-icon><CircleCheck /></el-icon>
            批量通过 ({{ pendingCount }})
          </el-button>
          <el-button 
            type="warning" 
            size="large"
            @click="startAIAnalysis"
            :loading="aiAnalyzing"
          >
            <el-icon><Histogram /></el-icon>
            {{ aiAnalyzing ? 'AI分析中...' : 'AI智能分析' }}
          </el-button>
        </div>
      </div>
    </div>

    <el-row :gutter="24">
      <!-- 评价概览卡片 -->
      <el-col :span="6" v-for="stat in feedbackStats" :key="stat.label">
        <div class="glass-card feedback-stat-card">
          <div class="stat-icon" :style="{ background: stat.bg }">
            <el-icon size="24" :color="stat.color"><component :is="stat.icon" /></el-icon>
          </div>
          <div class="stat-info">
            <span class="stat-label">{{ stat.label }}</span>
            <div class="stat-value">{{ stat.value }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-card class="main-card mt-30">
      <template #header>
        <div class="card-header">
          <div class="left">
            <el-radio-group v-model="filterType" size="default">
              <el-radio-button label="全部">全部 ({{ filteredStats.total }})</el-radio-button>
              <el-radio-button label="好评">好评 ({{ filteredStats.positive }})</el-radio-button>
              <el-radio-button label="中评">中评 ({{ filteredStats.neutral }})</el-radio-button>
              <el-radio-button label="差评">差评 ({{ filteredStats.negative }})</el-radio-button>
              <el-radio-button label="有图">有图 ({{ filteredStats.with_images }})</el-radio-button>
              <el-radio-button label="待回复">待回复 ({{ filteredStats.pending_reply }})</el-radio-button>
              <el-radio-button label="待审核">待审核 ({{ filteredStats.pending_review }})</el-radio-button>
              <el-radio-button label="已通过">已通过 ({{ filteredStats.approved }})</el-radio-button>
              <el-radio-button label="已拒绝">已拒绝 ({{ filteredStats.rejected }})</el-radio-button>
            </el-radio-group>
          </div>
          <div class="right">
            <el-select v-model="reviewTypeFilter" placeholder="选择评价类型" style="width: 180px; margin-right: 10px;">
              <el-option label="全部评价" value="all"></el-option>
              <el-option label="配送评价" value="deliverer"></el-option>
              <el-option label="餐品评价" value="meal"></el-option>
            </el-select>
            <el-input v-model="search" placeholder="搜索评价内容..." style="width: 250px" />
          </div>
        </div>
      </template>

      <div class="feedback-list">
        <div v-for="item in filteredFeedbackList" :key="item.id" class="feedback-item">
          <div class="item-header">
            <div class="user-info">
              <el-avatar :size="40" :style="{ backgroundColor: getAvatarColor(item.userName) }">
                {{ item.userName.charAt(0) }}
              </el-avatar>
              <div class="meta">
                <span class="name">{{ item.userName }}</span>
                <span class="time">{{ item.time }}</span>
              </div>
            </div>
            <div class="rating">
              <el-rate v-model="item.rate" disabled />
              <el-tag :type="item.rate >= 4 ? 'success' : (item.rate >= 3 ? 'warning' : 'danger')" size="small" effect="light">
                {{ item.tag }}
              </el-tag>
              <el-tag :type="item.status === 'pending' ? 'warning' : (item.status === 'approved' ? 'success' : 'danger')" size="small">
                {{ getStatusText(item.status) }}
              </el-tag>
              <!-- 评价类型标签 -->
              <el-tag :type="item.delivererId !== null && item.delivererId !== undefined ? 'info' : 'primary'" size="small" effect="plain">
                {{ item.delivererId !== null && item.delivererId !== undefined ? '配送员评价' : '餐品评价' }}
              </el-tag>
              <!-- 评价者类型标签 -->
              <el-tag :type="item.reviewerType === 'elderly' ? 'success' : 'warning'" size="small" effect="plain">
                {{ item.reviewerType === 'elderly' ? '老人自评' : '家属代评' }}
              </el-tag>
              <!-- AI审核标签 -->
              <el-tag v-if="item.aiReviewed" type="info" size="small" effect="plain">
                AI审核
              </el-tag>
              <!-- AI回复标签 -->
              <el-tag v-if="item.aiReplied" type="primary" size="small" effect="plain">
                AI回复
              </el-tag>
            </div>
          </div>
          
          <div class="item-content">
            <p class="text">{{ item.content }}</p>
            <div v-if="item.images && item.images.length" class="images">
              <template v-for="(media, index) in item.images" :key="index">
                <!-- 图片显示 -->
                <el-image 
                  v-if="isImage(media)"
                  :src="getMediaUrl(media)" 
                  :preview-src-list="item.images.filter(img => isImage(img)).map(img => getMediaUrl(img))"
                  fit="cover"
                  class="feedback-media"
                  @error="handleMediaError(media)"
                />
                <!-- 视频显示 -->
                <div v-else-if="isVideo(media)" class="video-container" @click="openVideoPreview(media)">
                  <video 
                    :src="getMediaUrl(media)"
                    controls
                    autoplay="false"
                    preload="auto"
                    class="feedback-media"
                    @error="handleMediaError(media)"
                    @canplay="handleVideoCanPlay"
                    @loadedmetadata="handleVideoLoaded"
                    @play="handleVideoPlay"
                    @pause="handleVideoPause"
                    @timeupdate="handleVideoTimeUpdate"
                    playsinline
                    crossorigin="anonymous"
                    width="100%"
                    height="100%"
                  >
                    您的浏览器不支持视频播放
                  </video>
                  <div class="video-overlay">
                    <el-icon class="zoom-icon"><ZoomIn /></el-icon>
                  </div>
                </div>
                <!-- 其他类型文件显示 -->
                <div v-else class="feedback-media file-placeholder">
                  <el-icon><Document /></el-icon>
                </div>
              </template>
            </div>
            <div class="order-ref">
              <el-icon><Ticket /></el-icon>
              <span>关联订单：{{ item.orderId }}</span>
              <el-divider direction="vertical" />
              <span>餐品：{{ item.mealName }}</span>
              <el-divider v-if="item.delivererName" direction="vertical" />
              <span v-if="item.delivererName" class="deliverer-info">
                配送员：{{ item.delivererName }}
                <span v-if="item.delivererPhone"> ({{ item.delivererPhone }})</span>
              </span>
            </div>
          </div>

          <div class="item-footer">
            <!-- AI审核建议 -->
            <div v-if="getAIReviewSuggestion(item.id)" class="ai-review-suggestion" :class="`ai-${getAIReviewSuggestion(item.id).suggestion}`">
              <el-icon><Cpu /></el-icon>
              <div class="ai-content">
                <div class="ai-title">AI智能审核</div>
                <div class="ai-suggestion">
                  <span class="suggestion-label">审核建议：</span>
                  <el-tag :type="getAIReviewSuggestion(item.id).suggestion === 'approved' ? 'success' : (getAIReviewSuggestion(item.id).suggestion === 'rejected' ? 'danger' : 'warning')" size="small">
                    {{ getAIReviewSuggestion(item.id).suggestion === 'approved' ? '通过' : (getAIReviewSuggestion(item.id).suggestion === 'rejected' ? '拒绝' : '待审核') }}
                  </el-tag>
                </div>
                <div class="ai-confidence">
                  <span class="confidence-label">置信度：</span>
                  <el-progress 
                    :percentage="Math.round(getAIReviewSuggestion(item.id).confidence * 100)" 
                    :color="getAIReviewSuggestion(item.id).confidence >= 0.9 ? '#67C23A' : (getAIReviewSuggestion(item.id).confidence >= 0.7 ? '#E6A23C' : '#F56C6C')"
                    :stroke-width="8"
                    :show-text="false"
                    class="confidence-bar"
                  />
                  <span class="confidence-value">{{ Math.round(getAIReviewSuggestion(item.id).confidence * 100) }}%</span>
                </div>
                <div class="ai-reason">
                  <span class="reason-label">审核理由：</span>
                  <span class="reason-text">{{ getAIReviewSuggestion(item.id).reason }}</span>
                </div>
                <div v-if="getAIReviewSuggestion(item.id).keywords && getAIReviewSuggestion(item.id).keywords.length" class="ai-keywords">
                  <span class="keywords-label">关键分析：</span>
                  <el-tag v-for="(keyword, index) in getAIReviewSuggestion(item.id).keywords" :key="index" size="small" effect="plain">{{ keyword }}</el-tag>
                </div>
                <div class="ai-risk">
                  <span class="risk-label">风险等级：</span>
                  <el-tag :type="getAIReviewSuggestion(item.id).risk_level === 'high' ? 'danger' : (getAIReviewSuggestion(item.id).risk_level === 'medium' ? 'warning' : 'success')" size="small">
                    {{ getAIReviewSuggestion(item.id).risk_level === 'high' ? '高风险' : (getAIReviewSuggestion(item.id).risk_level === 'medium' ? '中风险' : '低风险') }}
                  </el-tag>
                </div>
                <div v-if="!getAIReviewSuggestion(item.id).ai_analyzed" class="ai-fallback">
                  <el-tag type="info" size="small">备用分析模式</el-tag>
                  <span class="fallback-text">{{ getAIReviewSuggestion(item.id).error }}</span>
                </div>
              </div>
            </div>
            
            <!-- 官方回复 -->
            <div v-if="item.reply" class="admin-reply">
              <el-tag :type="item.aiReplied ? 'primary' : 'success'" size="small" class="reply-tag">{{ item.aiReplied ? 'AI回复' : '人工回复' }}</el-tag>
              <span class="reply-text">{{ item.reply }}</span>
            </div>
            
            <!-- 操作按钮 -->
            <div class="actions">
              <el-button v-if="item.status === 'pending'" type="success" size="small" @click="approveFeedback(item)">审核通过</el-button>
              <el-button v-if="item.status === 'pending'" type="danger" size="small" @click="rejectFeedback(item)">拒绝审核</el-button>
              <el-button type="primary" size="small" @click="handleReply(item)">回复评价</el-button>
              <el-button type="warning" size="small">标记异常</el-button>
            </div>
          </div>
        </div>
      </div>

      <div class="pagination-wrapper">
        <el-pagination background layout="prev, pager, next" :total="filteredFeedbackList.length" />
      </div>
    </el-card>

    <!-- 回复弹窗 -->
    <el-dialog v-model="replyVisible" title="回复评价" width="500px" border-radius="16px">
      <el-input
        v-model="replyContent"
        type="textarea"
        :rows="4"
        placeholder="请输入您的回复内容..."
      />
      <template #footer>
        <el-button @click="replyVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReply">提交回复</el-button>
      </template>
    </el-dialog>

    <!-- 视频预览对话框 -->
    <el-dialog
      v-model="videoPreviewVisible"
      title="视频预览"
      width="80%"
      top="5vh"
      :close-on-click-modal="false"
      @closed="closeVideoPreview"
    >
      <div class="video-preview-container">
        <video
          :src="previewVideoUrl"
          controls
          autoplay="false"
          preload="auto"
          class="preview-video"
          playsinline
          crossorigin="anonymous"
          width="100%"
          height="auto"
        >
          您的浏览器不支持视频播放
        </video>
      </div>
    </el-dialog>

    <!-- AI分析报告对话框 -->
    <el-dialog
      v-model="analysisDialogVisible"
      title="AI智能分析报告"
      width="80%"
      top="5vh"
      :close-on-click-modal="false"
    >
      <div v-if="analysisData" class="analysis-report">
        <!-- 总体概览 -->
        <div class="analysis-section">
          <h3>总体概览</h3>
          <div class="summary-cards">
            <div class="summary-card">
              <div class="summary-value">{{ analysisData.summary.total_reviews }}</div>
              <div class="summary-label">评价总数</div>
            </div>
            <div class="summary-card">
              <div class="summary-value">{{ analysisData.summary.average_rating }}</div>
              <div class="summary-label">平均评分</div>
            </div>
            <div class="summary-card">
              <div class="summary-value">{{ analysisData.summary.positive_rate }}%</div>
              <div class="summary-label">好评率</div>
            </div>
            <div class="summary-card">
              <div class="summary-value">{{ analysisData.summary.negative_rate }}%</div>
              <div class="summary-label">差评率</div>
            </div>
          </div>
        </div>

        <!-- 情感分析 -->
        <div class="analysis-section">
          <h3>情感分析</h3>
          <div class="sentiment-chart">
            <el-progress :percentage="analysisData.sentiment_analysis.positive / (analysisData.sentiment_analysis.positive + analysisData.sentiment_analysis.neutral + analysisData.sentiment_analysis.negative) * 100" :color="'#67C23A'" :stroke-width="15" :show-text="true">{{ analysisData.sentiment_analysis.positive }} 好评</el-progress>
            <el-progress :percentage="analysisData.sentiment_analysis.neutral / (analysisData.sentiment_analysis.positive + analysisData.sentiment_analysis.neutral + analysisData.sentiment_analysis.negative) * 100" :color="'#E6A23C'" :stroke-width="15" :show-text="true">{{ analysisData.sentiment_analysis.neutral }} 中评</el-progress>
            <el-progress :percentage="analysisData.sentiment_analysis.negative / (analysisData.sentiment_analysis.positive + analysisData.sentiment_analysis.neutral + analysisData.sentiment_analysis.negative) * 100" :color="'#F56C6C'" :stroke-width="15" :show-text="true">{{ analysisData.sentiment_analysis.negative }} 差评</el-progress>
          </div>
        </div>

        <!-- 热点话题 -->
        <div class="analysis-section">
          <h3>热点话题分析</h3>
          <div class="hot-topics">
            <div v-for="(topic, index) in analysisData.hot_topics" :key="index" class="topic-item" :class="topic.type === 'positive' ? 'positive-topic' : 'negative-topic'">
              <div class="topic-header">
                <span class="topic-name">{{ topic.topic }}</span>
                <span class="topic-count">{{ topic.count }} 次提及 ({{ topic.percentage }}%)</span>
              </div>
              <div v-if="topic.examples && topic.examples.length" class="topic-examples">
                <div v-for="(example, exIndex) in topic.examples" :key="exIndex" class="example-item">
                  <div class="example-rating">
                    <el-rate v-model="example.rating" disabled :show-score="false" />
                  </div>
                  <div class="example-content">{{ example.content }}</div>
                  <div class="example-time">{{ new Date(example.time).toLocaleString('zh-CN') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 关键词分析 -->
        <div class="analysis-section">
          <h3>关键词分析</h3>
          <div class="keyword-cloud">
            <el-tag 
              v-for="(keyword, index) in analysisData.keyword_analysis" 
              :key="index" 
              :size="keyword.count > 10 ? 'large' : 'medium'"
              :effect="keyword.count > 15 ? 'dark' : 'plain'"
              class="keyword-tag"
            >
              {{ keyword.category }} ({{ keyword.count }})
            </el-tag>
          </div>
        </div>

        <!-- 改进建议 -->
        <div class="analysis-section">
          <h3>改进建议</h3>
          <div class="suggestions">
            <div v-for="(suggestion, index) in analysisData.suggestions" :key="index" class="suggestion-item">
              <el-icon class="suggestion-icon"><Warning /></el-icon>
              <span class="suggestion-text">{{ suggestion }}</span>
            </div>
          </div>
        </div>

        <!-- 时间趋势 -->
        <div class="analysis-section" v-if="analysisData.trends && analysisData.trends.length">
          <h3>时间趋势分析</h3>
          <div class="trend-chart">
            <div v-for="(trend, index) in analysisData.trends" :key="index" class="trend-item">
              <div class="trend-date">{{ trend.date }}</div>
              <div class="trend-stats">
                <div class="trend-count">评价数: {{ trend.count }}</div>
                <div class="trend-rating">平均评分: {{ trend.average_rating }}</div>
                <div class="trend-sentiment">好评: {{ trend.positive_count }} | 差评: {{ trend.negative_count }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ChatDotRound, Star, Warning, CircleCheck, Cpu, Ticket, ChatLineRound, Document, ZoomIn, Histogram } from '@element-plus/icons-vue'
import { adminService } from '../api'
import { ElMessage, ElDialog } from 'element-plus'

const avgRate = ref(4.9)
const filterType = ref('全部')
const search = ref('')

// 视频预览相关
const videoPreviewVisible = ref(false)
const previewVideoUrl = ref('')
const replyVisible = ref(false)
const replyContent = ref('')
const currentItem = ref(null)
const loading = ref(false)
const stats = reactive({
  total: 0,
  positive: 0,
  neutral: 0,
  negative: 0,
  with_images: 0,
  pending_review: 0,
  approved: 0,
  rejected: 0,
  pending_reply: 0,
  deliverer_reviews: 0,
  meal_reviews: 0
})

// 评价类型筛选（第一次筛选）
const reviewTypeFilter = ref('all')

// AI审核相关状态
const aiReviewing = ref(false)
const aiReviewResults = ref({})

// AI回复相关状态
const aiReplying = ref(false)

// AI分析相关状态
const aiAnalyzing = ref(false)
const analysisDialogVisible = ref(false)
const analysisData = ref(null)

const feedbackList = ref([])

const filteredFeedbackList = computed(() => {
  console.log('筛选条件:', filterType.value)
  console.log('搜索关键词:', search.value)
  console.log('评价类型筛选:', reviewTypeFilter.value)
  
  const result = feedbackList.value.filter(item => {
    // 搜索筛选
    if (search.value && !item.content.toLowerCase().includes(search.value.toLowerCase())) {
      console.log('搜索筛选排除:', item.id, '内容不包含:', search.value)
      return false
    }
    
    // 第一次筛选：评价类型筛选（配送评价/餐品评价）
    let passReviewTypeFilter = true
    if (reviewTypeFilter.value !== 'all') {
      if (reviewTypeFilter.value === 'deliverer') {
        passReviewTypeFilter = item.delivererId !== null && item.delivererId !== undefined && item.delivererId !== ''
      } else if (reviewTypeFilter.value === 'meal') {
        passReviewTypeFilter = item.delivererId === null || item.delivererId === undefined || item.delivererId === ''
      }
    }
    
    // 第二次筛选：其他评价标签筛选
    let passTagFilter = true
    switch (filterType.value) {
      case '好评':
        passTagFilter = item.rate >= 4
        break
      case '中评':
        passTagFilter = item.rate === 3
        break
      case '差评':
        passTagFilter = item.rate <= 2
        break
      case '有图':
        passTagFilter = item.images && item.images.length > 0
        break
      case '待回复':
        passTagFilter = item.status === 'approved' && !item.reply
        break
      case '待审核':
        passTagFilter = item.status === 'pending'
        console.log('待审核筛选:', item.id, 'status:', item.status, '结果:', passTagFilter)
        break
      case '已通过':
        passTagFilter = item.status === 'approved'
        break
      case '已拒绝':
        passTagFilter = item.status === 'rejected'
        break
      default:
        passTagFilter = true
    }
    
    // 必须同时通过第一次筛选和第二次筛选
    return passReviewTypeFilter && passTagFilter
  })
  
  console.log('筛选结果数量:', result.length)
  return result
})

const pendingCount = computed(() => {
  return feedbackList.value.filter(item => item.status === 'pending').length
})

const unrepliedCount = computed(() => {
  return feedbackList.value.filter(item => item.status === 'approved' && !item.reply).length
})

// 根据筛选条件计算过滤后的统计数据
const filteredStats = computed(() => {
  // 先应用评价类型筛选
  let filteredItems = feedbackList.value
  if (reviewTypeFilter.value !== 'all') {
    if (reviewTypeFilter.value === 'deliverer') {
      filteredItems = filteredItems.filter(item => item.delivererId !== null && item.delivererId !== undefined && item.delivererId !== '')
    } else if (reviewTypeFilter.value === 'meal') {
      filteredItems = filteredItems.filter(item => item.delivererId === null || item.delivererId === undefined || item.delivererId === '')
    }
  }
  
  // 计算过滤后的统计数据
  const total = filteredItems.length
  const positive = filteredItems.filter(item => item.rate >= 4).length
  const neutral = filteredItems.filter(item => item.rate === 3).length
  const negative = filteredItems.filter(item => item.rate <= 2).length
  const withImages = filteredItems.filter(item => item.images && item.images.length > 0).length
  const pendingReview = filteredItems.filter(item => item.status === 'pending').length
  const approved = filteredItems.filter(item => item.status === 'approved').length
  const rejected = filteredItems.filter(item => item.status === 'rejected').length
  const pendingReply = filteredItems.filter(item => item.status === 'approved' && !item.reply).length
  
  return {
    total,
    positive,
    neutral,
    negative,
    with_images: withImages,
    pending_review: pendingReview,
    approved,
    rejected,
    pending_reply: pendingReply
  }
})

const feedbackStats = computed(() => {
  // 确保所有统计字段都有默认值，避免访问不存在的字段
  const s = stats || {}
  const total = s.total || 0
  const delivererReviews = s.deliverer_reviews || 0
  const mealReviews = s.meal_reviews || 0
  
  // 计算好评率和平均分，避免除以0
  const overallPositiveRate = total > 0 ? Math.round((s.positive / total * 100) || 0) : 0
  const overallAvgScore = total > 0 ? ((s.positive * 4.5 + (s.neutral || 0) * 3 + (s.negative || 0) * 1.5) / total).toFixed(1) : '0.0'
  
  const delivererPositiveRate = delivererReviews > 0 ? Math.round((s.deliverer_positive / delivererReviews * 100) || 0) : 0
  const delivererAvgScore = delivererReviews > 0 ? ((s.deliverer_positive * 4.5 + (s.deliverer_neutral || 0) * 3 + (s.deliverer_negative || 0) * 1.5) / delivererReviews).toFixed(1) : '0.0'
  
  const mealPositiveRate = mealReviews > 0 ? Math.round((s.meal_positive / mealReviews * 100) || 0) : 0
  const mealAvgScore = mealReviews > 0 ? ((s.meal_positive * 4.5 + (s.meal_neutral || 0) * 3 + (s.meal_negative || 0) * 1.5) / mealReviews).toFixed(1) : '0.0'
  
  return [
    { label: '配送好评率', value: `${delivererPositiveRate}%`, icon: 'CircleCheck', color: '#4facfe', bg: 'rgba(79, 172, 254, 0.1)' },
    { label: '配送平均分', value: delivererAvgScore, icon: 'Star', color: '#43e97b', bg: 'rgba(67, 233, 123, 0.1)' },
    { label: '餐品好评率', value: `${mealPositiveRate}%`, icon: 'CircleCheck', color: '#fa709a', bg: 'rgba(250, 112, 154, 0.1)' },
    { label: '餐品平均分', value: mealAvgScore, icon: 'Star', color: '#fee140', bg: 'rgba(254, 225, 64, 0.1)' },
  ]
})

// 加载评价数据
const loadReviews = async () => {
  try {
    loading.value = true
    const response = await adminService.getReviews({ page: 1, limit: 100 })
    
    console.log('原始响应数据:', response)
    console.log('原始items数据:', response.items)
    
    // 保存统计数据
    if (response.stats) {
      Object.assign(stats, response.stats)
      
      // 后端已经返回了完整的统计数据，包括配送评价和餐品评价的数量
    }
    
    feedbackList.value = response.items.map(item => {
        const mappedItem = {
            id: item.id,
            userName: item.elderly_name || '未知用户',
            time: new Date(item.created_at).toLocaleString('zh-CN'),
            rate: item.rating,
            tag: item.rating >= 4 ? '好评' : (item.rating >= 3 ? '中评' : '差评'),
            content: item.content,
            orderId: item.order_id ? `ORD${item.order_id}` : '无',
            mealName: item.mealName || '未知餐品',
            images: item.images || [],
            reply: item.reply,
            status: item.status ?? 'approved',
            aiReviewed: item.ai_reviewed === 1,
            aiReplied: item.ai_replied === 1,
            reviewerType: item.reviewer_type,
            delivererId: item.deliverer_id,
            delivererName: item.deliverer_name,
            delivererPhone: item.deliverer_phone
        }
        console.log('映射后的数据项:', mappedItem)
        return mappedItem
    })
    
    console.log('筛选前的feedbackList:', feedbackList.value)
    console.log('pendingCount:', pendingCount.value)
  } catch (error) {
    ElMessage.error('加载评价数据失败')
    console.error('加载评价数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadReviews()
})

const handleReply = (item) => {
  currentItem.value = item
  replyVisible.value = true
}

const submitReply = async () => {
  if (currentItem.value) {
    try {
      await adminService.updateReview(currentItem.value.id, { reply: replyContent.value, ai_replied: 0 })
      currentItem.value.reply = replyContent.value
      currentItem.value.aiReplied = false
      replyVisible.value = false
      replyContent.value = ''
      ElMessage.success('回复成功')
    } catch (error) {
      ElMessage.error('回复失败')
      console.error('回复失败:', error)
    }
  }
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return statusMap[status] || status
}

const approveFeedback = async (item) => {
  try {
    await adminService.updateReview(item.id, { status: 'approved' })
    item.status = 'approved'
    ElMessage.success('审核通过')
  } catch (error) {
    ElMessage.error('审核失败')
    console.error('审核失败:', error)
  }
}

const rejectFeedback = async (item) => {
  try {
    await adminService.updateReview(item.id, { status: 'rejected' })
    item.status = 'rejected'
    ElMessage.success('拒绝审核')
  } catch (error) {
    ElMessage.error('审核失败')
    console.error('审核失败:', error)
  }
}

// AI审核方法
const startAIReview = async () => {
  aiReviewing.value = true
  
  try {
    const response = await adminService.batchAIReview()
    console.log('AI审核结果:', response)
    
    // 检查响应数据
    if (!response) {
      ElMessage.warning('审核失败：服务器返回数据格式错误')
      return
    }
    
    // 如果没有待审核的评价
    if (response.message === '没有待审核的评价') {
      ElMessage.info(response.message)
      await loadReviews()
      return
    }
    
    // 更新本地数据
    if (response.ai_results) {
      response.ai_results.forEach(result => {
        aiReviewResults.value[result.review_id] = {
          suggestion: result.suggestion,
          confidence: result.confidence,
          reason: result.reason,
          keywords: result.keywords,
          risk_level: result.risk_level,
          ai_analyzed: result.ai_analyzed,
          error: result.error
        }
      })
    }
    
    // 重新加载数据以更新状态
    await loadReviews()
    
    // 显示成功消息
    if (response.auto_approved !== undefined) {
      let message = `AI审核完成！自动通过: ${response.auto_approved}, 自动拒绝: ${response.auto_rejected}, 待人工审核: ${response.pending_review}`
      if (response.auto_replied !== undefined && response.auto_replied > 0) {
        message += `, 自动回复: ${response.auto_replied}`
      }
      ElMessage.success(message)
    } else {
      ElMessage.success('AI审核完成！')
    }
  } catch (error) {
    ElMessage.error('AI审核失败')
    console.error('AI审核失败:', error)
  } finally {
    aiReviewing.value = false
  }
}

// AI回复方法
const startAIReply = async () => {
  aiReplying.value = true
  
  try {
    const response = await adminService.batchAIReply()
    console.log('AI回复结果:', response)
    
    // 检查响应数据
    if (!response) {
      ElMessage.warning('回复失败：服务器返回数据格式错误')
      return
    }
    
    // 如果没有未回复的评价
    if (response.message === '没有未回复的评价') {
      ElMessage.info(response.message)
      await loadReviews()
      return
    }
    
    // 重新加载数据以更新状态
    await loadReviews()
    
    // 显示成功消息
    if (response.total_reviews !== undefined) {
      ElMessage.success(`AI回复完成！处理评价数: ${response.total_reviews}, 生成回复: ${response.generated_replies}, 应用回复: ${response.applied_replies}`)
    } else {
      ElMessage.success('AI回复完成！')
    }
  } catch (error) {
    ElMessage.error('AI回复失败')
    console.error('AI回复失败:', error)
  } finally {
    aiReplying.value = false
  }
}

// 批量通过方法
const batchApprove = async () => {
  try {
    const pendingIds = feedbackList.value
      .filter(item => item.status === 'pending')
      .map(item => item.id)
    
    if (pendingIds.length === 0) {
      ElMessage.warning('没有待审核的评价')
      return
    }
    
    // 调用批量通过API
    const response = await adminService.batchApprove(pendingIds)
    console.log('批量审核结果:', response)
    
    // 重新加载数据
    await loadReviews()
    ElMessage.success(`批量审核完成！处理了 ${pendingIds.length} 条评价`)
  } catch (error) {
    ElMessage.error('批量审核失败')
    console.error('批量审核失败:', error)
  }
}

// 获取头像颜色
const getAvatarColor = (name) => {
  const colors = [
    '#4ecdc4', '#45aaf2', '#ff6b6b', '#fed330', 
    '#667eea', '#764ba2', '#4facfe', '#43e97b',
    '#fa709a', '#fee140', '#30cfd0', '#30a9de'
  ]
  
  // 根据用户名生成一个固定的颜色索引
  let hash = 0
  for (let i = 0; i< name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  const index = Math.abs(hash) % colors.length
  return colors[index]
}

// 获取AI审核建议
const getAIReviewSuggestion = (itemId) => {
  return aiReviewResults.value[itemId]
}

// 获取完整的媒体URL
const getMediaUrl = (url) => {
  if (!url || typeof url !== 'string') return url
  
  // 如果已经是完整URL，直接返回
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  
  // 如果是相对路径，添加静态文件前缀
  return `http://localhost:7678/static/${url}`
}

// 判断是否为图片
const isImage = (url) => {
  if (!url || typeof url !== 'string') return false
  
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.jpg.jpg', '.png.png']
  const lowerUrl = url.toLowerCase()
  
  // 检查是否包含图片扩展名
  const hasImageExt = imageExtensions.some(ext => lowerUrl.includes(ext))
  
  // 如果是外部图片URL且没有明确的视频扩展名，也当作图片处理
  if (!hasImageExt && !isVideo(url)) {
    // 检查是否是图片URL（包含常见图片域名或图片服务）
    const imageDomains = ['bing.net', 'unsplash.com', 'picsum.photos', 'images.unsplash.com']
    const isImageDomain = imageDomains.some(domain => lowerUrl.includes(domain))
    
    // 如果是图片域名，或者URL看起来像图片链接（包含常见图片参数）
    if (isImageDomain || lowerUrl.includes('id=') || lowerUrl.includes('photo-')) {
      return true
    }
  }
  
  return hasImageExt
}

// 判断是否为视频
const isVideo = (url) => {
  if (!url || typeof url !== 'string') return false
  
  const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv']
  const lowerUrl = url.toLowerCase()
  
  return videoExtensions.some(ext => lowerUrl.includes(ext))
}

// 处理媒体加载错误
const handleMediaError = (url) => {
  console.error('媒体加载失败:', url)
  ElMessage.warning(`媒体加载失败: ${url}`)
}

// 检测视频兼容性
const checkVideoCompatibility = (url) => {
  const video = document.createElement('video')
  const canPlay = video.canPlayType('video/mp4; codecs="avc1.42E01E"')
  console.log('视频兼容性检测:', canPlay)
  return canPlay !== ''
}

// 视频可以播放时的处理
const handleVideoCanPlay = () => {
  console.log('视频可以播放了')
}

// 视频元数据加载完成时的处理
const handleVideoLoaded = (event) => {
  console.log('视频元数据加载完成:', {
    duration: event.target.duration,
    width: event.target.videoWidth,
    height: event.target.videoHeight
  })
}

// 视频播放时的处理
const handleVideoPlay = (event) => {
  console.log('视频开始播放')
}

// 视频暂停时的处理
const handleVideoPause = (event) => {
  console.log('视频暂停播放')
}

// 视频时间更新时的处理
const handleVideoTimeUpdate = (event) => {
  console.log('视频时间更新:', event.target.currentTime)
}

// 打开视频预览
const openVideoPreview = (videoUrl) => {
  previewVideoUrl.value = getMediaUrl(videoUrl)
  videoPreviewVisible.value = true
}

// 关闭视频预览
const closeVideoPreview = () => {
  videoPreviewVisible.value = false
  previewVideoUrl.value = ''
}

// AI分析方法
const startAIAnalysis = async () => {
  aiAnalyzing.value = true
  
  try {
    const response = await adminService.analyzeReviews()
    console.log('AI分析结果:', response)
    
    if (response.success && response.data) {
      analysisData.value = response.data
      analysisDialogVisible.value = true
    } else {
      ElMessage.error('AI分析失败')
    }
  } catch (error) {
    ElMessage.error('AI分析失败')
    console.error('AI分析失败:', error)
  } finally {
    aiAnalyzing.value = false
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header-info h1 {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 8px 0;
}

.header-info p {
  color: var(--text-light);
  margin: 0;
}

.rating-summary {
  display: flex;
  align-items: center;
  gap: 20px;
  background: var(--bg-secondary);
  padding: 16px 30px;
  border-radius: 24px;
  box-shadow: var(--shadow-sm);
}

.ai-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.ai-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 12px;
  transition: all 0.3s;
}

.ai-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.rating-summary .score {
  font-size: 42px;
  font-weight: 900;
  color: var(--primary-color);
}

.stars-info {
  display: flex;
  flex-direction: column;
}

.stars-info .count {
  font-size: 12px;
  color: var(--text-light);
  margin-top: 4px;
}

.feedback-stat-card {
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 12px;
  color: var(--text-light);
  font-weight: 600;
}

.stat-value {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.feedback-item {
  padding: 20px;
  border-radius: 20px;
  background: var(--bg-primary);
  transition: all 0.3s;
}

.feedback-item:hover {
  background: var(--bg-secondary);
  box-shadow: var(--shadow-md);
  transform: scale(1.01);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info .meta {
  display: flex;
  flex-direction: column;
}

.user-info .name {
  font-weight: 800;
  font-size: 16px;
}

.user-info .time {
  font-size: 12px;
  color: var(--text-light);
}

.rating {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.item-content {
  margin-bottom: 20px;
}

.item-content .text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

.images {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.feedback-media {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  cursor: pointer;
  object-fit: cover;
  background-color: #1a1a1a;
}

video.feedback-media {
  background-color: #000;
  display: block;
  object-fit: cover;
  width: 200px;
  height: 150px;
}

video.feedback-media::-webkit-media-controls-panel {
  background-color: rgba(0, 0, 0, 0.8);
}

/* 播放按钮已隐藏 */

video.feedback-media::-webkit-media-controls-current-time-display,
video.feedback-media::-webkit-media-controls-time-remaining-display {
  color: white;
}

/* 隐藏视频中间的大播放/暂停按钮 */
video.feedback-media::-webkit-media-controls-start-playback-button {
  display: none !important;
}

/* 隐藏视频中央的播放按钮 */
video.feedback-media::-webkit-media-controls-play-button {
  display: none !important;
}

/* 移除网格背景 */

.file-placeholder {
  background-color: #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.file-placeholder .el-icon {
  font-size: 32px;
}

/* 视频容器样式 */
.video-container {
  position: relative;
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
}

.video-container:hover .video-overlay {
  opacity: 1;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.zoom-icon {
  color: white;
  font-size: 24px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  padding: 8px;
}

/* 视频预览对话框样式 */
.video-preview-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.preview-video {
  max-height: 70vh;
  border-radius: 8px;
}

.order-ref {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-light);
  background: var(--bg-secondary);
  padding: 8px 16px;
  border-radius: 10px;
  width: fit-content;
}

.item-footer {
  padding-top: 16px;
  border-top: 1px dashed var(--border-color);
}

.admin-reply {
  background: rgba(78, 205, 196, 0.05);
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.reply-tag {
  align-self: flex-start;
}

.reply-text {
  color: var(--text-secondary);
  line-height: 1.5;
}

.actions {
  display: flex;
  gap: 16px;
}

/* AI审核建议样式 */
.ai-review-suggestion {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 16px;
  margin-bottom: 16px;
  border: 2px solid;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
}

.ai-review-suggestion .el-icon {
  font-size: 24px;
  margin-top: 4px;
}

.ai-approved {
  border-color: var(--secondary-color);
  background: rgba(16, 185, 129, 0.1);
}

.ai-approved .el-icon {
  color: var(--secondary-color);
}

.ai-rejected {
  border-color: var(--danger-color);
  background: rgba(239, 68, 68, 0.1);
}

.ai-rejected .el-icon {
  color: var(--danger-color);
}

.ai-content {
  flex: 1;
}

.ai-title {
  font-weight: 800;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.ai-suggestion {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.suggestion-label {
  font-size: 12px;
  color: var(--text-muted);
}

.suggestion-value {
  font-weight: 700;
  font-size: 14px;
  color: #67C23A;
}

.ai-rejected .suggestion-value {
  color: #F56C6C;
}

.ai-confidence {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.confidence-label {
  font-size: 12px;
  color: var(--text-muted);
  min-width: 40px;
}

.confidence-bar {
  flex: 1;
  height: 8px;
}

.confidence-value {
  font-weight: 700;
  font-size: 12px;
  color: var(--text-primary);
  min-width: 35px;
}

.ai-reason {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.reason-label {
  font-size: 12px;
  color: var(--text-muted);
  min-width: 30px;
}

.reason-text {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.ai-keywords {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.keywords-label {
  font-size: 12px;
  color: var(--text-muted);
  min-width: 60px;
}

.ai-risk {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.risk-label {
  font-size: 12px;
  color: var(--text-muted);
  min-width: 60px;
}

.ai-fallback {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed var(--border-color);
}

.fallback-text {
  font-size: 11px;
  color: var(--text-light);
  flex: 1;
}

.mt-30 { margin-top: 30px; }
.pagination-wrapper {
    margin-top: 30px;
    display: flex;
    justify-content: center;
}

/* AI分析报告样式 */
.analysis-report {
    padding: 20px;
}

.analysis-section {
    margin-bottom: 40px;
}

.analysis-section h3 {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 20px;
    color: var(--text-primary);
    border-left: 4px solid var(--primary-color);
    padding-left: 12px;
}

.summary-cards {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.summary-card {
    flex: 1;
    min-width: 150px;
    background: var(--bg-secondary);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.summary-value {
    font-size: 32px;
    font-weight: 800;
    color: var(--primary-color);
    margin-bottom: 8px;
}

.summary-label {
    font-size: 14px;
    color: var(--text-light);
}

.sentiment-chart {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.hot-topics {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.topic-item {
    background: var(--bg-secondary);
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid;
}

.positive-topic {
    border-left-color: #67C23A;
}

.negative-topic {
    border-left-color: #F56C6C;
}

.topic-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.topic-name {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
}

.topic-count {
    font-size: 14px;
    color: var(--text-light);
}

.topic-examples {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.example-item {
    background: var(--bg-primary);
    padding: 16px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.example-rating {
    margin-bottom: 8px;
}

.example-content {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 8px;
}

.example-time {
    font-size: 12px;
    color: var(--text-light);
}

.keyword-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.keyword-tag {
    margin-bottom: 8px;
}

.suggestions {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.suggestion-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: rgba(239, 68, 68, 0.05);
    padding: 16px;
    border-radius: 8px;
    border-left: 4px solid #F56C6C;
}

.suggestion-icon {
    color: #F56C6C;
    margin-top: 2px;
}

.suggestion-text {
    flex: 1;
    font-size: 14px;
    line-height: 1.6;
    color: var(--text-secondary);
}

.trend-chart {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.trend-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    background: var(--bg-secondary);
    border-radius: 8px;
}

.trend-date {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    min-width: 80px;
}

.trend-stats {
    display: flex;
    gap: 20px;
    font-size: 14px;
    color: var(--text-secondary);
}
</style>
