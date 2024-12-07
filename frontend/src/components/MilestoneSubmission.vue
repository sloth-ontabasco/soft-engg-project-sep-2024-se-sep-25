<template>
  <div class="flex min-h-screen bg-gray-100">
    
    <!-- Main Content -->
    <main class="flex-1 p-10">
      <!-- Breadcrumb Navigation -->
      <nav class="text-sm text-gray-600 mb-5">
        <router-link :to="'/projects'" class="hover:underline">All Projects</router-link> / 
        <a href="#" class="hover:underline">SE Sept 2024</a> / 
          
          <Select v-model="selectedMilestone" :options="milestones" optionLabel="title" optionValue="id" :defaultValue="selectedMilestone.id" @update:modelValue="handleMilestoneChange" class="w-full md:w-56 custom-select" /> 
          <template v-if="canEdit">
            / <Select v-model="selectedTeam" :options="teams" optionLabel="team_name" optionValue="id" :defaultValue="selectedTeam.id" @update:modelValue="handleTeamChange" class="w-full md:w-56 custom-select" />
          </template>
      </nav>

      <!-- Header -->
      <div class="group flex items-center justify-between">
        <div>
          <h1 v-if="!editingHeading" class="text-black text-3xl font-bold mb-5">
            {{ selectedMilestone.title }} - User Stories Submission
          </h1>
          <input v-else type="text" v-model="editedHeading" class="border p-2 rounded text-3xl font-bold mb-5" @keyup.enter="saveHeading" />
        </div>
        <button class="hidden group-hover:inline-block text-white px-4 py-2 rounded" @click="toggleHeadingEdit">✏️</button>
      </div>

      <div class="group flex items-center justify-between">
        <div>
          <p v-if="!editingDescription" class="text-gray-700 mb-5">
            Use the options below to manage files and review feedback for {{ selectedMilestone.title }} for {{ selectedTeam.team_name }}.
          </p>
          <textarea v-else v-model="editedDescription" class="w-full p-2 border rounded focus:outline-none focus:ring mb-5" @keyup.enter="saveDescription"></textarea>
        </div>
        <button class="hidden group-hover:inline-block text-white px-4 py-2 rounded" @click="toggleDescriptionEdit">✏️</button>
      </div>

      <div :class="['inline-block px-6 py-3 rounded-lg text-sm font-semibold', isDeadlineNear ? 'bg-red-500 text-white animate-pulse' : 'bg-white text-black']" style="margin-left: 0;">Deadline: {{ deadline }}</div>
      <br>
      <br>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Files Submitted Section -->
        <div class="bg-white shadow-md rounded-lg p-5">
          <h2 class="text-black text-lg font-bold mb-3">Files Submitted</h2>
          <ul>
            <li class="flex justify-between mb-2">
              <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">Submission Status</span>
              <span class="text-green-600">Submitted</span>
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

       <!-- Feedback Section -->
       <div class="bg-white shadow-md rounded-lg p-5 mt-8">
        <h2 class="text-black text-lg font-bold mb-3">Feedback</h2>
        <ul>
          <li v-for="(feedback, index) in feedbackList" :key="index" class="mb-4 bg-gray-100 p-3 rounded shadow-sm">
            <div v-if="!feedback.editing">
              <p class="text-gray-700"><strong>{{ feedback.username }}:</strong> {{ feedback.text }}</p>
              <button class="text-blue-500 text-sm mt-2 underline" @click="editFeedback(index)">✏️ Edit</button>
            </div>
            <div v-else>
              <textarea v-model="feedback.editedText" class="w-full p-2 border rounded focus:outline-none focus:ring"></textarea>
              <button class="bg-green-500 text-white px-3 py-1 rounded mt-2" @click="saveFeedback(index)">Save</button>
              <button class="bg-red-500 text-white px-3 py-1 rounded mt-2" @click="cancelFeedbackEdit(index)">Cancel</button>
            </div>
          </li>
        </ul>
        <div class="mt-4">
          <textarea v-model="newFeedback" class="w-full p-2 border rounded focus:outline-none focus:ring bg-white text-black" placeholder="Add new feedback..."></textarea>
          <button class="bg-blue-500 text-white px-4 py-2 rounded mt-2 hover:bg-blue-700" @click="addFeedback">Add Feedback</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { getProjectMilestones } from '../api/milestone';
import { getProjectTeams } from '../api/team';
import Select from 'primevue/select';
import { mapState } from 'vuex';

export default {
  
  name: "MilestoneSubmission",
  data(){
    return{
      editingHeading: false,
      editingDescription: false,
      editedHeading: "",
      editedDescription: "",
      feedbackList: [
        { text: "Ensure all required files are uploaded before the deadline.", username: "TA John", editing: false, editedText: "" },
        { text: "Contact your TA for further clarifications.", username: "TA Jane", editing: false, editedText: "" },
      ],
      newFeedback: "",
      isMilestoneSubmitted: true, // Example state
      showPDF: false, // Controls the visibility of the PDF modal
      pdfURL: null, // URL for the fetched PDF
      deadline: "2024-12-08",
      isDeadlineNear: false,
      milestones: [],
      teams: [],
      selectedMilestone: { id: "", title: "Loading..." },
      selectedTeam: { id: "", team_name: "Loading..." }
    }
  },
  created() {
    this.fetchMilestones();
    this.fetchTeams();
 },
  components: {
    Select
  },
  computed: {
    ...mapState(['user']),
    canEdit() {
      return ['admin', 'instructor', 'ta'].includes(this.user.role);
    }
  },
  methods: {
    async fetchMilestones() {
      try {
        const milestones = await getProjectMilestones(this.$route.params.projectId);
        this.milestones = Array.isArray(milestones) ? milestones : [];
        if (this.milestones.length > 0) {
          this.selectedMilestone = this.milestones[0]; // Select the first milestone by default
          console.log(this.selectedMilestone.title)
        }
      } catch (error) {
        console.error("Error fetching milestones:", error);
      }
    },
    async fetchTeams() {
      try {
        const response = await getProjectTeams(this.$route.params.projectId);
        if (Array.isArray(response)) {
          this.teams = response;
        } else if (response && response.team) {
          this.teams = [response.team];
        } else {
          this.teams = [];
        }
        if (this.teams.length > 0) {
          this.selectedTeam = this.teams[0];
        }
      } catch (error) {
        console.error("Error fetching teams:", error);
      }
    },

    handleMilestoneChange(value) {
      this.selectedMilestone = this.milestones.find(milestone => milestone.id === value);
      console.log("Selected Milestone:", {
        id: this.selectedMilestone.id,
        title: this.selectedMilestone.title,
        description: this.selectedMilestone.description,
        due_date: this.selectedMilestone.due_date
      });
    },

    handleTeamChange(value) {
      this.selectedTeam = this.teams.find(team => team.id === value);
      console.log("Selected Team:", {
        id: this.selectedTeam.id,
        team_name: this.selectedTeam.team_name
      });
    },

    toggleHeadingEdit() {
      this.editingHeading = !this.editingHeading;
      if (this.editingHeading) {
        this.editedHeading = this.selectedMilestone.title;
      }
    },
    saveHeading() {
      this.selectedMilestone.title = this.editedHeading.trim();
      this.editingHeading = false;
    },
    toggleDescriptionEdit() {
      this.editingDescription = !this.editingDescription;
      if (this.editingDescription) {
        this.editedDescription = `Use the options below to manage files and review feedback for ${this.selectedMilestone.title}.`;
      }
    },
    saveDescription() {
      // Save description logic
      this.editingDescription = false;
    },
    editFeedback(index) {
      this.$set(this.feedbackList[index], "editing", true);
      this.$set(this.feedbackList[index], "editedText", this.feedbackList[index].text);
    },
    saveFeedback(index) {
      const feedback = this.feedbackList[index];
      feedback.text = feedback.editedText.trim();
      feedback.editing = false;
    },
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
    navigateToCreateMilestone() {
      this.$router.push({ name: "CreateMilestone" });
    },
    deleteFeedback(index) {
      this.feedbackList.splice(index, 1);
    },
    addFeedback() {
      if (this.newFeedback.trim()) {
        this.feedbackList.push({ text: this.newFeedback.trim(), username: this.username });
        this.newFeedback = "";
      } else {
        alert("Feedback cannot be empty.");
      }
    },
    checkDeadline() {
      const today = new Date();
      const deadlineDate = new Date(this.deadline);
      const diffInDays = Math.ceil((deadlineDate - today) / (1000 * 60 * 60 * 24));
      this.isDeadlineNear = diffInDays <= 3;
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
.custom-select {
  background-color: rgba(0, 0, 0, 0.443);
}

</style>
