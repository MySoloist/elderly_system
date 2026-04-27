# 数据库结构设计

## 1. 用户表（users）

用户表实体主要属性为：主键（id）、用户名（username）、密码哈希（password_hash）、用户类型（user_type）、状态（status）、创建时间（created_at）、更新时间（updated_at）、邮箱（email）、最后登录时间（last_login）、微信openid（openid）、微信unionid（unionid）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| username | character varying | 50 | 用户名 | 否 | 否 |
| password_hash | character varying | 255 | 密码哈希 | 否 | 否 |
| user_type | character varying | 20 | 用户类型 | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 是 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| email | character varying | 100 | 邮箱 | 否 | 否 |
| last_login | timestamp with time zone | - | 最后登录时间 | 否 | 否 |
| openid | character varying | 100 | 微信openid | 否 | 否 |
| unionid | character varying | 100 | 微信unionid | 否 | 否 |

## 2. 老年人档案表（elderly_profiles）

老年人档案表实体主要属性为：用户ID（user_id）、姓名（name）、电话（phone）、地址（address）、饮食偏好（dietary_preferences）、位置（location）、年龄（age）、性别（gender）、创建时间（created_at）、更新时间（updated_at）、社区ID（community_id）、健康标签ID（health_tag_id）、头像（avatar）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| user_id | integer | - | 用户ID | 是 | 否 |
| name | character varying | 50 | 姓名 | 否 | 否 |
| phone | character varying | 20 | 电话 | 否 | 否 |
| address | character varying | 255 | 地址 | 否 | 否 |
| dietary_preferences | text | - | 饮食偏好 | 否 | 否 |
| location | public.geography(Point,4326) | - | 位置 | 否 | 否 |
| age | integer | - | 年龄 | 否 | 否 |
| gender | character varying | 10 | 性别 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| community_id | integer | - | 社区ID | 否 | 否 |
| health_tag_id | integer | - | 健康标签ID | 否 | 否 |
| avatar | character varying | 255 | 头像 | 否 | 否 |

## 3. 家庭成员档案表（member_profiles）

家庭成员档案表实体主要属性为：用户ID（user_id）、姓名（name）、电话（phone）、创建时间（created_at）、更新时间（updated_at）、头像（avatar）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| user_id | integer | - | 用户ID | 是 | 否 |
| name | character varying | 50 | 姓名 | 否 | 否 |
| phone | character varying | 20 | 电话 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| avatar | character varying | 255 | 头像 | 否 | 否 |

## 4. 配送员档案表（deliverer_profiles）

配送员档案表实体主要属性为：用户ID（user_id）、姓名（name）、电话（phone）、交通工具类型（vehicle_type）、状态（status）、创建时间（created_at）、更新时间（updated_at）、区域ID（area_id）、头像（avatar）、纬度（latitude）、经度（longitude）、位置更新时间（location_updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| user_id | integer | - | 用户ID | 是 | 否 |
| name | character varying | 50 | 姓名 | 否 | 否 |
| phone | character varying | 20 | 电话 | 否 | 否 |
| vehicle_type | character varying | 50 | 交通工具类型 | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 是 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| area_id | integer | - | 区域ID | 否 | 否 |
| avatar | character varying | 255 | 头像 | 否 | 否 |
| latitude | character varying | 20 | 纬度 | 否 | 否 |
| longitude | character varying | 20 | 经度 | 否 | 否 |
| location_updated_at | timestamp with time zone | - | 位置更新时间 | 否 | 否 |

## 5. 管理员档案表（admin_profiles）

管理员档案表实体主要属性为：用户ID（user_id）、姓名（name）、电话（phone）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| user_id | integer | - | 用户ID | 是 | 否 |
| name | character varying | 50 | 姓名 | 否 | 否 |
| phone | character varying | 20 | 电话 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 6. 餐品表（meals）

餐品表实体主要属性为：主键（id）、名称（name）、价格（price）、描述（description）、特殊标签（special_tag）、图片URL（image_url）、状态（status）、创建时间（created_at）、更新时间（updated_at）、分类ID（category_id）、标签ID（tag_id）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| name | character varying | 100 | 名称 | 否 | 否 |
| price | numeric(10,2) | - | 价格 | 否 | 否 |
| description | text | - | 描述 | 否 | 否 |
| special_tag | character varying | 50 | 特殊标签 | 否 | 否 |
| image_url | character varying | 255 | 图片URL | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 是 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| category_id | integer | - | 分类ID | 否 | 否 |
| tag_id | integer | - | 标签ID | 否 | 否 |

## 7. 订单表（orders）

订单表实体主要属性为：主键（id）、老年人ID（elderly_id）、总金额（total_amount）、支付方式（payment_method）、支付状态（payment_status）、状态（status）、配送地址（delivery_address）、备注（notes）、创建时间（created_at）、更新时间（updated_at）、预定时间（scheduled_time）、订单类型（order_type）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| elderly_id | integer | - | 老年人ID | 否 | 否 |
| total_amount | numeric(10,2) | - | 总金额 | 否 | 否 |
| payment_method | character varying | 50 | 支付方式 | 否 | 否 |
| payment_status | character varying | 20 | 支付状态 | 否 | 是 |
| status | character varying | 20 | 状态 | 否 | 是 |
| delivery_address | character varying | 255 | 配送地址 | 否 | 否 |
| notes | text | - | 备注 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| scheduled_time | timestamp with time zone | - | 预定时间 | 否 | 否 |
| order_type | character varying | 20 | 订单类型 | 否 | 是 |

## 8. 订单项表（order_items）

订单项表实体主要属性为：主键（id）、订单ID（order_id）、餐品ID（meal_id）、数量（quantity）、单价（unit_price）、小计（subtotal）、创建时间（created_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| order_id | integer | - | 订单ID | 否 | 否 |
| meal_id | integer | - | 餐品ID | 否 | 否 |
| quantity | integer | - | 数量 | 否 | 否 |
| unit_price | numeric(10,2) | - | 单价 | 否 | 否 |
| subtotal | numeric(10,2) | - | 小计 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |

## 9. 配送表（deliveries）

配送表实体主要属性为：主键（id）、订单ID（order_id）、配送员ID（deliverer_id）、结束时间（end_time）、预计时间（estimated_time）、状态（status）、创建时间（created_at）、更新时间（updated_at）、实际时间（actual_time）、是否由管理员分配（is_assigned_by_admin）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| order_id | integer | - | 订单ID | 否 | 否 |
| deliverer_id | integer | - | 配送员ID | 否 | 否 |
| end_time | timestamp with time zone | - | 结束时间 | 否 | 否 |
| estimated_time | timestamp with time zone | - | 预计时间 | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| actual_time | timestamp with time zone | - | 实际时间 | 否 | 否 |
| is_assigned_by_admin | boolean | - | 是否由管理员分配 | 否 | 是 |

## 10. 老年人与家庭成员关系表（elder_member_relations）

老年人与家庭成员关系表实体主要属性为：主键（id）、老年人ID（elder_id）、家庭成员ID（member_id）、关系（relationship）、是否主要联系人（is_primary）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| elder_id | integer | - | 老年人ID | 否 | 否 |
| member_id | integer | - | 家庭成员ID | 否 | 否 |
| relationship | character varying | 50 | 关系 | 否 | 否 |
| is_primary | boolean | - | 是否主要联系人 | 否 | 是 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 11. 健康记录表（health_records）

健康记录表实体主要属性为：主键（id）、老年人ID（elderly_id）、身高（height）、体重（weight）、血压（blood_pressure）、血糖（blood_sugar）、过敏史（allergies）、 medications（medications）、医嘱（doctor_advice）、记录时间（recorded_at）、创建者（created_by）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| elderly_id | integer | - | 老年人ID | 否 | 否 |
| height | numeric(5,2) | - | 身高 | 否 | 否 |
| weight | numeric(5,2) | - | 体重 | 否 | 否 |
| blood_pressure | character varying | 20 | 血压 | 否 | 否 |
| blood_sugar | numeric(5,2) | - | 血糖 | 否 | 否 |
| allergies | text | - | 过敏史 | 否 | 否 |
| medications | text | - |  medications | 否 | 否 |
| doctor_advice | text | - | 医嘱 | 否 | 否 |
| recorded_at | timestamp with time zone | - | 记录时间 | 否 | 是 |
| created_by | integer | - | 创建者 | 否 | 否 |

## 12. 紧急呼叫表（emergency_calls）

紧急呼叫表实体主要属性为：主键（id）、老年人ID（elderly_id）、紧急类型（emergency_type）、消息（message）、响应状态（response_status）、响应时间（response_time）、创建时间（created_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| elderly_id | integer | - | 老年人ID | 否 | 否 |
| emergency_type | character varying | 50 | 紧急类型 | 否 | 否 |
| message | text | - | 消息 | 否 | 否 |
| response_status | character varying | 20 | 响应状态 | 否 | 是 |
| response_time | timestamp with time zone | - | 响应时间 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |

## 13. 异常表（exceptions）

异常表实体主要属性为：主键（id）、配送ID（delivery_id）、类型（type）、描述（description）、创建时间（created_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| delivery_id | integer | - | 配送ID | 否 | 否 |
| type | character varying | 50 | 类型 | 否 | 否 |
| description | text | - | 描述 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |

## 14. 支付表（payments）

支付表实体主要属性为：主键（id）、订单ID（order_id）、支付方式（payment_method）、金额（amount）、交易ID（transaction_id）、状态（status）、创建时间（created_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| order_id | integer | - | 订单ID | 否 | 否 |
| payment_method | character varying | 50 | 支付方式 | 否 | 否 |
| amount | double precision | - | 金额 | 否 | 否 |
| transaction_id | character varying | 100 | 交易ID | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |

## 15. 评价表（reviews）

评价表实体主要属性为：主键（id）、订单ID（order_id）、老年人ID（elderly_id）、评分（rating）、内容（content）、创建时间（created_at）、状态（status）、图片（images）、更新时间（updated_at）、回复（reply）、AI审核（ai_reviewed）、AI回复（ai_replied）、配送员ID（deliverer_id）、评价者类型（reviewer_type）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| order_id | integer | - | 订单ID | 否 | 否 |
| elderly_id | integer | - | 老年人ID | 否 | 否 |
| rating | integer | - | 评分 | 否 | 否 |
| content | text | - | 内容 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| status | character varying | 20 | 状态 | 否 | 是 |
| images | text[] | - | 图片 | 否 | 否 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 否 |
| reply | text | - | 回复 | 否 | 否 |
| ai_reviewed | integer | - | AI审核 | 否 | 是 |
| ai_replied | integer | - | AI回复 | 否 | 是 |
| deliverer_id | integer | - | 配送员ID | 否 | 否 |
| reviewer_type | character varying | 20 | 评价者类型 | 否 | 否 |

## 16. 公告表（announcements）

公告表实体主要属性为：主键（id）、标题（title）、内容（content）、类型（type）、优先级（priority）、状态（status）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| title | character varying | 100 | 标题 | 否 | 否 |
| content | text | - | 内容 | 否 | 否 |
| type | character varying | 50 | 类型 | 否 | 否 |
| priority | character varying | 20 | 优先级 | 否 | 是 |
| status | character varying | 20 | 状态 | 否 | 是 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 17. AI对话表（ai_conversations）

AI对话表实体主要属性为：主键（id）、用户ID（user_id）、对话ID（conversation_id）、用户查询（user_query）、AI响应（ai_response）、对话类型（conversation_type）、创建时间（created_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| user_id | integer | - | 用户ID | 否 | 否 |
| conversation_id | character varying | 100 | 对话ID | 否 | 否 |
| user_query | text | - | 用户查询 | 否 | 否 |
| ai_response | text | - | AI响应 | 否 | 否 |
| conversation_type | character varying | 50 | 对话类型 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |

## 18. 社区表（communities）

社区表实体主要属性为：主键（id）、名称（name）、地址（address）、联系电话（contact_phone）、负责人姓名（manager_name）、负责人电话（manager_phone）、创建时间（created_at）、更新时间（updated_at）、状态（status）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| name | character varying | 100 | 名称 | 否 | 否 |
| address | character varying | 255 | 地址 | 否 | 否 |
| contact_phone | character varying | 20 | 联系电话 | 否 | 否 |
| manager_name | character varying | 50 | 负责人姓名 | 否 | 否 |
| manager_phone | character varying | 20 | 负责人电话 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |
| status | character varying | 20 | 状态 | 否 | 否 |

## 19. 分类表（categories）

分类表实体主要属性为：主键（id）、名称（name）、描述（description）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| name | character varying | 50 | 名称 | 否 | 否 |
| description | character varying | 255 | 描述 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 20. 标签表（tags）

标签表实体主要属性为：主键（id）、名称（name）、描述（description）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| name | character varying | 50 | 名称 | 否 | 否 |
| description | character varying | 255 | 描述 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 21. 健康标签表（health_tags）

健康标签表实体主要属性为：主键（id）、名称（name）、描述（description）、颜色（color）、创建时间（created_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| name | character varying | 50 | 名称 | 否 | 否 |
| description | text | - | 描述 | 否 | 否 |
| color | character varying | 20 | 颜色 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |

## 22. 健康提醒表（health_reminders）

健康提醒表实体主要属性为：主键（id）、发送者ID（sender_id）、接收者ID（receiver_id）、提醒类型（reminder_type）、内容（content）、状态（status）、预定时间（scheduled_time）、发送时间（sent_time）、阅读时间（read_time）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| sender_id | integer | - | 发送者ID | 否 | 否 |
| receiver_id | integer | - | 接收者ID | 否 | 否 |
| reminder_type | character varying | 50 | 提醒类型 | 否 | 否 |
| content | text | - | 内容 | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 是 |
| scheduled_time | timestamp without time zone | - | 预定时间 | 否 | 否 |
| sent_time | timestamp without time zone | - | 发送时间 | 否 | 否 |
| read_time | timestamp without time zone | - | 阅读时间 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 23. 员工时间表（staff_schedules）

员工时间表实体主要属性为：主键（id）、员工ID（staff_id）、日期（schedule_date）、时间段（time_slot）、状态（status）、备注（note）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| staff_id | integer | - | 员工ID | 否 | 否 |
| schedule_date | date | - | 日期 | 否 | 否 |
| time_slot | character varying | 20 | 时间段 | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 是 |
| note | text | - | 备注 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 24. 配送区域表（delivery_areas）

配送区域表实体主要属性为：主键（id）、名称（name）、描述（description）、创建时间（created_at）、更新时间（updated_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| name | character varying | 50 | 名称 | 否 | 否 |
| description | text | - | 描述 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| updated_at | timestamp with time zone | - | 更新时间 | 否 | 是 |

## 25. 收藏表（favorites）

收藏表实体主要属性为：主键（id）、用户ID（user_id）、用户类型（user_type）、餐品ID（meal_id）、创建时间（created_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| user_id | integer | - | 用户ID | 否 | 否 |
| user_type | character varying | 20 | 用户类型 | 否 | 否 |
| meal_id | integer | - | 餐品ID | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |

## 26. 语音合成表（voice_synthesis）

语音合成表实体主要属性为：主键（id）、用户ID（user_id）、文本内容（text_content）、语音URL（voice_url）、语音类型（voice_type）、语言（language）、语速（speed）、状态（status）、创建时间（created_at）、完成时间（completed_at）等。

| 字段名称 | 类型 | 长度 | 字段说明 | 是否主键 | 是否默认值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| id | integer | - | 主键 | 是 | 否 |
| user_id | integer | - | 用户ID | 否 | 否 |
| text_content | text | - | 文本内容 | 否 | 否 |
| voice_url | character varying | 500 | 语音URL | 否 | 否 |
| voice_type | character varying | 50 | 语音类型 | 否 | 否 |
| language | character varying | 20 | 语言 | 否 | 否 |
| speed | double precision | - | 语速 | 否 | 否 |
| status | character varying | 20 | 状态 | 否 | 否 |
| created_at | timestamp with time zone | - | 创建时间 | 否 | 是 |
| completed_at | timestamp with time zone | - | 完成时间 | 否 | 否 |
