<!-- views/LoginView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-3xl shadow-xl">
      <div class="text-center">
        <!-- 로고/아이콘 영역 -->
        <div class="mx-auto h-12 w-12 bg-primary rounded-xl flex items-center justify-center text-white mb-4">
          <span class="material-symbols-outlined text-2xl">lock</span>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900">로그인</h2>
        <p class="mt-2 text-sm text-gray-600">
          계정이 없으신가요? 
          <!-- [수정] a 태그 -> RouterLink 사용 -->
          <RouterLink :to="{ name: 'signup' }" class="font-medium text-primary hover:text-indigo-500">
            회원가입
          </RouterLink>
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div class="mb-4">
            <label for="username" class="sr-only">아이디</label>
            <input 
              id="username" 
              v-model="credentials.username" 
              name="username" 
              type="text" 
              required 
              class="appearance-none rounded-xl relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm transition-all" 
              placeholder="아이디"
            >
          </div>
          <div>
            <label for="password" class="sr-only">비밀번호</label>
            <input 
              id="password" 
              v-model="credentials.password" 
              name="password" 
              type="password" 
              required 
              class="appearance-none rounded-xl relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm transition-all" 
              placeholder="비밀번호"
            >
          </div>
        </div>

        <div v-if="errorMsg" class="text-red-500 text-sm text-center font-bold">
          {{ errorMsg }}
        </div>

        <div>
          <button 
            type="submit" 
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all active:scale-95 disabled:opacity-50"
          >
            <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            로그인
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { RouterLink } from 'vue-router' // 명시적 임포트 (auto-import 안 쓸 경우 대비)

const authStore = useAuthStore()
const credentials = reactive({
  username: '',
  password: ''
})
const isLoading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  isLoading.value = true
  errorMsg.value = ''
  try {
    // AuthStore의 login 액션 호출 -> 성공 시 내부에서 router.push 발생
    await authStore.login(credentials)
  } catch (error) {
    console.error(error)
    // 백엔드 에러 메시지(예: 400 Bad Request)가 있으면 더 구체적으로 보여줄 수도 있음
    // if (error.response && error.response.status === 400) ...
    errorMsg.value = '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.'
  } finally {
    isLoading.value = false
  }
}
</script>
