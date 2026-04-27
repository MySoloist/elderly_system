import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import MainLayout from '../layout/MainLayout.vue'

// 懒加载路由
const Dashboard = () => import('../views/Dashboard.vue')
const Orders = () => import('../views/Orders.vue')
const Elderly = () => import('../views/Elderly.vue')
const MemberManagement = () => import('../views/MemberManagement.vue')
const Delivery = () => import('../views/Delivery.vue')
const Meals = () => import('../views/Meals.vue')
const Users = () => import('../views/Users.vue')
const StaffSchedule = () => import('../views/StaffSchedule.vue')
const Communities = () => import('../views/Communities.vue')
const Announcements = () => import('../views/Announcements.vue')
const Feedback = () => import('../views/Feedback.vue')
const Settings = () => import('../views/Settings.vue')
const QuickOrder = () => import('../views/QuickOrder.vue')
const Profile = () => import('../views/Profile.vue')

// 路由守卫
const requireAuth = (to, from, next) => {
  const token = localStorage.getItem('token')
  if (token) {
    next()
  } else {
    next('/login')
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { title: '登录' }
    },
    {
      path: '/',
      component: MainLayout,
      beforeEnter: requireAuth,
      children: [
        {
          path: '',
          redirect: '/dashboard'
        },
        {
          path: '/dashboard',
          name: 'Dashboard',
          component: Dashboard,
          meta: { title: '仪表盘' }
        },
        {
          path: '/orders',
          name: 'Orders',
          component: Orders,
          meta: { title: '订单管理' }
        },
        {
          path: '/elderly',
          name: 'Elderly',
          component: Elderly,
          meta: { title: '老人管理' }
        },

        {
          path: '/members',
          name: 'MemberManagement',
          component: MemberManagement,
          meta: { title: '家属管理' }
        },

        {
          path: '/delivery-staff',
          name: 'DeliveryStaff',
          component: Users,
          meta: { title: '跑腿管理' }
        },
        {
          path: '/staff-schedule',
          name: 'StaffSchedule',
          component: StaffSchedule,
          meta: { title: '配送员排班' }
        },
        {
          path: '/meals',
          name: 'Meals',
          component: Meals,
          meta: { title: '餐品管理' }
        },
        {
          path: '/users',
          name: 'Users',
          component: Users,
          meta: { title: '用户管理' }
        },
        {
          path: '/communities',
          name: 'Communities',
          component: Communities,
          meta: { title: '社区管理' }
        },
        {
          path: '/announcements',
          name: 'Announcements',
          component: Announcements,
          meta: { title: '通知公告' }
        },
        {
          path: '/feedback',
          name: 'Feedback',
          component: Feedback,
          meta: { title: '评价管理' }
        },
        {
          path: '/settings',
          name: 'Settings',
          component: Settings,
          meta: { title: '系统设置' }
        },
        {
          path: '/quick-order',
          name: 'QuickOrder',
          component: QuickOrder,
          meta: { title: '快速下单' }
        },
        {
          path: '/profile',
          name: 'Profile',
          component: Profile,
          meta: { title: '个人中心' }
        }
      ]
    }
  ]
})

// 设置页面标题
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 颐养膳食系统` : '颐养膳食系统'
  next()
})

export default router