import { api } from '../utils/api.js';

export const messageService = {
    // 获取已读消息ID列表
    getReadMessageIds() {
        try {
            const readIds = uni.getStorageSync('deliverReadMessageIds');
            return readIds ? JSON.parse(readIds) : [];
        } catch (error) {
            console.error('获取已读消息ID失败:', error);
            return [];
        }
    },
    
    // 保存已读消息ID列表
    saveReadMessageIds(readIds) {
        try {
            uni.setStorageSync('deliverReadMessageIds', JSON.stringify(readIds));
        } catch (error) {
            console.error('保存已读消息ID失败:', error);
        }
    },
    
    // 获取消息列表
    async getMessages() {
        try {
            console.log('开始获取消息列表...');
            
            // 使用Promise方式调用API
            const announcements = await new Promise((resolve, reject) => {
                uni.request({
                    url: 'http://127.0.0.1:7678/api/v1/older/announcements?page=1&limit=10',
                    method: 'GET',
                    header: {
                        'Authorization': `Bearer ${uni.getStorageSync('token')}`
                    },
                    success: function(res) {
                        console.log('公告数据:', res);
                        if (res.statusCode === 200) {
                            resolve(res.data);
                        } else {
                            reject(new Error(res.data?.detail || '获取公告失败'));
                        }
                    },
                    fail: function(err) {
                        console.log('获取公告失败:', err);
                        reject(err);
                    }
                });
            });
            
            // 获取已读消息ID列表
            const readMessageIds = this.getReadMessageIds();
            
            // 整合消息数据
            const messages = [];
            
            // 添加公告消息（根据公告类型分类）
            if (announcements && announcements.items) {
                console.log(`找到 ${announcements.items.length} 条公告`);
                announcements.items.forEach(announcement => {
                    let messageType = 'notice'; // 默认一般通知
                    let icon = '📢';
                    
                    if (announcement.type === 'system') {
                        messageType = 'system';
                        icon = '📢';
                    } else if (announcement.type === 'emergency') {
                        messageType = 'emergency';
                        icon = '🚨';
                    }
                    
                    const messageId = `announcement_${announcement.id}`;
                    messages.push({
                        id: messageId,
                        type: messageType,
                        icon: icon,
                        title: announcement.title,
                        preview: announcement.content.substring(0, 50) + (announcement.content.length > 50 ? '...' : ''),
                        time: this.formatTime(announcement.created_at),
                        read: readMessageIds.includes(messageId),
                        content: announcement.content
                    });
                });
            } else {
                console.log('没有找到公告数据');
            }
            
            // 按时间排序
            messages.sort((a, b) => new Date(b.time) - new Date(a.time));
            
            console.log('最终消息列表:', messages);
            return messages;
        } catch (error) {
            console.error('获取消息列表失败:', error);
            // 如果获取失败，返回空数组
            return [];
        }
    },
    
    // 获取未读消息数量
    async getUnreadCount() {
        try {
            const messages = await this.getMessages();
            return messages.filter(msg => !msg.read).length;
        } catch (error) {
            console.error('获取未读消息数量失败:', error);
            return 0;
        }
    },
    
    // 标记消息为已读
    async markAsRead(messageId) {
        try {
            // 获取当前已读消息ID列表
            const readMessageIds = this.getReadMessageIds();
            
            // 如果消息还未标记为已读，添加到已读列表
            if (!readMessageIds.includes(messageId)) {
                readMessageIds.push(messageId);
                this.saveReadMessageIds(readMessageIds);
            }
            
            console.log('标记消息为已读:', messageId);
            return { success: true };
        } catch (error) {
            console.error('标记消息为已读失败:', error);
            throw error;
        }
    },
    
    // 清除所有消息
    async clearAll() {
        try {
            // 清除localStorage中的已读消息ID
            this.saveReadMessageIds([]);
            console.log('清除所有消息');
            return { success: true };
        } catch (error) {
            console.error('清除消息失败:', error);
            throw error;
        }
    },
    
    // 格式化时间
    formatTime(timeString) {
        const date = new Date(timeString);
        const now = new Date();
        const diff = now - date;
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        
        if (days === 0) {
            return '今天';
        } else if (days === 1) {
            return '昨天';
        } else if (days < 7) {
            return `${days}天前`;
        } else {
            return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
        }
    }
};