<!-- views/SignUpView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl shadow-xl">
      <div class="text-center">
        <!-- 아이콘 변경 (lock -> person_add) -->
        <div class="mx-auto h-12 w-12 bg-primary rounded-xl flex items-center justify-center text-white mb-4">
          <span class="material-symbols-outlined text-2xl">person_add</span>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900">회원가입</h2>
        <p class="mt-2 text-sm text-gray-600">
          이미 계정이 있으신가요? 
          <RouterLink :to="{ name: 'login' }" class="font-medium text-primary hover:text-indigo-500">
            로그인하기
          </RouterLink>
        </p>
      </div>

      <form class="mt-8 space-y-4" @submit.prevent="handleSignup">
        <div class="rounded-md shadow-sm space-y-4">
          
          <!-- 아이디 -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">아이디</label>
            <input 
              id="username" 
              v-model="form.username" 
              type="text" 
              required 
              class="appearance-none rounded-xl block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="아이디를 입력하세요"
            >
          </div>

          <!-- 이메일 (선택사항, 백엔드 요구사항에 따라 required 조정) -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">이메일</label>
            <input 
              id="email" 
              v-model="form.email" 
              type="email" 
              class="appearance-none rounded-xl block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="example@email.com"
            >
          </div>

          <!-- 나이 (초기 코드에 있었으므로 추가) -->
          <div>
            <label for="age" class="block text-sm font-medium text-gray-700 mb-1">나이</label>
            <input 
              id="age" 
              v-model.number="form.age" 
              type="number" 
              min="0"
              class="appearance-none rounded-xl block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="나이를 입력하세요"
            >
          </div>

          <!-- 비밀번호 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
            <input 
              id="password" 
              v-model="form.password" 
              type="password" 
              required 
              class="appearance-none rounded-xl block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="비밀번호"
            >
          </div>

          <!-- 비밀번호 확인 -->
          <div>
            <label for="passwordConfirm" class="block text-sm font-medium text-gray-700 mb-1">비밀번호 확인</label>
            <input 
              id="passwordConfirm" 
              v-model="form.passwordConfirm" 
              type="password" 
              required 
              class="appearance-none rounded-xl block w-full px-4 py-3 border border-gray-300 placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="비밀번호를 한 번 더 입력하세요"
            >
            <p v-if="passwordMismatch" class="mt-1 text-xs text-red-500 font-bold">
              비밀번호가 일치하지 않습니다.
            </p>
          </div>
        </div>

        <div v-if="errorMsg" class="text-red-500 text-sm text-center font-bold">
          {{ errorMsg }}
        </div>

        <div>
          <button 
            type="submit" 
            :disabled="isLoading || passwordMismatch"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            가입하기
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { RouterLink } from 'vue-router'

const authStore = useAuthStore()
const isLoading = ref(false)
const errorMsg = ref('')

const form = reactive({
  username: '',
  email: '',
  age: null,
  password: '',
  passwordConfirm: ''
})

// 비밀번호 일치 여부 실시간 확인
const passwordMismatch = computed(() => {
  return form.password && form.passwordConfirm && form.password !== form.passwordConfirm
})

const handleSignup = async () => {
  // 클라이언트 측 유효성 검사
  if (passwordMismatch.value) {
    errorMsg.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  isLoading.value = true
  errorMsg.value = ''

  try {

    // [수정] 백엔드가 원하는 이름(password1, password2)으로 변경
    const payload = {
      username: form.username,
      email: form.email,
      password1: form.password,       // password -> password1
      password2: form.passwordConfirm // passwordConfirm -> password2
      // age: form.age // ⚠️ 주의: 백엔드에 age 필드 설정 안 되어 있으면 에러 날 수 있음. 일단 주석 처리 추천.
    }

    // store의 signup 액션 호출 (내부에서 자동 로그인까지 수행)
    await authStore.signup(payload)
    
    // 성공 시 store 내부에서 페이지 이동 처리됨

  } catch (error) {
    console.error(error)
    // 백엔드 유효성 검사 에러 처리 (예: 이미 존재하는 아이디)
    if (error.response?.data) {
       // DRF의 경우 에러 메시지가 객체로 옴 (예: { username: ['이미 존재합니다.'] })
       const data = error.response.data
       // 첫 번째 에러 메시지 추출 예시
       const firstKey = Object.keys(data)[0]
       errorMsg.value = `${firstKey}: ${data[firstKey]}`
    } else {
       errorMsg.value = '회원가입 중 오류가 발생했습니다.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
