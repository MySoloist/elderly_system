// 认证服务
export const authService = {
  // 登录
  async login(username, password) {
    console.log('=== 开始登录 ===');
    console.log('账号:', username);
    console.log('密码:', password);
    
    // 直接使用uni.request发送请求
    return new Promise((resolve, reject) => {
      uni.request({
        url: 'http://127.0.0.1:7678/api/v1/auth/login',
        method: 'POST',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&grant_type=password`,
        success: function(res) {
          console.log('=== 请求成功 ===');
          console.log('状态码:', res.statusCode);
          console.log('响应数据:', res.data);
          
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '登录失败'));
          }
        },
        fail: function(err) {
          console.log('=== 请求失败 ===');
          console.log('错误信息:', err);
          reject(err);
        },
        complete: function() {
          console.log('=== 请求完成 ===');
        }
      });
    });
  },
  
  // 注册
  async register(registerData) {
    console.log('=== 开始注册 ===');
    console.log('注册数据:', registerData);
    
    return new Promise((resolve, reject) => {
      uni.request({
        url: 'http://127.0.0.1:7678/api/v1/auth/register',
        method: 'POST',
        header: {
          'Content-Type': 'application/json'
        },
        data: registerData,
        success: function(res) {
          console.log('=== 注册请求成功 ===');
          console.log('状态码:', res.statusCode);
          console.log('响应数据:', res.data);
          
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '注册失败'));
          }
        },
        fail: function(err) {
          console.log('=== 注册请求失败 ===');
          console.log('错误信息:', err);
          reject(err);
        },
        complete: function() {
          console.log('=== 注册请求完成 ===');
        }
      });
    });
  },
  
  // 获取当前用户信息
  async getCurrentUser() {
    console.log('=== 获取当前用户信息 ===');
    
    return new Promise((resolve, reject) => {
      uni.request({
        url: 'http://127.0.0.1:7678/api/v1/auth/profile',
        method: 'GET',
        header: {
          'Authorization': `Bearer ${uni.getStorageSync('token')}`
        },
        success: function(res) {
          console.log('=== 获取用户信息成功 ===');
          console.log('状态码:', res.statusCode);
          console.log('响应数据:', res.data);
          
          if (res.statusCode === 200) {
            // 返回用户的姓名、手机号和头像信息
            const userData = {
              name: res.data.profile?.name || res.data.username || '用户',
              phone: res.data.profile?.phone || '',
              avatar: res.data.profile?.avatar || ''
            };
            resolve(userData);
          } else {
            reject(new Error(res.data?.detail || '获取用户信息失败'));
          }
        },
        fail: function(err) {
          console.log('=== 获取用户信息失败 ===');
          console.log('错误信息:', err);
          reject(err);
        },
        complete: function() {
          console.log('=== 获取用户信息请求完成 ===');
        }
      });
    });
  },
  
  // 微信登录
  async wechatLogin(code, userType) {
    console.log('=== 开始微信登录 ===');
    console.log('微信登录码:', code);
    console.log('用户类型:', userType);
    
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
          console.log('=== 微信登录请求成功 ===');
          console.log('状态码:', res.statusCode);
          console.log('响应数据:', res.data);
          
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '微信登录失败'));
          }
        },
        fail: function(err) {
          console.log('=== 微信登录请求失败 ===');
          console.log('错误信息:', err);
          reject(err);
        },
        complete: function() {
          console.log('=== 微信登录请求完成 ===');
        }
      });
    });
  }
};