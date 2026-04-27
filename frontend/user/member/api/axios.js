// 创建API客户端
const apiClient = {
  baseURL: 'http://127.0.0.1:7678/api/v1',
  
  // 请求方法
  async request(options) {
    const token = uni.getStorageSync('token');
    
    const config = {
      url: `${this.baseURL}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': options.contentType || 'application/json',
        ...options.header
      }
    };
    
    // 添加token
    if (token) {
      config.header['Authorization'] = `Bearer ${token}`;
    }
    
    console.log('发送请求:', config);
    
    return new Promise((resolve, reject) => {
      uni.request({
        ...config,
        success: (response) => {
          console.log('请求成功:', response);
          if (response.statusCode === 200) {
            resolve(response.data);
          } else {
            // 构造错误对象
            const error = new Error(response.data?.detail || `请求失败: ${response.statusCode}`);
            error.response = response;
            error.status = response.statusCode;
            reject(error);
          }
        },
        fail: (error) => {
          console.error('请求失败:', error);
          reject(error);
        }
      });
    });
  },
  
  // GET请求
  async get(url, params) {
    // 将params转换为查询字符串
    let requestUrl = url;
    if (params && Object.keys(params).length > 0) {
      const queryString = Object.entries(params)
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
        .join('&');
      requestUrl += `?${queryString}`;
    }
    
    return this.request({
      url: requestUrl,
      method: 'GET'
    });
  },
  
  // POST请求
  async post(url, data, contentType = 'application/json') {
    return this.request({
      url,
      method: 'POST',
      data,
      contentType
    });
  },
  
  // PUT请求
  async put(url, data) {
    return this.request({
      url,
      method: 'PUT',
      data
    });
  },
  
  // DELETE请求
  async delete(url) {
    return this.request({
      url,
      method: 'DELETE'
    });
  }
};

export default apiClient;