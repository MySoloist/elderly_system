import axios from './axios.js';

export const messageService = {
    // 获取已读消息ID列表
    getReadMessageIds() {
        try {
            const readIds = uni.getStorageSync('readMessageIds');
            return readIds ? JSON.parse(readIds) : [];
        } catch (error) {
            console.error('获取已读消息ID失败:', error);
            return [];
        }
    },
    
    // 保存已读消息ID列表
    saveReadMessageIds(readIds) {
        try {
            uni.setStorageSync('readMessageIds', JSON.stringify(readIds));
        } catch (error) {
            console.error('保存已读消息ID失败:', error);
        }
    },
    
    // 获取消息列表
    async getMessages() {
        try {
            console.log('开始获取消息列表...');
            
            // 1. 从公告表获取系统通知
            console.log('获取公告数据...');
            const announcements = await axios.get('/member/announcements', {
                params: {
                    page: 1,
                    limit: 10
                }
            });
            console.log('公告数据:', announcements);
            
            // 2. 获取绑定的老人列表
            console.log('获取绑定老人数据...');
            const bindings = await axios.get('/member/bindings');
            console.log('绑定老人数据:', bindings);
            console.log('绑定老人数量:', bindings.length);
            bindings.forEach((bind, index) => {
                console.log(`绑定老人 ${index}:`, bind);
            });
            
            // 3. 获取每个老人的订单
            const orders = [];
            if (bindings && bindings.length > 0) {
                console.log(`找到 ${bindings.length} 个绑定的老人`);
                for (const binding of bindings) {
                    try {
                        console.log(`获取老人 ${binding.elderly_name} 的订单...`);
                        const elderOrders = await axios.get('/member/orders', {
                            params: {
                                elder_id: binding.elderly_id,
                                status: 'delivering,completed',
                                page: 1,
                                limit: 5
                            }
                        });
                        console.log(`老人 ${binding.elderly_name} 的订单数据:`, elderOrders);
                        if (elderOrders && elderOrders.data && elderOrders.data.items) {
                            orders.push(...elderOrders.data.items);
                        }
                    } catch (error) {
                        console.error(`获取老人 ${binding.elderly_name} 的订单失败:`, error);
                    }
                }
            } else {
                console.log('没有绑定的老人');
            }
            
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
                        timestamp: new Date(announcement.created_at).getTime(),
                        read: readMessageIds.includes(messageId),
                        content: announcement.content
                    });
                });
            } else {
                console.log('没有找到公告数据');
            }
            
            // 添加订单状态更新（作为一般通知）
            console.log(`找到 ${orders.length} 个订单`);
            orders.forEach(order => {
                const messageId = `order_${order.id}`;
                messages.push({
                    id: messageId,
                    type: 'notice',
                    icon: '📦',
                    title: '配送提醒',
                    preview: `订单 ${order.id} 状态已更新为 ${this.getOrderStatusText(order.status)}`,
                    time: this.formatTime(order.updated_at),
                    timestamp: new Date(order.updated_at).getTime(),
                    read: readMessageIds.includes(messageId),
                    content: `您的订单 ${order.id} 状态已更新为 ${this.getOrderStatusText(order.status)}。请及时关注订单状态。`
                });
            });
            
            // 获取老人发送的消息
            if (bindings && bindings.length > 0) {
                console.log(`开始处理 ${bindings.length} 个绑定老人的消息`);
                for (const binding of bindings) {
                    try {
                        console.log(`获取老人 ${binding.elderly_name} (ID: ${binding.elderly_id}) 的消息...`);
                        const emergencyCalls = await axios.get('/member/elderly-emergency-calls', {
                            elderly_id: binding.elderly_id,
                            emergency_type: 'in-wechat-app'
                        });
                        console.log(`老人 ${binding.elderly_name} 的消息API返回:`, emergencyCalls);
                        
                        // 直接使用emergencyCalls作为数据，因为axios返回的就是data
                        const callData = emergencyCalls || [];
                        console.log(`找到 ${callData.length} 条消息`);
                        callData.forEach(call => {
                                console.log(`处理消息:`, call);
                                const messageId = `message_${call.id}`;
                                // 提取消息内容
                                console.log(`原始消息内容:`, call.message);
                                let messageContent = call.message;
                                // 尝试提取消息内容
                                const contentMatch = call.message.match(/发送消息(：|:)\s*(.+)/);
                                if (contentMatch && contentMatch[2]) {
                                    messageContent = contentMatch[2];
                                }
                                console.log(`提取的消息内容:`, messageContent);
                                
                                const newMessage = {
                                    id: messageId,
                                    type: 'emergency',
                                    icon: '📩',
                                    title: `${binding.elderly_name}的消息`,
                                    preview: messageContent.substring(0, 50) + (messageContent.length > 50 ? '...' : ''),
                                    time: this.formatTime(call.created_at),
                                    timestamp: new Date(call.created_at).getTime(),
                                    read: readMessageIds.includes(messageId),
                                    content: `${binding.elderly_name}通过微信小程序给您发送了消息：${messageContent}`
                                };
                                console.log(`添加消息:`, newMessage);
                                messages.push(newMessage);
                            });
                        
                        // 如果没有消息，显示提示
                        if (callData.length === 0) {
                            console.log(`老人 ${binding.elderly_name} 没有消息`);
                        }
                    } catch (error) {
                        console.error(`获取老人 ${binding.elderly_name} 的消息失败:`, error);
                    }
                }
            } else {
                console.log('没有绑定的老人');
            }
            
            // 按时间戳排序，最新的消息显示在最前面
            messages.sort((a, b) => b.timestamp - a.timestamp);
            
            console.log('最终消息列表:', messages);
            console.log('消息总数:', messages.length);
            console.log('紧急消息数量:', messages.filter(msg => msg.type === 'emergency').length);
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
            return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        } else if (days === 1) {
            return '昨天';
        } else if (days < 7) {
            return `${days}天前`;
        } else {
            return date.toLocaleDateString('zh-CN');
        }
    },
    
    // 获取订单状态文本
    getOrderStatusText(status) {
        const statusMap = {
            'pending_payment': '待支付',
            'pending_accept': '待接单',
            'delivering': '配送中',
            'completed': '已完成',
            'cancelled': '已取消'
        };
        return statusMap[status] || status;
    },
    

};
