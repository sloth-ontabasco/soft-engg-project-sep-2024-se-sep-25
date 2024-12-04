import { createStore } from 'vuex'
import {login} from '../api/auth'
import * as jose from 'jose'

const user = JSON.parse(localStorage.getItem('user'))
const initialState = user
  ? {
      loggedIn: true,
      user: user,
      msg: '',
      loading: false
    }
  : {
      loggedIn: false ,
      user: null,
      msg: '',
      loading: false
    }

export default createStore({
  state: initialState,
  actions: {
    async getAuthToken({ commit }, jwt) {
      try {
        const res = await login(jwt) 
        localStorage.setItem("token", res.token);
        commit('loginSuccess',res.token)
      } catch(e) {
        console.log(e)
        commit("loginFailure");
        throw new Error("Login Failure");
      }
    },
  },
  mutations: {
    loginSuccess(state, jwt) {
        let decoded_user = jose.decodeJwt(jwt)
        localStorage.setItem("user", JSON.stringify(decoded_user));
        state.user = decoded_user 
        state.loggedIn = true;
    },
    loginFailure(state) {
        state.loggedIn = false;
        state.user = null;
    },
    logout(state) {
        state.loggedIn = false;
        state.user = null;
    },
    showLoader(state) {
      console.log('showLoader called')
      state.loading = true
    },
    hideLoader(state) {
      state.loading = false
    },
  },
  modules: {
    // auth
  },
})
