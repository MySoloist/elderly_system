# 数据库结构详细信息

## 数据库概览

**总表数**: 31

**表列表**:

| 序号 | 表名 |
|------|------|
| 1 | `admin_profiles` |
| 2 | `ai_conversations` |
| 3 | `announcements` |
| 4 | `categories` |
| 5 | `communities` |
| 6 | `deliverer_locations` |
| 7 | `deliverer_profiles` |
| 8 | `deliveries` |
| 9 | `delivery_areas` |
| 10 | `elder_member_relations` |
| 11 | `elderly_profiles` |
| 12 | `emergency_calls` |
| 13 | `exceptions` |
| 14 | `favorites` |
| 15 | `favorites_member` |
| 16 | `geography_columns` |
| 17 | `geometry_columns` |
| 18 | `health_records` |
| 19 | `health_reminders` |
| 20 | `health_tags` |
| 21 | `meals` |
| 22 | `member_profiles` |
| 23 | `order_items` |
| 24 | `orders` |
| 25 | `payments` |
| 26 | `reviews` |
| 27 | `spatial_ref_sys` |
| 28 | `staff_schedules` |
| 29 | `tags` |
| 30 | `users` |
| 31 | `voice_synthesis` |

## `admin_profiles` 表结构

**主键**: `user_id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `user_id` | `integer` | - | ✗ | - | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `phone` | `character varying` | 20 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `user_id` | `users` | `id` | `admin_profiles_user_id_fkey` |

## `ai_conversations` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('ai_conversations_id_seq'::regclass) | - |
| `user_id` | `integer` | - | ✓ | - | - |
| `conversation_id` | `character varying` | 100 | ✗ | - | - |
| `user_query` | `text` | - | ✗ | - | - |
| `ai_response` | `text` | - | ✗ | - | - |
| `conversation_type` | `character varying` | 50 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `user_id` | `users` | `id` | `ai_conversations_user_id_fkey` |

## `announcements` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('announcements_id_seq'::regclass) | - |
| `title` | `character varying` | 100 | ✗ | - | - |
| `content` | `text` | - | ✗ | - | - |
| `type` | `character varying` | 50 | ✓ | - | - |
| `priority` | `character varying` | 20 | ✓ | 'normal'::character varying | - |
| `status` | `character varying` | 20 | ✓ | 'active'::character varying | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |

## `categories` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('categories_id_seq'::regclass) | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `description` | `character varying` | 255 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |

## `communities` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('communities_id_seq'::regclass) | - |
| `name` | `character varying` | 100 | ✗ | - | - |
| `address` | `character varying` | 255 | ✓ | - | - |
| `contact_phone` | `character varying` | 20 | ✓ | - | - |
| `manager_name` | `character varying` | 50 | ✓ | - | - |
| `manager_phone` | `character varying` | 20 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `status` | `character varying` | 20 | ✓ | - | - |

## `deliverer_locations` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('deliverer_locations_id_seq'::regclass) | - |
| `deliverer_id` | `integer` | - | ✗ | - | - |
| `latitude` | `character varying` | 20 | ✗ | - | - |
| `longitude` | `character varying` | 20 | ✗ | - | - |
| `timestamp` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `deliverer_id` | `users` | `id` | `deliverer_locations_deliverer_id_fkey` |

## `deliverer_profiles` 表结构

**主键**: `user_id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `user_id` | `integer` | - | ✗ | - | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `phone` | `character varying` | 20 | ✓ | - | - |
| `vehicle_type` | `character varying` | 50 | ✓ | - | - |
| `status` | `character varying` | 20 | ✓ | 'offline'::character varying | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `area_id` | `integer` | - | ✓ | - | - |
| `avatar` | `character varying` | 255 | ✓ | - | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `user_id` | `users` | `id` | `deliverer_profiles_user_id_fkey` |
| `area_id` | `delivery_areas` | `id` | `deliverer_profiles_area_id_fkey` |

## `deliveries` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('deliveries_id_seq'::regclass) | - |
| `order_id` | `integer` | - | ✓ | - | - |
| `deliverer_id` | `integer` | - | ✓ | - | - |
| `end_time` | `timestamp with time zone` | - | ✓ | - | - |
| `estimated_time` | `timestamp with time zone` | - | ✓ | - | - |
| `status` | `character varying` | 20 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `actual_time` | `timestamp with time zone` | - | ✓ | - | - |
| `is_assigned_by_admin` | `boolean` | - | ✓ | false | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `order_id` | `orders` | `id` | `deliveries_order_id_fkey` |
| `deliverer_id` | `users` | `id` | `deliveries_deliverer_id_fkey` |

## `delivery_areas` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('delivery_areas_id_seq'::regclass) | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `description` | `text` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |

## `elder_member_relations` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('elder_member_relations_id_seq'::regclass) | - |
| `elder_id` | `integer` | - | ✓ | - | - |
| `member_id` | `integer` | - | ✓ | - | - |
| `relationship` | `character varying` | 50 | ✓ | - | - |
| `is_primary` | `boolean` | - | ✓ | false | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `elder_id` | `users` | `id` | `elder_member_relations_elder_id_fkey` |
| `member_id` | `users` | `id` | `elder_member_relations_member_id_fkey` |

## `elderly_profiles` 表结构

**主键**: `user_id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `user_id` | `integer` | - | ✗ | - | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `phone` | `character varying` | 20 | ✓ | - | - |
| `address` | `character varying` | 255 | ✓ | - | - |
| `dietary_preferences` | `text` | - | ✓ | - | - |
| `emergency_contact` | `character varying` | 50 | ✓ | - | - |
| `emergency_phone` | `character varying` | 20 | ✓ | - | - |
| `location` | `USER-DEFINED` | - | ✓ | - | - |
| `age` | `integer` | - | ✓ | - | - |
| `gender` | `character varying` | 10 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `community_id` | `integer` | - | ✓ | - | - |
| `health_tag_id` | `integer` | - | ✓ | - | - |
| `avatar` | `character varying` | 255 | ✓ | - | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `user_id` | `users` | `id` | `elderly_profiles_user_id_fkey` |
| `community_id` | `communities` | `id` | `fk_elderly_community` |
| `health_tag_id` | `health_tags` | `id` | `elderly_profiles_health_tag_id_fkey` |

## `emergency_calls` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('emergency_calls_id_seq'::regclass) | - |
| `elderly_id` | `integer` | - | ✓ | - | - |
| `emergency_type` | `character varying` | 50 | ✓ | - | - |
| `message` | `text` | - | ✓ | - | - |
| `location` | `USER-DEFINED` | - | ✓ | - | - |
| `response_status` | `character varying` | 20 | ✓ | 'pending'::character varying | - |
| `response_time` | `timestamp with time zone` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `elderly_id` | `users` | `id` | `emergency_calls_elderly_id_fkey` |

## `exceptions` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('exceptions_id_seq'::regclass) | - |
| `delivery_id` | `integer` | - | ✗ | - | - |
| `type` | `character varying` | 50 | ✗ | - | - |
| `description` | `text` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `delivery_id` | `deliveries` | `id` | `exceptions_delivery_id_fkey` |

## `favorites` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('favorites_id_seq'::regclass) | - |
| `elderly_id` | `integer` | - | ✓ | - | - |
| `meal_id` | `integer` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `elderly_id` | `users` | `id` | `favorites_elderly_id_fkey` |
| `meal_id` | `meals` | `id` | `favorites_meal_id_fkey` |

## `favorites_member` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('favorites_member_id_seq'::regclass) | - |
| `member_id` | `integer` | - | ✗ | - | - |
| `meal_id` | `integer` | - | ✗ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `member_id` | `users` | `id` | `favorites_member_member_id_fkey` |
| `meal_id` | `meals` | `id` | `favorites_member_meal_id_fkey` |

## `geography_columns` 表结构

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `f_table_catalog` | `name` | - | ✓ | - | - |
| `f_table_schema` | `name` | - | ✓ | - | - |
| `f_table_name` | `name` | - | ✓ | - | - |
| `f_geography_column` | `name` | - | ✓ | - | - |
| `coord_dimension` | `integer` | - | ✓ | - | - |
| `srid` | `integer` | - | ✓ | - | - |
| `type` | `text` | - | ✓ | - | - |

## `geometry_columns` 表结构

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `f_table_catalog` | `character varying` | 256 | ✓ | - | - |
| `f_table_schema` | `name` | - | ✓ | - | - |
| `f_table_name` | `name` | - | ✓ | - | - |
| `f_geometry_column` | `name` | - | ✓ | - | - |
| `coord_dimension` | `integer` | - | ✓ | - | - |
| `srid` | `integer` | - | ✓ | - | - |
| `type` | `character varying` | 30 | ✓ | - | - |

## `health_records` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('health_records_id_seq'::regclass) | - |
| `elderly_id` | `integer` | - | ✓ | - | - |
| `height` | `numeric` | - | ✓ | - | - |
| `weight` | `numeric` | - | ✓ | - | - |
| `blood_pressure` | `character varying` | 20 | ✓ | - | - |
| `blood_sugar` | `numeric` | - | ✓ | - | - |
| `allergies` | `text` | - | ✓ | - | - |
| `medications` | `text` | - | ✓ | - | - |
| `doctor_advice` | `text` | - | ✓ | - | - |
| `recorded_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `created_by` | `integer` | - | ✓ | - | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `elderly_id` | `users` | `id` | `health_records_elderly_id_fkey` |
| `created_by` | `users` | `id` | `health_records_created_by_fkey` |

## `health_reminders` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('health_reminders_id_seq'::regclass) | - |
| `sender_id` | `integer` | - | ✗ | - | - |
| `receiver_id` | `integer` | - | ✗ | - | - |
| `reminder_type` | `character varying` | 50 | ✗ | - | - |
| `content` | `text` | - | ✗ | - | - |
| `status` | `character varying` | 20 | ✓ | 'pending'::character varying | - |
| `scheduled_time` | `timestamp without time zone` | - | ✓ | - | - |
| `sent_time` | `timestamp without time zone` | - | ✓ | - | - |
| `read_time` | `timestamp without time zone` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | CURRENT_TIMESTAMP | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | CURRENT_TIMESTAMP | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `sender_id` | `users` | `id` | `health_reminders_sender_id_fkey` |
| `receiver_id` | `users` | `id` | `health_reminders_receiver_id_fkey` |

## `health_tags` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('health_tags_id_seq'::regclass) | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `description` | `text` | - | ✓ | - | - |
| `color` | `character varying` | 20 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

## `meals` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('meals_id_seq'::regclass) | - |
| `name` | `character varying` | 100 | ✗ | - | - |
| `price` | `numeric` | - | ✗ | - | - |
| `description` | `text` | - | ✓ | - | - |
| `special_tag` | `character varying` | 50 | ✓ | - | - |
| `image_url` | `character varying` | 255 | ✓ | - | - |
| `status` | `character varying` | 20 | ✓ | 'available'::character varying | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `category_id` | `integer` | - | ✓ | - | - |
| `tag_id` | `integer` | - | ✓ | - | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `category_id` | `categories` | `id` | `meals_category_id_fkey` |
| `tag_id` | `tags` | `id` | `meals_tag_id_fkey` |

## `member_profiles` 表结构

**主键**: `user_id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `user_id` | `integer` | - | ✗ | - | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `phone` | `character varying` | 20 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `avatar` | `character varying` | 255 | ✓ | - | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `user_id` | `users` | `id` | `member_profiles_user_id_fkey` |

## `order_items` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('order_items_id_seq'::regclass) | - |
| `order_id` | `integer` | - | ✓ | - | - |
| `meal_id` | `integer` | - | ✓ | - | - |
| `quantity` | `integer` | - | ✗ | - | - |
| `unit_price` | `numeric` | - | ✗ | - | - |
| `subtotal` | `numeric` | - | ✗ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `order_id` | `orders` | `id` | `order_items_order_id_fkey` |
| `meal_id` | `meals` | `id` | `order_items_meal_id_fkey` |

## `orders` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('orders_id_seq'::regclass) | - |
| `elderly_id` | `integer` | - | ✓ | - | - |
| `total_amount` | `numeric` | - | ✗ | - | - |
| `payment_method` | `character varying` | 50 | ✓ | - | - |
| `payment_status` | `character varying` | 20 | ✓ | 'pending'::character varying | - |
| `status` | `character varying` | 20 | ✓ | 'pending_payment'::character varying | - |
| `delivery_address` | `character varying` | 255 | ✓ | - | - |
| `notes` | `text` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `scheduled_time` | `timestamp with time zone` | - | ✓ | - | - |
| `order_type` | `character varying` | 20 | ✓ | 'immediate'::character varying | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `elderly_id` | `users` | `id` | `orders_elderly_id_fkey` |

## `payments` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('payments_id_seq'::regclass) | - |
| `order_id` | `integer` | - | ✗ | - | - |
| `payment_method` | `character varying` | 50 | ✗ | - | - |
| `amount` | `double precision` | - | ✗ | - | - |
| `transaction_id` | `character varying` | 100 | ✓ | - | - |
| `status` | `character varying` | 20 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `order_id` | `orders` | `id` | `payments_order_id_fkey` |

## `reviews` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('reviews_id_seq'::regclass) | - |
| `order_id` | `integer` | - | ✓ | - | - |
| `elderly_id` | `integer` | - | ✓ | - | - |
| `rating` | `integer` | - | ✓ | - | - |
| `content` | `text` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `status` | `character varying` | 20 | ✓ | 'approved'::character varying | - |
| `images` | `ARRAY` | - | ✓ | - | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | - | - |
| `reply` | `text` | - | ✓ | - | - |
| `ai_reviewed` | `integer` | - | ✓ | 0 | - |
| `ai_replied` | `integer` | - | ✓ | 0 | - |
| `deliverer_id` | `integer` | - | ✓ | - | - |
| `reviewer_type` | `character varying` | 20 | ✗ | - | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `order_id` | `orders` | `id` | `reviews_order_id_fkey` |
| `elderly_id` | `users` | `id` | `reviews_elderly_id_fkey` |
| `deliverer_id` | `users` | `id` | `reviews_deliverer_id_fkey` |

## `spatial_ref_sys` 表结构

**主键**: `srid`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `srid` | `integer` | - | ✗ | - | - |
| `auth_name` | `character varying` | 256 | ✓ | - | - |
| `auth_srid` | `integer` | - | ✓ | - | - |
| `srtext` | `character varying` | 2048 | ✓ | - | - |
| `proj4text` | `character varying` | 2048 | ✓ | - | - |

## `staff_schedules` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('staff_schedules_id_seq'::regclass) | - |
| `staff_id` | `integer` | - | ✗ | - | - |
| `schedule_date` | `date` | - | ✗ | - | - |
| `time_slot` | `character varying` | 20 | ✗ | - | - |
| `status` | `character varying` | 20 | ✓ | 'confirmed'::character varying | - |
| `note` | `text` | - | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `staff_id` | `users` | `id` | `staff_schedules_staff_id_fkey` |

## `tags` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('tags_id_seq'::regclass) | - |
| `name` | `character varying` | 50 | ✗ | - | - |
| `description` | `character varying` | 255 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |

## `users` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('users_id_seq'::regclass) | - |
| `username` | `character varying` | 50 | ✗ | - | - |
| `password_hash` | `character varying` | 255 | ✗ | - | - |
| `user_type` | `character varying` | 20 | ✗ | - | - |
| `status` | `character varying` | 20 | ✓ | 'active'::character varying | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `updated_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `email` | `character varying` | 100 | ✓ | - | - |
| `last_login` | `timestamp with time zone` | - | ✓ | - | - |
| `openid` | `character varying` | 100 | ✓ | - | - |
| `unionid` | `character varying` | 100 | ✓ | - | - |

## `voice_synthesis` 表结构

**主键**: `id`

| 列名 | 数据类型 | 长度 | 允许为空 | 默认值 | 注释 |
|------|----------|------|----------|--------|------|
| `id` | `integer` | - | ✗ | nextval('voice_synthesis_id_seq'::regclass) | - |
| `user_id` | `integer` | - | ✓ | - | - |
| `text_content` | `text` | - | ✗ | - | - |
| `voice_url` | `character varying` | 500 | ✓ | - | - |
| `voice_type` | `character varying` | 50 | ✓ | - | - |
| `language` | `character varying` | 20 | ✓ | - | - |
| `speed` | `double precision` | - | ✓ | - | - |
| `status` | `character varying` | 20 | ✓ | - | - |
| `created_at` | `timestamp with time zone` | - | ✓ | now() | - |
| `completed_at` | `timestamp with time zone` | - | ✓ | - | - |

**外键约束**:

| 列名 | 关联表 | 关联列 | 约束名称 |
|------|--------|--------|----------|
| `user_id` | `users` | `id` | `voice_synthesis_user_id_fkey` |

## 表关系信息

### 外键关系列表

| 表名 | 列名 | 关联表 | 关联列 |
|------|------|--------|--------|
| `admin_profiles` | `user_id` | `users` | `id` |
| `ai_conversations` | `user_id` | `users` | `id` |
| `deliverer_locations` | `deliverer_id` | `users` | `id` |
| `deliverer_profiles` | `user_id` | `users` | `id` |
| `deliverer_profiles` | `area_id` | `delivery_areas` | `id` |
| `deliveries` | `order_id` | `orders` | `id` |
| `deliveries` | `deliverer_id` | `users` | `id` |
| `elder_member_relations` | `elder_id` | `users` | `id` |
| `elder_member_relations` | `member_id` | `users` | `id` |
| `elderly_profiles` | `user_id` | `users` | `id` |
| `elderly_profiles` | `community_id` | `communities` | `id` |
| `elderly_profiles` | `health_tag_id` | `health_tags` | `id` |
| `emergency_calls` | `elderly_id` | `users` | `id` |
| `exceptions` | `delivery_id` | `deliveries` | `id` |
| `favorites` | `elderly_id` | `users` | `id` |
| `favorites` | `meal_id` | `meals` | `id` |
| `favorites_member` | `member_id` | `users` | `id` |
| `favorites_member` | `meal_id` | `meals` | `id` |
| `health_records` | `elderly_id` | `users` | `id` |
| `health_records` | `created_by` | `users` | `id` |
| `health_reminders` | `sender_id` | `users` | `id` |
| `health_reminders` | `receiver_id` | `users` | `id` |
| `meals` | `category_id` | `categories` | `id` |
| `meals` | `tag_id` | `tags` | `id` |
| `member_profiles` | `user_id` | `users` | `id` |
| `order_items` | `order_id` | `orders` | `id` |
| `order_items` | `meal_id` | `meals` | `id` |
| `orders` | `elderly_id` | `users` | `id` |
| `payments` | `order_id` | `orders` | `id` |
| `reviews` | `order_id` | `orders` | `id` |
| `reviews` | `elderly_id` | `users` | `id` |
| `reviews` | `deliverer_id` | `users` | `id` |
| `staff_schedules` | `staff_id` | `users` | `id` |
| `voice_synthesis` | `user_id` | `users` | `id` |
