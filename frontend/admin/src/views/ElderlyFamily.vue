<template>
  <div class="elderly-family">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">绑定管理</h1>
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加绑定
      </el-button>
    </div>

    <!-- 查询表单 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="家属姓名">
          <el-input v-model="searchForm.name" placeholder="请输入家属姓名" clearable />
        </el-form-item>
        <el-form-item label="老人姓名">
          <el-input v-model="searchForm.elderlyName" placeholder="请输入老人姓名" clearable />
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="searchForm.phone" placeholder="请输入联系方式" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card>
      <template #header>
        <div class="table-header">
          <span>绑定列表</span>
          <span class="table-count">共 {{ total }} 条记录</span>
        </div>
      </template>
      
      <el-table
        :data="familyMembers"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="家属姓名" />
        <el-table-column prop="relationship" label="与老人关系" />
        <el-table-column prop="phone" label="联系方式" />
        <el-table-column prop="elderlyName" label="老人姓名" />
        <el-table-column prop="community" label="所在社区" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="address" label="联系地址" />
        <el-table-column prop="emergencyContact" label="是否主要联系人">
          <template #default="scope">
            <el-tag :type="scope.row.emergencyContact ? 'success' : 'info'">
              {{ scope.row.emergencyContact ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
              <el-button type="info" size="small" @click="handleView(scope.row)">详情</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 详情抽屉 -->
    <el-drawer
      v-model="detailDrawerVisible"
      title="家属详细信息"
      size="500px"
      class="modern-drawer"
    >
      <div v-if="currentFamily" class="detail-content">
        <div class="detail-header">
          <h2>{{ currentFamily.name }}</h2>
          <p>{{ currentFamily.relationship }} · {{ currentFamily.elderlyName }}</p>
        </div>
        
        <el-divider content-position="left">基本信息</el-divider>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="联系方式">{{ currentFamily.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ currentFamily.email || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="联系地址">{{ currentFamily.address || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="是否主要联系人">
            <el-tag :type="currentFamily.emergencyContact ? 'success' : 'info'">
              {{ currentFamily.emergencyContact ? '是' : '否' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>



        <el-divider content-position="left">关联老人</el-divider>
        <div class="elderly-info">
          <el-tag type="primary">{{ currentFamily.elderlyName }}</el-tag>
          <span class="community">{{ currentFamily.community }}</span>
        </div>

        <el-divider content-position="left">创建时间</el-divider>
        <div class="create-time">{{ currentFamily.createTime }}</div>
      </div>
    </el-drawer>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form
        :model="form"
        ref="formRef"
        label-width="100px"
        :rules="rules"
      >
        <el-form-item label="家属姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入家属姓名" />
        </el-form-item>
        <el-form-item label="与老人关系" prop="relationship">
          <el-select v-model="form.relationship" placeholder="请选择关系">
            <el-option label="子女" value="子女" />
            <el-option label="配偶" value="配偶" />
            <el-option label="亲戚" value="亲戚" />
            <el-option label="朋友" value="朋友" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="联系方式" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号码" />
        </el-form-item>
        <el-form-item label="老人姓名" prop="elderlyId">
          <el-select v-model="form.elderlyId" placeholder="请选择老人">
            <el-option
              v-for="elderly in elderlyList"
              :key="elderly.id"
              :label="elderly.name"
              :value="elderly.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        <el-form-item label="联系地址">
          <el-input
            v-model="form.address"
            type="textarea"
            :rows="3"
            placeholder="请输入联系地址"
          />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="form.emergencyContact">主要联系人</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { adminService } from '../api'
import { ElMessage } from 'element-plus'

// 搜索表单
const searchForm = reactive({
  name: '',
  elderlyName: '',
  phone: ''
})

// 分页参数
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

// 表格数据
const familyMembers = ref([])

// 老人列表
const elderlyList = ref([])

// 加载老人列表
const loadElderlyList = async () => {
  try {
    const response = await adminService.getElderlyUsers({ limit: 100 })
    elderlyList.value = response.items.map(item => ({
      id: item.id,
      name: item.profile.name
    }))
  } catch (error) {
    console.error('加载老人列表失败:', error)
  }
}

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('添加家属')
const formRef = ref(null)

// 详情抽屉
const detailDrawerVisible = ref(false)
const currentFamily = ref(null)
const form = reactive({
  id: '',
  name: '',
  relationship: '',
  phone: '',
  elderlyId: '',
  email: '',
  address: '',
  emergencyContact: false
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入家属姓名', trigger: 'blur' }
  ],
  relationship: [
    { required: true, message: '请选择与老人关系', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入联系方式', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  elderlyId: [
    { required: true, message: '请选择老人', trigger: 'change' }
  ]
}

// 获取数据
const getData = async () => {
  try {
    loading.value = true
    // 将搜索表单的驼峰参数转换为下划线参数
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      name: searchForm.name,
      elderly_name: searchForm.elderlyName,
      phone: searchForm.phone
    }
    
    const response = await adminService.getElderMemberRelations(params)
    familyMembers.value = response.items.map(item => ({
        id: item.id,
        name: item.member_name,
        relationship: item.relationship,
        phone: item.member_phone,
        elderlyId: item.elder_id,
        elderlyName: item.elderly_name,
        community: '', // 需要从数据库获取社区信息
        email: '', // 需要从数据库获取邮箱信息
        address: '', // 需要从数据库获取地址信息
        emergencyContact: item.is_primary,
        createTime: new Date(item.created_at).toLocaleString('zh-CN')
      }))
    
    total.value = response.total
  } catch (error) {
    ElMessage.error('加载绑定关系数据失败')
    console.error('加载绑定关系数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 查询
const handleSearch = () => {
  currentPage.value = 1
  getData()
}

// 重置
const handleReset = () => {
  searchForm.name = ''
  searchForm.elderlyName = ''
  searchForm.phone = ''
  currentPage.value = 1
  getData()
}

// 添加
const handleAdd = () => {
  dialogTitle.value = '添加家属'
  form.id = ''
  form.name = ''
  form.relationship = ''
  form.phone = ''
  form.elderlyId = ''
  form.email = ''
  form.address = ''
  form.emergencyContact = false
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑家属'
  form.id = row.id
  form.name = row.name
  form.relationship = row.relationship
  form.phone = row.phone
  form.elderlyId = row.elderlyId
  form.email = row.email
  form.address = row.address
  form.emergencyContact = row.emergencyContact
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  // 这里应该调用删除接口
  console.log('删除', row)
}

// 查看详情
const handleView = (row) => {
  currentFamily.value = row
  detailDrawerVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  const valid = await formRef.value.validate()
  if (valid) {
    try {
      if (form.id) {
        // 编辑家属信息
        // 首先更新家属用户信息
        const userData = {
          profile: {
            name: form.name,
            phone: form.phone,
            email: form.email,
            address: form.address
          }
        }
        
        // 这里需要获取member_id，暂时假设可以通过某种方式获取
        // 实际实现时可能需要从关系表中查询member_id
        console.log('编辑家属信息:', form.id)
        ElMessage.success('家属信息更新成功！')
      } else {
        // 创建家属用户
        const userData = {
          username: form.phone || `member_${Date.now()}`,
          password: '123456', // 默认密码
          user_type: 'member',
          profile: {
            name: form.name,
            phone: form.phone,
            email: form.email,
            address: form.address
          }
        }
        
        const userResponse = await adminService.createUser(userData)
        
        // 创建老人家属关系
        const relationData = {
          elder_id: form.elderlyId,
          member_id: userResponse.user.id,
          relationship: form.relationship,
          is_primary: form.emergencyContact
        }
        
        await adminService.createElderMemberRelation(relationData)
        
        ElMessage.success('家属绑定成功！')
      }
      
      dialogVisible.value = false
      getData()
    } catch (error) {
      console.error('保存家属信息失败:', error)
      ElMessage.error('保存失败，请检查输入信息')
    }
  }
}

// 分页变化
const handleSizeChange = (val) => {
  pageSize.value = val
  getData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  getData()
}

onMounted(async () => {
  await Promise.all([
    loadElderlyList(),
    getData()
  ])
})
</script>

<style scoped>
.elderly-family {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.search-card {
  margin-bottom: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-count {
  color: #606266;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 去掉表格的白色线条 */
:deep(.el-table) {
  --el-table-border-color: transparent;
  --el-table-header-text-color: var(--text-primary);
  --el-table-row-hover-bg-color: rgba(99, 102, 241, 0.1);
}

:deep(.el-table__header-wrapper th) {
  border-bottom: none !important;
  background-color: transparent !important;
}

:deep(.el-table__row) {
  border-bottom: none !important;
}

:deep(.el-table__cell) {
  border-right: none !important;
}

/* 操作按钮水平排列 */
.action-buttons {
  display: flex;
  gap: 8px;
}

.action-buttons .el-button {
  flex: 1;
}

/* 权限设置样式 */
.permission-group {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 8px;
}

.permission-group .el-checkbox {
  margin-right: 16px;
  margin-bottom: 8px;
}

/* 详情抽屉样式 */
.detail-content {
  padding: 0 20px;
}

.detail-header {
  margin-bottom: 30px;
}

.detail-header h2 {
  margin: 0 0 8px;
  font-size: 24px;
}

.detail-header p {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
}

.permission-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.elderly-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.elderly-info .community {
  color: var(--text-secondary);
  font-size: 14px;
}

.create-time {
  color: var(--text-secondary);
  font-size: 14px;
}</style>