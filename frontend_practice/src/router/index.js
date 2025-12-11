import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // Pinia Store

// 뷰 컴포넌트 임포트
import HomeView from '../views/HomeView.vue'
import SurveyView from '../views/SurveyView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { hideNavbar: true } // 로그인 페이지는 헤더 숨김
    },
    {
      path: '/survey',
      name: 'survey',
      component: SurveyView,
      meta: { 
        requiresAuth: true, // 로그인 필요
        hideNavbar: true    // 헤더 숨김
      }
    },
    // 필요 시 회원가입 등 추가 라우트 여기에 등록
  ]
})

// --- 전역 네비게이션 가드 ---
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 1. 로그인 상태인지 확인 (토큰 유무 등)
  // 새로고침 시 Pinia 상태가 날아갈 수 있으므로 토큰 있으면 유저 정보 한번 불러오는 로직이 필요할 수 있음
  // 여기서는 간단히 store의 getter 사용
  const isAuthenticated = authStore.isAuthenticated

  // 2. 인증이 필요한 페이지인데 로그인을 안 했다면? -> 로그인 페이지로
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login')
  }

  // 3. 로그인 상태일 때 로직
  if (isAuthenticated) {
    // 유저 정보가 아직 로드 안 됐을 수도 있으니 체크 (optional)
    if (!authStore.user) {
      await authStore.fetchUser()
    }

    const isSurveyCompleted = authStore.user?.is_survey_completed

    // Case A: 설문을 아직 안 함 -> 무조건 설문 페이지로 납치
    // (단, 이미 설문 페이지에 있거나 로그아웃 중이면 제외)
    if (!isSurveyCompleted && to.name !== 'survey' && to.name !== 'logout') {
      return next('/survey')
    }

    // Case B: 설문을 이미 완료함 -> 설문 페이지 접근 차단 -> 메인으로
    if (isSurveyCompleted && to.name === 'survey') {
      return next('/')
    }
    
    // Case C: 이미 로그인된 상태에서 로그인 페이지 접근 시 -> 메인으로
    if (to.name === 'login') {
      return next('/')
    }
  }

  next()
})

export default router
