<template>
  <div class="flex flex-col mr-5">
    <!-- Add Announcement Button -->
    <div><br>
      <div class="flex justify-between mb-4">
        <h2 class="text-2xl text-white font-bold mb-1">Announcements</h2>
        <button
          v-if="canEdit"
          @click="showModal = true"
          class="bg-transparent text-green-500 py-2 px-4 rounded hover:bg-green-600 hover:text-white border border-green-500 focus:outline-none"
        >
          <i class="fa fa-bullhorn"></i> Announce
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <main>
      <div v-if="loading" class="text-center text-gray-500">Loading announcements...</div>
      <div v-else-if="announcements.length === 0" class="text-center text-gray-500">No announcements were made</div>
      <div v-else>
        <div
          v-for="(announcement, index) in announcements"
          :key="announcement.id"
          @click="toggleExpand(index)"
          class="flex flex-col p-5 bg-gray-100 rounded-lg mb-4 shadow-md cursor-pointer bg-opacity-90"
        >
          <div class="flex items-center justify-between">
            <h2 class="text-xl text-black font-bold mb-2">
              {{ announcement.title }}
            </h2>
            <div class="flex items-center">
              <button class="text-gray-500 hover:text-black focus:outline-none">
                <i :class="expandedIndex === index ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"></i>
              </button>
              <button
                v-if="canEdit"
                @click.stop="editAnnouncement(index)"
                class="text-blue-500 hover:text-blue-700 focus:outline-none ml-2"
              >
                <i class="fa fa-edit"></i>
              </button>
              <button
                v-if="canEdit"
                @click.stop="confirmDeleteAnnouncement(index)"
                class="text-red-500 hover:text-red-700 focus:outline-none ml-2"
              >
                <i class="fa fa-trash"></i>
              </button>
            </div>
          </div>
          <div class="text-sm text-gray-600 mb-2">
            Posted by {{ announcement.posted_by }} on {{ formatDate(announcement.created_at) }}
            <span v-if="announcement.updated_at && announcement.updated_at !== announcement.created_at">(Updated on {{ formatDate(announcement.updated_at) }})</span>
          </div>
          <p v-if="expandedIndex === index" class="text-gray-700">
            {{ announcement.content }}
          </p>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-black bg-opacity-90 p-6 rounded-lg w-1/3 shadow-lg">
        <h3 class="text-lg font-bold mb-4 text-white">{{ isEditing ? 'Edit Announcement' : 'Add New Announcement' }}</h3>
        <form @submit.prevent="isEditing ? updateAnnouncement() : submitAnnouncement()">
          <div class="mb-4">
            <label for="title" class="block font-medium text-white">Title</label>
            <input
              v-model="newAnnouncement.title"
              id="title"
              type="text"
              required
              class="w-full border border-gray-300 rounded p-2 bg-gray-800 text-white"
            />
          </div>
          <div class="mb-4">
            <label for="message" class="block font-medium text-white">Message</label>
            <textarea
              v-model="newAnnouncement.message"
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
    
  </div>
</template>

<script>
import { getAnnouncements, deleteAnnouncement, createAnnouncement, updateAnnouncement } from '../api/announcements'
import { mapState } from 'vuex'
import {error, info, success} from '../utils/toast';

export default {
  data() {
    return {
      showModal: false,
      expandedIndex: null,
      loading: true,
      announcements: [],
      newAnnouncement: {
        title: "",
        message: "",
        postedBy: "",
      },
      notification: {
        message: "",
        type: "success"
      },
      isEditing: false,
      editingIndex: null
    };
  },
  computed: {
    ...mapState(['user']),
    canEdit() {
      return this.user && ['instructor', 'ta', 'admin'].includes(this.user.role);
    }
  },
  async created() {
    try {
      const projectId = this.$route.params.projectId;
      const announcements = await getAnnouncements(projectId)
      this.announcements = announcements || [];
      this.announcements.forEach(announcement => {
        console.log(announcement.title);
      });
    } catch (error) {
      console.error('Error fetching projects:', error)
    } finally {
      this.loading = false;
    }
  },
  methods: {
    toggleExpand(index) {
      this.expandedIndex = this.expandedIndex === index ? null : index;
    },
    async submitAnnouncement() {
      const projectId = this.$route.params.projectId;
      const newAnnouncement = {
        title: this.newAnnouncement.title,
        content: this.newAnnouncement.message, // Ensure 'content' is used instead of 'message'
        posted_by: this.user.name // Ensure 'posted_by' is included
      };

      try {
        await createAnnouncement(projectId, newAnnouncement);
        await this.refreshAnnouncements(); // Refresh announcements after creating a new one
        this.resetForm();
        this.showModal = false;
        success("Success","Announcement posted");
      } catch (error) {
        console.error('Failed to create announcement:', error);
        error("Error","Failed to post announcement");
      }
    },
    async updateAnnouncement() {
      const projectId = this.$route.params.projectId;
      const announcementId = this.announcements[this.editingIndex].id;
      const updatedAnnouncement = {
        title: this.newAnnouncement.title,
        content: this.newAnnouncement.message,
      };

      try {
        await updateAnnouncement(projectId, announcementId, updatedAnnouncement);
        await this.refreshAnnouncements(); // Refresh announcements after updating
        this.resetForm();
        this.showModal = false;
        info("Info","Announcement updated");
      } catch (error) {
        console.error('Failed to update announcement:', error);
        error("Error","Failed to update announcement");
      }
    },
    async refreshAnnouncements() {
      const projectId = this.$route.params.projectId;
      this.loading = true;
      try {
        const announcements = await getAnnouncements(projectId);
        this.announcements = announcements || [];
      } catch (error) {
        console.error('Error fetching announcements:', error);
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.newAnnouncement = {
        title: "",
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
    formatDate(dateString) {
      const date = new Date(dateString);
      const options = { day: 'numeric', month: 'long', year: 'numeric' };
      return date.toLocaleDateString('en-IN', options).replace(/(\d+)(th|st|nd|rd)/, '$1$2');
    },
    async confirmDeleteAnnouncement(index) {
      const projectId = this.$route.params.projectId;
      if (confirm(`Are you sure you wish to delete "${this.announcements[index].title}"?`)) {
        this.deleteAnnouncement(index);
      }
    },
    async deleteAnnouncement(index) {
      const projectId = this.$route.params.projectId;
      const announcementId = this.announcements[index].id;
      try {
        await deleteAnnouncement(projectId, announcementId);
        this.announcements.splice(index, 1);
        error("Error","Announcement deleted");
      } catch (error) {
        console.error('Failed to delete announcement:', error);
        error("Error","Failed to delete announcement");
      }
    },
    editAnnouncement(index) {
      this.isEditing = true;
      this.editingIndex = index;
      const announcement = this.announcements[index];
      this.newAnnouncement = {
        title: announcement.title,
        message: announcement.content,
        postedBy: announcement.posted_by,
      };
      this.showModal = true;
    }
    
  },
};
</script>

<style>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}
.modal-enter,
.modal-leave-to {
  opacity: 0;
}
</style>
