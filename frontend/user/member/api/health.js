import axios from './axios.js';

export const healthService = {
    // 发送健康提醒
    async sendHealthReminder(reminderData) {
        try {
            const response = await axios.post('/member/health-reminders', reminderData);
            return response;
        } catch (error) {
            console.error('发送健康提醒失败:', error);
            throw error;
        }
    },
    
    // 获取健康提醒列表
    async getHealthReminders(params) {
        try {
            const response = await axios.get('/member/health-reminders', params);
            return response;
        } catch (error) {
            console.error('获取健康提醒列表失败:', error);
            throw error;
        }
    },
    
    // 获取AI健康建议
    async getHealthAdvice(elderlyId) {
        try {
            const response = await axios.get(`/member/health-advice/${elderlyId}`);
            return response;
        } catch (error) {
            console.error('获取健康建议失败:', error);
            throw error;
        }
    }
};
