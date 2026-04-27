// 绑定管理API服务
export const bindService = {
  // 获取绑定列表
  async getBindList() {
    console.log('获取绑定列表...');
    
    return new Promise((resolve, reject) => {
      uni.request({
        url: 'http://127.0.0.1:7678/api/v1/member/bindings',
        method: 'GET',
        header: {
          'Authorization': `Bearer ${uni.getStorageSync('token')}`
        },
        success: function(res) {
          console.log('获取绑定列表成功:', res);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '获取绑定列表失败'));
          }
        },
        fail: function(err) {
          console.log('获取绑定列表失败:', err);
          reject(err);
        }
      });
    });
  },
  
  // 添加绑定
  async addBind(bindData) {
    console.log('添加绑定:', bindData);
    
    return new Promise((resolve, reject) => {
      uni.request({
        url: 'http://127.0.0.1:7678/api/v1/member/bindings',
        method: 'POST',
        header: {
          'Authorization': `Bearer ${uni.getStorageSync('token')}`,
          'Content-Type': 'application/json'
        },
        data: bindData,
        success: function(res) {
          console.log('添加绑定成功:', res);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '添加绑定失败'));
          }
        },
        fail: function(err) {
          console.log('添加绑定失败:', err);
          reject(err);
        }
      });
    });
  },
  
  // 更新绑定
  async updateBind(bindId, bindData) {
    console.log('更新绑定:', bindId, bindData);
    
    return new Promise((resolve, reject) => {
      uni.request({
        url: `http://127.0.0.1:7678/api/v1/member/bindings/${bindId}`,
        method: 'PUT',
        header: {
          'Authorization': `Bearer ${uni.getStorageSync('token')}`,
          'Content-Type': 'application/json'
        },
        data: bindData,
        success: function(res) {
          console.log('更新绑定成功:', res);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '更新绑定失败'));
          }
        },
        fail: function(err) {
          console.log('更新绑定失败:', err);
          reject(err);
        }
      });
    });
  },
  
  // 删除绑定
  async deleteBind(bindId) {
    console.log('删除绑定:', bindId);
    
    return new Promise((resolve, reject) => {
      uni.request({
        url: `http://127.0.0.1:7678/api/v1/member/bindings/${bindId}`,
        method: 'DELETE',
        header: {
          'Authorization': `Bearer ${uni.getStorageSync('token')}`
        },
        success: function(res) {
          console.log('删除绑定成功:', res);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(res.data?.detail || '删除绑定失败'));
          }
        },
        fail: function(err) {
          console.log('删除绑定失败:', err);
          reject(err);
        }
      });
    });
  }
};
