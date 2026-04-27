// 应用配置文件
// 所有配置项都可以在这里修改

export const CONFIG = {
  // API配置
  api: {
    baseUrl: 'http://127.0.0.1:7678/api/v1',
    timeout: 30000, // API请求超时时间（毫秒）
    headers: {
      'Content-Type': 'application/json',
      // 可以在这里添加API key等其他请求头
      // 'X-API-Key': 'your-api-key-here'
    }
  },
  
  // 应用配置
  app: {
    name: '颐养膳食',
    version: '1.0.0',
    debug: false // 是否开启调试模式
  },
  
  // 存储配置
  storage: {
    tokenKey: 'token',
    userKey: 'user',
    expireTime: 7 * 24 * 60 * 60 * 1000 // token过期时间（毫秒）
  },
  
  // UI配置
  ui: {
    primaryColor: '#FF7A45',
    secondaryColor: '#409EFF',
    successColor: '#67C23A',
    warningColor: '#E6A23C',
    dangerColor: '#F56C6C'
  }
};

export default CONFIG;
