<!-- src/components/Dropdown.vue -->
<template>
    <div class="relative">
        <span class="cursor-pointer" @mouseenter="toggleDropdown(true)" @mouseleave="startCloseTimer">
            <slot name="toggle"></slot>
        </span>
        <div v-if="isOpen" class="submenu" @mouseenter="toggleDropdown(true)" @mouseleave="closeDropdown">
            <slot name="content"></slot>
        </div>
    </div>
</template>

<script setup>
    import { ref, onUnmounted } from 'vue';

    const isOpen = ref(false);
    let closeTimer = null;

    const toggleDropdown = (state) => {
        isOpen.value = state;
    };

    const startCloseTimer = () => {
        closeTimer = setTimeout(() => {
            isOpen.value = false;
        }, 200);
    };

    const closeDropdown = () => {
        clearTimeout(closeTimer);
        isOpen.value = true;
    };

    onUnmounted(() => {
        clearTimeout(closeTimer);
    });
</script>

<style scoped>
    .submenu {
        position: absolute;
        left: 0;
        top: calc(100% + 5px);
        background-color: white;
        border: 1px solid #090a0a;
        margin-top: 0.5rem;
        padding: 0.5rem;
        z-index: 10;
        min-width: 120px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .submenu button,
    .submenu a {
        display: block;
        width: 100%;
        text-align: left;
        padding: 0.5rem 1rem;
        color: #4b5563;
        text-decoration: none;
    }

    .submenu button:hover,
    .submenu a:hover {
        background-color: #7dd3fc;
    }
</style>