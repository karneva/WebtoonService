<template>
  <div class="animate-fade-in-up relative">
    <h2 class="text-2xl font-extrabold text-gray-900 mb-2">거의 다 왔습니다!</h2>
    <p class="text-gray-500 mb-8">주로 이용하는 웹툰 플랫폼을 알려주세요.</p>

    <div class="space-y-3 mb-8">
      <label 
        v-for="p in platforms" :key="p"
        class="flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all hover:bg-gray-50"
        :class="selected === p ? 'border-primary bg-primary/5 ring-1 ring-primary' : 'border-gray-100'"
      >
        <input type="radio" :value="p" v-model="selected" class="w-5 h-5 text-primary focus:ring-primary border-gray-300">
        <span class="ml-3 font-bold text-gray-700">{{ p }}</span>
      </label>
    </div>

    <button 
      @click="submit" 
      :disabled="!selected || isSubmitting"
      class="w-full py-4 rounded-xl font-bold text-white bg-primary shadow-lg shadow-primary/30 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      결과 보기
    </button>

    <!-- 로딩 오버레이 -->
    <div v-if="isSubmitting" class="absolute inset-0 bg-white/90 backdrop-blur-sm flex flex-col items-center justify-center z-10 rounded-xl">
      <div class="w-12 h-12 border-4 border-gray-200 border-t-primary rounded-full animate-spin mb-4"></div>
      <p class="font-bold text-gray-800 animate-pulse">취향 분석 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
defineProps(['isSubmitting'])
const emit = defineEmits(['submit'])

const platforms = ['네이버웹툰', '카카오웹툰', '카카오페이지']
const selected = ref('')

const submit = () => emit('submit', { platform: selected.value })
</script>
