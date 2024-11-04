<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="mt-8">
      <h2 class="text-lg text-black font-bold">Upcoming Milestones</h2>
      <div v-for="milestone in milestones" :key="milestone.id" class="flex justify-between items-center mt-4 border-b pb-2">
        <div>
          <p >{{ milestone.title }}</p>
          <p class="text-gray-500">{{ milestone.subtitle }}</p>
        </div>
        <p class="text-gray-400">{{ milestone.date }}</p>
      </div>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        milestones: [
          { id: 1, title: "Milestone 2 - SE Sept 2024", subtitle: "Wireframe Submission", date: "14th Oct - Midnight" },
          { id: 2, title: "Level 1 Viva - SPG Sept 2024", subtitle: "Viva", date: "12th Oct - 06:00PM" },
        ],
      };
    },
  };
</script>
  
  
  