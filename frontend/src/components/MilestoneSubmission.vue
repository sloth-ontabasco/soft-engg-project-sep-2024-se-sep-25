<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Main Content -->
    <main class="flex-1 p-10">
      <!-- Breadcrumb Navigation -->
      <nav class="flex justify-between items-center text-sm text-gray-600 mb-5">
        <div>
          <a href="#" class="hover:underline">All Projects</a> / 
          <a href="#" class="hover:underline">SE Sept 2024</a> / 
          <!-- Milestone Dropdown -->
          <select
            v-model="selectedMilestone"
            @change="handleMilestoneChange"
            class="border rounded px-3 py-1 text-gray-600 bg-gray-100 focus:outline-none focus:ring"
          >
            <option
              v-for="milestone in milestones"
              :key="milestone"
              :value="milestone"
            >
              {{ milestone }}
            </option>
          </select>
        </div>
      </nav>

      <!-- Header -->
      <h1 class="text-black text-3xl font-bold mb-5">
        {{ selectedMilestone }} - User Stories Submission
      </h1>
      <p class="text-gray-700 mb-5">
        Use the options below to manage files and review feedback for {{ selectedMilestone }}.
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
          <div class="flex gap-2 mt-4">
            <label class="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600">
              Upload Files
              <input type="file" class="hidden" @change="handleFileUpload" />
            </label>
            <button class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700" @click="downloadAllFiles">
              Download
            </button>
            <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700" @click="deleteAllSubmissions">
              Delete
            </button>
            <div :class="['px-4 py-2 rounded text-sm font-semibold ml-auto', isDeadlineNear ? 'bg-red-500 text-white animate-pulse' : 'bg-pink-200 text-black']">
    Deadline: {{ deadline }}
</div>
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
        </div>

        <!-- GitHub Tracker Section -->
        <div class="bg-white shadow-md rounded-lg p-5">
          <h2 class="text-black text-lg font-bold mb-3">GitHub Tracker - {{ selectedMilestone }}</h2>
          <ul>
            <li class="mb-3">
              <span class="text-blue-500 cursor-pointer">JIRA-5677 Google OAuth</span>
              <p class="text-gray-600 text-sm">@student.email closed this issue Oct 1, 3:33PM</p>
            </li>
            <li class="mb-3">
              <span class="text-blue-500 cursor-pointer">JIRA-Issue-5902 Google OAuth Login Bug</span>
              <p class="text-gray-600 text-sm">@student.email closed this issue Oct 1, 3:33PM</p>
            </li>
          </ul>
        </div>
      </div>

      <!-- TA Feedback Section -->
      <div class="bg-white shadow-md rounded-lg p-5 mt-8">
        <h2 class="text-black text-lg font-bold mb-3">TA Feedback</h2>
        <p class="text-gray-700">
          Ensure all required files are uploaded before the deadline. Contact your TA for further clarifications.
        </p>
      </div>
    </main>
    
  </div>
</template>

<script>
export default {
  name: "MilestoneSubmission",
  data(){
    return{
      isMilestoneSubmitted: true, // Example state
      showPDF: false, // Controls the visibility of the PDF modal
      pdfURL: null, // URL for the fetched PDF
      milestones: ["Milestone 1", "Milestone 2", "Milestone 3"],
      selectedMilestone: "Milestone 1",
      deadline: "2024-12-05", // Example deadline
      isDeadlineNear: false,
    }
  },
  methods: {
    handleFileUpload(event) {
      const files = Array.from(event.target.files);
      if (files.length) {
        files.forEach(file => {
          console.log(`File selected: ${file.name}`);
        });
      }
    },
    checkDeadline() {
      const today = new Date();
      const deadlineDate = new Date(this.deadline);
      const diffInDays = Math.ceil((deadlineDate - today) / (1000 * 60 * 60 * 24));

      // If the deadline is within 3 days, set `isDeadlineNear` to true
      this.isDeadlineNear = diffInDays <= 3;
    },
    downloadAllFiles() {
      console.log("Downloading all files...");
      alert("All files have been downloaded successfully.");
    },
    deleteAllSubmissions() {
      console.log("Deleting all submissions...");
      const confirmed = confirm("Are you sure you want to delete all submissions?");
      if (confirmed) {
        alert("All submissions have been deleted.");
      }
    },
    handleMilestoneChange() {
      console.log("Selected Milestone:", this.selectedMilestone);
      alert(`Switched to ${this.selectedMilestone}`);
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
  },
  mounted(){
    this.checkDeadline();
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
