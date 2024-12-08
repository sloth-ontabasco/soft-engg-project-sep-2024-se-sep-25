<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="rounded-xl shadow-lg p-6">
    <h2 class="text-2xl font-bold text-gray-800 border-b pb-4">Upcoming Milestones</h2>

    <!-- Show loading message -->
    <div v-if="loading" class="text-gray-500 text-center py-4">
      Loading milestones...
    </div>

    <!-- Show an error message if fetching fails -->
    <div v-if="error" class="text-red-500 text-center py-4">
      Failed to load milestones. Please try again later.
    </div>

    <!-- Show a message if there are no milestones -->
    

    <!-- Render a list of milestones -->
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
import { getMilestonesByUser } from '../api/milestone';

export default {
  data() {
    return {
      milestones: [], // Store fetched milestones
      loading: true, // Track loading state
      error: false,  // Track error state
    };
  },
  created() {
    this.fetchMilestones();
  },
  methods: {
    /**
     * Fetch upcoming milestones for the logged-in user.
     */
    async fetchMilestones() {
      this.loading = true;
      this.error = false;
      try {
        const userId = this.$store.state.user.id; // Assuming user ID is stored in Vuex store
        this.milestones = await getMilestonesByUser(userId);
      } catch (error) {
        console.error("Failed to fetch upcoming milestones:", error);
        this.error = true;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
