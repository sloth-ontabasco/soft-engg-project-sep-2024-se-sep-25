<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div>
      <h2 class="text-2xl text-black font-bold p-4">Upcoming Milestones</h2>
      <div v-for="milestone in milestones" :key="milestone.id" class="flex p-4 items-center mt-1 border-b pb-3">
        <div>
          <p class="text-black text-lg font-bold">{{ milestone.title }}</p>
          <p class="text-gray-500">{{ milestone.subtitle }}</p>
        </div>
        <div >
          <p class="text-gray-400 text-left">{{ milestone.date }}</p>
        </div>
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