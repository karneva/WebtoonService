// stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

const savedToken = localStorage.getItem('token')
if (savedToken) {
  axios.defaults.headers.common['Authorization'] = `Token ${savedToken}`
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null, // user.is_survey_completed 포함
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
  async login(credentials) {
    try {
      const res = await axios.post('/api/auth/login/', credentials)
      
      // 1. 토큰 저장
      this.token = res.data.key
      localStorage.setItem('token', this.token)
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`
      
      // 2. 유저 정보 할당 (방어 코드 추가!)
      if (res.data.user) {
        // 백엔드에서 user 정보를 같이 보내준 경우
        this.user = res.data.user
      } else {
        // 백엔드 설정이 안 돼서 user 정보가 없는 경우 -> 직접 가져옴
        console.log("유저 정보가 없어서 직접 가져옵니다...")
        const userRes = await axios.get('/api/auth/user/')
        this.user = userRes.data
      }
      
      // 3. 라우팅 분기
      if (!this.user.is_survey_completed) {
        router.push('/survey')
      } else {
        router.push('/')
      }
    } catch (error) {
      console.error('로그인 실패', error)
      throw error
    }
  },
    
    // 유저 정보 갱신 (설문 완료 후 호출)
    async fetchUser() {
      if (!this.token) return
      try {
        const res = await axios.get('/api/auth/user/')
        this.user = res.data
      } catch (error) {
        console.error('유저 정보 로드 실패', error)
      }
    },

    // 설문 완료 처리 (서버 전송은 컴포넌트에서 하거나 여기서 해도 됨)
    async completeSurvey() {
       this.user.is_survey_completed = true
       await this.fetchUser() // 확실하게 서버 상태 동기화
    },
  // 👇 [추가] 로그아웃 액션
  async logout() {
    try {
      // 서버에 로그아웃 요청 (선택 사항: dj-rest-auth 사용 시 토큰 무효화 요청)
      if (this.token) {
        await axios.post('/api/auth/logout/')
      }
    } catch (error) {
      console.error('로그아웃 요청 실패', error)
      // 서버 에러가 나더라도 클라이언트는 로그아웃 처리 진행
    } finally {
      // 1. 상태 초기화
      this.token = null
      this.user = null
      
      // 2. 로컬 스토리지 삭제
      localStorage.removeItem('token')
      
      // 3. 헤더 삭제
      delete axios.defaults.headers.common['Authorization']
      
      // 4. 로그인 페이지로 이동
      router.push('/login')
    }
  },
  }
})
