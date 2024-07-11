<template>
    <main v-if="isAuthenticated">
        <p>Protected View</p>
    </main>
    <div v-else>
        <p>Redirecting to login...</p>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import authApi from '@/core/authApi'
    import { router } from '@/router'

    const isAuthenticated = ref(false)

    onMounted(async () => {
        const authStatus = await authApi.checkAuth()
        if (authStatus) {
            isAuthenticated.value = true
        } else {
            router.push({ name: 'login' })
        }
    })
</script>