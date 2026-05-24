<template>
  <div
    v-if="success.show"
    class="position-fixed top-0 end-0 p-3"
    style="z-index: 11"
  >
    <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto">{{ success.title }}</strong>
        <small>Just now</small>
        <button
          type="button"
          class="btn-close"
          @click="close"
        ></button>
      </div>
      <div class="toast-body" style="color: #000;">
        {{ success.message }}
      </div>
    </div>
  </div>
</template>

<script>
import { computed, watch } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'SuccessToastComponent',
  setup() {
    const store = useStore()

    const success = computed(() => store.state.success.successToast)

    // Auto-hide after 4 seconds
    watch(
      () => success.value?.timestamp,
      () => {
        if (success.value && success.value.show) {
          setTimeout(() => {
            store.dispatch('success/hideSuccess')
          }, 4000)
        }
      }
    )

    const close = () => {
      store.dispatch('success/hideSuccess')
    }

    return {
      success,
      close
    }
  }
}
</script>


<style>
.toast-header {
    background-color: #d1ecf1;
    color: #0c5460;
    border-bottom: 1px solid #bee5eb;
}
</style>