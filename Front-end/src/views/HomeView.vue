<!-- src/views/HomeView.vue -->
<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/api/axios'; // [중요] 설정해둔 axios import
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const webtoons = ref([]);
const loading = ref(false);
const currentProvider = ref('NAVER');

// 1. 웹툰 목록 불러오기 (Axios 사용)
async function loadWebtoons(provider) {
  currentProvider.value = provider;
  loading.value = true;
  webtoons.value = [];

  try {
    // axios는 기본 baseURL이 설정되어 있으므로 뒷부분 경로만 작성
    // 주의: 백엔드 urls.py 구조에 따라 경로가 다를 수 있음. 
    // 예: /api/webtoons/ 가 맞는지 확인 필요 (이전 코드에선 /api/webtoons/)
    const response = await axios.get('http://127.0.0.1:8000/api/webtoons/', {
      params: {
        provider,
        page: 1,
        per_page: 100,
      }
    });
    
    // DRF Pagination을 쓴다면 .results 안에 데이터가 있음
    webtoons.value = response.data.results || response.data;
    console.log(`불러온 웹툰 개수: ${webtoons.value.length}`);
  } catch (error) {
    console.error('웹툰 로드 실패:', error);
    alert('웹툰 정보를 가져오는 데 실패했습니다.');
  } finally {
    loading.value = false;
  }
}

// 2. 즐겨찾기 토글
async function toggleFavorite(toon) {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.');
    return;
  }

  const previousState = toon.is_favorited;
  toon.is_favorited = !toon.is_favorited;

  try {
    // Axios 요청 (토큰은 인터셉터가 자동 추가)
    await axios.post(`http://127.0.0.1:8000/api/webtoons/${toon.id}/favorite/`);
  } catch (error) {
    // 실패 시 롤백
    toon.is_favorited = previousState;
    console.error('즐겨찾기 오류:', error);
    alert('오류가 발생했습니다.');
  }
}

onMounted(() => {
  loadWebtoons('NAVER');
});
</script>

<template>
  <div>
    <!-- Title Section -->
    <div class="text-center mb-10">
      <h2 class="text-3xl font-extrabold text-text-main mb-2">오늘의 웹툰</h2>
      <p class="text-text-muted text-sm">다양한 플랫폼의 웹툰을 한눈에 모아보세요.</p>
    </div>

    <!-- Filter Buttons -->
    <div class="flex flex-wrap justify-center gap-3 mb-12">
      <button 
        v-for="provider in ['NAVER', 'KAKAO', 'KAKAOPAGE']" 
        :key="provider"
        @click="loadWebtoons(provider)"
        :class="[
          'px-6 py-2.5 rounded-full text-sm font-bold shadow-sm transition-all duration-200 transform hover:-translate-y-0.5',
          currentProvider === provider 
            ? 'bg-primary text-white ring-2 ring-primary ring-offset-2' 
            : 'bg-white text-text-muted hover:bg-gray-50 border border-gray-200'
        ]"
      >
        {{ provider === 'KAKAOPAGE' ? '카카오페이지' : (provider === 'NAVER' ? '네이버' : '카카오') }}
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
  </div>
</template>
