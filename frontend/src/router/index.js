import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import Profile from '@/components/ProfilePage.vue'
import HomeView from '@/views/HomeView.vue'
import AboutView from '../views/AboutView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component:  HomeView,
      children: [
        {path: '', component: Profile},
        {path: 'profile', component: Profile, meta: {home:true}, name: 'Profile'},
        {path: 'projects', component: AboutView, meta: {home:true}, name: 'Projects'}
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue'),
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
  const loggedIn = localStorage.getItem('token')
  const urlParams = new URLSearchParams(window.location.search)

  if (authRequired && !loggedIn) {
    if (to.path === '/' && urlParams.has('jwt')) {
      let jwt = urlParams.get('jwt')
      store.dispatch('getAuthToken', jwt).then(next()).catch(() => {
        next('/login')
      })
    } else next('/login')
  } else {
    next()
  }
})

export default router
