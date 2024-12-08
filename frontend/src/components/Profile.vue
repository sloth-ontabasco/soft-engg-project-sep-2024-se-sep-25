<template>
  <div class="flex items-center bg-white p-6 rounded-xl shadow-lg space-x-4">
    <!-- User Avatar -->
    <img 
      :src="profileImage" 
      alt="User Avatar" 
      class="w-16 h-16 rounded-full object-cover border border-gray-200"
    />


    <!-- User Information -->
    <div class="flex-1">
      <h1 class="text-xl font-bold text-gray-800 flex items-center space-x-2">
        <span>User Name</span>
        <span>{{ user.name }}</span>
        
      </h1>
      <p class="text-gray-500">{{ user.email }}</p>
      
      <!-- Social Link -->
      <div class="mt-2">
        <a 
          :href="user.socialLink" 
          target="_blank" 
          rel="noopener noreferrer" 
          class="text-blue-500 hover:underline flex items-center space-x-1"
        >
          
        </a>
      </div>
    </div>

    <!-- Github Button -->
    <button 
      class="bg-gray-800 text-white py-2 px-4 rounded-lg hover:bg-gray-700 transition duration-200"
    >
      Github
    </button>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import profileImage from '@/assets/profile.png'
export default {
  
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Profile',
  data(){
    return{
      profileImage
    }
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    editProfile() {
      console.log("Edit profile clicked");
    },
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
