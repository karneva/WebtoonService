import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)

  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
  }

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials) => {
    try {
      const res = await axios.post('/api/auth/login/', credentials)
      
      const receivedToken = res.data.key
      token.value = receivedToken
      localStorage.setItem('token', receivedToken)
      axios.defaults.headers.common['Authorization'] = `Token ${receivedToken}`

      if (res.data.user) {
        user.value = res.data.user
      } else {
        await fetchUser()
      }

      if (!user.value?.is_survey_completed) {
        router.push({ name: 'survey' })
      } else {
        router.push({ name: 'home' })
      }
    } catch (error) {
      console.error('로그인 실패', error)
      throw error
    }
  }

  // [추가] 회원가입 액션
  const signup = async (payload) => {
    try {
      // 1. 회원가입 요청
      // (백엔드 URL이 /accounts/signup/ 인지 /api/auth/registration/ 인지 확인 필요)
      // 여기서는 일반적인 관례인 /api/auth/signup/ 으로 작성합니다.
      await axios.post('/api/auth/registration/', payload)
      
      // 2. 가입 성공 시 자동 로그인 시도
      const { username } = payload
      
      // [수정] payload에 password1이 있으면 그걸 쓰고, 없으면 password를 씀 (안전장치)
      const password = payload.password1 || payload.password 

      await login({ username, password })

    } catch (error) {
      console.error('회원가입 실패', error)
      throw error
    }
  }

  const fetchUser = async () => {
    if (!token.value) return
    try {
      const res = await axios.get('/api/auth/user/')
      user.value = res.data
    } catch (error) {
      console.error('유저 정보 로드 실패', error)
    }
  }

  const completeSurvey = async () => {
    if (user.value) {
      user.value.is_survey_completed = true
      await fetchUser() 
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await axios.post('/api/auth/logout/')
      }
    } catch (error) {
      console.error('로그아웃 요청 실패', error)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      router.push({ name: 'login' })
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    signup, // 외부로 노출
    fetchUser,
    completeSurvey,
    logout,
  }
})
