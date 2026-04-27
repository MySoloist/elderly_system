<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/*每个页面公共css */
	/* 全局色彩方案 */
	:root {
		/* 主色调 */
		--primary-color: #FF7A45; /* 温暖橙色 */
		--primary-gradient: linear-gradient(135deg, #FF7A45 0%, #FF9A72 100%);
		--secondary-color: #409EFF; /* 柔和蓝色 */
		--background-color: #F5F5F5; /* 浅灰色 */
		--card-background: #FFFFFF; /* 白色 */
		--card-shadow: 0 10px 28px rgba(255, 122, 69, 0.12);
		--card-shadow-soft: 0 6px 18px rgba(0, 0, 0, 0.06);
		--radius-large: 20px;
		--radius-medium: 14px;
		
		/* 文字颜色 */
		--text-primary: #333333; /* 深灰色 */
		--text-secondary: #666666; /* 中灰色 */
		--text-light: #999999; /* 浅灰色 */
		
		/* 状态颜色 */
		--success-color: #67C23A; /* 绿色 */
		--warning-color: #E6A23C; /* 黄色 */
		--danger-color: #F56C6C; /* 红色 */
		
		/* 字体大小 */
		--font-large: 20px; /* 大标题 */
		--font-medium: 18px; /* 中标题 */
		--font-normal: 16px; /* 正文 */
		--font-small: 14px; /* 小字 */
		
		/* 间距 */
		--padding-page: 20px; /* 页面边距 */
		--padding-element: 16px; /* 元素间距 */
		--padding-card: 16px; /* 卡片间距 */
		--padding-content: 12px; /* 内容间距 */
		--button-height: 48px; /* 按钮高度 */
		--input-height: 48px; /* 输入框高度 */
	}

	/* 全局重置样式 */
	view, text, image, button, input, textarea {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}
	
	body, uni-page {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
		font-size: var(--font-normal);
		color: var(--text-primary);
		background: linear-gradient(180deg, #FFF9F6 0%, #F5F5F5 200px, #F5F5F5 100%);
		line-height: 1.6;
	}
	
	/* 按钮样式 */
	.btn-primary {
		background-color: var(--primary-color);
		color: white;
		border: none;
		border-radius: 8px;
		height: var(--button-height);
		font-size: var(--font-normal);
		font-weight: 600;
		line-height: var(--button-height);
		text-align: center;
		display: block;
		width: 100%;
	}
	
	.btn-secondary {
		background-color: var(--secondary-color);
		color: white;
		border: none;
		border-radius: 8px;
		height: var(--button-height);
		font-size: var(--font-normal);
		font-weight: 600;
		line-height: var(--button-height);
		text-align: center;
		display: block;
		width: 100%;
	}
	
	.btn-danger {
		background-color: var(--danger-color);
		color: white;
		border: none;
		border-radius: 8px;
		height: var(--button-height);
		font-size: var(--font-normal);
		font-weight: 600;
		line-height: var(--button-height);
		text-align: center;
		display: block;
		width: 100%;
	}
	
	/* 输入框样式 */
	.input-normal {
		height: var(--input-height);
		border: 1px solid #DDDDDD;
		border-radius: 8px;
		padding: 0 16px;
		font-size: var(--font-normal);
		color: var(--text-primary);
		background-color: white;
	}
	
	.input-normal:focus {
		border-color: var(--primary-color);
		outline: none;
	}
	
	/* 卡片样式 */
	.card {
		background-color: var(--card-background);
		border-radius: 12px;
		padding: var(--padding-element);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
	}
	
	/* 标题样式 */
	.title-large {
		font-size: var(--font-large);
		font-weight: 700;
		line-height: 1.4;
		color: var(--text-primary);
	}
	
	.title-medium {
		font-size: var(--font-medium);
		font-weight: 600;
		line-height: 1.5;
		color: var(--text-primary);
	}
	
	.title-normal {
		font-size: var(--font-normal);
		font-weight: 600;
		line-height: 1.6;
		color: var(--text-primary);
	}
	
	/* 文字样式 */
	.text-primary {
		color: var(--text-primary);
	}
	
	.text-secondary {
		color: var(--text-secondary);
	}
	
	.text-light {
		color: var(--text-light);
	}
	
	.text-small {
		font-size: var(--font-small);
	}
	
	/* 标签样式 */
	.tag {
		display: inline-block;
		padding: 4px 12px;
		border-radius: 12px;
		font-size: var(--font-small);
		font-weight: 500;
	}
	
	.tag-primary {
		background-color: rgba(255, 122, 69, 0.1);
		color: var(--primary-color);
	}
	
	.tag-success {
		background-color: rgba(103, 194, 58, 0.1);
		color: var(--success-color);
	}
	
	.tag-warning {
		background-color: rgba(230, 162, 60, 0.1);
		color: var(--warning-color);
	}
	
	.tag-danger {
		background-color: rgba(245, 108, 108, 0.1);
		color: var(--danger-color);
	}
	
	/* 布局样式 */
	.container {
		padding: var(--padding-page);
	}
	
	.flex {
		display: flex;
	}
	
	.flex-center {
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.flex-between {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	
	.flex-column {
		display: flex;
		flex-direction: column;
	}
	
	/* 通用工具类 */
	.mt-16 {
		margin-top: 16px;
	}
	
	.mb-16 {
		margin-bottom: 16px;
	}
	
	.mt-20 {
		margin-top: 20px;
	}
	
	.mb-20 {
		margin-bottom: 20px;
	}
	
	.ml-16 {
		margin-left: 16px;
	}
	
	.mr-16 {
		margin-right: 16px;
	}
</style>
