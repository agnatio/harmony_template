<!-- src/components/TopMenu.vue -->
<template>
    <nav class="flex gap-4 bg-gray-100 p-4">
        <router-link to="/" class="text-blue-500 hover:text-blue-700" active-class="font-bold">Home</router-link>
        <router-link to="/about" class="text-blue-500 hover:text-blue-700" active-class="font-bold">About</router-link>
    </nav>
</template>

<script setup>
</script>

<!-- No additional styles needed -->