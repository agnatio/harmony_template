<template>
  <div id="app" class="">
    <TopMenu />
    <router-view></router-view>
  </div>
</template>

<script setup>
  import TopMenu from './components/TopMenu.vue'
</script>
