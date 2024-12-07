import { createStore } from 'vuex'
import { login } from '../api/auth'
import { getUsers } from '../api/user'
import * as jose from 'jose'

const user = JSON.parse(localStorage.getItem('user'))
const initialState = user
  ? {
      loggedIn: true,
      user: user,
      users: [],
      msg: '',
      loading: false,
    }
  : {
      loggedIn: false,
      user: null,
      users: [],
      msg: '',
      loading: false,
    }

export default createStore({
  state: initialState,
  actions: {
    async getAuthToken({ dispatch, commit }, jwt) {
      try {
        const res = await login(jwt)
        localStorage.setItem('token', res.token)
        console.log('getAuthToken stored')
        dispatch('getAllUsers').then(() => {
          
        commit('loginSuccess', res.token)
        })
      } catch (e) {
        console.log(e)
        commit('loginFailure')
        throw new Error('Login Failure')
      }
    },
    async getAllUsers({ commit }) {
      console.log('getAllUsers called')
      try {
        if (['admin', 'instructor', 'ta'].includes(user.role)) {
          console.log('role matches')
          commit('showLoader')
          const res = await getUsers()
          commit('storeUsers', res.users)
          commit('hideLoader')
        }
        else {
          console.log('role does not match')
          commit('hideLoader')
        }
      } catch (e) {
        console.log(e)
        commit('hideLoader')
      }
    },
  },
  getters: {
    allStudents: state => {
      return state.users.filter(user => user.role === 'student')
    },
    allInstructors: state => {
      return state.users.filter(user => user.role === 'instructor')
    },
    allTAs: state => {
      return state.users.filter(user => user.role === 'ta')
    },
  },
  mutations: {
    loginSuccess(state, jwt) {
      let decoded_user = jose.decodeJwt(jwt)
      localStorage.setItem('user', JSON.stringify(decoded_user))
      state.user = decoded_user
      state.loggedIn = true
    },
    loginFailure(state) {
      state.loggedIn = false
      state.user = null
    },
    logout(state) {
      state.loggedIn = false
      state.user = null
    },
    showLoader(state) {
      console.log('showLoader called')
      state.loading = true
    },
    hideLoader(state) {
      state.loading = false
    },
    storeUsers(state, users) {
      state.users = users
    },
    updateUser(state, id, details) {
      state.users = state.users.map(user => {
        if (user.id === id) {
          return {
            ...user,
            ...details,
          }
        }
        return user
      })
    },
  },
  modules: {
    // auth
  },
})
