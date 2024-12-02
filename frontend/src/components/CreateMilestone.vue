<template>
    <div class="p-8 bg-gray-100 min-h-screen">
      <h1 class="text-3xl text-black font-bold mb-6">Create a New Milestone</h1>
      <form
        @submit.prevent="submitMilestone"
        class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
      >
        <!-- Milestone Title -->
        <div class="mb-4">
          <label class="block text-gray-700 text-xl font-bold mb-2" for="title">
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
          <label class="block text-gray-700 text-xl font-bold mb-2" for="description">
            Description
          </label>
          <textarea
            v-model="form.description"
            class="shadow appearance-none border rounded w-full py-2 px-3 bg-white text-black leading-tight focus:outline-none focus:shadow-outline"
            id="description"
            rows="4"
            placeholder="Describe the milestone"
          ></textarea>
          <p v-if="errors.description" class="text-red-500 text-xs italic mt-2">
            {{ errors.description }}
          </p>
        </div>
  
        <!-- Deadline -->
        <div class="mb-4">
          <label class="block text-gray-700 text-xl font-bold mb-2" for="deadline">
            Deadline
          </label>
          <input
            v-model="form.deadline"
            class="shadow appearance-none border rounded w-full py-2 px-3 bg-white text-gray-400 leading-tight focus:outline-none focus:shadow-outline"
            id="deadline"
            type="date"
          />
          <p v-if="errors.deadline" class="text-red-500 text-xs italic mt-2">
            {{ errors.deadline }}
          </p>
        </div>
  
        <!-- Assigned Teams -->
        <div class="mb-4">
          <label class="block text-gray-700 text-xl font-bold mb-2" for="project">
            Assigned Teams
          </label>
          <select
            v-model="form.projectId"
            class="shadow appearance-none border rounded w-full py-2 px-3 bg-white text-gray-400 leading-tight focus:outline-none focus:shadow-outline"
            id="project"
          >
            <option disabled value="">Select a Team</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
          <p v-if="errors.projectId" class="text-red-500 text-xs italic mt-2">
            {{ errors.projectId }}
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
            @click="resetForm"
            class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {
          title: "",
          description: "",
          deadline: "",
          projectId: "",
        },
        errors: {
          title: null,
          description: null,
          deadline: null,
          projectId: null,
        },
        projects: [
          { id: 1, name: "Team A" },
          { id: 2, name: "Team B" },
        ],
      };
    },
    methods: {
      submitMilestone() {
        this.clearErrors();
  
        if (!this.validateForm()) {
          return;
        }
  
        console.log("Milestone submitted:", this.form);
        alert("Milestone created successfully!");
        this.resetForm();
      },
      resetForm() {
        this.form = {
          title: "",
          description: "",
          deadline: "",
          projectId: "",
        };
        this.clearErrors();
      },
      validateForm() {
        let isValid = true;
  
        if (!this.form.title) {
          this.errors.title = "Title is required.";
          isValid = false;
        }
  
        if (!this.form.description) {
          this.errors.description = "Description is required.";
          isValid = false;
        }
  
        if (!this.form.deadline) {
          this.errors.deadline = "Deadline is required.";
          isValid = false;
        }
  
        if (!this.form.projectId) {
          this.errors.projectId = "Please select a project.";
          isValid = false;
        }
  
        return isValid;
      },
      clearErrors() {
        this.errors = {
          title: null,
          description: null,
          deadline: null,
          projectId: null,
        };
      },
    },
  };
  </script>
  
  <style scoped>
  /* Custom styles if needed */
  </style>
  