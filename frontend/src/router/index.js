import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import Profile from '@/components/ProfilePage.vue'
import HomeView from '@/views/HomeView.vue'
import LoginPage from '@/views/LoginPage.vue'
import ProjectTable from '@/components/ProjectTable.vue'
import UserTable from '@/components/UserTable.vue'
import TeamTable from '@/components/TeamTable.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children: [
        { path: '', component: Profile },
        {
          path: 'profile',
          component: Profile,
          meta: { home: true },
          name: 'Profile',
        },
        {
          path: 'projects',
          component: ProjectTable,
          meta: { home: true },
          name: 'Projects',
        },
        {
          path: 'users',
          component: UserTable,
          meta: { home: true },
          name: 'Users',
        },
        {
          path: 'teams',
          component: TeamTable,
          meta: { home: true },
          name: 'Teams',
        }
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)
  // const loggedIn = localStorage.getItem('token')
  console.log('window location: ', window.location.search)
  const urlParams = new URLSearchParams(window.location.search)

  if (authRequired) {
    console.log('from path: ', from.path)
    console.log('to path: ', to.path)
    console.log('urlParams: ', urlParams)
    if (to.path === '/' && from.path === '/' && !urlParams.has('jwt'))
      () => {
        console.log(
          'calling next() when from and to are same and no jwt is present',
        )
        next()
      }
    if (to.path === '/' && urlParams.has('jwt')) {
      let jwt = urlParams.get('jwt')
      store
        .dispatch('getAuthToken', jwt)
        .then(() => {
          console.log('calling next() when jwt is present')
          next()
        })
        .catch(() => {
          next('/login')
        })
    }
    next()
  } else {
    next()
  }
})

export default router
