export default {
  namespaced: true,
  state: {
    errorToast: {
      show: false,
      title: 'Error',
      message: '',
      timestamp: null
    }
  },
  mutations: {
    SHOW_ERROR(state, payload) {
      state.errorToast.show = true
      state.errorToast.title = payload.title || 'Error'
      state.errorToast.message = payload.message
      state.errorToast.timestamp = Date.now()
    },
    HIDE_ERROR(state) {
      state.errorToast.show = false
      state.errorToast.message = ''
    }
  },
  actions: {
    showError({ commit }, payload) {
      commit('SHOW_ERROR', payload)
    },
    hideError({ commit }) {
      commit('HIDE_ERROR')
    }
  },
  getters: {
    errorToast: (state) => state.errorToast
  }
}


