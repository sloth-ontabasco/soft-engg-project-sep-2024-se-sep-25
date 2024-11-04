<!-- eslint-disable vue/multi-word-component-names -->

<template>
  <div class="flex items-center bg-white p-6 rounded-xl shadow">
    <div>
      <h1 class="text-xl text-black font-bold">{{ user.name }} <span @click="editProfile" class="cursor-pointer">✏️</span></h1>
      <p class="text-gray-500">{{ user.email }}</p>
      <div class="flex items-center mt-1">
        <a :href="user.socialLink">
          <div class="text-xl">@{{ user.username }}</div>
        </a>
      </div>
    </div>
    <img :src="user.avatar" alt="User Avatar" class="w-16 h-16 rounded-full object-cover" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: "Priyangshu Bala",
        email: "21f3001205@ds.study.iitm.ac.in",
        username: "PriyangshuBala2412",
        socialLink: "https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",
        avatar: "https://lh3.googleusercontent.com/ogw/AF2bZygJS_cDMy1hgnNw3OheIdcs_48aejAaxJREmTJLhdqrLcs=s32-c-mo",
      },
    };
  },
  methods: {
    editProfile() {
      // Trigger profile edit
      console.log("Edit profile clicked");
    },
  },
};
</script>
