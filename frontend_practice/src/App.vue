<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // Pinia Store 사용
import { computed } from 'vue'

const route = useRoute()
const authStore = useAuthStore()

// 현재 라우트의 meta 정보에 따라 네비게이션 표시 여부 결정
const showNavbar = computed(() => !route.meta.hideNavbar)

const handleLogout = () => {
  if (confirm('정말 로그아웃 하시겠습니까?')) {
    authStore.logout() // AuthStore에 구현된 로그아웃 액션 호출
    // 또는 location.href = '/login' 등 처리
  }
}
</script>

<template>
  <div class="min-h-screen bg-background-light text-text-main font-sans selection:bg-primary/20 selection:text-primary pb-20">
    
    <!-- Navbar (Sticky) -->
    <!-- showNavbar가 true일 때만 렌더링 -->
    <header 
      v-if="showNavbar" 
      class="sticky top-0 z-50 w-full bg-white/90 backdrop-blur-md border-b border-gray-100 shadow-sm transition-all duration-300"
    >
      <div class="max-w-[1200px] mx-auto px-6 h-16 flex items-center justify-between">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2 group">
          <div class="size-8 bg-primary rounded-lg flex items-center justify-center text-white shadow-sm group-hover:bg-accent transition-colors">
            <span class="material-symbols-outlined">auto_stories</span>
          </div>
          <h1 class="text-xl font-extrabold tracking-tight text-primary group-hover:text-accent transition-colors">ToonsToon</h1>
        </router-link>

        <!-- Nav Links -->
        <nav class="flex items-center gap-4">
          <router-link to="/" class="text-sm font-semibold text-text-muted hover:text-primary transition-colors">홈</router-link>
          <a href="#" class="text-sm font-semibold text-text-muted hover:text-primary transition-colors">마이페이지</a>
          
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="text-sm font-semibold text-primary hover:underline">로그인</router-link>
          </template>
          <template v-else>
            <button @click="handleLogout" class="px-4 py-1.5 text-xs font-bold text-white bg-primary rounded-full hover:bg-opacity-90 shadow-sm transition-transform active:scale-95">
              로그아웃
            </button>
          </template>
        </nav>
      </div>
    </header>

    <!-- Main Content Area -->
    <main>
      <!-- 현재 URL에 맞는 컴포넌트(HomeView, SurveyView 등)가 여기에 표시됨 -->
      <router-view />
    </main>

  </div>
</template>
