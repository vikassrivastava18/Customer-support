function check_auth() {
  const token = localStorage.getItem('Authentication-Token')
  if (token) {
    return true
  }
  return false
}

export default {
  namespaced: true,
  state: {
    isAuthenticated: check_auth()
  },
  mutations: {
    login(state) {
      state.isAuthenticated = true
    },
    logout(state) {
      state.isAuthenticated = false
      localStorage.removeItem('Authentication-Token')
    }
  },
  actions: {
    login({ commit }) {
      commit('login')
    },
    logout({ commit }) {
      commit('logout')
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated
  }
}

