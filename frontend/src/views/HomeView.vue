<script setup>
import NavBar from '@/components/NavBar.vue'
import { mapState } from 'vuex'
</script>

<template>
  <div class="h-screen w-screen">
    <div class="flex flex-row h-full w-full">
      <NavBar v-if="loggedIn" class="w-1/5 min-w-0" />
      <RouterView class="flex-grow flex-basis-2/3" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  computed: { ...mapState(['loggedIn']) },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.has('jwt')) {
      console.log('replacing jwt in mounted hook')
      this.$router.replace(this.$route.path);
    }
  },
}
</script>

