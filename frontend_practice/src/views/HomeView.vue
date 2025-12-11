<!-- src/views/HomeView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // 즐겨찾기 시 로그인 체크용

// --- [상태 관리 (State)] ---
const webtoons = ref([])
const loading = ref(false)
const currentProvider = ref('NAVER')
const authStore = useAuthStore()

// --- [기능 로직 (Actions)] ---

// 1. 웹툰 목록 불러오기
async function loadWebtoons(provider) {
  currentProvider.value = provider
  loading.value = true
  webtoons.value = []

  try {
    // axios 사용으로 변경 (프록시 /api/ 적용)
    const res = await axios.get('/api/webtoons/', {
      params: {
        provider: provider,
        page: 1,
        per_page: 100
      }
    })
    
    // DRF 응답 구조에 맞게 데이터 할당
    // (만약 에러나면 res.data 만 써보세요)
    webtoons.value = res.data.results || res.data
    
  } catch (error) {
    console.error('웹툰 로드 실패:', error)
    alert('웹툰 정보를 가져오는 데 실패했습니다.')
  } finally {
    loading.value = false
  }
}

// 2. 즐겨찾기 토글 (좋아요)
async function toggleFavorite(toon) {
  // Pinia Store로 로그인 상태 확인
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  // 낙관적 업데이트
  const previousState = toon.is_favorited
  toon.is_favorited = !toon.is_favorited

  try {
    // axios 사용
    await axios.post(`/api/webtoons/${toon.id}/favorite/`)
  } catch (error) {
    // 실패 시 롤백
    toon.is_favorited = previousState
    console.error('즐겨찾기 오류:', error)
    if (error.response && error.response.status === 401) {
      alert('로그인이 필요합니다.')
    } else {
      alert('오류가 발생했습니다.')
    }
  }
}

// --- [생명주기 훅 (Mounted)] ---
onMounted(() => {
  // 인증 체크 로직 삭제함 (App.vue에서 처리)
  loadWebtoons('NAVER')
})
</script>

<template>
  <div class="min-h-screen bg-background-light text-text-main font-sans selection:bg-primary/20 selection:text-primary pb-20">
    <main class="w-full max-w-[1200px] mx-auto px-6 mt-8">
      
      <!-- Title Section -->
      <div class="text-center mb-10">
        <h2 class="text-3xl font-extrabold text-text-main mb-2">오늘의 웹툰</h2>
        <p class="text-text-muted text-sm">다양한 플랫폼의 웹툰을 한눈에 모아보세요.</p>
      </div>

      <!-- Filter Buttons -->
      <div class="flex flex-wrap justify-center gap-3 mb-12">
        <button 
          v-for="provider in ['NAVER', 'KAKAO', 'KAKAO_PAGE']" 
          :key="provider"
          @click="loadWebtoons(provider)"
          :class="[
            'px-6 py-2.5 rounded-full text-sm font-bold shadow-sm transition-all duration-200 transform hover:-translate-y-0.5',
            currentProvider === provider 
              ? 'bg-primary text-white ring-2 ring-primary ring-offset-2' 
              : 'bg-white text-text-muted hover:bg-gray-50 border border-gray-200'
          ]"
        >
          {{ provider === 'KAKAO_PAGE' ? '카카오페이지' : (provider === 'NAVER' ? '네이버' : '카카오') }}
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-text-muted">
        <div class="size-10 border-4 border-gray-200 border-t-primary rounded-full animate-spin mb-4"></div>
        <p>웹툰을 불러오고 있습니다...</p>
      </div>

      <!-- Webtoon Grid -->
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-x-6 gap-y-10">
        <div v-for="toon in webtoons" :key="toon.id" class="group flex flex-col gap-3">
          
          <!-- Image Card -->
          <div class="relative aspect-[3/4] w-full rounded-2xl overflow-hidden shadow-soft group-hover:shadow-lg group-hover:-translate-y-1 transition-all duration-300 bg-gray-100">
            <!-- Link to Webtoon -->
            <a :href="toon.url" target="_blank" class="block w-full h-full">
              <img :src="toon.thumbnail" :alt="toon.title" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy">
            </a>

            <!-- Like Button -->
            <button 
              @click.stop="toggleFavorite(toon)"
              :class="[
                'absolute top-2 right-2 p-2 rounded-full backdrop-blur-md shadow-sm transition-all duration-200 z-10',
                toon.is_favorited ? 'bg-yellow-400 text-white' : 'bg-black/30 text-white/70 hover:bg-black/50'
              ]"
            >
              <span class="material-symbols-outlined text-[20px] block" style="font-variation-settings: 'FILL' 1;">star</span>
            </button>
          </div>

          <!-- Info -->
          <div>
            <h3 class="text-base font-bold text-text-main leading-tight truncate group-hover:text-primary transition-colors">
              {{ toon.title }}
            </h3>
            <div class="flex items-center justify-between mt-1">
              <p class="text-xs text-text-muted truncate max-w-[70%]">{{ toon.authors }}</p>
              <span class="text-[10px] font-bold text-primary bg-primary-light px-1.5 py-0.5 rounded">
                {{ toon.update_days }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && webtoons.length === 0" class="text-center py-20 text-gray-400">
        <span class="material-symbols-outlined text-4xl mb-2 block">sentiment_dissatisfied</span>
        <p>표시할 웹툰이 없습니다.</p>
      </div>
    </main>
  </div>
</template>
