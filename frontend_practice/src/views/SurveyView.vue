<!-- views/SurveyView.vue -->
<template>
  <div class="min-h-screen bg-background-light flex items-center justify-center p-6">
    <div class="w-full max-w-lg bg-white rounded-3xl shadow-xl overflow-hidden">
      
      <!-- 상단 진행바 -->
      <div class="h-1.5 w-full bg-gray-100">
        <div 
          class="h-full bg-primary transition-all duration-500 ease-out" 
          :style="{ width: (currentStep / 4) * 100 + '%' }"
        ></div>
      </div>

      <!-- 컨텐츠 영역 -->
      <div class="p-8 md:p-10">
        <SurveyStep1 
          v-if="currentStep === 1" 
          @next="handleNext" 
        />
        <SurveyStep2 
          v-if="currentStep === 2" 
          @next="handleNext" 
        />
        <SurveyStep3 
          v-if="currentStep === 3" 
          @next="handleNext" 
          @update-data="updateWebtoonRatings"
        />
        <SurveyStep4 
          v-if="currentStep === 4" 
          @submit="handleSubmit" 
          :is-submitting="isSubmitting"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

import SurveyStep1 from '@/components/survey/SurveyStep1.vue'
import SurveyStep2 from '@/components/survey/SurveyStep2.vue'
import SurveyStep3 from '@/components/survey/SurveyStep3.vue'
import SurveyStep4 from '@/components/survey/SurveyStep4.vue'

const router = useRouter()
const authStore = useAuthStore()

const currentStep = ref(1)
const isSubmitting = ref(false)

const surveyData = reactive({
  birth_year: null,
  gender: null,
  genres: [],
  ratings: {},
  platform: ''
})

const handleNext = (stepData) => {
  if (stepData) Object.assign(surveyData, stepData)
  currentStep.value++
}

const updateWebtoonRatings = (ratings) => {
  surveyData.ratings = ratings
}

const handleSubmit = async (platformData) => {
  surveyData.platform = platformData.platform
  isSubmitting.value = true
  
  try {
    // API 호출 (헤더 토큰은 axios 설정 확인 필요)
    await axios.post('/api/survey/submit/', surveyData)
    await authStore.completeSurvey()
    
    // 로딩 효과를 위해 잠시 대기 (UX)
    setTimeout(() => {
        router.push('/')
    }, 1000)
  } catch (error) {
    console.error(error)
    alert("오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
  } finally {
    isSubmitting.value = false
  }
}
</script>
