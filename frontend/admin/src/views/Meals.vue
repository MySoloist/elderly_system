<template>
  <div class="meals-manage">
    <div class="page-header">
      <div class="header-info">
        <h1>餐品菜谱管理</h1>
        <p>管理社区每日供应的营养餐点与菜谱</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" size="large" round @click="handleAdd">
          <el-icon><Plus /></el-icon>发布新餐品
        </el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-tabs v-model="activeTab" class="modern-tabs" @tab-change="handleTabChange">
        <el-tab-pane label="按分类筛选" name="category" />
        <el-tab-pane label="按标签筛选" name="tag" />
      </el-tabs>
      
      <div v-show="activeTab === 'category'" class="category-tabs">
        <el-tabs v-model="activeCategory" @tab-change="loadMeals">
          <el-tab-pane label="全部餐品" name="all" />
          <el-tab-pane 
            v-for="category in categories" 
            :key="category.id" 
            :label="category.name" 
            :name="category.id.toString()" 
          />
        </el-tabs>
      </div>
      
      <div v-show="activeTab === 'tag'" class="tag-tabs">
        <el-tabs v-model="activeTag" @tab-change="loadMeals">
          <el-tab-pane label="全部餐品" name="all" />
          <el-tab-pane 
            v-for="tag in tags" 
            :key="tag.id" 
            :label="tag.name" 
            :name="tag.id.toString()" 
          />
        </el-tabs>
      </div>
      
      <div class="search-wrapper">
        <el-input v-model="search" placeholder="搜索菜名..." prefix-icon="Search" clearable />
      </div>
    </div>

    <el-row :gutter="24">
      <el-col :span="6" v-for="meal in meals" :key="meal.id" class="mb-30">
        <transition name="fade">
          <div class="meal-card-v2" :key="meal.id">
            <div class="image-wrapper">
              <img :src="meal.image" :alt="meal.name" />
              <transition name="status-change">
                <div 
                  class="status-badge" 
                  :class="meal.status === '供应中' ? 'active' : 'soldout'"
                  :key="meal.status"
                >
                  {{ meal.status }}
                </div>
              </transition>
              <div class="hover-actions">
                <el-button type="primary" circle :icon="Edit" @click="handleEdit(meal)" />
                <el-button type="danger" circle :icon="Delete" @click="handleDelete(meal)" />
              </div>
            </div>
            <div class="meal-content">
              <div class="meal-header">
                <h3 class="meal-title">{{ meal.name }}</h3>
                <span class="meal-price">￥{{ meal.price }}</span>
              </div>
              <p class="meal-desc">{{ meal.description }}</p>
              <div class="meal-footer">
                <div class="nutrition-tags">
                  <span v-for="tag in meal.nutrition" :key="tag" class="n-tag">{{ tag }}</span>
                </div>
                <el-switch v-model="meal.isAvailable" size="small" @change="handleStatusChange(meal)" />
              </div>
            </div>
          </div>
        </transition>
      </el-col>
    </el-row>

    <!-- 添加/编辑餐品弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditMode ? '编辑餐品' : '发布新餐品'"
      width="600px"
      center
    >
      <el-form :model="mealForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="餐品名称" required>
              <el-input v-model="mealForm.name" placeholder="请输入餐品名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="价格" required>
              <el-input-number v-model="mealForm.price" :min="0" :precision="2" step="0.01" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类标签" required>
              <el-select
                v-model="mealForm.category"
                placeholder="请选择餐品分类"
                style="width: 100%"
              >
                <el-option 
                  v-for="category in categories" 
                  :key="category.id" 
                  :label="category.name" 
                  :value="category.name" 
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="营养标签">
              <el-select
                v-model="mealForm.nutrition"
                multiple
                placeholder="请选择营养标签"
                style="width: 100%"
              >
                <el-option 
                  v-for="tag in nutritionTags" 
                  :key="tag.name" 
                  :label="tag.name" 
                  :value="tag.name" 
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="餐品描述" required>
          <el-input
            v-model="mealForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入餐品描述"
          />
        </el-form-item>
        
        <el-form-item label="餐品图片">
          <el-input v-model="mealForm.image" placeholder="请输入图片URL" />
          <div v-if="mealForm.image" class="image-preview">
            <el-image
              :src="mealForm.image"
              fit="cover"
              style="width: 100%; max-height: 200px;"
              :preview-src-list="[mealForm.image]"
            />
          </div>
        </el-form-item>
        
        <el-form-item label="供应状态">
          <el-radio-group v-model="mealForm.status">
            <el-radio label="供应中" />
            <el-radio label="已售罄" />
          </el-radio-group>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMeal">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit, Delete, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminService } from '../api'

const activeTab = ref('category')
const activeCategory = ref('all')
const activeTag = ref('all')
const search = ref('')
const dialogVisible = ref(false)
const isEditMode = ref(false)
const currentMeal = ref(null)
const loading = ref(false)

// 餐品表单数据
const mealForm = ref({
  name: '',
  price: 0,
  category: '',
  description: '',
  nutrition: [],
  image: '',
  status: '供应中',
  isAvailable: true
})

const meals = ref([])
const nutritionTags = ref([])
const categories = ref([])
const tags = ref([])

// 加载营养标签
const loadNutritionTags = async () => {
  try {
    const response = await adminService.getTags()
    nutritionTags.value = response.tags || []
  } catch (error) {
    console.error('加载营养标签失败:', error)
    // 如果获取标签失败，使用默认标签
    nutritionTags.value = [
      { name: '低糖' },
      { name: '素食' },
      { name: '清淡' },
      { name: '高蛋白' },
      { name: '易消化' },
      { name: '营养' }
    ]
  }
}

// 加载标签数据
const loadTags = async () => {
  try {
    const response = await adminService.getTags()
    tags.value = response.tags || []
  } catch (error) {
    console.error('加载标签数据失败:', error)
    // 如果获取标签失败，使用默认标签
    tags.value = [
      { id: 8, name: '低糖' },
      { id: 9, name: '素食' },
      { id: 10, name: '清淡' },
      { id: 11, name: '高蛋白' },
      { id: 12, name: '易消化' },
      { id: 13, name: '营养' }
    ]
  }
}

// 加载分类数据
const loadCategories = async () => {
  try {
    const response = await adminService.getCategories()
    categories.value = response.categories || []
  } catch (error) {
    console.error('加载分类数据失败:', error)
    // 如果获取分类失败，使用默认分类
    categories.value = [
      { id: 4, name: '主食' },
      { id: 5, name: '凉菜' },
      { id: 6, name: '荤菜' },
      { id: 7, name: '辅食' },
      { id: 10, name: '营养套餐' }
    ]
  }
}



// 处理标签切换
const handleTabChange = () => {
  // 切换标签时重新加载餐品数据
  loadMeals()
}

// 加载餐品数据
const loadMeals = async () => {
  try {
    loading.value = true
    
    const params = {}
    
    // 根据当前选中的标签页进行筛选
    if (activeTab.value === 'category') {
      // 按分类筛选
      if (activeCategory.value !== 'all') {
        const category = categories.value.find(cat => cat.id.toString() === activeCategory.value)
        if (category) {
          params.category = category.name
        }
      }
    } else {
      // 按标签筛选
      if (activeTag.value !== 'all') {
        const tag = tags.value.find(t => t.id.toString() === activeTag.value)
        if (tag) {
          params.tag = tag.name
        }
      }
    }
    
    const response = await adminService.getMeals(params)
    meals.value = response.items.map(item => {
      // 处理标签数据
      let nutrition = []
      
      // 如果有special_tag（多个标签）
      if (item.special_tag) {
        nutrition = item.special_tag.split(',')
      } 
      // 如果只有单个标签
      else if (item.tag) {
        nutrition = [item.tag.name]
      }
      
      return {
        id: item.id,
        name: item.name,
        price: item.price,
        description: item.description || '',
        status: item.status === 'available' ? '供应中' : '已售罄',
        isAvailable: item.status === 'available',
        nutrition: nutrition,
        image: item.image_url || ''
      }
    })
  } catch (error) {
    ElMessage.error('加载餐品数据失败')
    console.error('加载餐品数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 添加餐品
const handleAdd = () => {
  isEditMode.value = false
  mealForm.value = {
    name: '',
    price: 0,
    description: '',
    nutrition: [],
    image: '',
    status: '供应中',
    isAvailable: true
  }
  dialogVisible.value = true
}

// 编辑餐品
const handleEdit = (meal) => {
  isEditMode.value = true
  currentMeal.value = meal
  mealForm.value = { ...meal }
  dialogVisible.value = true
}

// 删除餐品
const handleDelete = async (meal) => {
  ElMessageBox.confirm(
    `确定要删除餐品 "${meal.name}" 吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await adminService.deleteMeal(meal.id)
      const index = meals.value.findIndex(item => item.id === meal.id)
      if (index !== -1) {
        meals.value.splice(index, 1)
        ElMessage.success('删除成功！')
      }
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('删除餐品失败:', error)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 状态切换
const handleStatusChange = async (meal) => {
  try {
    const updateData = {
      status: meal.isAvailable ? 'available' : 'unavailable'
    }
    await adminService.updateMeal(meal.id, updateData)
    meal.status = meal.isAvailable ? '供应中' : '已售罄'
    ElMessage.success(`餐品 "${meal.name}" 已${meal.isAvailable ? '启用' : '禁用'}供应`)
  } catch (error) {
    meal.isAvailable = !meal.isAvailable
    ElMessage.error('更新状态失败')
    console.error('更新餐品状态失败:', error)
  }
}

// 保存餐品
const saveMeal = async () => {
  // 表单验证
  if (!mealForm.value.name) {
    ElMessage.warning('请输入餐品名称')
    return
  }
  if (!mealForm.value.price) {
    ElMessage.warning('请输入餐品价格')
    return
  }
  if (!mealForm.value.category) {
    ElMessage.warning('请选择餐品分类')
    return
  }
  if (!mealForm.value.description) {
    ElMessage.warning('请输入餐品描述')
    return
  }
  
  try {
    if (isEditMode.value) {
        // 编辑模式 - 提交所有字段
        const updateData = {
          name: mealForm.value.name,
          price: mealForm.value.price,
          description: mealForm.value.description,
          category: mealForm.value.category,
          image_url: mealForm.value.image,
          status: mealForm.value.status === '供应中' ? 'available' : 'unavailable',
          nutrition: mealForm.value.nutrition
        }
        await adminService.updateMeal(currentMeal.value.id, updateData)
        ElMessage.success('编辑成功！')
    } else {
          // 添加模式
          const createData = {
            name: mealForm.value.name,
            price: mealForm.value.price,
            description: mealForm.value.description,
            category: mealForm.value.category || '营养套餐',
            image_url: mealForm.value.image,
            nutrition: mealForm.value.nutrition
          }
      await adminService.createMeal(createData)
      ElMessage.success('添加成功！')
    }
    
    dialogVisible.value = false
    await loadMeals()
  } catch (error) {
    ElMessage.error('保存餐品失败')
    console.error('保存餐品失败:', error)
  }
}

// 组件挂载时加载数据
onMounted(async () => {
  await loadNutritionTags()
  await loadCategories()
  await loadTags()
  await loadMeals()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header-info h1 {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 8px 0;
}

.header-info p {
  color: var(--text-light);
  margin: 0;
}

.filter-bar {
  margin-bottom: 30px;
  background: var(--bg-secondary);
  padding: 20px 24px;
  border-radius: 16px;
  box-shadow: var(--shadow-sm);
}

.modern-tabs {
  margin-bottom: 20px;
}

.category-tabs, .tag-tabs {
  margin-bottom: 20px;
}

.search-wrapper {
  width: 250px;
}

.mb-30 { margin-bottom: 30px; }

.meal-card-v2 {
  background: var(--bg-secondary);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.meal-card-v2:hover {
  transform: translateY(-10px);
  box-shadow: var(--shadow-lg);
}

.image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.meal-card-v2:hover .image-wrapper img {
  transform: scale(1.1);
}

.status-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  backdrop-filter: blur(4px);
}

.status-badge.active {
  background: rgba(78, 205, 196, 0.9);
  color: #fff;
}

.status-badge.soldout {
  background: rgba(178, 190, 195, 0.9);
  color: #fff;
}

.hover-actions {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-wrapper:hover .hover-actions {
  opacity: 1;
}

.meal-content {
  padding: 20px;
}

.meal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.meal-title {
  font-size: 18px;
  font-weight: 800;
  margin: 0;
  color: var(--text-main);
}

.meal-price {
  font-size: 20px;
  font-weight: 800;
  color: var(--primary-color);
}

.meal-desc {
  font-size: 13px;
  color: var(--text-regular);
  line-height: 1.6;
  height: 42px;
  overflow: hidden;
  margin-bottom: 16px;
}

.meal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #f1f2f6;
}

.nutrition-tags {
  display: flex;
  gap: 6px;
}

.n-tag {
  font-size: 10px;
  background: #f1f2f6;
  color: var(--text-regular);
  padding: 2px 8px;
  border-radius: 6px;
  font-weight: 600;
}

/* 图片预览样式 */
.image-preview {
  margin-top: 12px;
  max-width: 100%;
  border-radius: 8px;
  overflow: hidden;
}</style>
