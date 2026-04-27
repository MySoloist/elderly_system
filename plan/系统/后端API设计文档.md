# 老年人社区餐饮配送系统 - 后端API设计文档

## 1. 概述

本文档详细描述老年人社区餐饮配送系统的后端API设计方案，基于Python 3.12 + FastAPI技术栈，提供完整的RESTful API接口，支持四个前端端：老人端、家属端、配送员端和管理端。

## 2. API架构

### 2.1 技术栈
- **后端框架**：FastAPI
- **认证方式**：JWT + OAuth2
- **数据验证**：Pydantic
- **API文档**：Swagger UI + ReDoc

### 2.2 API版本控制
- 基础路径：`/api/v1`
- 未来版本升级支持

### 2.3 认证机制
- 使用Bearer Token认证
- Token有效期：2小时
- 支持Token刷新机制

## 3. 认证API

### 3.1 用户登录
```
POST /api/v1/auth/login
```

**请求体**：
```json
{
  "username": "string",
  "password": "string"
}
```

**响应**：
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "string",
    "user_type": "elderly",
    "profile": {
      "name": "string",
      "phone": "string"
    }
  }
}
```

### 3.2 用户注册
```
POST /api/v1/auth/register
```

**请求体**：
```json
{
  "username": "string",
  "password": "string",
  "user_type": "elderly",
  "profile": {
    "name": "string",
    "phone": "string"
  }
}
```

**响应**：
```json
{
  "id": 1,
  "username": "string",
  "user_type": "elderly",
  "status": "active"
}
```

### 3.3 获取用户信息
```
GET /api/v1/auth/profile
```

**响应**：
```json
{
  "id": 1,
  "username": "string",
  "user_type": "elderly",
  "profile": {
    "name": "string",
    "phone": "string",
    "address": "string",
    "health_status": "string",
    "dietary_preferences": "string"
  }
}
```

### 3.4 更新用户信息
```
PUT /api/v1/auth/profile
```

**请求体**：
```json
{
  "name": "string",
  "phone": "string",
  "address": "string",
  "health_status": "string",
  "dietary_preferences": "string"
}
```

**响应**：
```json
{
  "id": 1,
  "username": "string",
  "profile": {
    "name": "string",
    "phone": "string",
    "address": "string",
    "health_status": "string",
    "dietary_preferences": "string"
  }
}
```

### 3.5 修改密码
```
POST /api/v1/auth/change-password
```

**请求体**：
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**响应**：
```json
{
  "message": "密码修改成功"
}
```

## 4. 老人端API

### 4.1 分类和标签

#### 4.1.1 获取分类列表
```
GET /api/v1/older/categories
```

**响应**：
```json
{
  "categories": [
    {
      "id": 1,
      "name": "主食",
      "description": "主食类餐品"
    }
  ]
}
```

#### 4.1.2 获取标签列表
```
GET /api/v1/older/tags
```

**响应**：
```json
{
  "tags": [
    {
      "id": 1,
      "name": "低糖",
      "description": "适合糖尿病患者的低糖餐品"
    }
  ]
}
```

### 4.2 餐品管理

#### 4.2.1 获取餐品列表
```
GET /api/v1/older/meals
```

**查询参数**：
- `category_id`: 分类ID（可选）
- `tag_id`: 标签ID（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 100,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "name": "营养套餐A",
      "price": 28.00,
      "description": "营养均衡的套餐",
      "category_id": 1,
      "tag_id": 1,
      "special_tag": "低糖",
      "image_url": "string"
    }
  ]
}
```

### 4.3 订单管理

#### 4.3.1 创建订单
```
POST /api/v1/older/orders
```

**请求体**：
```json
{
  "items": [
    {
      "meal_id": 1,
      "quantity": 1
    }
  ],
  "delivery_address": "幸福小区3号楼2单元501室",
  "special_notes": "备注信息",
  "scheduled_time": "2024-01-15T12:00:00",
  "order_type": "immediate"
}
```

**响应**：
```json
{
  "id": 1,
  "total_amount": 28.00,
  "status": "pending_payment",
  "delivery_address": "幸福小区3号楼2单元501室",
  "created_at": "2024-01-15T10:00:00",
  "scheduled_time": "2024-01-15T12:00:00",
  "order_type": "immediate",
  "items": [
    {
      "id": 1,
      "meal_id": 1,
      "meal_name": "营养套餐A",
      "quantity": 1,
      "price": 28.00,
      "image_url": "string"
    }
  ]
}
```

#### 4.3.2 获取订单列表
```
GET /api/v1/older/orders
```

**查询参数**：
- `status`: 订单状态（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 50,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "total_amount": 28.00,
      "status": "completed",
      "delivery_address": "幸福小区3号楼2单元501室",
      "created_at": "2024-01-15T10:00:00",
      "scheduled_time": "2024-01-15T12:00:00",
      "order_type": "immediate",
      "items": [],
      "reviewed": false,
      "delivery": {
        "deliverer_id": 1,
        "deliverer_name": "李师傅",
        "deliverer_phone": "139****9012",
        "status": "delivered"
      }
    }
  ]
}
```

#### 4.3.3 获取订单详情
```
GET /api/v1/older/orders/{order_id}
```

**响应**：
```json
{
  "id": 1,
  "total_amount": 28.00,
  "status": "delivering",
  "delivery_address": "幸福小区3号楼2单元501室",
  "created_at": "2024-01-15T10:00:00",
  "scheduled_time": "2024-01-15T12:00:00",
  "order_type": "immediate",
  "items": [
    {
      "id": 1,
      "meal_id": 1,
      "meal_name": "营养套餐A",
      "quantity": 1,
      "price": 28.00,
      "image_url": "string"
    }
  ],
  "reviewed": false,
  "delivery": {
    "deliverer_id": 1,
    "deliverer_name": "李师傅",
    "deliverer_phone": "139****9012",
    "status": "in_transit"
  }
}
```

#### 4.3.4 取消订单
```
DELETE /api/v1/older/orders/{order_id}
```

**响应**：
```json
{
  "message": "订单取消成功",
  "order_id": 1,
  "status": "cancelled"
}
```

#### 4.3.5 支付订单
```
POST /api/v1/older/orders/{order_id}/pay
```

**请求体**：
```json
{
  "payment_method": "wechat"
}
```

**响应**：
```json
{
  "message": "支付成功",
  "order_id": 1,
  "payment_id": 1,
  "status": "paid"
}
```

### 4.4 餐品收藏

#### 4.4.1 获取收藏列表
```
GET /api/v1/older/favorites
```

**响应**：
```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "meal": {
        "id": 1,
        "name": "营养套餐A",
        "price": 28.00,
        "category": "主食",
        "image_url": "string"
      },
      "created_at": "2024-01-15T10:00:00"
    }
  ]
}
```

#### 4.4.2 添加收藏
```
POST /api/v1/older/favorites
```

**请求体**：
```json
{
  "meal_id": 1
}
```

**响应**：
```json
{
  "id": 1,
  "meal_id": 1,
  "created_at": "2024-01-15T10:00:00"
}
```

#### 4.4.3 删除收藏
```
DELETE /api/v1/older/favorites/{meal_id}
```

**响应**：
```json
{
  "message": "收藏已删除",
  "meal_id": 1
}
```

### 4.5 健康记录

#### 4.5.1 获取健康记录列表
```
GET /api/v1/older/health-records
```

**响应**：
```json
[
  {
    "id": 1,
    "height": 170.0,
    "weight": 65.0,
    "blood_pressure": "120/80",
    "blood_sugar": 5.6,
    "allergies": "海鲜过敏",
    "medications": "降压药",
    "doctor_advice": "注意休息",
    "recorded_at": "2024-01-15T10:00:00"
  }
]
```

#### 4.5.2 创建健康记录
```
POST /api/v1/older/health-records
```

**请求体**：
```json
{
  "height": 170.0,
  "weight": 65.0,
  "blood_pressure": "120/80",
  "blood_sugar": 5.6,
  "allergies": "海鲜过敏",
  "medications": "降压药",
  "doctor_advice": "注意休息"
}
```

**响应**：
```json
{
  "id": 1,
  "height": 170.0,
  "weight": 65.0,
  "blood_pressure": "120/80",
  "blood_sugar": 5.6,
  "allergies": "海鲜过敏",
  "medications": "降压药",
  "doctor_advice": "注意休息",
  "recorded_at": "2024-01-15T10:00:00"
}
```

#### 4.5.3 获取健康记录详情
```
GET /api/v1/older/health-records/{record_id}
```

**响应**：同创建健康记录响应

#### 4.5.4 更新健康记录
```
PUT /api/v1/older/health-records/{record_id}
```

**请求体**：同创建健康记录请求体

**响应**：同创建健康记录响应

#### 4.5.5 删除健康记录
```
DELETE /api/v1/older/health-records/{record_id}
```

**响应**：
```json
{
  "message": "健康记录删除成功",
  "record_id": 1
}
```

### 4.6 口味偏好

#### 4.6.1 获取口味偏好
```
GET /api/v1/older/preferences
```

**响应**：
```json
{
  "dietary_preferences": "低糖饮食，清淡口味"
}
```

#### 4.6.2 更新口味偏好
```
PUT /api/v1/older/preferences
```

**请求体**：
```json
{
  "dietary_preferences": "低糖饮食，清淡口味"
}
```

**响应**：
```json
{
  "message": "饮食偏好更新成功",
  "dietary_preferences": "低糖饮食，清淡口味"
}
```

### 4.7 紧急联系

#### 4.7.1 获取紧急联系人列表
```
GET /api/v1/older/emergency-contacts
```

**响应**：
```json
{
  "contacts": [
    {
      "id": 1,
      "name": "张小明",
      "relationship": "儿子",
      "phone": "138****5678",
      "is_primary": 0,
      "user_id": 2
    }
  ]
}
```

#### 4.7.2 设置主要联系人
```
PUT /api/v1/older/emergency-contacts/{contact_id}/primary
```

**响应**：
```json
{
  "id": 1,
  "name": "张小明",
  "relationship": "儿子",
  "phone": "138****5678",
  "is_primary": 0,
  "message": "设置主要联系人成功"
}
```

#### 4.7.3 创建紧急呼叫
```
POST /api/v1/older/emergency-calls
```

**请求体**：
```json
{
  "emergency_type": "medical",
  "message": "身体不适，需要紧急帮助"
}
```

**响应**：
```json
{
  "id": 1,
  "emergency_type": "medical",
  "record_message": "身体不适，需要紧急帮助",
  "created_at": "2024-01-15T10:00:00",
  "message": "紧急呼叫记录创建成功"
}
```

#### 4.7.4 发送消息给家属
```
POST /api/v1/older/send-message
```

**请求体**：
```json
{
  "contact_id": 1,
  "content": "我很好，不用担心"
}
```

**响应**：
```json
{
  "message": "消息发送成功",
  "call_id": 1
}
```

### 4.8 AI助手

#### 4.8.1 发送AI咨询
```
POST /api/v1/older/ai/query
```

**请求体**：
```json
{
  "query": "推荐适合高血压老人的餐品"
}
```

**响应**：
```json
{
  "response": "根据您的健康状况，推荐以下餐品：清蒸鱼、蔬菜沙拉、小米粥等低盐低脂餐品",
  "conversation_id": "conv_123456",
  "timestamp": "2024-01-15T10:00:00"
}
```

#### 4.8.2 获取对话历史
```
GET /api/v1/older/ai/conversations
```

**响应**：
```json
{
  "total": 20,
  "conversations": [
    {
      "id": 1,
      "conversation_id": "conv_123456",
      "user_query": "推荐适合高血压老人的餐品",
      "ai_response": "根据您的健康状况，推荐以下餐品...",
      "timestamp": "2024-01-15T10:00:00"
    }
  ]
}
```

#### 4.8.3 文本转语音
```
POST /api/v1/older/ai/tts
```

**请求体**：
```json
{
  "text": "您好，有什么可以帮您的吗？",
  "voice_type": "xiaoyun",
  "language": "zh_CN",
  "speed": 0.8
}
```

**响应**：
```json
{
  "voice_url": "http://localhost:7678/static/voice/xxx.mp3",
  "status": "completed",
  "record_id": 1,
  "timestamp": "2024-01-15T10:00:00"
}
```

#### 4.8.4 语音转文本
```
POST /api/v1/older/ai/speech-to-text
```

**请求体**：multipart/form-data，字段名`audio`，音频文件

**响应**：
```json
{
  "success": true,
  "message": "语音识别成功",
  "data": {
    "text": "我想吃米饭",
    "audio_url": "/static/uploads/audio/xxx.wav"
  }
}
```

#### 4.8.5 获取语音合成记录
```
GET /api/v1/older/ai/voice-records
```

**响应**：
```json
{
  "total": 10,
  "records": [
    {
      "id": 1,
      "text_content": "您好",
      "voice_url": "http://localhost:7678/static/voice/xxx.mp3",
      "voice_type": "xiaoyun",
      "status": "completed",
      "created_at": "2024-01-15T10:00:00",
      "completed_at": "2024-01-15T10:00:05"
    }
  ]
}
```

#### 4.8.6 获取阿里云语音Token
```
GET /api/v1/older/ai/aliyun-token
```

**响应**：
```json
{
  "success": true,
  "token": "xxx",
  "appkey": "xxx",
  "expire_time": 1234567890
}
```

#### 4.8.7 获取AI智能推荐
```
GET /api/v1/older/ai/recommendations
```

**响应**：
```json
{
  "recommendations": [
    {
      "id": 1,
      "name": "清蒸鱼",
      "price": 35.00,
      "image_url": "string",
      "tag_name": "低盐",
      "description": "新鲜清蒸鱼",
      "reasons": ["低盐饮食，适合血压偏高的老人"]
    }
  ]
}
```

### 4.9 评价管理

#### 4.9.1 获取评价列表
```
GET /api/v1/older/reviews
```

**响应**：
```json
{
  "total": 10,
  "reviews": [
    {
      "id": 1,
      "order_id": 1,
      "rating": 5,
      "content": "配送及时，服务周到",
      "status": "approved",
      "reply": "感谢您的评价",
      "created_at": "2024-01-15T10:00:00",
      "order": {
        "id": 1,
        "meal_name": "营养套餐A",
        "meal_image": "string"
      }
    }
  ]
}
```

#### 4.9.2 提交评价
```
POST /api/v1/older/reviews
```

**请求体**：
```json
{
  "order_id": 1,
  "rating": 5,
  "content": "配送及时，服务周到",
  "images": ["url1", "url2"],
  "deliverer_id": 1
}
```

**响应**：
```json
{
  "message": "评价提交成功",
  "review": {
    "id": 1,
    "order_id": 1,
    "rating": 5,
    "content": "配送及时，服务周到"
  }
}
```

### 4.10 公告管理

#### 4.10.1 获取公告列表
```
GET /api/v1/older/announcements
```

**查询参数**：
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 20,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "title": "端午节放假安排",
      "content": "端午节期间配送时间调整通知",
      "type": "notice",
      "priority": "normal",
      "status": "active",
      "created_at": "2024-06-01T10:00:00",
      "updated_at": "2024-06-01T10:00:00"
    }
  ]
}
```

#### 4.10.2 获取公告详情
```
GET /api/v1/older/announcements/{announcement_id}
```

**响应**：同公告列表项格式

### 4.11 健康提醒

#### 4.11.1 获取健康提醒列表
```
GET /api/v1/older/health-reminders
```

**查询参数**：
- `status`: 提醒状态（可选：pending/read）

**响应**：
```json
[
  {
    "id": 1,
    "sender_id": 2,
    "sender_name": "张小明",
    "reminder_type": "diet",
    "content": "记得按时吃药",
    "status": "pending",
    "scheduled_time": "2024-01-15T18:00:00",
    "sent_time": "2024-01-15T18:00:00",
    "read_time": null,
    "created_at": "2024-01-15T10:00:00"
  }
]
```

#### 4.11.2 标记提醒为已读
```
PUT /api/v1/older/health-reminders/{reminder_id}/read
```

**响应**：
```json
{
  "id": 1,
  "status": "read",
  "read_time": "2024-01-15T10:30:00"
}
```

### 4.12 其他接口

#### 4.12.1 获取所有家属列表
```
GET /api/v1/older/members
```

**响应**：
```json
{
  "members": [
    {
      "id": 2,
      "username": "member001",
      "name": "张小明",
      "phone": "138****5678"
    }
  ]
}
```

#### 4.12.2 上传图片
```
POST /api/v1/older/upload/image
```

**请求体**：multipart/form-data，字段名`file`，图片文件

**响应**：
```json
{
  "url": "http://localhost:7678/static/uploads/images/xxx.jpg"
}
```

#### 4.12.3 上传头像
```
POST /api/v1/older/avatar
```

**请求体**：multipart/form-data，字段名`avatar`，图片文件

**响应**：
```json
{
  "success": true,
  "message": "头像上传成功",
  "data": {
    "avatar_url": "http://localhost:7678/static/uploads/avatars/xxx.jpg"
  }
}
```

## 5. 家属端API

### 5.1 老人绑定管理

#### 5.1.1 获取绑定老人列表
```
GET /api/v1/member/bindings
```

**响应**：
```json
[
  {
    "id": 1,
    "elderly_id": 1,
    "elderly_name": "张奶奶",
    "elderly_age": 75,
    "elderly_gender": "female",
    "elderly_address": "幸福小区3号楼2单元501室",
    "relation": "母亲"
  }
]
```

#### 5.1.2 添加老人绑定
```
POST /api/v1/member/bindings
```

**请求体**：
```json
{
  "elderly_id": 1,
  "relation": "母亲"
}
```

**响应**：
```json
{
  "id": 1,
  "elderly_id": 1,
  "elderly_name": "张奶奶",
  "elderly_age": 75,
  "elderly_gender": "female",
  "relation": "母亲"
}
```

#### 5.1.3 获取绑定详情
```
GET /api/v1/member/bindings/{elder_id}
```

**响应**：同添加绑定响应

#### 5.1.4 更新绑定信息
```
PUT /api/v1/member/bindings/{binding_id}
```

**请求体**：
```json
{
  "relation": "母亲"
}
```

**响应**：同添加绑定响应

#### 5.1.5 删除绑定
```
DELETE /api/v1/member/bindings/{binding_id}
```

**响应**：
```json
{
  "message": "绑定已删除"
}
```

#### 5.1.6 获取可绑定老人列表
```
GET /api/v1/member/elderly-list
```

**响应**：
```json
[
  {
    "id": 1,
    "name": "张奶奶",
    "phone": "138****5678",
    "age": 75,
    "gender": "female"
  }
]
```

### 5.2 订单管理

#### 5.2.1 获取老人订单列表
```
GET /api/v1/member/orders
```

**查询参数**：
- `elder_id`: 老人ID（可选）
- `status`: 订单状态（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 30,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "elderly_id": 1,
      "total_amount": 28.00,
      "status": "delivering",
      "order_type": "immediate",
      "scheduled_time": "2024-01-15T12:00:00",
      "delivery_address": "幸福小区3号楼2单元501室",
      "notes": "备注",
      "created_at": "2024-01-15T10:00:00",
      "updated_at": "2024-01-15T11:00:00",
      "paid_at": "2024-01-15T10:05:00",
      "items": [
        {
          "meal": {
            "id": 1,
            "name": "营养套餐A",
            "price": 28.00,
            "image_url": "string"
          },
          "quantity": 1,
          "unit_price": 28.00,
          "subtotal": 28.00
        }
      ]
    }
  ]
}
```

#### 5.2.2 获取订单详情
```
GET /api/v1/member/orders/{order_id}
```

**响应**：
```json
{
  "id": 1,
  "elderly_id": 1,
  "elderly_name": "张奶奶",
  "total_amount": 28.00,
  "status": "delivering",
  "order_type": "immediate",
  "scheduled_time": "2024-01-15T12:00:00",
  "delivery_address": "幸福小区3号楼2单元501室",
  "notes": "备注",
  "payment_method": "wechat",
  "delivery_man": "李师傅",
  "delivery_phone": "139****9012",
  "estimated_time": "2024-01-15T12:30:00",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T11:00:00",
  "paid_at": "2024-01-15T10:05:00",
  "items": []
}
```

#### 5.2.3 为老人下单
```
POST /api/v1/member/orders
```

**请求体**：
```json
{
  "elder_id": 1,
  "items": [
    {
      "meal_id": 1,
      "quantity": 1
    }
  ],
  "delivery_address": "幸福小区3号楼2单元501室",
  "special_notes": "备注信息",
  "scheduled_time": "2024-01-15T12:00:00",
  "order_type": "immediate"
}
```

**响应**：
```json
{
  "id": 1,
  "order_no": "ORD20240115001",
  "elderly_id": 1,
  "member_id": 2,
  "total_amount": 28.00,
  "status": "pending_payment"
}
```

#### 5.2.4 支付订单
```
POST /api/v1/member/orders/{order_id}/pay
```

**请求体**：
```json
{
  "payment_method": "wechat"
}
```

**响应**：
```json
{
  "id": 1,
  "status": "pending_accept",
  "payment_method": "wechat",
  "payment_status": "paid",
  "transaction_id": "TXN202401151000001"
}
```

#### 5.2.5 取消订单
```
POST /api/v1/member/orders/{order_id}/cancel
```

**响应**：
```json
{
  "message": "订单取消成功",
  "order_id": 1,
  "status": "cancelled"
}
```

#### 5.2.6 跟踪订单配送
```
GET /api/v1/member/orders/{order_id}/track
```

**响应**：
```json
{
  "order_id": 1,
  "status": "delivering",
  "estimated_time": "2024-01-15T12:30:00",
  "deliverer": {
    "name": "李师傅",
    "phone": "139****9012",
    "current_location": {
      "latitude": 39.9042,
      "longitude": 116.4074
    },
    "distance": "1.2km",
    "estimated_arrival": "12:25"
  },
  "elderly_location": {
    "latitude": 39.9142,
    "longitude": 116.4174
  }
}
```

### 5.3 健康管理

#### 5.3.1 获取老人健康记录
```
GET /api/v1/member/health/{elder_id}
```

**查询参数**：
- `date`: 查询日期，格式：YYYY-MM-DD（可选）

**响应**：
```json
{
  "elder_id": 1,
  "elder_name": "张奶奶",
  "health_status": "正常",
  "health_tags": ["高血压", "清淡饮食"],
  "nutrition": {
    "calories": 1250,
    "protein": 45,
    "fat": 25,
    "carbs": 180
  },
  "diet_pattern": {
    "breakfast": {"time": "07:30", "has_meal": true},
    "lunch": {"time": "12:00", "has_meal": true},
    "dinner": {"time": "18:00", "has_meal": true}
  },
  "diet_regularity": "良好",
  "diet_records": [
    {
      "time": "07:30",
      "meal": "早餐",
      "foods": [
        {"name": "小米粥", "calories": 150, "image": "string"}
      ],
      "totalCalories": 340,
      "nutritionTags": ["蛋白质", "碳水"]
    }
  ]
}
```

#### 5.3.2 添加健康记录
```
POST /api/v1/member/health
```

**请求体**：
```json
{
  "elderly_id": 1,
  "blood_pressure": "135/85",
  "blood_sugar": 5.6,
  "weight": 65.0,
  "temperature": 36.5,
  "heart_rate": 75,
  "notes": "血压稳定",
  "tags": ["高血压"]
}
```

**响应**：
```json
{
  "id": 1,
  "elderly_id": 1,
  "blood_pressure": "135/85",
  "blood_sugar": 5.6,
  "weight": 65.0,
  "doctor_advice": "体温: 36.5°C\n心率: 75次/分钟\n备注: 血压稳定\n健康标签: 高血压",
  "created_at": "2024-01-15T10:00:00"
}
```

### 5.4 口味偏好

#### 5.4.1 获取老人口味偏好
```
GET /api/v1/member/elderly/{elder_id}/preferences
```

**响应**：
```json
{
  "elder_id": 1,
  "elder_name": "张奶奶",
  "tastes": ["清淡", "少盐"],
  "allergies": ["海鲜"],
  "special_needs": "需要软食"
}
```

#### 5.4.2 更新老人口味偏好
```
POST /api/v1/member/elderly/{elder_id}/preferences
```

**请求体**：
```json
{
  "tastes": ["清淡", "少盐"],
  "allergies": ["海鲜"],
  "special_needs": "需要软食"
}
```

**响应**：同获取口味偏好响应，包含updated_at字段

### 5.5 消费统计

#### 5.5.1 获取老人消费统计
```
GET /api/v1/member/consume/{elder_id}
```

**查询参数**：
- `date`: 查询日期，格式：YYYY-MM-DD（可选）
- `start_date`: 开始日期，格式：YYYY-MM-DD（可选）
- `end_date`: 结束日期，格式：YYYY-MM-DD（可选）

**响应**：
```json
{
  "total_amount": 1250.50,
  "order_count": 45,
  "avg_amount": 27.80,
  "amount_trend": 12,
  "order_trend": 8,
  "avg_trend": 5,
  "bill_groups": [
    {
      "date": "2024-01-15",
      "bills": [
        {"name": "早餐", "time": "07:30", "amount": 28.00}
      ]
    }
  ]
}
```

### 5.6 健康提醒

#### 5.6.1 发送健康提醒
```
POST /api/v1/member/health-reminders
```

**请求体**：
```json
{
  "receiver_id": 1,
  "reminder_type": "diet",
  "content": "记得按时吃药",
  "scheduled_time": "2024-01-15T18:00:00"
}
```

**响应**：
```json
{
  "id": 1,
  "sender_id": 2,
  "receiver_id": 1,
  "reminder_type": "diet",
  "content": "记得按时吃药",
  "status": "pending",
  "scheduled_time": "2024-01-15T18:00:00",
  "created_at": "2024-01-15T10:00:00"
}
```

### 5.7 紧急呼叫记录

#### 5.7.1 获取老人紧急呼叫记录
```
GET /api/v1/member/elderly-emergency-calls
```

**查询参数**：
- `elderly_id`: 老人ID（必填）
- `emergency_type`: 紧急类型（可选）

**响应**：
```json
[
  {
    "id": 1,
    "elderly_id": 1,
    "emergency_type": "medical",
    "message": "身体不适",
    "response_status": "pending",
    "response_time": null,
    "created_at": "2024-01-15T10:00:00"
  }
]
```

### 5.8 AI健康建议

#### 5.8.1 获取老人AI健康建议
```
GET /api/v1/member/health-advice/{elderly_id}
```

**响应**：
```json
{
  "advice": "根据老人的健康数据，建议..."
}
```

### 5.9 餐品收藏

#### 5.9.1 添加收藏
```
POST /api/v1/member/favorites
```

**请求体**：
```json
{
  "meal_id": 1
}
```

**响应**：
```json
{
  "id": 1,
  "meal_id": 1,
  "created_at": "2024-01-15T10:00:00"
}
```

#### 5.9.2 获取收藏列表
```
GET /api/v1/member/favorites
```

**响应**：
```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "name": "营养套餐A",
      "price": 28.00,
      "image_url": "string",
      "category": "主食",
      "special_tag": "低糖"
    }
  ]
}
```

#### 5.9.3 删除收藏
```
DELETE /api/v1/member/favorites/{meal_id}
```

**响应**：
```json
{
  "message": "收藏已移除"
}
```

### 5.10 评价管理

#### 5.10.1 获取评价列表
```
GET /api/v1/member/reviews
```

**响应**：
```json
{
  "reviews": [
    {
      "id": 1,
      "order_id": 1,
      "rating": 5,
      "content": "很好",
      "images": [],
      "reply": "感谢您的评价",
      "created_at": "2024-01-15T10:00:00",
      "order": {
        "meal_name": "营养套餐A",
        "meal_image": "string"
      }
    }
  ]
}
```

### 5.11 其他接口

#### 5.11.1 获取分类列表
```
GET /api/v1/member/categories
```

**响应**：同老人端分类列表

#### 5.11.2 获取公告列表
```
GET /api/v1/member/announcements
```

**响应**：同老人端公告列表

#### 5.11.3 上传头像
```
POST /api/v1/member/avatar
```

**请求体**：multipart/form-data，字段名`avatar`，图片文件

**响应**：
```json
{
  "success": true,
  "message": "头像上传成功",
  "data": {
    "avatar_url": "http://localhost:7678/static/uploads/avatars/xxx.jpg"
  }
}
```

## 6. 配送员端API

### 6.1 订单管理

#### 6.1.1 获取订单列表
```
GET /api/v1/deliver/orders
```

**查询参数**：
- `status`: 订单状态（可选：pending_accept/delivering/completed）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "orders": [
    {
      "id": 1,
      "order_number": "ORD20240115001",
      "elderly_name": "张奶奶",
      "elderly_phone": "138****5678",
      "delivery_address": "幸福小区3号楼2单元501室",
      "community_name": "幸福小区",
      "meal_name": "营养套餐A x1",
      "quantity": 1,
      "unit_price": 28.00,
      "total_amount": 28.00,
      "created_at": "2024-01-15T10:00:00",
      "status": "pending_accept",
      "elderly_location": {
        "latitude": 39.9042,
        "longitude": 116.4074
      },
      "is_assigned_by_admin": false,
      "assigned_deliverer_id": null,
      "meal_items": [
        {
          "name": "营养套餐A",
          "quantity": 1,
          "unit_price": 28.00,
          "subtotal": 28.00
        }
      ]
    }
  ],
  "total": 15,
  "page": 1,
  "limit": 20
}
```

#### 6.1.2 获取订单详情
```
GET /api/v1/deliver/orders/{order_id}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "id": 1,
    "order_no": "ORD20240115001",
    "elderly_name": "张奶奶",
    "elderly_phone": "138****5678",
    "delivery_address": "幸福小区3号楼2单元501室",
    "community_name": "幸福小区",
    "meal_name": "营养套餐A x1",
    "quantity": 1,
    "notes": "",
    "created_at": "2024-01-15 10:00",
    "delivery_time": "12:30前送达",
    "distance": "距离2.5km",
    "status": "pending_accept",
    "is_assigned_by_admin": false,
    "assigned_deliverer_id": null,
    "meal_items": []
  }
}
```

#### 6.1.3 接单
```
POST /api/v1/deliver/orders/{order_id}/accept
```

**响应**：
```json
{
  "success": true,
  "order_id": 1,
  "status": "delivering",
  "message": "接单成功"
}
```

#### 6.1.4 完成配送
```
POST /api/v1/deliver/orders/{order_id}/complete
```

**响应**：
```json
{
  "order_id": 1,
  "status": "completed",
  "message": "配送完成",
  "income": 5.00
}
```

#### 6.1.5 获取配送中订单
```
GET /api/v1/deliver/orders/delivering
```

**响应**：
```json
[
  {
    "id": 1,
    "order_no": "ORD20240115001",
    "elderly_name": "张奶奶",
    "delivery_address": "幸福小区3号楼2单元501室",
    "community_name": "幸福小区",
    "delivery_time": "2024-01-15T10:00:00",
    "remaining_time": "30分钟",
    "elderly_phone": "138****5678",
    "elderly_location": {
      "latitude": 39.9042,
      "longitude": 116.4074
    },
    "is_assigned_by_admin": false
  }
]
```

### 6.2 位置管理

#### 6.2.1 更新位置信息
```
POST /api/v1/deliver/location
```

**请求体**：
```json
{
  "latitude": "39.9042",
  "longitude": "116.4074",
  "accuracy": 5.0
}
```

**响应**：
```json
{
  "message": "位置更新成功",
  "timestamp": "2024-01-15T11:30:00"
}
```

### 6.3 收入统计

#### 6.3.1 获取收入统计
```
GET /api/v1/deliver/income
```

**查询参数**：
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）

**响应**：
```json
{
  "today_income": 150.00,
  "month_income": 2500.00,
  "total_income": 8500.00,
  "balance": 8500.00,
  "income_details": [
    {
      "id": 1,
      "order_no": "ORD20240115001",
      "meal_name": "营养套餐A x1",
      "amount": 28.00,
      "time": "12:30"
    }
  ]
}
```

### 6.4 异常处理

#### 6.4.1 上报配送异常
```
POST /api/v1/deliver/exceptions
```

**请求体**：
```json
{
  "order_id": 1,
  "exception_type": "late_delivery",
  "description": "客户地址有误，需要额外时间寻找"
}
```

**响应**：
```json
{
  "id": 1,
  "order_id": 1,
  "exception_type": "late_delivery",
  "description": "客户地址有误，需要额外时间寻找",
  "status": "reported",
  "created_at": "2024-01-15T10:00:00"
}
```

#### 6.4.2 获取异常记录
```
GET /api/v1/deliver/exceptions
```

**查询参数**：
- `status`: 异常状态（可选）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 10,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "delivery_id": 1,
      "type": "late_delivery",
      "description": "客户地址有误",
      "created_at": "2024-01-15T10:00:00",
      "order": {
        "order_id": 1,
        "order_no": "ORD20240115001",
        "elderly_name": "张奶奶"
      }
    }
  ]
}
```

### 6.5 个人信息

#### 6.5.1 获取配送员资料
```
GET /api/v1/deliver/profile
```

**响应**：
```json
{
  "deliverer": {
    "id": 1,
    "name": "李师傅",
    "phone": "139****9012",
    "status": "online",
    "avatar": "string"
  },
  "stats": {
    "today_orders": 5,
    "total_orders": 120,
    "rating_rate": "98%",
    "total_income": 8500.00
  }
}
```

#### 6.5.2 获取详细个人信息
```
GET /api/v1/deliver/personal-info
```

**响应**：
```json
{
  "name": "李师傅",
  "phone": "139****9012",
  "idCard": "",
  "gender": "male",
  "age": "",
  "vehicle_type": "电动车",
  "avatar": "string"
}
```

### 6.6 评价管理

#### 6.6.1 获取评价列表
```
GET /api/v1/deliver/reviews
```

**查询参数**：
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 50,
  "page": 1,
  "limit": 20,
  "average_rating": 4.8,
  "total_reviews": 50,
  "rating_stats": [
    {
      "rating": 5,
      "count": 40,
      "percentage": 80.0
    }
  ],
  "reviews": [
    {
      "id": 1,
      "order_id": 1,
      "reviewer_name": "张奶奶",
      "rating": 5,
      "content": "配送及时",
      "images": [],
      "reply": "感谢您的评价",
      "created_at": "2024-01-15 10:00",
      "reviewer_type": "elderly"
    }
  ]
}
```

### 6.7 其他接口

#### 6.7.1 上传头像
```
POST /api/v1/deliver/avatar
```

**请求体**：multipart/form-data，字段名`avatar`，图片文件

**响应**：
```json
{
  "success": true,
  "message": "头像上传成功",
  "data": {
    "avatar_url": "http://localhost:7678/static/uploads/avatars/xxx.jpg"
  }
}
```

## 7. 管理端API

### 7.1 工作台

#### 7.1.1 获取工作台统计数据
```
GET /api/v1/admin/dashboard
```

**响应**：
```json
{
  "stats": [
    {
      "title": "今日订单总数",
      "value": 156,
      "unit": "单",
      "icon": "ShoppingCart",
      "color": "#6366f1",
      "bg": "rgba(99, 102, 241, 0.1)",
      "trend": 12,
      "trendType": "up"
    }
  ],
  "deliveringOrders": 12,
  "trendData": [
    {
      "date": "01-15",
      "orders": 156
    }
  ],
  "revenueData": [
    {
      "date": "01-15",
      "revenue": 4446.00
    }
  ]
}
```

### 7.2 用户管理

#### 7.2.1 获取用户列表
```
GET /api/v1/admin/users
```

**查询参数**：
- `user_type`: 用户类型（可选：elderly/member/deliverer/admin）
- `status`: 用户状态（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 248,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "username": "elderly001",
      "user_type": "elderly",
      "status": "active",
      "profile": {
        "name": "张奶奶",
        "phone": "138****5678",
        "age": 75,
        "gender": "female",
        "address": "幸福小区3号楼2单元501室"
      },
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### 7.2.2 获取老人用户列表
```
GET /api/v1/admin/users/elderly
```

**查询参数**：
- `status`: 用户状态（可选）
- `community_id`: 社区ID（可选）
- `health_tag_id`: 健康标签ID（可选，0表示良好）
- `search`: 搜索关键词（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 128,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "username": "elderly001",
      "status": "active",
      "profile": {
        "name": "张奶奶",
        "phone": "138****5678",
        "age": 75,
        "gender": "female",
        "address": "幸福小区3号楼2单元501室",
        "health_status": "高血压",
        "dietary_preferences": "低糖饮食",
        "community_id": 1,
        "health_tag_id": 1,
        "community": {
          "id": 1,
          "name": "幸福小区"
        },
        "health_tag": {
          "id": 1,
          "name": "高血压",
          "color": "#ff0000"
        }
      },
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### 7.2.3 获取家属用户列表
```
GET /api/v1/admin/users/members
```

**查询参数**：同用户列表

**响应**：用户列表格式，profile包含name和phone

#### 7.2.4 获取配送员用户列表
```
GET /api/v1/admin/users/deliverers
```

**查询参数**：同用户列表

**响应**：
```json
{
  "total": 24,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "username": "deliverer001",
      "status": "active",
      "profile": {
        "name": "李师傅",
        "phone": "139****9012",
        "vehicle_type": "电动车",
        "current_location": {
          "latitude": 39.9042,
          "longitude": 116.4074,
          "timestamp": "2024-01-15T10:00:00"
        },
        "status": "online",
        "area": {
          "id": 1,
          "name": "朝阳区"
        }
      },
      "created_at": "2024-01-01T00:00:00",
      "today_orders": 5,
      "rating": 4.8
    }
  ]
}
```

#### 7.2.5 创建用户
```
POST /api/v1/admin/users
```

**请求体**：
```json
{
  "username": "user001",
  "password": "password123",
  "user_type": "elderly",
  "profile": {
    "name": "张奶奶",
    "phone": "138****5678"
  }
}
```

**响应**：
```json
{
  "message": "用户创建成功",
  "user": {
    "id": 1,
    "username": "user001",
    "user_type": "elderly",
    "status": "active"
  }
}
```

#### 7.2.6 更新用户
```
PUT /api/v1/admin/users/{user_id}
```

**请求体**：
```json
{
  "username": "user001",
  "status": "active",
  "profile": {
    "name": "张奶奶",
    "phone": "138****5678"
  }
}
```

**响应**：同创建用户响应

#### 7.2.7 删除用户
```
DELETE /api/v1/admin/users/{user_id}
```

**响应**：
```json
{
  "message": "用户删除成功",
  "user_id": 1
}
```

### 7.3 订单管理

#### 7.3.1 获取订单列表
```
GET /api/v1/admin/orders
```

**查询参数**：
- `status`: 订单状态（可选）
- `order_type`: 订单类型（可选）
- `elderly_id`: 老人ID（可选）
- `deliverer_id`: 配送员ID（可选）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 1256,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "order_no": "ORD202401150001",
      "transaction_id": "TXN202401151000001",
      "elderly_name": "张奶奶",
      "deliverer_name": "李师傅",
      "total_amount": 28.00,
      "status": "completed",
      "delivery_address": "幸福小区3号楼2单元501室",
      "notes": "备注",
      "created_at": "2024-01-15T10:00:00",
      "updated_at": "2024-01-15T12:00:00",
      "scheduled_time": "2024-01-15T12:00:00",
      "order_type": "immediate",
      "items": [
        {
          "meal_name": "营养套餐A",
          "quantity": 1,
          "price": 28.00
        }
      ]
    }
  ]
}
```

#### 7.3.2 获取订单详情
```
GET /api/v1/admin/orders/{order_id}
```

**响应**：
```json
{
  "id": 1,
  "order_no": "ORD202401150001",
  "total_amount": 28.00,
  "status": "completed",
  "delivery_address": "幸福小区3号楼2单元501室",
  "notes": "备注",
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T12:00:00",
  "elderly": {
    "id": 1,
    "name": "张奶奶",
    "phone": "138****5678",
    "address": "幸福小区3号楼2单元501室"
  },
  "items": [
    {
      "id": 1,
      "meal_id": 1,
      "meal_name": "营养套餐A",
      "quantity": 1,
      "unit_price": 28.00,
      "subtotal": 28.00
    }
  ],
  "payment": {
    "id": 1,
    "payment_method": "wechat",
    "amount": 28.00,
    "status": "paid",
    "transaction_id": "TXN202401151000001"
  },
  "delivery": {
    "id": 1,
    "deliverer_id": 1,
    "deliverer_name": "李师傅",
    "status": "delivered",
    "estimated_time": "2024-01-15T12:30:00",
    "actual_time": "2024-01-15T12:25:00"
  }
}
```

#### 7.3.3 更新订单状态
```
PUT /api/v1/admin/orders/{order_id}/status
```

**请求体**：
```json
{
  "status": "completed"
}
```

**响应**：
```json
{
  "id": 1,
  "status": "completed",
  "message": "订单状态更新成功"
}
```

#### 7.3.4 快速下单
```
POST /api/v1/admin/orders/quick
```

**请求体**：
```json
{
  "elderly_id": 1,
  "items": [
    {
      "meal_id": 1,
      "quantity": 1
    }
  ],
  "delivery_address": "幸福小区3号楼2单元501室",
  "notes": "备注",
  "payment_method": "cash"
}
```

**响应**：
```json
{
  "id": 1,
  "order_no": "ORD202401150001",
  "elderly_name": "张奶奶",
  "total_amount": 28.00,
  "status": "pending_accept",
  "message": "快速下单成功"
}
```

#### 7.3.5 指派配送员
```
POST /api/v1/admin/deliveries/assign
```

**请求体**：
```json
{
  "order_id": 1,
  "deliverer_id": 1,
  "estimated_time": "12:30",
  "remark": "备注"
}
```

**响应**：
```json
{
  "id": 1,
  "order_id": 1,
  "deliverer_id": 1,
  "deliverer_name": "李师傅",
  "status": "assigned",
  "estimated_time": "2024-01-15T12:30:00",
  "message": "配送指派成功"
}
```

### 7.4 餐品管理

#### 7.4.1 获取分类列表
```
GET /api/v1/admin/categories
```

**响应**：
```json
{
  "categories": [
    {
      "id": 1,
      "name": "主食",
      "description": "主食类餐品"
    }
  ]
}
```

#### 7.4.2 获取标签列表
```
GET /api/v1/admin/tags
```

**响应**：
```json
{
  "tags": [
    {
      "id": 1,
      "name": "低糖",
      "description": "适合糖尿病患者的低糖餐品"
    }
  ]
}
```

#### 7.4.3 获取餐品列表
```
GET /api/v1/admin/meals
```

**查询参数**：
- `category`: 分类（可选）
- `tag`: 标签（可选）
- `status`: 状态（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 86,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "name": "营养套餐A",
      "price": 28.00,
      "description": "营养均衡的套餐",
      "category": "主食",
      "status": "available",
      "image_url": "string",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### 7.4.4 添加餐品
```
POST /api/v1/admin/meals
```

**请求体**：
```json
{
  "name": "营养套餐B",
  "price": 32.00,
  "description": "高蛋白营养套餐",
  "category": "主食",
  "image_url": "string",
  "nutrition": ["高蛋白", "低脂肪"]
}
```

**响应**：
```json
{
  "id": 2,
  "name": "营养套餐B",
  "price": 32.00,
  "status": "available"
}
```

#### 7.4.5 更新餐品
```
PUT /api/v1/admin/meals/{meal_id}
```

**请求体**：
```json
{
  "name": "营养套餐B",
  "price": 35.00,
  "description": "更新后的描述",
  "status": "available",
  "nutrition": ["高蛋白"]
}
```

**响应**：同添加餐品响应

#### 7.4.6 删除餐品
```
DELETE /api/v1/admin/meals/{meal_id}
```

**响应**：
```json
{
  "message": "餐品删除成功",
  "meal_id": 2
}
```

### 7.5 社区管理

#### 7.5.1 获取社区列表
```
GET /api/v1/admin/communities
```

**查询参数**：
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 12,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "name": "幸福小区",
      "address": "北京市朝阳区幸福路1号",
      "contact_phone": "010-12345678",
      "manager_name": "王经理",
      "manager_phone": "13800138000",
      "elderly_count": 25,
      "status": "正常",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### 7.5.2 获取社区详情
```
GET /api/v1/admin/communities/{community_id}
```

**响应**：同社区列表项格式

#### 7.5.3 添加社区
```
POST /api/v1/admin/communities
```

**请求体**：
```json
{
  "name": "幸福小区",
  "address": "北京市朝阳区幸福路1号",
  "contact_phone": "010-12345678",
  "manager_name": "王经理",
  "manager_phone": "13800138000",
  "status": "正常"
}
```

**响应**：
```json
{
  "message": "社区创建成功",
  "community": {
    "id": 1,
    "name": "幸福小区",
    "address": "北京市朝阳区幸福路1号",
    "contact_phone": "010-12345678",
    "manager_name": "王经理",
    "manager_phone": "13800138000",
    "elderly_count": 0,
    "status": "正常"
  }
}
```

#### 7.5.4 更新社区
```
PUT /api/v1/admin/communities/{community_id}
```

**请求体**：同添加社区

**响应**：同添加社区响应

#### 7.5.5 删除社区
```
DELETE /api/v1/admin/communities/{community_id}
```

**响应**：
```json
{
  "message": "社区删除成功",
  "community_id": 1
}
```

### 7.6 公告管理

#### 7.6.1 获取公告列表
```
GET /api/v1/admin/announcements
```

**查询参数**：
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 20,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "title": "端午节放假安排",
      "content": "端午节期间配送时间调整通知",
      "type": "notice",
      "priority": "normal",
      "status": "active",
      "created_at": "2024-06-01T10:00:00"
    }
  ]
}
```

#### 7.6.2 获取公告详情
```
GET /api/v1/admin/announcements/{announcement_id}
```

**响应**：同公告列表项格式

#### 7.6.3 添加公告
```
POST /api/v1/admin/announcements
```

**请求体**：
```json
{
  "title": "端午节放假安排",
  "content": "端午节期间配送时间调整通知",
  "type": "notice",
  "priority": "normal",
  "status": "active"
}
```

**响应**：
```json
{
  "message": "通知创建成功",
  "announcement": {
    "id": 1,
    "title": "端午节放假安排",
    "content": "端午节期间配送时间调整通知",
    "type": "notice",
    "priority": "normal",
    "status": "active"
  }
}
```

#### 7.6.4 更新公告
```
PUT /api/v1/admin/announcements/{announcement_id}
```

**请求体**：同添加公告

**响应**：同添加公告响应

#### 7.6.5 删除公告
```
DELETE /api/v1/admin/announcements/{announcement_id}
```

**响应**：
```json
{
  "message": "通知删除成功",
  "announcement_id": 1
}
```

### 7.7 评价管理

#### 7.7.1 获取评价列表
```
GET /api/v1/admin/reviews
```

**查询参数**：
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 100,
  "page": 1,
  "limit": 20,
  "stats": {
    "total": 100,
    "positive": 80,
    "neutral": 15,
    "negative": 5,
    "with_images": 20,
    "pending_review": 10,
    "approved": 85,
    "rejected": 5,
    "pending_reply": 30,
    "deliverer_reviews": 40,
    "meal_reviews": 60,
    "deliverer_positive": 35,
    "deliverer_neutral": 4,
    "deliverer_negative": 1,
    "meal_positive": 45,
    "meal_neutral": 11,
    "meal_negative": 4
  },
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "elderly_id": 1,
      "elderly_name": "张奶奶",
      "rating": 5,
      "content": "配送及时，服务周到",
      "status": "approved",
      "images": [],
      "reply": "感谢您的评价",
      "created_at": "2024-01-15T10:00:00",
      "ai_reviewed": 1,
      "ai_replied": 1,
      "mealName": "营养套餐A",
      "reviewer_type": "elderly",
      "deliverer_id": 1,
      "deliverer_name": "李师傅",
      "deliverer_phone": "139****9012"
    }
  ]
}
```

#### 7.7.2 获取评价详情
```
GET /api/v1/admin/reviews/{review_id}
```

**响应**：
```json
{
  "id": 1,
  "order_id": 1,
  "elderly_id": 1,
  "elderly_name": "张奶奶",
  "rating": 5,
  "content": "配送及时，服务周到",
  "created_at": "2024-01-15T10:00:00"
}
```

#### 7.7.3 创建评价
```
POST /api/v1/admin/reviews
```

**请求体**：
```json
{
  "order_id": 1,
  "elderly_id": 1,
  "rating": 5,
  "content": "很好"
}
```

**响应**：
```json
{
  "message": "评价创建成功",
  "review": {
    "id": 1,
    "order_id": 1,
    "elderly_id": 1,
    "rating": 5,
    "content": "很好"
  }
}
```

#### 7.7.4 更新评价
```
PUT /api/v1/admin/reviews/{review_id}
```

**请求体**：
```json
{
  "rating": 5,
  "content": "更新后的评价内容",
  "status": "approved",
  "reply": "感谢您的评价"
}
```

**响应**：同创建评价响应

#### 7.7.5 删除评价
```
DELETE /api/v1/admin/reviews/{review_id}
```

**响应**：
```json
{
  "message": "评价删除成功",
  "review_id": 1
}
```

#### 7.7.6 AI智能分析评价
```
GET /api/v1/admin/reviews/analysis
```

**响应**：
```json
{
  "success": true,
  "data": {
    "analysis_result": "分析结果..."
  }
}
```

#### 7.7.7 批量AI审核
```
POST /api/v1/admin/reviews/ai-review/batch
```

**响应**：
```json
{
  "message": "AI审核完成",
  "total_reviews": 10,
  "auto_approved": 8,
  "auto_rejected": 1,
  "pending_review": 1,
  "auto_replied": 5,
  "ai_results": []
}
```

#### 7.7.8 单个AI审核
```
POST /api/v1/admin/reviews/{review_id}/ai-review
```

**响应**：
```json
{
  "review_id": 1,
  "ai_analysis": {
    "sentiment": "positive",
    "score": 0.95
  }
}
```

#### 7.7.9 应用AI审核结果
```
POST /api/v1/admin/reviews/ai-review/apply
```

**请求体**：
```json
{
  "review_ids": [1, 2, 3]
}
```

**响应**：
```json
{
  "message": "AI审核结果应用完成",
  "results": [
    {
      "review_id": 1,
      "action": "approved",
      "reason": "正面评价"
    }
  ]
}
```

#### 7.7.10 AI回复单个评价
```
POST /api/v1/admin/reviews/{review_id}/ai-reply
```

**响应**：
```json
{
  "message": "AI回复生成成功",
  "review_id": 1,
  "reply": "感谢您的评价",
  "ai_generated": true,
  "confidence": 0.95,
  "error": null
}
```

#### 7.7.11 批量AI回复
```
POST /api/v1/admin/reviews/ai-reply/batch
```

**响应**：
```json
{
  "message": "AI批量回复完成",
  "total_reviews": 10,
  "generated_replies": 10,
  "applied_replies": 10,
  "results": []
}
```

#### 7.7.12 应用AI回复
```
POST /api/v1/admin/reviews/{review_id}/apply-reply
```

**请求体**：
```json
{
  "reply_content": "感谢您的评价"
}
```

**响应**：
```json
{
  "message": "回复应用成功",
  "review_id": 1,
  "reply": "感谢您的评价"
}
```

#### 7.7.13 批量通过评价
```
POST /api/v1/admin/reviews/batch-approve
```

**请求体**：
```json
{
  "review_ids": [1, 2, 3]
}
```

**响应**：
```json
{
  "message": "批量审核通过成功",
  "review_ids": [1, 2, 3],
  "processed_count": 3
}
```

### 7.8 老人家属关系管理

#### 7.8.1 获取关系列表
```
GET /api/v1/admin/elder-member-relations
```

**查询参数**：
- `member_id`: 家属ID（可选）
- `elder_id`: 老人ID（可选）
- `name`: 家属姓名（可选）
- `elderly_name`: 老人姓名（可选）
- `phone`: 联系方式（可选）
- `page`: 页码（默认1）
- `limit`: 每页数量（默认20）

**响应**：
```json
{
  "total": 50,
  "page": 1,
  "limit": 20,
  "items": [
    {
      "id": 1,
      "member_id": 2,
      "member_name": "张小明",
      "member_phone": "138****5678",
      "elder_id": 1,
      "elderly_name": "张奶奶",
      "relationship": "母亲",
      "is_primary": true,
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### 7.8.2 创建关系
```
POST /api/v1/admin/elder-member-relations
```

**请求体**：
```json
{
  "member_id": 2,
  "elder_id": 1,
  "relationship": "母亲",
  "is_primary": true
}
```

**响应**：
```json
{
  "id": 1,
  "member_id": 2,
  "member_name": "张小明",
  "elder_id": 1,
  "elderly_name": "张奶奶",
  "relationship": "母亲",
  "is_primary": true,
  "created_at": "2024-01-01T00:00:00",
  "message": "绑定关系创建成功"
}
```

### 7.9 配送员位置

#### 7.9.1 获取配送员位置
```
GET /api/v1/admin/deliverer-locations
```

**查询参数**：
- `deliverer_id`: 配送员ID（可选）

**响应**：
```json
{
  "locations": [
    {
      "deliverer_id": 1,
      "latitude": 39.9042,
      "longitude": 116.4074,
      "timestamp": "2024-01-15T10:00:00"
    }
  ]
}
```

### 7.10 统计分析

#### 7.10.1 获取统计数据
```
GET /api/v1/admin/statistics
```

**查询参数**：
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）
- `group_by`: 分组方式（可选：day/week/month）

**响应**：
```json
{
  "order_statistics": {
    "total_orders": 1256,
    "completed_orders": 1240,
    "cancelled_orders": 16,
    "avg_amount": 28.50
  },
  "delivery_statistics": {
    "avg_delivery_time": 22.5,
    "on_time_rate": 98.5,
    "total_distance": 1256000
  },
  "user_statistics": {
    "elderly_count": 128,
    "member_count": 96,
    "deliverer_count": 24
  },
  "trends": [
    {
      "date": "2024-01-15",
      "orders": 156,
      "amount": 4446.00
    }
  ]
}
```

### 7.11 AI对话

#### 7.11.1 管理员AI查询
```
POST /api/v1/admin/ai/query
```

**请求体**：
```json
{
  "query": "今天有多少订单？"
}
```

**响应**：
```json
{
  "response": "今天共有156个订单...",
  "conversation_id": "conv_admin_001",
  "timestamp": "2024-01-15T10:00:00"
}
```

#### 7.11.2 获取AI对话记录
```
GET /api/v1/admin/ai/conversations
```

**响应**：
```json
{
  "total": 20,
  "conversations": [
    {
      "id": 1,
      "conversation_id": "conv_admin_001",
      "user_query": "今天有多少订单？",
      "ai_response": "今天共有156个订单...",
      "created_at": "2024-01-15T10:00:00"
    }
  ]
}
```

### 7.12 个人信息

#### 7.12.1 获取管理员资料
```
GET /api/v1/admin/profile
```

**响应**：
```json
{
  "username": "admin001",
  "user_type": "admin",
  "email": "admin@example.com",
  "phone": "138****5678",
  "name": "管理员",
  "created_at": "2024-01-01T00:00:00",
  "last_login": "2024-01-15T10:00:00"
}
```

#### 7.12.2 更新管理员资料
```
PUT /api/v1/admin/profile
```

**请求体**：
```json
{
  "username": "admin001",
  "email": "admin@example.com",
  "phone": "138****5678",
  "name": "管理员"
}
```

**响应**：同获取管理员资料响应

#### 7.12.3 修改密码
```
POST /api/v1/admin/profile/password
```

**请求体**：
```json
{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

**响应**：
```json
{
  "message": "密码修改成功"
}
```

#### 7.12.4 更新安全设置
```
PUT /api/v1/admin/profile/security
```

**请求体**：
```json
{
  "two_factor_auth": true,
  "login_notification": true,
  "remote_login_alert": true
}
```

**响应**：
```json
{
  "message": "安全设置保存成功",
  "settings": {
    "two_factor_auth": true,
    "login_notification": true,
    "remote_login_alert": true
  }
}
```

### 7.13 系统设置

#### 7.13.1 获取AI设置
```
GET /api/v1/admin/settings/ai
```

**响应**：
```json
{
  "chat_model": "deepseek-chat",
  "elderly_chat_model": "deepseek-chat",
  "review_model": "deepseek-chat",
  "api_url": "https://api.deepseek.com",
  "api_key": "sk-xxx"
}
```

#### 7.13.2 更新AI设置
```
PUT /api/v1/admin/settings/ai
```

**请求体**：
```json
{
  "chat_model": "deepseek-chat",
  "elderly_chat_model": "deepseek-chat",
  "review_model": "deepseek-chat",
  "api_url": "https://api.deepseek.com",
  "api_key": "sk-xxx"
}
```

**响应**：
```json
{
  "message": "AI设置保存成功，已更新.env文件",
  "settings": {}
}
```

#### 7.13.3 获取AI模型列表
```
GET /api/v1/admin/settings/ai/models
```

**查询参数**：
- `api_url`: API地址（必填）
- `api_key`: API密钥（可选）

**响应**：
```json
{
  "models": [
    {"value": "deepseek-chat", "label": "deepseek-chat"},
    {"value": "deepseek-reasoner", "label": "deepseek-reasoner"}
  ]
}
```

### 7.14 数据备份

#### 7.14.1 创建备份
```
POST /api/v1/admin/backup
```

**响应**：
```json
{
  "message": "备份创建成功",
  "backup": {
    "filename": "backup_20240115_100000.sql",
    "size": 1024000,
    "created_at": "2024-01-15T10:00:00"
  }
}
```

#### 7.14.2 获取备份列表
```
GET /api/v1/admin/backups
```

**响应**：
```json
{
  "backups": [
    {
      "filename": "backup_20240115_100000.sql",
      "size": 1024000,
      "size_text": "1.00 MB",
      "created_at": "2024-01-15T10:00:00"
    }
  ]
}
```

#### 7.14.3 下载备份
```
GET /api/v1/admin/backup/{filename}
```

**响应**：文件下载

#### 7.14.4 恢复备份
```
POST /api/v1/admin/backup/restore/{filename}
```

**响应**：
```json
{
  "message": "备份恢复成功"
}
```

### 7.15 排班管理

#### 7.15.1 获取排班列表
```
GET /api/v1/admin/staff-schedules
```

**查询参数**：
- `staff_id`: 配送员ID（必填）
- `start_date`: 开始日期，格式：YYYY-MM-DD（可选）
- `end_date`: 结束日期，格式：YYYY-MM-DD（可选）

**响应**：
```json
{
  "schedules": [
    {
      "id": 1,
      "staff_id": 1,
      "schedule_date": "2024-01-15",
      "time_slot": "morning",
      "status": "scheduled",
      "note": "早班",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### 7.15.2 创建排班
```
POST /api/v1/admin/staff-schedules
```

**请求体**：
```json
{
  "staff_id": 1,
  "schedule_date": "2024-01-15",
  "time_slot": "morning",
  "note": "早班"
}
```

**响应**：
```json
{
  "id": 1,
  "staff_id": 1,
  "schedule_date": "2024-01-15",
  "time_slot": "morning",
  "status": "scheduled",
  "note": "早班"
}
```

#### 7.15.3 更新排班
```
PUT /api/v1/admin/staff-schedules/{schedule_id}
```

**请求体**：
```json
{
  "note": "早班（调整）",
  "status": "scheduled"
}
```

**响应**：同创建排班响应

#### 7.15.4 删除排班
```
DELETE /api/v1/admin/staff-schedules/{schedule_id}
```

**响应**：
```json
{
  "message": "排班记录删除成功"
}
```

#### 7.15.5 获取月度排班
```
GET /api/v1/admin/staff-schedules/month
```

**查询参数**：
- `staff_id`: 配送员ID（必填）
- `year`: 年份（必填）
- `month`: 月份（必填）

**响应**：
```json
{
  "schedules": [
    {
      "id": 1,
      "staff_id": 1,
      "schedule_date": "2024-01-15",
      "time_slot": "morning",
      "status": "scheduled",
      "note": "早班"
    }
  ]
}
```

### 7.16 健康标签管理

健康标签管理API请参考独立的健康标签路由文档。

## 8. 错误处理

### 8.1 标准错误响应格式
```json
{
  "detail": "错误信息"
}
```

### 8.2 常见HTTP状态码
- **200**: 请求成功
- **201**: 创建成功
- **400**: 请求参数错误
- **401**: 未授权，需要登录
- **403**: 权限不足
- **404**: 资源不存在
- **409**: 资源冲突
- **422**: 请求格式错误
- **500**: 服务器内部错误

## 9. API文档

### 9.1 Swagger UI
- 访问地址：`/docs`
- 提供交互式API测试界面
- 自动生成API文档

### 9.2 ReDoc
- 访问地址：`/redoc`
- 提供更简洁的文档展示

## 10. 性能优化

### 10.1 缓存策略
- 使用Redis缓存热点数据
- 设置合理的缓存过期时间

### 10.2 分页机制
- 所有列表接口支持分页
- 默认每页20条数据

### 10.3 异步处理
- 支持异步API调用
- 使用asyncio提高并发性能

## 11. 安全考虑

### 11.1 认证授权
- JWT令牌认证
- 基于角色的权限控制
- Token过期和刷新机制

### 11.2 输入验证
- 使用Pydantic进行数据验证
- 防止SQL注入和XSS攻击

### 11.3 数据加密
- 密码使用bcrypt加密
- 敏感信息传输加密

## 12. 部署考虑

### 12.1 环境配置
- 开发环境：本地开发
- 测试环境：Docker容器
- 生产环境：云服务器部署

### 12.2 监控和日志
- 详细的API访问日志
- 性能监控和告警
- 错误日志收集
