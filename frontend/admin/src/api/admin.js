import apiClient from './axios';

export const adminService = {
  // 获取仪表盘数据
  getDashboard() {
    return apiClient.get('/admin/dashboard');
  },

  // 获取订单列表
  getOrders(params) {
    return apiClient.get('/admin/orders', { params });
  },

  // 获取订单详情
  getOrderDetail(orderId) {
    return apiClient.get(`/admin/orders/${orderId}`);
  },

  // 更新订单状态
  updateOrderStatus(orderId, status) {
    return apiClient.put(`/admin/orders/${orderId}/status`, { status });
  },

  // 快速下单
  quickOrder(orderData) {
    return apiClient.post('/admin/orders/quick', orderData);
  },

  // 指派配送员
  assignDelivery(assignData) {
    return apiClient.post('/admin/deliveries/assign', assignData);
  },

  // 获取用户列表
  getUsers(params) {
    return apiClient.get('/admin/users', { params });
  },

  // 获取老人用户列表
  getElderlyUsers(params) {
    return apiClient.get('/admin/users/elderly', { params });
  },

  // 获取家属用户列表
  getMemberUsers(params) {
    return apiClient.get('/admin/users/members', { params });
  },

  // 获取配送员列表
  getDelivererUsers(params) {
    return apiClient.get('/admin/users/deliverers', { params });
  },

  // 获取餐品列表
  getMeals(params) {
    return apiClient.get('/admin/meals', { params });
  },

  // 创建餐品
  createMeal(mealData) {
    return apiClient.post('/admin/meals', mealData);
  },

  // 更新餐品
  updateMeal(mealId, mealData) {
    return apiClient.put(`/admin/meals/${mealId}`, mealData);
  },

  // 删除餐品
  deleteMeal(mealId) {
    return apiClient.delete(`/admin/meals/${mealId}`);
  },

  // 获取统计数据
  getStatistics(params) {
    return apiClient.get('/admin/statistics', { params });
  },

  // 获取社区列表
  getCommunities(params) {
    return apiClient.get('/admin/communities', { params });
  },

  // 创建社区
  createCommunity(communityData) {
    return apiClient.post('/admin/communities', communityData);
  },

  // 更新社区
  updateCommunity(communityId, communityData) {
    return apiClient.put(`/admin/communities/${communityId}`, communityData);
  },

  // 删除社区
  deleteCommunity(communityId) {
    return apiClient.delete(`/admin/communities/${communityId}`);
  },

  // 获取通知列表
  getAnnouncements(params) {
    return apiClient.get('/admin/announcements', { params });
  },

  // 创建通知
  createAnnouncement(announcementData) {
    return apiClient.post('/admin/announcements', announcementData);
  },

  // 更新通知
  updateAnnouncement(announcementId, announcementData) {
    return apiClient.put(`/admin/announcements/${announcementId}`, announcementData);
  },

  // 删除通知
  deleteAnnouncement(announcementId) {
    return apiClient.delete(`/admin/announcements/${announcementId}`);
  },

  // 获取评价列表
  getReviews(params) {
    return apiClient.get('/admin/reviews', { params });
  },

  // 创建评价
  createReview(reviewData) {
    return apiClient.post('/admin/reviews', reviewData);
  },

  // 更新评价
  updateReview(reviewId, reviewData) {
    return apiClient.put(`/admin/reviews/${reviewId}`, reviewData);
  },

  // 删除评价
  deleteReview(reviewId) {
    return apiClient.delete(`/admin/reviews/${reviewId}`);
  },

  // AI批量审核评价
  batchAIReview() {
    return apiClient.post('/admin/reviews/ai-review/batch', {}, { timeout: 60000 });
  },

  // 单个评价AI审核
  aiReviewSingle(reviewId) {
    return apiClient.post(`/admin/reviews/${reviewId}/ai-review`, {}, { timeout: 60000 });
  },

  // 应用AI审核结果
  applyAIReview(reviewIds) {
    return apiClient.post('/admin/reviews/ai-review/apply', reviewIds);
  },

  // AI回复相关方法
  aiReplySingle(reviewId) {
    return apiClient.post(`/admin/reviews/${reviewId}/ai-reply`, {}, { timeout: 60000 });
  },

  // 批量AI回复
  batchAIReply() {
    return apiClient.post('/admin/reviews/ai-reply/batch', {}, { timeout: 60000 });
  },

  // 应用AI回复
  applyAIReply(reviewId, replyContent) {
    return apiClient.post(`/admin/reviews/${reviewId}/apply-reply`, { reply_content: replyContent });
  },

  // 批量审核通过
  batchApprove(reviewIds) {
    return apiClient.post('/admin/reviews/batch-approve', { review_ids: reviewIds });
  },
  
  // AI分析评价数据
  analyzeReviews() {
    return apiClient.get('/admin/reviews/analysis');
  },

  // 个人中心相关方法
  getProfile() {
    return apiClient.get('/admin/profile');
  },

  updateProfile(profileData) {
    return apiClient.put('/admin/profile', profileData);
  },

  changePassword(passwordData) {
    return apiClient.post('/admin/profile/password', passwordData);
  },

  updateSecuritySettings(securityData) {
    return apiClient.put('/admin/profile/security', securityData);
  },

  // AI设置相关方法
  getAISettings() {
    return apiClient.get('/admin/settings/ai');
  },

  updateAISettings(aiData) {
    return apiClient.put('/admin/settings/ai', aiData);
  },

  getAIModels(apiUrl, apiKey) {
    return apiClient.get('/admin/settings/ai/models', {
      params: { api_url: apiUrl, api_key: apiKey }
    });
  },

  // 备份相关方法
  createBackup() {
    return apiClient.post('/admin/backup');
  },

  getBackupList() {
    return apiClient.get('/admin/backups');
  },

  downloadBackup(filename) {
    return apiClient.get(`/admin/backup/${filename}`, {
      responseType: 'blob'
    });
  },

  restoreBackup(filename) {
    return apiClient.post(`/admin/backup/restore/${filename}`);
  },

  // 获取标签列表
  getTags() {
    return apiClient.get('/admin/tags');
  },
  
  // 获取分类列表
  getCategories() {
    return apiClient.get('/admin/categories');
  },
  
  // 获取健康标签列表
  getHealthTags() {
    return apiClient.get('/admin/health-tags');
  },
  
  // 获取老人家属绑定关系列表
  getElderMemberRelations(params) {
    return apiClient.get('/admin/elder-member-relations', { params });
  },
  
  // 创建老人家属绑定关系
  createElderMemberRelation(relationData) {
    return apiClient.post('/admin/elder-member-relations', relationData);
  },
  
  // 创建用户
  createUser(userData) {
    return apiClient.post('/admin/users', userData);
  },
  
  // 更新用户
  updateUser(userId, userData) {
    return apiClient.put(`/admin/users/${userId}`, userData);
  },
  
  // 删除用户
  deleteUser(userId) {
    return apiClient.delete(`/admin/users/${userId}`);
  },

  // 获取配送异常列表
  getExceptions(params) {
    return apiClient.get('/deliver/exceptions', { params });
  },

  // 排班管理相关方法
  getStaffSchedules(params) {
    return apiClient.get('/admin/staff-schedules', { params });
  },

  createStaffSchedule(scheduleData) {
    return apiClient.post('/admin/staff-schedules', scheduleData);
  },

  updateStaffSchedule(scheduleId, scheduleData) {
    return apiClient.put(`/admin/staff-schedules/${scheduleId}`, scheduleData);
  },

  deleteStaffSchedule(scheduleId) {
    return apiClient.delete(`/admin/staff-schedules/${scheduleId}`);
  },

  getMonthSchedules(params) {
    return apiClient.get('/admin/staff-schedules/month', { params });
  },

  // 获取配送员实时位置
  getDelivererLocations(params) {
    return apiClient.get('/admin/deliverer-locations', { params });
  },

  

};