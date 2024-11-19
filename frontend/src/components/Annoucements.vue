<template>
  <div class="flex flex-col">
    <!-- Add Announcement Button -->
    <div><br>
      <div class="flex justify-between mb-4">
        <h2 class="text-2xl text-black font-bold mb-1">Announcements</h2>
        <button
          @click="showModal = true"
          class="bg-transparent text-blue-500 py-2 px-4 rounded hover:bg-blue-600 hover:text-white border border-blue-500 focus:outline-none"
        >
          Add Announcement
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <main>
      <div
        v-for="(announcement, index) in announcements"
        :key="announcement.id"
        @click="toggleExpand(index)"
        class="flex flex-col p-5 bg-gray-100 rounded-lg mb-4 shadow-md cursor-pointer"
      >
        <div class="flex items-center justify-between">
          <h2 class="text-xl text-black font-bold mb-2">
            {{ announcement.title }}
          </h2>
          <button class="text-gray-500 hover:text-black focus:outline-none">
            <span v-if="expandedIndex === index">-</span>
            <span v-else>+</span>
          </button>
        </div>
        <div class="text-sm text-gray-600 mb-2">
          Posted by {{ announcement.postedBy }} on {{ announcement.timestamp }}
        </div>
        <p v-if="expandedIndex === index" class="text-gray-700">
          {{ announcement.message }}
        </p>
      </div>
    </main>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg w-1/3 shadow-lg">
        <h3 class="text-lg font-bold mb-4">Add New Announcement</h3>
        <form @submit.prevent="submitAnnouncement">
          <div class="mb-4">
            <label for="title" class="block font-medium text-gray-700">Title</label>
            <input
              v-model="newAnnouncement.title"
              id="title"
              type="text"
              required
              class="w-full border border-gray-300 rounded p-2"
            />
          </div>
          <div class="mb-4">
            <label for="message" class="block font-medium text-gray-700">Message</label>
            <textarea
              v-model="newAnnouncement.message"
              id="message"
              required
              class="w-full border border-gray-300 rounded p-2"
            ></textarea>
          </div>

         
          <div class="flex justify-end">
            <button
              type="button"
              @click="showModal = false"
              class="bg-gray-300 text-gray-700 py-2 px-4 rounded mr-2 hover:bg-gray-400 focus:outline-none"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none"
            >
              Add
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showModal: false, // Controls modal visibility
      expandedIndex: null, // Tracks which announcement is expanded
      announcements: [
        {
          id: 1,
          title: "Scheduled Maintenance",
          message:
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
          postedBy: "Admin",
          timestamp: "2024-11-19 10:00 AM",
        },
        {
          id: 2,
          title: "New Features Released",
          message:
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
          postedBy: "Nidhish",
          timestamp: "2024-11-18 3:45 PM",
        },
        {
          id: 3,
          title: "Holiday Announcement",
          message:
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
          postedBy: "Arun",
          timestamp: "2024-11-17 8:20 AM",
        },
        {
          id: 4,
          title: "Policy Update",
          message:
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
          postedBy: "TA",
          timestamp: "2024-11-16 5:30 PM",
        },
      ],
      newAnnouncement: {
        title: "",
        message: "",
        
      },
    };
  },
  methods: {
    toggleExpand(index) {
      this.expandedIndex = this.expandedIndex === index ? null : index;
    },
    submitAnnouncement() {
      const timestamp = new Date().toLocaleString("en-IN", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Asia/Kolkata",
      });
      const newId = this.announcements.length + 1;

      const announcement = {
        id: newId,
        title: this.newAnnouncement.title,
        message: this.newAnnouncement.message,
        postedBy: this.newAnnouncement.postedBy,
        timestamp,
      };

      this.announcements.unshift(announcement); // Add new announcement to the top
      this.resetForm();
      this.showModal = false; // Close the modal
    },
    resetForm() {
      this.newAnnouncement = {
        title: "",
        message: "",
        postedBy: "",
      };
    },
  },
};
</script>

<style>
/* Optional: Modal Animation */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}
.modal-enter,
.modal-leave-to {
  opacity: 0;
}
</style>
