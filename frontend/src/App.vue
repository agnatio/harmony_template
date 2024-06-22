<!-- src/App.vue -->
<template>
  <div id="app" class="font-sans text-center text-gray-800">
    <TopMenu />
    <router-view></router-view>
  </div>
</template>

<script setup>
  import TopMenu from './components/TopMenu.vue'
</script>

<!-- No need for additional styles since Tailwind is used -->
