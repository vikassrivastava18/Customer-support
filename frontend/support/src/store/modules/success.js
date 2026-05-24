export default {
  namespaced: true,
  state: {
    successToast: {
      show: false,
      title: 'Success',
      message: '',
      timestamp: null
    }
  },
  mutations: {
    SHOW_SUCCESS(state, payload) {
      state.successToast.show = true
      state.successToast.title = payload.title || 'Sucess'
      state.successToast.message = payload.message
      state.successToast.timestamp = Date.now()
    },
    HIDE_SUCCESS(state) {
      state.successToast.show = false
      state.successToast.message = ''
    }
  },
  actions: {
    showSucsess({ commit }, payload) {
      commit('SHOW_SUCCESS', payload)
    },
    hideSuccess({ commit }) {
      commit('HIDE_SUCCESS')
    }
  },
  getters: {
    sucessToast: (state) => state.successToast
  }
}


