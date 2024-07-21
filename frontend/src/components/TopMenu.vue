<template>
    <nav class="flex justify-between items-center border border-sky-600 text-sm bg-sky-200 px-10">
        <!-- Left side menu items -->
        <div class="flex items-center gap-4">
            <!-- Render left routes -->
            <div v-for="(route, index) in filteredLeftRoutes" :key="index" class="relative">
                <div v-if="route.children && route.children.length > 0">
                    <!-- Dropdown toggle for routes with children -->
                    <span class="cursor-pointer" @mouseenter="toggleSubmenu(index, true)"
                        @mouseleave="closeSubmenu(index)">
                        {{ route.name.charAt(0).toUpperCase() + route.name.slice(1) }} &#9662;
                    </span>
                    <!-- Submenu for routes that have children -->
                    <div v-if="showSubmenu[index]" class="submenu" @mouseenter="keepSubmenuOpen(index)"
                        @mouseleave="closeSubmenu(index)">
                        <router-link v-for="child in route.children" :key="child.name" :to="child.path"
                            class="block w-full text-left px-4 py-2 text-gray-600 hover:bg-sky-300"
                            active-class="font-bold">
                            {{ child.name.charAt(0).toUpperCase() + child.name.slice(1) }}
                        </router-link>
                    </div>
                </div>
                <router-link v-else :to="route.path" class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                    active-class="font-bold">
                    {{ route.name.charAt(0).toUpperCase() + route.name.slice(1) }}
                </router-link>
            </div>
        </div>

        <!-- Right side authentication controls -->
        <div class="flex items-center gap-8 relative">
            <span v-if="authStore.isAuthenticated && authStore.loginDataState"
                @mouseenter="toggleSubmenu('userMenu', true)" @mouseleave="closeSubmenu('userMenu')">
                Hello, {{ authStore.loginDataState.username }} &#9662;
            </span>
            <router-link v-if="!authStore.isAuthenticated" to="/login"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1"
                active-class="font-bold">Login</router-link>
            <button v-else @click="handleLogout"
                class="text-gray-600 hover:bg-sky-300 hover:text-white px-3 py-1">Logout
            </button>
            <!-- Submenu for authenticated user -->
            <div v-if="showSubmenu['userMenu']" class="submenu" @mouseenter="keepSubmenuOpen('userMenu')"
                @mouseleave="closeSubmenu('userMenu')">
                <button @click="handleLogout"
                    class="block w-full text-left px-4 py-2 text-gray-600 hover:bg-sky-300">Logout
                </button>
                <router-link to="/settings"
                    class="block w-full text-left px-4 py-2 text-gray-600 hover:bg-sky-300">Settings
                </router-link>
                <router-link to="/user-details"
                    class="block w-full text-left px-4 py-2 text-gray-600 hover:bg-sky-300">User
                    Details
                </router-link>
            </div>
        </div>
    </nav>
</template>

<script setup>
    import { ref, onMounted, computed } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import allRoutes from '@/data/allRoutesMenu.json';

    const authStore = useAuthStore();
    const showSubmenu = ref({});
    const submenuTimers = {};

    // XOR function for visibility logic
    const xnor = (a, b) => !(a ^ b);

    const leftRoutes = computed(() => allRoutes.filter(route => route.side === 'left'));

    const filteredLeftRoutes = computed(() => {
        return leftRoutes.value.filter(route => xnor(authStore.isAuthenticated, route.protected));
    });

    const toggleSubmenu = (key, state) => {
        showSubmenu.value[key] = state;
    };

    const keepSubmenuOpen = (key) => {
        clearTimeout(submenuTimers[key]);
        showSubmenu.value[key] = true;
    };

    const closeSubmenu = (key) => {
        submenuTimers[key] = setTimeout(() => {
            showSubmenu.value[key] = false;
        }, 20);
    };

    const handleLogout = () => {
        authStore.logout();
        showSubmenu.value['userMenu'] = false;
    };

    // Check authentication status on component mount
    onMounted(() => {
        authStore.checkAuth();
    });

    // Close all submenus when clicking outside
    document.addEventListener('click', (event) => {
        const target = event.target;
        if (!target.closest('.submenu') && !target.closest('span')) {
            Object.keys(showSubmenu.value).forEach(key => {
                showSubmenu.value[key] = false;
            });
        }
    });
</script>

<style scoped>
    .relative {
        position: relative;
    }

    .submenu {
        position: absolute;
        left: 0;
        /* Aligns submenu directly under the parent */
        top: calc(100% + 5px);
        /* Positions submenu just below the parent */
        background-color: white;
        border: 1px solid #38bdf8;
        margin-top: 0.5rem;
        padding: 0.5rem;
        z-index: 10;
        min-width: 120px;
        /* Adjust as needed */
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
