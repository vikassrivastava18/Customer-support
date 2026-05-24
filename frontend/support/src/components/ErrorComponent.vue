<template>
  <div
    v-if="error.show"
    class="position-fixed top-0 end-0 p-3"
    style="z-index: 11"
  >
    <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto">{{ error.title }}</strong>
        <small>Just now</small>
        <button
          type="button"
          class="btn-close"
          @click="close"
        ></button>
      </div>
      <div class="toast-body" style="color: #000;">
        {{ error.message }}
      </div>
    </div>
  </div>
</template>

<script>
import { computed, watch } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'ErrorComponent',
  setup() {
    const store = useStore()

    const error = computed(() => store.state.error.errorToast)

    // Auto-hide after 4 seconds
    watch(
      () => error.value?.timestamp,
      () => {
        if (error.value && error.value.show) {
          setTimeout(() => {
            store.dispatch('error/hideError')
          }, 4000)
        }
      }
    )

    const close = () => {
      store.dispatch('error/hideError')
    }

    return {
      error,
      close
    }
  }
}
</script>

<style scoped>
.toast-header {
    background-color: #e03d4b;
    color: #fcf2f3;
    border-bottom: 1px solid #f5c6cb;
}
</style>