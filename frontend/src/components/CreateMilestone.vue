<template>
    <div class="p-8 bg-gray-100 min-h-screen">
      <h1 class="text-2xl text-gray-700 font-bold mb-6">Create a New Milestone</h1>
      <form
        @submit.prevent="submitMilestone"
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
      >
        <!-- Milestone Title -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="title">
            Milestone Title
          </label>
          <input
            v-model="form.title"
            class="shadow appearance-none border rounded w-full py-2 px-3 bg-white text-black leading-tight focus:outline-none focus:shadow-outline"
            id="title"
            type="text"
            placeholder="Enter milestone title"
          />
          <p v-if="errors.title" class="text-red-500 text-xs italic mt-2">
            {{ errors.title }}
          </p>
        </div>

        <!-- Description -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="description">
            Description
          </label>
          <textarea
            v-model="form.description"
            class="shadow appearance-none border rounded w-full py-2 px-3 bg-white text-black leading-tight focus:outline-none focus:shadow-outline"
            id="description"
            rows="4"
            placeholder="Describe the milestone"
            style="width: 100%;"
          ></textarea>
          <p v-if="errors.description" class="text-red-500 text-xs italic mt-2">
            {{ errors.description }}
          </p>
        </div>

        <!-- Deadline -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="deadline">
            Deadline
          </label>
          <input
            v-model="form.deadline"
            class="shadow appearance-none border rounded w-full py-2 px-3 bg-white text-black leading-tight focus:outline-none focus:shadow-outline"
            id="deadline"
            type="date"
            style="color: black;"
          />
          <p v-if="errors.deadline" class="text-red-500 text-xs italic mt-2">
            {{ errors.deadline }}
          </p>
        </div>

        <!-- Buttons -->
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Create Milestone
          </button>
          <button
            type="button"
            @click="cancelCreation"
            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </template>

  <script>
  import { createMilestone } from '../api/milestone'

  export default {
    data() {
      return {
        form: {
          title: "",
          description: "",
          deadline: "",
        },
        errors: {
          title: null,
          description: null,
          deadline: null,
        },
      };
    },
    methods: {
      async submitMilestone() {
        this.clearErrors();
  
        if (!this.validateForm()) {
          return;
        }
  
        try {
          const projectId = this.$route.params.projectId;
          const formattedDeadline = new Date(this.form.deadline).toISOString().split('T')[0] + 'T00:00:00';
          const response = await createMilestone(projectId, {
            title: this.form.title,
            description: this.form.description,
            due_date: formattedDeadline,
          });
          alert("Milestone created successfully!");
          this.$store.commit('setSelectedMilestoneId', response.data.id);
          this.$router.push({ name: 'Milestones', params: { projectId } });
        } catch (error) {
          console.error("Error creating milestone:", error);
          alert("Failed to create milestone.");
        }
      },
      cancelCreation() {
        const projectId = this.$route.params.projectId;
        this.$router.push({ name: 'Milestones', params: { projectId } });
      },
      validateForm() {
        let isValid = true;
  
        if (!this.form.title) {
          this.errors.title = "Title is required.";
          isValid = false;
        }
  
        if (!this.form.deadline) {
          this.errors.deadline = "Deadline is required.";
          isValid = false;
        }
  
        return isValid;
      },
      clearErrors() {
        this.errors = {
          title: null,
          description: null,
          deadline: null,
        };
      },
    },
  };
  </script>
