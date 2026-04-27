import apiClient from './axios';

export const authService = {
  // 登录
  login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 获取个人资料
  getProfile() {
    return apiClient.get('/auth/profile');
  },

  // 修改密码
  changePassword(oldPassword, newPassword) {
    return apiClient.post('/auth/change-password', {
      old_password: oldPassword,
      new_password: newPassword
    });
  },

  // 注册用户
  register(username, password, userType, profile) {
    return apiClient.post('/auth/register', {
      username,
      password,
      user_type: userType,
      profile
    });
  }
};