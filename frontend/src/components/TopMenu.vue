<!-- src/components/TopMenu.vue -->
<template>
    <nav class="flex gap-4 bg-sky-100 p-1">
        <router-link to="/" class="text-gray-750 hover:text-gray-900" active-class="font-bold">Home</router-link>
        <router-link to="/about" class="text-gray-750 hover:text-gray-900" active-class="font-bold">About</router-link>
        <router-link to="/login" class="text-gray-750 hover:text-gray-900" active-class="font-bold">Login</router-link>
    </nav>
</template>

<script setup>
</script>

<!-- No additional styles needed -->