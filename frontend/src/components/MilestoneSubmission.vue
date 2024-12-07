<template>
  <div class="flex min-h-screen bg-gray-100">
    
    <!-- Main Content -->
    <main class="flex-1 p-10">
      <!-- Breadcrumb Navigation -->
      <nav class="text-sm text-gray-600 mb-5">
        <router-link :to="'/projects'" class="hover:underline">All Projects</router-link> / 
        <a href="#" class="hover:underline">SE Sept 2024</a> / 
        <span>Milestone 1</span>
      </nav>

      <!-- Header -->
      <h1 class="text-black text-3xl font-bold mb-5">User Stories Submission</h1>
      <p class="text-gray-700 mb-5">
        Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature...
      </p>

      <!-- Tags -->
      <div class="flex gap-2 mb-5">
        <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">Files Required</span>
        <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">User Stories</span>
        <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">Architecture</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Files Submitted Section -->
        <div class="bg-white shadow-md rounded-lg p-5">
          <h2 class="text-black text-lg font-bold mb-3">Files Submitted</h2>
          <ul>
            <li class="flex justify-between mb-2">
              <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">User Stories</span>
              <span class="text-green-600">Submitted</span>
            </li>
            <li class="flex justify-between mb-2">
              <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">User Stories - Team</span>
              <span class="text-green-600">Submitted</span>
            </li>
            <li class="flex justify-between mb-2">
              <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">User Requirements</span>
              <span class="text-red-600">Not Submitted</span>
            </li>
          </ul>

          <!-- Buttons: Upload, Download, Delete -->
          <div class="flex justify-between mt-4">
            <!-- Left-aligned buttons -->
            <div class="flex gap-2">
              <label class="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600">
                Upload Files
                <input type="file" class="hidden" @change="handleFileUpload" />
              </label>
              <button class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600" @click="downloadAllFiles">
                Download
              </button>
              <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600" @click="deleteAllSubmissions">
                Delete
              </button>
            </div>
            
            <!-- Right-aligned button -->
            <div>
              <button 
                class="bg-gray-400 text-white px-4 py-2 rounded"
                :class="{ 'bg-yellow-500 hover:bg-yellow-600': isMilestoneSubmitted }"
              
                @click="fetchReport"
              >
                GenAI Report
              </button>
            </div>
          </div>
            <!-- PDF Viewer Modal -->
          <div 
            v-if="showPDF" 
            class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-75 flex justify-center items-center z-50"
          >
            <div class="bg-white p-4 rounded shadow-lg w-4/5 h-4/5 relative">
              <button 
                class="absolute top-2 right-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                @click="closePDF"
              >
                Close
              </button>
              <iframe 
                :src="pdfURL" 
                class="w-full h-full border-none"
              ></iframe>
            </div>
          </div>
        </div>

        <!-- GitHub Tracker Section -->
        <div class="bg-white shadow-md rounded-lg p-5">
          <h2 class="text-black text-lg font-bold mb-3">GitHub Tracker - Milestone 1</h2>
          <ul>
            <li class="mb-3">
              <span class="text-blue-500">JIRA-5677 Google OAuth</span>
              <p class="text-gray-600 text-sm">@student.email closed this issue Oct 1, 3:33PM</p>
            </li>
            <li class="mb-3">
              <span class="text-blue-500">JIRA-Issue-5902 Google OAuth Login Bug</span>
              <p class="text-gray-600 text-sm">@student.email closed this issue Oct 1, 3:33PM</p>
            </li>
          </ul>
        </div>
      </div>

      <!-- TA Feedback Section -->
      <Feedbacks :projectId="$route.params.projectId" :user="user" />
    </main>
  </div>
</template>

<script>
import Feedbacks from './Feedbacks.vue';
import { mapState } from 'vuex';

export default {
  name: "MilestoneSubmission",
  components: {
    Feedbacks
  },
  data(){
    return{
      isMilestoneSubmitted: true, // Example state
      showPDF: false, // Controls the visibility of the PDF modal
      pdfURL: null, // URL for the fetched PDF
    }
  },
  computed: {
    ...mapState(['user']),
    canEdit() {
      return this.user && ['instructor', 'ta', 'admin'].includes(this.user.role);
    }
  },
  async created() {
    // write the logic here to fetch the milestone details from project ID
    // get project ID like so $route.params.id
    await this.fetchFeedbacks();
  },
  methods: {
    handleFileUpload(event) {
      const files = event.target.files;
      if (files.length) {
        console.log('Files selected:', files);
        // Handle file upload logic here
      }
    },
    downloadAllFiles() {
      console.log("Downloading all files...");
      // Implement download all files logic here
    },
    deleteAllSubmissions() {
      console.log("Deleting all submissions...");
      // Implement delete all submissions logic here
   },
    fetchReport() {
          this.$store.commit('showLoader') 
      this.$axios
        .get('/api/submission/674611a5dc0301f4122804ea', { responseType: 'blob' })
        .then(response => {
          // Create a blob URL for the fetched PDF
          this.pdfURL = URL.createObjectURL(new Blob([response.data], { type: 'text/html' }));
          this.showPDF = true; // Show the PDF viewer
          this.$store.commit('hideLoader') // Hide loader
        })
        .catch(error => {
          console.error('Error fetching GenAI report:', error);
          this.$store.commit('hideLoader') // Hide loader
        });
    },
    closePDF() {
      this.showPDF = false; // Hide the PDF viewer
      this.pdfURL = null; // Clean up the URL
    },
   
    }
  };

</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8); /* Translucent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loader {
  border: 16px solid rgba(243, 243, 243, 0.7); /* Translucent border */
  border-radius: 50%;
  border-top: 16px solid rgba(52, 152, 219, 0.8); /* Translucent border-top */
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
  background: rgba(255, 255, 255, 0.8); /* Translucent background */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
