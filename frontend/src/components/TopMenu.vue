<!-- src/components/TopMenu.vue -->
<template>
    <nav class="flex justify-between items-center border border-sky-600 text-sm bg-sky-200 px-10">
        <div class="flex items-center gap-4">
            <router-link to="/" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">Home</router-link>
            <router-link to="/about" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">About</router-link>
            <router-link to="/register" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">Register</router-link>
            <!-- Add more links or groupings here as needed -->
        </div>
        <div class="flex items-center gap-8">
            <router-link to="/login" class="text-gray-600 hover:bg-sky-300 hover:text-white hover: px-3 py-1"
                active-class="font-bold">Login</router-link>
        </div>
    </nav>
</template>


<script setup>
</script>

<!-- No additional styles needed -->