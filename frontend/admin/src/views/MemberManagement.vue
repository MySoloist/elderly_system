<template>
  <div class="member-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">家属管理</h1>
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>添加家属
      </el-button>
    </div>

    <!-- 查询表单 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="家属姓名">
          <el-input v-model="searchForm.name" placeholder="请输入家属姓名" clearable />
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
          <span>家属列表</span>
          <span class="table-count">共 {{ total }} 条记录</span>
        </div>
      </template>
      
      <el-table
        :data="members"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="name" label="家属姓名" />
        <el-table-column prop="phone" label="联系方式" />

        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="400">
          <template #default="scope">
            <div style="display: flex; gap: 8px;">
              <el-button size="small" type="info" @click="handleView(scope.row)">详情</el-button>
              <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
              <el-button size="small" type="warning" @click="handleBind(scope.row)">绑定</el-button>
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

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="formData"
        label-width="100px"
        :rules="rules"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="家属姓名" prop="name">
          <el-input v-model="formData.name" placeholder="请输入家属姓名" />
        </el-form-item>
        <el-form-item label="联系方式" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入手机号码" />
        </el-form-item>


      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="家属详情"
      width="700px"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="用户名">
          {{ detailRow?.username }}
        </el-descriptions-item>
        <el-descriptions-item label="家属姓名">
          {{ detailRow?.name }}
        </el-descriptions-item>
        <el-descriptions-item label="联系方式">
          {{ detailRow?.phone }}
        </el-descriptions-item>

        <el-descriptions-item label="创建时间">
          {{ detailRow?.created_at }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 绑定老人列表 -->
      <el-divider content-position="left">绑定老人列表</el-divider>
      <el-table
        :data="boundElderlyList"
        style="width: 100%"
        v-loading="boundElderlyLoading"
      >
        <el-table-column prop="elderlyName" label="老人姓名" />
        <el-table-column prop="relationship" label="与老人关系" />
        <el-table-column prop="emergencyContact" label="主要联系人">
          <template #default="scope">
            <el-tag :type="scope.row.emergencyContact ? 'success' : 'info'">
              {{ scope.row.emergencyContact ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="绑定时间" width="180" />
      </el-table>
      <div v-if="boundElderlyList.length === 0 && !boundElderlyLoading" class="empty-state">
        <el-empty description="暂无绑定老人" />
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="300px"
    >
      <p>确定要删除家属 <span style="color: #f56c6c">{{ deleteRow?.name }}</span> 吗？</p>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="handleConfirmDelete">确定删除</el-button>
        </div>
      </template>
    </el-dialog>



    <!-- 绑定老人对话框 -->
    <el-dialog
      v-model="bindDialogVisible"
      :title="bindDialogTitle"
      width="500px"
    >
      <el-form
        :model="bindForm"
        ref="bindFormRef"
        label-width="100px"
        :rules="bindRules"
      >
        <el-form-item label="与老人关系" prop="relationship">
          <el-select v-model="bindForm.relationship" placeholder="请选择关系">
            <el-option label="子女" value="子女" />
            <el-option label="配偶" value="配偶" />
            <el-option label="亲戚" value="亲戚" />
            <el-option label="朋友" value="朋友" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="老人姓名" prop="elderlyId">
          <el-select v-model="bindForm.elderlyId" placeholder="请选择老人">
            <el-option
              v-for="elderly in elderlyList"
              :key="elderly.id"
              :label="elderly.name"
              :value="elderly.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="bindForm.emergencyContact">主要联系人</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="bindDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleBindSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { adminService } from '../api/admin'

// 家属管理数据
const members = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)

// 老人列表（用于绑定功能）
const elderlyList = ref([])

// 绑定老人列表（用于详情查看）
const boundElderlyList = ref([])
const boundElderlyLoading = ref(false)

// 查询表单
const searchForm = reactive({
  name: '',
  phone: ''
})

// 对话框
const dialogVisible = ref(false)
const detailDialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const bindDialogVisible = ref(false)
const dialogTitle = ref('添加家属')
const bindDialogTitle = ref('绑定老人')
const formRef = ref(null)
const bindFormRef = ref(null)
const formData = reactive({
  id: null,
  username: '',
  name: '',
  phone: ''
})
const bindForm = reactive({
  memberId: '',
  relationship: '',
  elderlyId: '',
  emergencyContact: false
})
const detailRow = ref(null)
const deleteRow = ref(null)

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入家属姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系方式', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],

}

// 绑定表单验证规则
const bindRules = {
  relationship: [
    { required: true, message: '请选择与老人关系', trigger: 'change' }
  ],
  elderlyId: [
    { required: true, message: '请选择老人', trigger: 'change' }
  ]
}

// 获取数据
const getData = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      ...searchForm
    }
    
    const response = await adminService.getMemberUsers(params)
    members.value = response.items.map(item => ({
      ...item,
      name: item.profile?.name || '',
      phone: item.profile?.phone || ''
    }))
    
    total.value = response.total
  } catch (error) {
    ElMessage.error('加载家属数据失败')
    console.error('加载家属数据失败:', error)
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
  searchForm.phone = ''
  currentPage.value = 1
  getData()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  getData()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  getData()
}

// 获取家属绑定的老人列表
const getBoundElderlyList = async (memberId) => {
  try {
    boundElderlyLoading.value = true
    console.log('获取绑定列表，memberId:', memberId)
    const response = await adminService.getElderMemberRelations({ member_id: memberId })
    console.log('绑定列表响应:', response)
    boundElderlyList.value = response.items.map(item => ({
      elderlyName: item.elderly_name,
      relationship: item.relationship,
      emergencyContact: item.is_primary,
      createTime: new Date(item.created_at).toLocaleString('zh-CN')
    }))
    console.log('处理后的绑定列表:', boundElderlyList.value)
  } catch (error) {
    console.error('加载绑定老人列表失败:', error)
    boundElderlyList.value = []
  } finally {
    boundElderlyLoading.value = false
  }
}

// 查看详情
const handleView = async (row) => {
  detailRow.value = row
  await getBoundElderlyList(row.id)
  detailDialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑家属'
  formData.id = row.id
  formData.username = row.username
  formData.name = row.name
  formData.phone = row.phone
  dialogVisible.value = true
}

// 删除确认
const handleDelete = (row) => {
  deleteRow.value = row
  deleteDialogVisible.value = true
}

// 确认删除
const handleConfirmDelete = async () => {
  try {
    await adminService.deleteUser(deleteRow.value.id)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    getData()
  } catch (error) {
    ElMessage.error('删除失败')
    console.error('删除失败:', error)
  }
}

// 添加家属
const handleAdd = () => {
  dialogTitle.value = '添加家属'
  formData.id = null
  formData.username = ''
  formData.name = ''
  formData.phone = ''
  dialogVisible.value = true
}

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (formData.id) {
          // 更新
          await adminService.updateUser(formData.id, {
            username: formData.username,
            profile: {
              name: formData.name,
              phone: formData.phone
            }
          })
          ElMessage.success('更新成功')
        } else {
          // 添加
          await adminService.createUser({
            username: formData.username,
            password: '123456', // 默认密码
            user_type: 'member',
            profile: {
              name: formData.name,
              phone: formData.phone
            }
          })
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        getData()
      } catch (error) {
        ElMessage.error(formData.id ? '更新失败' : '添加失败')
        console.error('提交失败:', error)
      }
    }
  })
}

// 加载老人列表（用于绑定功能）
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

// 处理绑定按钮点击
const handleBind = (row) => {
  bindDialogTitle.value = '绑定老人'
  bindForm.memberId = row.id
  bindForm.relationship = ''
  bindForm.elderlyId = ''
  bindForm.emergencyContact = false
  bindDialogVisible.value = true
}

// 处理绑定表单提交
const handleBindSubmit = async () => {
  if (!bindFormRef.value) return
  const valid = await bindFormRef.value.validate()
  if (valid) {
    try {
      // 调用绑定接口
      await adminService.createElderMemberRelation({
        member_id: bindForm.memberId,
        elder_id: bindForm.elderlyId,
        relationship: bindForm.relationship,
        is_primary: bindForm.emergencyContact
      })
      ElMessage.success('绑定成功')
      bindDialogVisible.value = false
    } catch (error) {
      ElMessage.error('绑定失败')
      console.error('绑定失败:', error)
    }
  }
}

// 初始化
onMounted(async () => {
  await Promise.all([
    getData(),
    loadElderlyList()
  ])
})
</script>

<style scoped>
.member-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
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
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 详情对话框样式 */
:deep(.el-descriptions) {
  background-color: #1a1a2e !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

:deep(.el-descriptions__inner) {
  background-color: #1a1a2e !important;
}

:deep(.el-descriptions__header) {
  color: #ffffff !important;
}

:deep(.el-descriptions__table) {
  color: #ffffff !important;
  background-color: #1a1a2e !important;
}

:deep(.el-descriptions__cell) {
  background-color: #1a1a2e !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #ffffff !important;
}

:deep(.el-descriptions__label) {
  color: #ffffff !important;
  font-weight: 600;
}

:deep(.el-descriptions__content) {
  color: #ffffff !important;
}

:deep(.el-divider__text) {
  color: #ffffff !important;
}
</style>
