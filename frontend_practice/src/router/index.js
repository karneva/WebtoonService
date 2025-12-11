import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // 수정된 Pinia Store

// 뷰 컴포넌트 임포트
import HomeView from '../views/HomeView.vue'
import SurveyView from '../views/SurveyView.vue'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue' // [추가] 회원가입 뷰 임포트

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
      path: '/signup', // [추가] 회원가입 라우트
      name: 'signup',
      component: SignUpView,
      meta: { hideNavbar: true }
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
  ]
})

// --- 전역 네비게이션 가드 ---
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 1. 로그인 여부 확인
  const isAuthenticated = authStore.isAuthenticated

  // [중요] 로그인 상태인데 유저 정보가 없다면? (새로고침 상황 등)
  // 설문조사 완료 여부(is_survey_completed)를 알기 위해 반드시 정보를 가져와야 함
  if (isAuthenticated && !authStore.user) {
    await authStore.fetchUser()
  }

  // 2. 비로그인 유저가 인증이 필요한 페이지 접근 시 -> 로그인 페이지로
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'login' })
  }

  // 3. 로그인된 유저 처리 로직
  if (isAuthenticated) {
    const isSurveyCompleted = authStore.user?.is_survey_completed

    // Case A: 이미 로그인했는데 '로그인'이나 '회원가입' 페이지에 가려 할 때 -> 메인으로
    if (to.name === 'login' || to.name === 'signup') {
      return next({ name: 'home' })
    }

    // Case B: 설문을 아직 안 함 -> 무조건 설문 페이지로 납치
    // (단, 이미 설문 페이지에 있거나, 로그아웃 등의 예외 상황은 제외)
    if (!isSurveyCompleted && to.name !== 'survey') {
      // alert('서비스 이용을 위해 추가 정보를 입력해주세요!') // 필요 시 주석 해제
      return next({ name: 'survey' })
    }

    // Case C: 설문을 이미 완료함 -> 설문 페이지 접근 차단 -> 메인으로
    if (isSurveyCompleted && to.name === 'survey') {
      return next({ name: 'home' })
    }
  }

  next()
})

export default router
