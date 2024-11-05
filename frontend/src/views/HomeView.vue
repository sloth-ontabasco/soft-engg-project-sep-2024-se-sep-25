<script setup>
import NavBar from '@/components/NavBar.vue'
import { mapState } from 'vuex'
</script>

<template>
  <div class="h-screen w-screen overflow-hidden">
    <div class="flex flex-row h-full w-full">
      <NavBar v-if="loggedIn" class="h-full w-1/4"/>
      <RouterView class="flex-grow"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  computed: { ...mapState(['loggedIn']) },
}
</script>
