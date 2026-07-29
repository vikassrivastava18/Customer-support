
function checkAuth() {
  const token = localStorage.getItem('Authentication-Token')
  if (token) {
    return true
  }
  return false
}

function checkStaff() {
  const isStaff = localStorage.getItem('Is-Staff')
  console.log("isStaff", isStaff)
  return isStaff === 'true'
}

export default {
  namespaced: true,
  state: {
    isAuthenticated: checkAuth(),
    isStaff: checkStaff()
  },
  mutations: {
    login(state) {
      state.isAuthenticated = true
    },
    logout(state) {
      state.isAuthenticated = false
      localStorage.removeItem('Authentication-Token')
    },
    setStaff(state) {
      state.isStaff = true
    },
    removeStaff(state) {
      state.isStaff = false
      localStorage.removeItem('Is-Staff')
    }
  },
  actions: {
    login({ commit }) {
      commit('login')
    },
    logout({ commit }) {
      commit('logout')
    },
    setStaff({ commit}) {
      commit('setStaff')
    },
    removeStaff({ commit}) {
      commit('removeStaff')
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    isStaff: state => state.isStaff
  }
}

