<script setup>
import NavBar from '@/components/NavBar.vue'
import { mapState } from 'vuex'
</script>

<template>
  <div class="h-screen w-screen">
    <div class="flex flex-row h-full w-full">
      <NavBar v-if="loggedIn" class="w-1/5 min-w-0"/>
      <RouterView class="flex-grow flex-basis-2/3"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  computed: { ...mapState(['loggedIn']) },
}
</script>

