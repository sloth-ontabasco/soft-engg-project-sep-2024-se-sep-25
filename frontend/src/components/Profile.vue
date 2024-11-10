<!-- eslint-disable vue/multi-word-component-names -->

<template>
  <div class="flex items-center bg-white p-6 rounded-xl shadow">
    <div>
      <h1 class="text-xl text-black font-bold">{{ user.name }} <span @click="editProfile" class="cursor-pointer">✏️</span></h1>
      <p class="text-gray-500">{{ user.email }}</p>
      <div class="flex items-center mt-1">
        <a :href="user.socialLink">
          <div> <p class="text-gray-500">user</p></div>
        </a>
      </div>
    </div>
    <img :src="user.picture" alt="User Avatar" class="w-16 h-16 rounded-full object-cover" />
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Profile',
  computed: {
    ...mapState(['user']),
  },
  methods: {
    editProfile() {
      // Trigger profile edit
      console.log("Edit profile clicked");
    },
  },
};
</script>
