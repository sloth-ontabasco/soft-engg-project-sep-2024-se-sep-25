<script setup>
import NavBar from '@/components/NavBar.vue';
import { mapState } from 'vuex'
</script>

<template>
<div class="flex flex-row flex-nowrap h-svh max-h-svh w-full ">
  <v-if loggedIn>
    <NavBar/>
  </v-if>
  <RouterView/> 
</div>
</template>

<script>
export default {
  name: 'HomeView',
  computed: { ...mapState(['loggedIn']) },
}
</script>
