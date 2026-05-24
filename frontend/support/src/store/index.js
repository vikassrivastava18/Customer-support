// src/store/index.js
import { createStore } from 'vuex'

import auth from './modules/auth'
import error from './modules/error'
import success from './modules/success'


export default createStore({
  modules: {
    auth,
    error,
    success
  }
})
