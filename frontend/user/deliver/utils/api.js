// API工具类
// 防重复调用标志
const isUpdatingLocation = {
  inProgress: false
}

export const api = {
  auth: {
    // 登录
    async login(credentials) {
      console.log('配送员登录开始:', credentials);
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: 'http://127.0.0.1:7678/api/v1/auth/login',
          method: 'POST',
          header: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          data: `username=${encodeURIComponent(credentials.username)}&password=${encodeURIComponent(credentials.password)}&grant_type=password`,
          success: function(res) {
            console.log('登录请求成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '登录失败'));
            }
          },
          fail: function(err) {
            console.log('登录请求失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 注册
    async register(registerData) {
      console.log('配送员注册开始:', registerData);
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: 'http://127.0.0.1:7678/api/v1/auth/register',
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          data: registerData,
          success: function(res) {
            console.log('注册请求成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '注册失败'));
            }
          },
          fail: function(err) {
            console.log('注册请求失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 退出登录
    async logout() {
      console.log('配送员退出登录');
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: 'http://127.0.0.1:7678/api/v1/auth/logout',
          method: 'POST',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          },
          success: function(res) {
            console.log('退出登录成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '退出登录失败'));
            }
          },
          fail: function(err) {
            console.log('退出登录失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 微信登录
    async wechatLogin(code, userType) {
      console.log('配送员微信登录开始:', { code, userType });
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: 'http://127.0.0.1:7678/api/v1/auth/wechat-login',
          method: 'POST',
          header: {
            'Content-Type': 'application/json'
          },
          data: {
            code: code,
            user_type: userType
          },
          success: function(res) {
            console.log('微信登录请求成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '微信登录失败'));
            }
          },
          fail: function(err) {
            console.log('微信登录请求失败:', err);
            reject(err);
          }
        });
      });
    }
  },
  
  orders: {
    // 获取订单列表
    async getOrders(status) {
      console.log('获取订单列表:', status);
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: `http://127.0.0.1:7678/api/v1/deliver/orders${status ? `?status=${status}` : ''}`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`
          },
          success: function(res) {
            console.log('获取订单列表成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '获取订单列表失败'));
            }
          },
          fail: function(err) {
            console.log('获取订单列表失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 接单
    async acceptOrder(orderId) {
      console.log('接单:', orderId);
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: `http://127.0.0.1:7678/api/v1/deliver/orders/${orderId}/accept`,
          method: 'POST',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          },
          success: function(res) {
            console.log('接单成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '接单失败'));
            }
          },
          fail: function(err) {
            console.log('接单失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 完成订单
    async completeOrder(orderId) {
      console.log('完成订单:', orderId);
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: `http://127.0.0.1:7678/api/v1/deliver/orders/${orderId}/complete`,
          method: 'POST',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          },
          success: function(res) {
            console.log('完成订单成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '完成订单失败'));
            }
          },
          fail: function(err) {
            console.log('完成订单失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 获取订单详情
    async getOrderDetail(orderId) {
      console.log('获取订单详情:', orderId);
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: `http://127.0.0.1:7678/api/v1/deliver/orders/${orderId}`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`
          },
          success: function(res) {
            console.log('获取订单详情成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '获取订单详情失败'));
            }
          },
          fail: function(err) {
            console.log('获取订单详情失败:', err);
            reject(err);
          }
        });
      });
    }
  },
  
  exceptions: {
    // 提交异常
    async reportException(orderId, exceptionType, description) {
      console.log('提交异常:', { orderId, exceptionType, description });
      
      // 构建查询参数
      let url = `http://127.0.0.1:7678/api/v1/deliver/exceptions?order_id=${orderId}&exception_type=${exceptionType}&description=${encodeURIComponent(description)}`;
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: url,
          method: 'POST',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          },
          success: function(res) {
            console.log('提交异常成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '提交异常失败'));
            }
          },
          fail: function(err) {
            console.log('提交异常失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 获取异常记录
    async getExceptions(params = {}) {
      console.log('获取异常记录:', params);
      
      const query = Object.keys(params)
        .map(key => `${key}=${encodeURIComponent(params[key])}`)
        .join('&');
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: `http://127.0.0.1:7678/api/v1/deliver/exceptions${query ? `?${query}` : ''}`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`
          },
          success: function(res) {
            console.log('获取异常记录成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '获取异常记录失败'));
            }
          },
          fail: function(err) {
            console.log('获取异常记录失败:', err);
            reject(err);
          }
        });
      });
    }
  },
  
  profile: {
    // 获取个人信息
    async getProfile() {
      console.log('获取个人信息');
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: 'http://127.0.0.1:7678/api/v1/deliver/profile',
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`
          },
          success: function(res) {
            console.log('获取个人信息成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '获取个人信息失败'));
            }
          },
          fail: function(err) {
            console.log('获取个人信息失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 获取详细个人信息
    async getPersonalInfo() {
      console.log('获取详细个人信息');
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: 'http://127.0.0.1:7678/api/v1/deliver/personal-info',
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`
          },
          success: function(res) {
            console.log('获取详细个人信息成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '获取详细个人信息失败'));
            }
          },
          fail: function(err) {
            console.log('获取详细个人信息失败:', err);
            reject(err);
          }
        });
      });
    },
    
    // 获取收入统计
    async getIncomeStatistics(timeRange = 'today') {
      console.log('获取收入统计:', timeRange);
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: `http://127.0.0.1:7678/api/v1/deliver/income?time_range=${timeRange}`,
          method: 'GET',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`
          },
          success: function(res) {
            console.log('获取收入统计成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '获取收入统计失败'));
            }
          },
          fail: function(err) {
            console.log('获取收入统计失败:', err);
            reject(err);
          }
        });
      });
    }
  },
  
  location: {
    // 更新位置
    async updateLocation(latitude, longitude, accuracy) {
      // 防止重复调用
      if (isUpdatingLocation.inProgress) {
        console.log('位置更新已在进行中，跳过重复调用');
        return Promise.resolve({ message: '位置更新已在进行中' });
      }
      
      console.log('更新位置:', { latitude, longitude, accuracy });
      
      isUpdatingLocation.inProgress = true;
      
      return new Promise((resolve, reject) => {
        uni.request({
          url: 'http://127.0.0.1:7678/api/v1/deliver/location',
          method: 'POST',
          header: {
            'Authorization': `Bearer ${uni.getStorageSync('token')}`,
            'Content-Type': 'application/json'
          },
          data: {
            latitude: latitude.toString(),
            longitude: longitude.toString(),
            accuracy: accuracy
          },
          success: function(res) {
            console.log('更新位置成功:', res);
            if (res.statusCode === 200) {
              resolve(res.data);
            } else {
              reject(new Error(res.data?.detail || '更新位置失败'));
            }
          },
          fail: function(err) {
            console.log('更新位置失败:', err);
            reject(err);
          },
          complete: function() {
            // 无论成功失败，都重置标志
            isUpdatingLocation.inProgress = false;
          }
        });
      });
    }
  },
  
  schedule: {
        // 获取排班列表
        async getSchedules(params = {}) {
            console.log('获取排班列表:', params);
            
            const query = Object.keys(params)
                .map(key => `${key}=${encodeURIComponent(params[key])}`)
                .join('&');
            
            return new Promise((resolve, reject) => {
                uni.request({
                    url: `http://127.0.0.1:7678/api/v1/admin/staff-schedules${query ? `?${query}` : ''}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('token')}`
                    },
                    success: function(res) {
                        console.log('获取排班列表成功:', res);
                        if (res.statusCode === 200) {
                            resolve(res.data);
                        } else {
                            reject(new Error(res.data?.detail || '获取排班列表失败'));
                        }
                    },
                    fail: function(err) {
                        console.log('获取排班列表失败:', err);
                        reject(err);
                    }
                });
            });
        },
        
        // 获取月度排班
        async getMonthSchedules(params) {
            console.log('获取月度排班:', params);
            
            const query = Object.keys(params)
                .map(key => `${key}=${encodeURIComponent(params[key])}`)
                .join('&');
            
            return new Promise((resolve, reject) => {
                uni.request({
                    url: `http://127.0.0.1:7678/api/v1/admin/staff-schedules/month?${query}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('token')}`
                    },
                    success: function(res) {
                        console.log('获取月度排班成功:', res);
                        if (res.statusCode === 200) {
                            resolve(res.data);
                        } else {
                            reject(new Error(res.data?.detail || '获取月度排班失败'));
                        }
                    },
                    fail: function(err) {
                        console.log('获取月度排班失败:', err);
                        reject(err);
                    }
                });
            });
        }
    },
    
    reviews: {
        // 获取配送员评价列表
        async getReviews(page = 1, limit = 20) {
            console.log('获取配送员评价列表:', { page, limit });
            
            return new Promise((resolve, reject) => {
                uni.request({
                    url: `http://127.0.0.1:7678/api/v1/deliver/reviews?page=${page}&limit=${limit}`,
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('token')}`
                    },
                    success: function(res) {
                        console.log('获取评价列表成功:', res);
                        if (res.statusCode === 200) {
                            resolve(res.data);
                        } else {
                            reject(new Error(res.data?.detail || '获取评价列表失败'));
                        }
                    },
                    fail: function(err) {
                        console.log('获取评价列表失败:', err);
                        reject(err);
                    }
                });
            });
        }
    }
};
