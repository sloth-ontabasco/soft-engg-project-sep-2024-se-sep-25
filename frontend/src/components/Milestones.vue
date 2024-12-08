<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="rounded-xl shadow-lg p-6">
    <h2 class="text-2xl font-bold text-gray-800 border-b pb-4">
      Upcoming Milestones for User: {{ user.id }}
    </h2>

    <!-- Loading state -->
    <div v-if="loading" class="text-gray-500 text-center py-4">
      Loading milestones...
    </div>

    <!-- Error state -->
    <div v-if="error" class="text-red-500 text-center py-4">
      Failed to load milestones. Please try again later.
    </div>

    <!-- Empty milestones -->
    <div v-if="!loading && milestones.length === 0" class="text-gray-500 text-center py-4">
      No milestones available.
    </div>

    <!-- Render milestones -->
    <div
      v-for="milestone in milestones"
      :key="milestone.id"
      class="flex items-center justify-between py-4 border-b last:border-none hover:bg-gray-50 transition duration-200"
    >
      <div>
        <p class="text-lg font-semibold text-gray-800">{{ milestone.title }}</p>
        <p class="text-gray-500 text-sm">{{ milestone.due_date }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getProjectsByUser } from '../api/project';
import { mapState } from 'vuex';

export default {
  data() {
    return {
      loading: false,
      error: false,
      milestones: [],
    };
  },
  computed: {
    ...mapState(['user']),
  },
  async created(){
    await this.fetchMilestones();
  },
  methods: {
    async fetchMilestones() {
      const userId = this.user?.id;
      console.log(userId);
      try{
      const milestones = await getProjectsByUser(userId);
      this.milestones = Array.isArray(milestones) ? milestones : [];
      console.log(milestones);
      } catch (error) {
        console.error("Error fetching Milestones:", error);
      }
    },
  },
};
</script>
