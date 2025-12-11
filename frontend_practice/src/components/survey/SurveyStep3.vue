<template>
  <div class="animate-fade-in-up">
    <!-- 헤더 -->
    <div class="text-center mb-6">
      <h2 class="text-2xl font-extrabold text-gray-900 mb-2">이 작품 어떠셨나요? 🤔</h2>
      <p class="text-gray-500 text-sm">
        본 적 있는 웹툰만 평가해주세요.<br>
        <span class="text-primary font-bold">5개 이상</span> 평가하면 추천 정확도가 올라갑니다!
      </p>
    </div>

    <!-- 진행률 바 (Progress Bar) -->
    <div class="mb-8">
      <div class="flex justify-between text-xs font-bold mb-2">
        <span :class="validCount >= targetCount ? 'text-primary' : 'text-gray-400'">
          {{ validCount >= targetCount ? '✅ 목표 달성!' : '데이터 수집 중...' }}
        </span>
        <span class="text-gray-500">{{ validCount }}/{{ targetCount }}</span>
      </div>
      <div class="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
        <div 
          class="h-full transition-all duration-500 ease-out rounded-full"
          :class="validCount >= targetCount ? 'bg-primary' : 'bg-primary/60'"
          :style="{ width: Math.min((validCount / targetCount) * 100, 100) + '%' }"
        ></div>
      </div>
    </div>

    <!-- 메인 컨텐츠 영역 -->
    <div v-if="currentWebtoon" class="relative">
      
      <!-- 웹툰 카드 -->
      <div class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm mb-6">
        <!-- 썸네일 이미지 -->
        <div class="aspect-[2/3] w-full rounded-xl overflow-hidden bg-gray-100 mb-4 relative shadow-inner">
          <img 
            v-if="currentWebtoon.thumbnail_url" 
            :src="currentWebtoon.thumbnail_url" 
            alt="웹툰 썸네일"
            class="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
            @error="handleImageError" 
          />
          <div v-else class="absolute inset-0 flex items-center justify-center text-gray-400 font-bold text-sm">
            이미지 준비중
          </div>
        </div>
        
        <!-- 타이틀 -->
        <h3 class="text-xl font-bold text-gray-800 text-center truncate px-2 mb-1">
          {{ currentWebtoon.title }}
        </h3>
        <p class="text-xs text-gray-400 text-center mb-4">
           {{ currentWebtoon.genre || '장르 정보 없음' }}
        </p>

        <!-- 평가 버튼 그리드 -->
        <div class="grid grid-cols-4 gap-2 mb-3">
          <button 
            v-for="opt in ratingOptions" 
            :key="opt.value"
            @click="handleRate(opt.value)"
            class="flex flex-col items-center justify-center py-3 rounded-xl transition-all duration-200 active:scale-95 shadow-sm text-white font-bold text-sm"
            :class="opt.colorClass"
          >
            <span>{{ opt.label }}</span>
          </button>
        </div>

        <!-- 보지 않음 버튼 -->
        <button 
          @click="handleRate('보지 않음')" 
          class="w-full py-3 rounded-xl border-2 border-gray-100 text-gray-500 font-bold hover:bg-gray-50 hover:border-gray-200 transition-colors"
        >
          아직 안 봤어요 (Skip)
        </button>
      </div>

    </div>

    <!-- 로딩 상태 (데이터 없을 때) -->
    <div v-else class="flex flex-col items-center justify-center py-20">
      <div class="w-10 h-10 border-4 border-gray-200 border-t-primary rounded-full animate-spin mb-4"></div>
      <p class="text-gray-400 font-medium animate-pulse">다음 작품을 불러오고 있어요...</p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits(['next', 'update-data'])

// --- State ---
const webtoonQueue = ref([])      
const currentIndex = ref(0)       
const ratings = ref({})           
const isLoading = ref(false)
const targetCount = 5             // 목표 유효 응답 수

// 버튼 옵션 (Tailwind 컬러 적용)
const ratingOptions = [
  { label: '별로', value: '최악', colorClass: 'bg-rose-400 hover:bg-rose-500' },
  { label: '글쎄', value: '나쁨', colorClass: 'bg-amber-400 hover:bg-amber-500' },
  { label: '볼만해', value: '좋음', colorClass: 'bg-emerald-400 hover:bg-emerald-500' },
  { label: '최고야', value: '최고', colorClass: 'bg-violet-500 hover:bg-violet-600' },
]

// --- Computed ---
const currentWebtoon = computed(() => webtoonQueue.value[currentIndex.value] || null)

const validCount = computed(() => {
  return Object.values(ratings.value).filter(val => val !== '보지 않음').length
})

// --- Methods ---
const fetchWebtoons = async (count) => {
  try {
    isLoading.value = true
    const res = await axios.get('/api/webtoons/random/', { params: { count } })
    
    // 중복 및 이미 평가한 항목 제외
    const newItems = res.data.filter(item => {
      const isRated = ratings.value.hasOwnProperty(item.title) // ID 대신 title을 키로 쓸 수도 있음 (기획에 따라 조정)
      // 여기서는 title로 중복체크 하거나 ID로 하거나 통일 필요. 
      // API가 id를 준다면 id 권장. 
      const isRatedById = ratings.value[item.id] !== undefined
      const isInQueue = webtoonQueue.value.some(q => q.id === item.id)
      return !isRatedById && !isInQueue
    })
    
    webtoonQueue.value.push(...newItems)
  } catch (error) {
    console.error("데이터 로드 실패:", error)
  } finally {
    isLoading.value = false
  }
}

const handleImageError = (e) => {
  // 이미지 로드 실패 시 투명 이미지나 기본 배경색 유지
  e.target.style.display = 'none'; 
  e.target.parentElement.classList.add('flex', 'items-center', 'justify-center', 'text-xs', 'text-gray-400');
  e.target.parentElement.innerText = '이미지 없음';
}

const handleRate = async (score) => {
  if (!currentWebtoon.value) return

  // 1. 데이터 기록
  const webtoonId = currentWebtoon.value.id
  ratings.value[webtoonId] = score
  
  emit('update-data', ratings.value)

  // 2. 다음 로직 판단
  const isLastItem = currentIndex.value >= webtoonQueue.value.length - 1

  if (isLastItem) {
    // 큐의 끝
    if (validCount.value >= targetCount) {
      emit('next') // 완료
    } else {
      // 부족함 -> 추가 로드
      // UX: 사용자에게 살짝 알림 (Toast 대신 버튼 텍스트 변경 등으로 처리 가능하나 여기선 바로 로드)
      const needed = targetCount - validCount.value + 3 // 넉넉하게 3개 추가
      await fetchWebtoons(needed)
      currentIndex.value++
    }
  } else {
    // 큐 남음
    currentIndex.value++
  }
}

onMounted(() => {
  fetchWebtoons(10)
})
</script>
