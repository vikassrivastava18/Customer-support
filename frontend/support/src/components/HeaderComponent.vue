<template>
  <header class="topbar">
    <div class="brand-wrap">
      <router-link to="/" class="brand-link" aria-label="Home">
        <img src="../../public/logo.png" alt="Logo" />
      </router-link>
    </div>

    <nav class="nav-group" aria-label="Main navigation">
      <template v-if="isStaff">
        <router-link to="/admin" class="nav-link">
          TICKETS
        </router-link>
      </template>

      <template v-else>
        <router-link to="/books" class="nav-link">
          MY BOOKS
        </router-link>

        <router-link to="/tickets" class="nav-link">
          TICKETS
        </router-link>
      </template>
    </nav>

    <div class="auth-area">
      <button
        v-if="isAuthenticated"
        type="button"
        class="auth-btn logout-btn"
        @click="logout"
      >
        Logout
      </button>

      <button
        v-else
        type="button"
        class="auth-btn login-btn"
        @click="login"
      >
        Login
      </button>
    </div>
  </header>
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
:root {
  --header-bg: #6d5456;
  --header-accent: #f6d1d5;
  --header-soft: #f7f1f2;
  --header-text: #ffffff;
  --header-muted: rgba(255, 255, 255, 0.75);
  --header-hover: #f2b3b8;
  --header-active: #ffd9dd;
  --button-text: #6d5456;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: linear-gradient(135deg, #6d5456 0%, #83686b 100%);
  padding: 0.7rem 1.5rem;
  box-shadow: 0 6px 18px rgba(32, 16, 18, 0.15);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-wrap {
  display: flex;
  align-items: center;
}

.brand-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.brand-link:hover {
  transform: scale(1.02);
}

.brand-link img {
  width: 100px;
  height: auto;
  display: block;
}

.nav-group {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  gap: 0.5rem;
}

.nav-link {
  color: var(--header-text);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.6rem 1rem;
  border-radius: 999px;
  transition: all 0.2s ease;
  opacity: 0.9;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  opacity: 1;
}

.router-link-exact-active,
.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.14);
  color: var(--header-active);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.12);
}

.auth-area {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  min-width: 120px;
}

.auth-btn {
  border: none;
  border-radius: 999px;
  padding: 0.6rem 1.1rem;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.login-btn {
  background: #fff;
  color: var(--button-text);
}

.logout-btn {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.auth-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
}

.login-btn:hover {
  background: #f6ebec;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .topbar {
    flex-wrap: wrap;
    justify-content: center;
    padding: 0.8rem 1rem;
  }

  .nav-group {
    width: 100%;
    order: 3;
    flex-wrap: wrap;
  }

  .auth-area {
    min-width: auto;
  }
}
</style>