<template>

    <div class="bg-gray-100 min-h-screen w-full shadow">
      <Profile />
      <UpcomingMilestones />
    </div>
</template>
  
  <script>
  import Profile from "./Profile.vue";
  import UpcomingMilestones from "./Milestones.vue";
  
  export default {
    components: {
      Profile,
      UpcomingMilestones,
    },
  };
  </script>
  
  <style scoped>
  /* Additional styles if needed */
  </style>
  