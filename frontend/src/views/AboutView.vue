<template>
  <main class="flex items-top justify-center h-[calc(100vh-1.3rem)] bg-gray-500 pt-10">
    <div class="text-left space-y-6">
      <p class="text-lg text-gray-800">Welcome to SQL Harmony project! Your access to Oracle Fusion queries</p>
      <div class="aspect-w-16 aspect-h-9">
        <iframe class="rounded-lg shadow-md" width="560" height="315"
          src="https://www.youtube.com/embed/EHFOJzrnjD4?si=yh8m4H4g4Ivge8WK" title="YouTube video player"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
    </div>
  </main>
</template>

<script setup>
import {onMounted} from 'vue'
import authApi from '@/core/authApi'

onMounted(() => {
  authApi.checkAuth()
})
</script>
