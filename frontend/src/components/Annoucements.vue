<template>
  <div class="basis-3/4">
    <h2>Annoucements</h2>
    <div class="flex flex-col ...">
      <div v-for="(annoucement, index) in this.data" :key="index">
        <h3>Annoucment {{ index }}</h3>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'
export default {
  components: {
    NavBar,
  },
  data() {
    return {
      data: ['test'],
    }
  },
  methods: {
    async Annoucements() {
      await this.$axios
        .post('/api/annoucement-router')
        .then(response => {
          this.data = response.data
        })
        .catch(error => console.error(error))
    },
  },
  mounted() {
    this.Annoucements()
  },
}
</script>

<!-- <style>
.container {
    display: flex;
  }
  
  .left {
    flex: 1; 
    padding: 20px;
    background-color: #f0f0f0;
  }
  
  .right {
    flex: 2; 
    padding: 20px;
    background-color: #d0d0d0;
  }
</style> -->
