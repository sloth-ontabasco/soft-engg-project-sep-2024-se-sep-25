<script setup>
import NavBar from '@/components/NavBar.vue'
import { mapState } from 'vuex'
</script>

<template>
  <div class="h-screen w-screen">
    <div v-if="loading" class="overlay">
      <div class="loader"></div>
    </div>
    <div class="flex flex-row h-full w-full">
      <NavBar v-if="loggedIn" class="w-1/5 min-w-0" />
      <RouterView class="flex-grow flex-basis-2/3" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  computed: { ...mapState(['loggedIn', 'loading']) },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.has('jwt')) {
      console.log('replacing jwt in mounted hook')
      this.$router.replace(this.$route.path)
    }
  },
}
</script>
<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8); /* Translucent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loader {
  border: 16px solid rgba(243, 243, 243, 0.7); /* Translucent border */
  border-radius: 50%;
  border-top: 16px solid rgba(52, 152, 219, 0.8); /* Translucent border-top */
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
  background: rgba(255, 255, 255, 0.8); /* Translucent background */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>