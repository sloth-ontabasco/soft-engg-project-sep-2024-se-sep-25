<template>
  <div class="bg-white shadow-md rounded-lg p-5 mt-8">
    <div class="flex justify-between mb-3">
      <h2 class="text-black text-lg font-bold">Feedbacks</h2>
      <button
        v-if="canEdit"
        @click="showModal = true"
        class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none flex items-center"
      >
        <i class="fa fa-comment-dots mr-2"></i> Post
      </button>
    </div>
    <div v-if="loadingFeedback" class="text-center text-gray-500">Loading feedback...</div>
    <div v-else-if="feedbacks.length === 0" class="text-center text-gray-500">No feedback available</div>
    <div v-else>
      <div
        v-for="(feedback, index) in feedbacks"
        :key="feedback.id"
        class="flex flex-col p-5 bg-gray-100 rounded-lg mb-4 shadow-md"
      >
        <div class="flex items-center justify-between">
          <h2 class="text-xl text-black font-bold mb-2">
            Feedback from {{ feedback.posted_by }}
          </h2>
          <div class="flex items-center">
            <button
              v-if="canEdit"
              @click.stop="editFeedback(index)"
              class="text-blue-500 hover:text-blue-700 focus:outline-none ml-2"
            >
              <i class="fa fa-edit"></i>
            </button>
            <button
              v-if="canEdit"
              @click.stop="confirmDeleteFeedback(index)"
              class="text-red-500 hover:text-red-700 focus:outline-none ml-2"
            >
              <i class="fa fa-trash"></i>
            </button>
          </div>
        </div>
        <div class="text-sm text-gray-600 mb-2">
          Posted on {{ formatDate(feedback.created_at) }}
          <span v-if="feedback.updated_at && feedback.updated_at !== feedback.created_at">(Updated on {{ formatDate(feedback.updated_at) }})</span>
        </div>
        <p class="text-gray-700">
          {{ feedback.content }}
        </p>
      </div>
    </div>
    <!-- Modal for Feedback -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-black bg-opacity-90 p-6 rounded-lg w-1/3 shadow-lg">
        <h3 class="text-lg font-bold mb-4 text-white">{{ isEditing ? 'Edit Feedback' : 'Add New Feedback' }}</h3>
        <form @submit.prevent="isEditing ? updateFeedback() : submitFeedback()">
          <div class="mb-4">
            <label for="message" class="block font-medium text-white">Message</label>
            <textarea
              v-model="newFeedback.message"
              id="message"
              required
              class="w-full border border-gray-300 rounded p-2 bg-gray-800 text-white"
            ></textarea>
          </div>
          <div class="flex justify-end">
            <button
              type="button"
              @click="closeModal"
              class="bg-gray-300 text-gray-700 py-2 px-4 rounded mr-2 hover:bg-gray-400 focus:outline-none"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none"
            >
              {{ isEditing ? 'Update' : 'Add' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    <div v-if="notification.message" :class="`fixed bottom-4 right-4 p-4 rounded shadow-lg ${notification.type === 'success' ? 'bg-green-500' : notification.type === 'error' ? 'bg-red-500' : 'bg-blue-500'} text-white flex items-center`">
      <i class="fa fa-info-circle mr-2"></i>
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
import { getFeedbacks, createFeedback, updateFeedback, deleteFeedback } from '../api/feedbacks.js';

export default {
  name: "Feedbacks",
  props: {
    projectId: {
      type: String,
      required: true
    },
    user: {
      type: Object,
      required: true
    },
    selectedMilestone: {
      type: Object,
      required: true
    },
    selectedTeam: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      feedbacks: [],
      loadingFeedback: true,
      showModal: false,
      newFeedback: {
        message: "",
        postedBy: "",
      },
      isEditing: false,
      editingIndex: null,
      notification: {
        message: "",
        type: "success"
      }
    };
  },
  computed: {
    canEdit() {
      return this.user && ['instructor', 'ta', 'admin'].includes(this.user.role);
    }
  },
  async created() {
    await this.fetchFeedbacks();
  },
  methods: {
    async fetchFeedbacks() {
      try {
        console.log("Fetching feedbacks for", this.selectedMilestone.title, this.selectedTeam.team_name);
        const feedbacks = await getFeedbacks(this.projectId, this.selectedMilestone.id, this.selectedTeam.id);
        this.feedbacks = feedbacks || [];
      } catch (error) {
        console.error('Error fetching feedbacks:', error);
      } finally {
        this.loadingFeedback = false;
      }
    },
    async submitFeedback() {
      const newFeedback = {
        content: this.newFeedback.message,
        posted_by: this.user.name
      };

      try {
        await createFeedback(this.projectId, this.selectedMilestone.id, this.selectedTeam.id, newFeedback);
        await this.fetchFeedbacks();
        this.resetForm();
        this.showModal = false;
        this.showNotification("Feedback posted", "success");
      } catch (error) {
        console.error('Failed to create feedback:', error);
        this.showNotification("Failed to post feedback", "error");
      }
    },
    async updateFeedback() {
      const feedbackId = this.feedbacks[this.editingIndex].id;
      const updatedFeedback = {
        content: this.newFeedback.message,
      };

      try {
        await updateFeedback(this.projectId, this.selectedMilestone.id, this.selectedTeam.id, feedbackId, updatedFeedback);
        await this.fetchFeedbacks();
        this.resetForm();
        this.showModal = false;
        this.showNotification("Feedback updated", "info");
      } catch (error) {
        console.error('Failed to update feedback:', error);
        this.showNotification("Failed to update feedback", "error");
      }
    },
    async confirmDeleteFeedback(index) {
      if (confirm('Are you sure you wish to delete this feedback?')) {
        this.deleteFeedback(index);
      }
    },
    async deleteFeedback(index) {
      const feedbackId = this.feedbacks[index].id;
      try {
        await deleteFeedback(this.projectId, this.selectedMilestone.id, this.selectedTeam.id, feedbackId);
        this.feedbacks.splice(index, 1);
        this.showNotification("Feedback deleted", "error");
      } catch (error) {
        console.error('Failed to delete feedback:', error);
        this.showNotification("Failed to delete feedback", "error");
      }
    },
    editFeedback(index) {
      this.isEditing = true;
      this.editingIndex = index;
      const feedback = this.feedbacks[index];
      this.newFeedback = {
        message: feedback.content,
        postedBy: feedback.posted_by,
      };
      this.showModal = true;
    },
    resetForm() {
      this.newFeedback = {
        message: "",
        postedBy: "",
      };
      this.isEditing = false;
      this.editingIndex = null;
    },
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
    showNotification(message, type) {
      this.notification.message = message;
      this.notification.type = type;
      setTimeout(() => {
        this.notification.message = "";
      }, 3000);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const options = { day: 'numeric', month: 'long', year: 'numeric' };
      return date.toLocaleDateString('en-IN', options).replace(/(\d+)(th|st|nd|rd)/, '$1$2');
    },
  }
};
</script>
