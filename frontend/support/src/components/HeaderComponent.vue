<template>
    <div class="d-flex justify-content-between p-2" id="headerDiv">
        <router-link to="/" class="nav-link text_white">
            <img src="../../public/logo.png" width="100" alt="">
        </router-link>

        <div v-if="isStaff">
            <router-link to="/admin" class="nav-link">
                TICKETS
            </router-link>
        </div>

        <div v-if="!isStaff">
            <router-link to="/books" class="nav-link">
                MY BOOKS
            </router-link>
        </div>

        <div v-if="!isStaff">
            <router-link to="/tickets" class="nav-link">
                TICKETS
            </router-link>
        </div>

        <div class="text-end mt-2" v-if="isAuthenticated">
            <button type="button" class="btn btn-sm me-4" @click="logout">Logout</button>
        </div>
        <div class="text-end" v-else>
            <button type="button" class="btn btn-sm me-4" @click="login">Login</button>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const isAuthenticated = computed(() => store.state.auth.isAuthenticated)
const isStaff = computed(() => store.state.auth.isStaff)

const logout = () => {
    store.dispatch('auth/logout')
    store.dispatch('auth/removeStaff')
    router.push('/login')
}

const login = () => {
    router.push('/login')
}
</script>

<style scoped>
    h3,
    h4 {
        color: #e76774;
    }

    .text_black {
        color: black;
    }

    .text_white {
        color: white;
        font-size: smaller
    }

    .nav-link {
        padding: 0.3rem 1rem;
        font-size: x-large;
        line-height: 1.2;
    }

    button {
        background-color: #fff;
    }

    .router-link-exact-active {
        color: #42b983;
        font-weight: bold;
    }
</style>