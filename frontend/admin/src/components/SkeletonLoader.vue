<template>
  <div class="skeleton-loader">
    <!-- 标题骨架 -->
    <div v-if="showTitle" class="skeleton-title">
      <div class="skeleton-line short"></div>
      <div class="skeleton-line medium"></div>
    </div>
    
    <!-- 表格骨架 -->
    <div v-if="type === 'table'" class="skeleton-table">
      <div v-for="i in rows" :key="i" class="skeleton-table-row">
        <div class="skeleton-table-cell avatar"></div>
        <div class="skeleton-table-cell text"></div>
        <div class="skeleton-table-cell text short"></div>
        <div class="skeleton-table-cell text medium"></div>
        <div class="skeleton-table-cell tags"></div>
        <div class="skeleton-table-cell buttons"></div>
      </div>
    </div>
    
    <!-- 卡片骨架 -->
    <div v-if="type === 'cards'" class="skeleton-cards">
      <div v-for="i in cards" :key="i" class="skeleton-card">
        <div class="skeleton-image"></div>
        <div class="skeleton-card-content">
          <div class="skeleton-line short"></div>
          <div class="skeleton-line medium"></div>
          <div class="skeleton-line long"></div>
          <div class="skeleton-line short"></div>
        </div>
      </div>
    </div>
    
    <!-- 统计卡片骨架 -->
    <div v-if="type === 'stats'" class="skeleton-stats">
      <div v-for="i in stats" :key="i" class="skeleton-stat-card">
        <div class="skeleton-icon"></div>
        <div class="skeleton-stat-content">
          <div class="skeleton-line short"></div>
          <div class="skeleton-line medium"></div>
          <div class="skeleton-line short"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'table',
    validator: (value) => ['table', 'cards', 'stats', 'form'].includes(value)
  },
  rows: {
    type: Number,
    default: 5
  },
  cards: {
    type: Number,
    default: 4
  },
  stats: {
    type: Number,
    default: 8
  },
  showTitle: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.skeleton-loader {
  width: 100%;
}

/* 动画效果 */
@keyframes pulse {
  0% {
    background-color: rgba(200, 200, 200, 0.1);
  }
  50% {
    background-color: rgba(200, 200, 200, 0.3);
  }
  100% {
    background-color: rgba(200, 200, 200, 0.1);
  }
}

/* 通用样式 */
.skeleton-line,
.skeleton-image,
.skeleton-icon,
.skeleton-table-cell,
.skeleton-stat-card,
.skeleton-card {
  animation: pulse 1.5s ease-in-out infinite;
  border-radius: 4px;
}

/* 标题样式 */
.skeleton-title {
  margin-bottom: 24px;
}

.skeleton-title .skeleton-line {
  margin-bottom: 8px;
}

/* 线条样式 */
.skeleton-line {
  height: 16px;
  background-color: rgba(200, 200, 200, 0.2);
}

.skeleton-line.short {
  width: 30%;
}

.skeleton-line.medium {
  width: 60%;
}

.skeleton-line.long {
  width: 100%;
}

/* 表格骨架样式 */
.skeleton-table {
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.skeleton-table-row {
  display: flex;
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
}

.skeleton-table-row:last-child {
  border-bottom: none;
}

.skeleton-table-cell {
  margin-right: 16px;
  background-color: rgba(200, 200, 200, 0.2);
}

.skeleton-table-cell.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.skeleton-table-cell.text {
  flex: 1;
  height: 20px;
}

.skeleton-table-cell.text.short {
  flex: 0.5;
}

.skeleton-table-cell.text.medium {
  flex: 0.8;
}

.skeleton-table-cell.tags {
  width: 120px;
  height: 24px;
}

.skeleton-table-cell.buttons {
  width: 120px;
  height: 32px;
}

/* 卡片骨架样式 */
.skeleton-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.skeleton-card {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: 20px;
}

.skeleton-image {
  width: 100%;
  height: 150px;
  margin-bottom: 16px;
  border-radius: var(--radius-md);
}

.skeleton-card-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 统计卡片骨架样式 */
.skeleton-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
}

.skeleton-stat-card {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.skeleton-icon {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-lg);
}

.skeleton-stat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>