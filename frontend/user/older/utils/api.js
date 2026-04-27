// 导入配置
import CONFIG from './config.js';

// 通用请求方法
async function request(url, options = {}) {
  const token = uni.getStorageSync(CONFIG.storage.tokenKey);
  
  const defaultOptions = {
    url: `${CONFIG.api.baseUrl}${url}`,
    timeout: CONFIG.api.timeout,
    header: {
      ...CONFIG.api.headers,
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    ...options
  };
  
  console.log('请求选项:', defaultOptions);
  
  try {
    console.log('开始发送请求...');
    const response = await uni.request(defaultOptions);
    console.log('请求响应:', response);
    
    if (response.statusCode === 200) {
      console.log('请求成功，返回数据:', response.data);
      return response.data;
    } else if (response.statusCode === 401) {
      // Token过期，清除登录状态
      uni.removeStorageSync('token');
      uni.removeStorageSync('user');
      uni.showToast({
        title: '登录已过期，请重新登录',
        icon: 'none'
      });
      setTimeout(() => {
        uni.reLaunch({
          url: '/pages/login/login'
        });
      }, 1500);
      throw new Error('未授权');
    } else {
      console.error('请求失败，状态码:', response.statusCode);
      console.error('错误信息:', response.data);
      uni.showToast({
        title: response.data?.detail || '请求失败',
        icon: 'none'
      });
      throw new Error(response.data?.detail || '请求失败');
    }
  } catch (error) {
    console.error('API请求错误:', error);
    throw error;
  }
}

// API接口
export const api = {
  // 认证相关
  auth: {
    login: (data) => {
      console.log('登录请求数据:', data);
      const formData = `username=${encodeURIComponent(data.username)}&password=${encodeURIComponent(data.password)}&grant_type=password`;
      console.log('格式化后的表单数据:', formData);
      console.log('请求URL:', `${CONFIG.api.baseUrl}/auth/login`);
      
      return request('/auth/login', {
        method: 'POST',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: formData
      });
    },
    register: (data) => request('/auth/register', {
      method: 'POST',
      data
    }),
    getProfile: () => request('/auth/profile'),
    updateProfile: (data) => request('/auth/profile', {
      method: 'PUT',
      data
    }),
    changePassword: (data) => request('/auth/change-password', {
      method: 'POST',
      data
    }),
    wechatLogin: (data) => request('/auth/wechat-login', {
      method: 'POST',
      data
    })
  },
  
  // 老人端相关
    older: {
        // 餐品相关
        getMeals: (params) => {
            let url = '/older/meals';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        // 获取分类列表
        getCategories: () => request('/older/categories'),
        // 获取标签列表
        getTags: () => request('/older/tags'),
        
        // 订单相关
        createOrder: (data) => request('/older/orders', {
            method: 'POST',
            data
        }),
        getOrders: (params) => {
            let url = '/older/orders';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        getOrder: (orderId) => request(`/older/orders/${orderId}`),
        cancelOrder: (orderId) => request(`/older/orders/${orderId}`, {
            method: 'DELETE'
        }),
        payOrder: (orderId, data) => request(`/older/orders/${orderId}/pay`, {
            method: 'POST',
            data
        }),
        
        // 收藏相关
        addFavorite: (mealId) => request(`/older/favorites?meal_id=${mealId}`, {
            method: 'POST'
        }),
        getFavorites: () => request('/older/favorites'),
        removeFavorite: (mealId) => request(`/older/favorites/${mealId}`, {
            method: 'DELETE'
        }),
        
        // 评价相关
        submitReview: (data) => request('/older/reviews', {
            method: 'POST',
            data
        }),
        getReviews: () => request('/older/reviews'),
        
        // 健康记录相关
        getHealthRecords: () => request('/older/health-records'),
        createHealthRecord: (data) => request('/older/health-records', {
            method: 'POST',
            data
        }),
        updateHealthRecord: (recordId, data) => request(`/older/health-records/${recordId}`, {
            method: 'PUT',
            data
        }),
        deleteHealthRecord: (recordId) => request(`/older/health-records/${recordId}`, {
            method: 'DELETE'
        }),
        
        // 饮食偏好相关
        getPreferences: () => request('/older/preferences'),
        updatePreferences: (data) => request('/older/preferences', {
            method: 'PUT',
            data
        }),
        
        // 紧急联系人相关
        getMembers: () => request('/older/members'),
        getEmergencyContacts: () => request('/older/emergency-contacts'),
        setEmergencyContactAsPrimary: (contactId) => request(`/older/emergency-contacts/${contactId}/primary`, {
            method: 'PUT'
        }),
        
        // 发送消息相关
        sendMessage: (contactId, content) => request('/older/send-message', {
            method: 'POST',
            data: {
                contact_id: contactId,
                content: content
            }
        }),
        
        // 紧急呼叫相关
        createEmergencyCall: (data) => request('/older/emergency-calls', {
            method: 'POST',
            data
        }),
        
        // AI助手相关
        sendAIQuery: (data) => request('/older/ai/query', {
            method: 'POST',
            data
        }),
        getAIConversations: () => request('/older/ai/conversations'),
        // 语音合成相关
        textToSpeech: (data) => request('/older/ai/tts', {
            method: 'POST',
            data
        }),
        getVoiceRecords: () => request('/older/ai/voice-records'),
        // 获取阿里云Token
        getAliyunToken: () => request('/older/ai/aliyun-token'),
        
        // AI推荐相关
        getAIRecommendations: () => request('/older/ai/recommendations'),
        
        // 公告相关
        getAnnouncements: (params) => {
            let url = '/older/announcements';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        getAnnouncement: (announcementId) => request(`/older/announcements/${announcementId}`),
        
        // 健康提醒相关
        getHealthReminders: (params) => {
            let url = '/older/health-reminders';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        markHealthReminderAsRead: (reminderId) => request(`/older/health-reminders/${reminderId}/read`, {
            method: 'PUT'
        })
    },
  
  // 家属端相关
    member: {
        // 老人管理
        getElders: () => request('/member/elders'),
        bindElder: (data) => request('/member/elders', {
            method: 'POST',
            data
        }),
        
        // 订单管理
        getOrders: (params) => {
            let url = '/member/orders';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        createOrder: (data) => request('/member/orders', {
            method: 'POST',
            data
        }),
        trackOrder: (orderId) => request(`/member/orders/${orderId}/track`),
        
        // 健康管理
        getHealth: (elderId) => request(`/member/health/${elderId}`),
        addHealthRecord: (elderId, data) => request(`/member/health/${elderId}`, {
            method: 'POST',
            data
        })
    },
    
    // 配送员端相关
    deliver: {
        // 订单管理
        getAvailableOrders: (params) => {
            let url = '/deliver/orders';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        acceptOrder: (orderId) => request(`/deliver/orders/${orderId}/accept`, {
            method: 'PUT'
        }),
        completeOrder: (orderId, data) => request(`/deliver/orders/${orderId}/complete`, {
            method: 'PUT',
            data
        }),
        getDeliveringOrders: () => request('/deliver/orders/delivering'),
        
        // 位置更新
        updateLocation: (data) => request('/deliver/location', {
            method: 'POST',
            data
        }),
        
        // 收入统计
        getIncome: (params) => {
            let url = '/deliver/income';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        
        // 异常处理
        reportException: (data) => request('/deliver/exceptions', {
            method: 'POST',
            data
        }),
        getExceptions: (params) => {
            let url = '/deliver/exceptions';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        }
    },
    
    // 管理端相关
    admin: {
        // 工作台
        getDashboard: () => request('/admin/dashboard'),
        
        // 用户管理
        getUsers: (params) => {
            let url = '/admin/users';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        
        // 订单管理
        getOrders: (params) => {
            let url = '/admin/orders';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        
        // 餐品管理
        getMeals: (params) => {
            let url = '/admin/meals';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        },
        createMeal: (data) => request('/admin/meals', {
            method: 'POST',
            data
        }),
        updateMeal: (mealId, data) => request(`/admin/meals/${mealId}`, {
            method: 'PUT',
            data
        }),
        deleteMeal: (mealId) => request(`/admin/meals/${mealId}`, {
            method: 'DELETE'
        }),
        
        // 统计分析
        getStatistics: (params) => {
            let url = '/admin/statistics';
            if (params) {
                const queryString = Object.keys(params)
                    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
                    .join('&');
                url += `?${queryString}`;
            }
            return request(url);
        }
    }
};

export default api;