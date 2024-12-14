<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Main Content -->
    <main class="flex-1 p-10">
      <!-- Breadcrumb Navigation -->
      <nav class="text-sm text-gray-600 mb-5">
        <router-link :to="'/projects'" class="hover:underline"
          >All Projects</router-link
        >
        / <a href="#" class="hover:underline">{{ projectName }}</a> /

        <Select
          v-if="milestones.length > 0"
          v-model="selectedMilestone"
          :options="milestones"
          optionLabel="title"
          optionValue="id"
          :defaultValue="selectedMilestone.id"
          @update:modelValue="handleMilestoneChange"
          class="w-full md:w-56 custom-select"
        />
        <template v-if="canEdit && milestones.length > 0">
          /
          <Select
            v-model="selectedTeam"
            :options="teams"
            optionLabel="team_name"
            optionValue="id"
            :defaultValue="selectedTeam.id"
            @update:modelValue="handleTeamChange"
            class="w-full md:w-56 custom-select"
          />
        </template>
      </nav>

      <!-- Add Milestone Button -->
      <div v-if="canEdit" class="mb-5 flex justify-between items-center">
        <button
          @click="navigateToCreateMilestone"
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Add Milestone
        </button>
        <button
          v-if="milestones.length > 0"
          @click="confirmDeleteMilestone"
          class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Delete Milestone
        </button>
      </div>

      <!-- No Milestones Message for Instructor -->
      <div v-if="canEdit && milestones.length === 0" class="text-center text-gray-600">
        No milestones found. Start organizing your project now.
      </div>

      <!-- No Milestones Message for Students -->
      <div v-if="!canEdit && milestones.length === 0" class="text-center text-gray-600">
        You will see milestones here when uploaded by the instructor.
      </div>

      <!-- Milestone Details -->
      <div v-if="milestones.length > 0">
        <!-- Header -->
        <div class="group flex items-center justify-between">
          <div>
            <h1 v-if="!editingHeading" class="text-black text-3xl font-bold mb-5">
              Milestone - {{ selectedMilestone.title }} 
            </h1>
            <input
              v-else
              type="text"
              v-model="editedHeading"
              class="border p-2 rounded text-3xl font-bold mb-5"
              @keyup.enter="saveHeading"
            />
          </div>
          <i
            v-if="canEdit"
            @click="toggleHeadingEdit"
            class="fa fa-edit text-blue-500 hover:text-blue-700 cursor-pointer"
          ></i>
        </div>

        <div class="group flex items-center justify-between">
          <div>
            <p v-if="!editingDescription" class="text-gray-700 mb-5">
              {{ selectedMilestone.description || 'No description' }}
            </p>
            <textarea
              v-else
              v-model="editedDescription"
              class="w-full max-w-full p-2 border rounded focus:outline-none focus:ring mb-5"
              @keyup.enter="saveDescription"
            ></textarea>
          </div>
          <i
            v-if="canEdit"
            @click="toggleDescriptionEdit"
            class="fa fa-edit text-blue-500 hover:text-blue-700 cursor-pointer"
          ></i>
        </div>

        <div class="group flex items-center justify-between">
          <div>
            <div
              :class="[ 
                'inline-block px-6 py-3 rounded-lg text-sm font-semibold',
                isDeadlineNear
                  ? 'bg-red-500 text-white animate-pulse'
                  : 'bg-white text-black',
              ]"
              style="margin-left: 0"
            >
              Deadline: {{ formattedDeadline }}
            </div>
            <input
              v-if="editingDeadline"
              type="date"
              v-model="editedDeadline"
              class="border p-2 rounded text-sm font-semibold mb-5"
              @change="saveDeadline"
            />
          </div>
          <i
            v-if="canEdit"
            @click="toggleDeadlineEdit"
            class="fa fa-edit text-blue-500 hover:text-blue-700 cursor-pointer"
          ></i>
        </div>
        <br />
        <br />

        <!-- No Teams Message for Instructor -->
        <div v-if="canEdit && teams.length === 0" class="text-center text-gray-600">
          No teams assigned. Head over to the Teams section to get started.
        </div>

        <!-- No Teams Message for Students -->
        <div v-if="!canEdit && teams.length === 0" class="text-center text-gray-600">
          You are not part of this project.
        </div>

        <!-- Submissions and GitHub Tracker Sections -->
        <div v-if="teams.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Files Submitted Section -->
          <div class="bg-white shadow-md rounded-lg p-5">
            <h2 class="text-black text-lg font-bold mb-3">Submissions</h2>
            <ul>
              <li v-if="hasFile" class="flex justify-between mb-2">
                <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full">
                  {{ submission.file_name }}
                </span>
                <span class="text-green-600"> Submitted </span>
              </li>
              <li v-else class="flex justify-between mb-2">
                <span class="text-red-600"> Submission Pending </span>
              </li>
            </ul>

            <!-- Buttons: Upload, Download, Delete -->
            <div class="flex justify-between mt-4">
              <!-- Left-aligned buttons -->
              <div class="flex gap-2">
                <label
                  v-if="!hasFile && !canEdit"
                  class="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600"
                >
                  <i class="fas fa-upload"></i> Upload
                  <!-- Upload Icon -->
                  <input
                    type="file"
                    accept=".zip"
                    class="hidden"
                    @change="handleFileUpload"
                  />
                </label>
                <button
                  v-if="hasFile"
                  class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                  @click="downloadAllFiles"
                >
                  <i class="fas fa-download"></i> Download
                  <!-- Download Icon -->
                </button>
                <button
                  v-if="hasFile && !canEdit"
                  class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                  @click="deleteAllSubmissions"
                >
                  <i class="fas fa-trash-alt"></i> Delete
                  <!-- Delete Icon -->
                </button>
                <button
                  v-if="canEdit"
                  :disabled="!hasFile"
                  class="bg-gray-400 text-white px-4 py-2 rounded"
                  :class="{
                    'bg-sky-500 hover:bg-sky-400': isMilestoneSubmitted,
                    'opacity-50 hover:bg-sky-500': !hasFile,
                  }"
                  @click="fetchReport"
                >
                  <i class="fas fa-robot"></i> GenAI Report
                  <!-- GenAI Icon -->
                </button>
                <button
                  v-if="canEdit"
                  :disabled="!hasFile"
                  @click="showRubricsModal = true"
                  class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none flex items-center"
                  :class="{ 'opacity-50 hover:bg-blue-500': !hasFile }"
                >
                  <i class="fa fa-edit mr-2"></i> Rubrics for AI
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
                <iframe :src="pdfURL" class="w-full h-full border-none"></iframe>
              </div>
            </div>
          </div>

          <!-- GitHub Tracker Section -->
          <div class="bg-white shadow-md rounded-lg p-5">
            <h2 class="text-black text-lg font-bold mb-3">
              GitHub Tracker - {{ selectedMilestone.title }}
            </h2>
            <ul>
              <li class="mb-3">
                <span class="text-blue-500">JIRA-5677 Google OAuth</span>
                <p class="text-gray-600 text-sm">
                  @student.email closed this issue Oct 1, 3:33PM
                </p>
              </li>
              <li class="mb-3">
                <span class="text-blue-500"
                  >JIRA-Issue-5902 Google OAuth Login Bug</span
                >
                <p class="text-gray-600 text-sm">
                  @student.email closed this issue Oct 1, 3:33PM
                </p>
              </li>
            </ul>
          </div>
        </div>
        <!-- Rubrics Section -->

        <!-- Modal for Rubrics -->
        <div
          v-if="showRubricsModal"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        >
          <div class="bg-white p-6 rounded-lg w-1/3 shadow-lg">
            <h3 class="text-lg font-bold mb-4">
              {{ isEditingRubrics ? 'Edit Rubrics' : 'Add Rubrics' }}
            </h3>
            <form @submit.prevent="saveRubrics">
              <div class="mb-4">
                <label for="rubrics" class="block font-medium text-gray-700"
                  >Rubrics</label
                >
                <textarea
                  v-model="editedRubrics"
                  id="rubrics"
                  class="w-full border border-gray-300 rounded p-2"
                ></textarea>
              </div>
              <div class="flex justify-end">
                <button
                  type="button"
                  @click="closeRubricsModal"
                  class="bg-gray-300 text-gray-700 py-2 px-4 rounded mr-2 hover:bg-gray-400 focus:outline-none"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
        <!-- Feedback Section -->
        <Feedbacks
          v-if="selectedMilestone.id && selectedTeam.id"
          :projectId="$route.params.projectId"
          :user="user"
          :selectedMilestone="selectedMilestone"
          :selectedTeam="selectedTeam"
          ref="feedbacksComponent"
        />
      </div>
    </main>
  </div>
</template>

<script>
import Feedbacks from './Feedbacks.vue'
import { getProjectMilestones, updateMilestone, deleteMilestone } from '../api/milestone'
import { getProjectTeams } from '../api/team'
import {
  getSubmission,
  createSubmission,
  updateSubmission,
  getSubmissionFile,
  fetchGenAIReport,
} from '../api/submissions'
import Select from 'primevue/select'
import { mapState } from 'vuex'
import { success, error } from '../utils/toast'

export default {
  name: 'MilestoneSubmission',
  components: {
    Feedbacks,
    // eslint-disable-next-line vue/no-reserved-component-names
    Select,
  },
  data() {
    return {
      editingHeading: false,
      editingDescription: false,
      editedHeading: '',
      editedDescription: '',
      isMilestoneSubmitted: true, // Example state
      showPDF: false, // Controls the visibility of the PDF modal
      pdfURL: null, // URL for the fetched PDF
      deadline: '2024-12-07T07:22:04.216+00:00',
      isDeadlineNear: false,
      milestones: [],
      teams: [],
      selectedMilestone: { id: '', title: 'Loading...' },
      selectedTeam: { id: '', team_name: 'Loading...' },
      hasSubmission: false,
      hasFile: false,
      submission: {},
      showRubricsModal: false,
      editedRubrics: '',
      isEditingRubrics: false,
      canEdit: true,
      editingDeadline: false,
      editedDeadline: '',
    }
  },
  // eslint-disable-next-line no-dupe-keys
  computed: {
    ...mapState(['user', 'selectedProjectName']),
    canEdit() {
      return this.user && ['instructor', 'ta', 'admin'].includes(this.user.role)
    },
    projectName() {
      return this.selectedProjectName;
    },
    formattedDeadline() {
      if (!this.selectedMilestone.due_date) return 'No deadline';
      const date = new Date(this.selectedMilestone.due_date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
    },
  },
  // eslint-disable-next-line no-dupe-keys
  async mounted() {
    await this.fetchMilestones()
    await this.fetchTeams()
    const milestoneId = this.$store.state.selectedMilestoneId;
    if (milestoneId) {
      this.selectedMilestone = this.milestones.find(milestone => milestone.id === milestoneId) || this.milestones[0];
      this.$store.commit('setSelectedMilestoneId', null); // Clear the stored milestone ID
    } else {
      this.selectNearestUpcomingMilestone();
    }
    if (this.selectedMilestone.id && this.selectedTeam.id) {
      this.$refs.feedbacksComponent.fetchFeedbacks()
      await this.fetchSubmissionStatus()
    }
    this.checkDeadline()
  },
  methods: {
    async fetchMilestones() {
      try {
        const milestones = await getProjectMilestones(
          this.$route.params.projectId,
        )
        this.milestones = Array.isArray(milestones) ? milestones.sort((a, b) => new Date(a.due_date) - new Date(b.due_date)) : []
        if (this.milestones.length > 0) {
          this.selectedMilestone = this.milestones[0] // Select the first milestone by default
          console.log(this.selectedMilestone.title)
        }
      } catch (error) {
        console.error('Error fetching milestones:', error)
      }
    },
    selectNearestUpcomingMilestone() {
      const today = new Date();
      const nearestMilestone = this.milestones.find(milestone => new Date(milestone.due_date) >= today);
      this.selectedMilestone = nearestMilestone || this.milestones[0];
      this.checkDeadline(); // Update the deadline status
    },
    async fetchTeams() {
      try {
        const response = await getProjectTeams(this.$route.params.projectId)
        console.log(response)
        if (Array.isArray(response)) {
          console.log('!!!! dewgwe')
          this.teams = response
        } else if (response && response.team) {
        console.log('here!!!!!')
          this.teams = [response.team]
        } else {
          this.teams = []
        }
        if (this.teams.length > 0) {
          console.log("kdjwcksdjch")
          this.selectedTeam = this.teams[0]
        }
      } catch (error) {
        console.error('Error fetching teams:', error)
      }
    },

    async fetchSubmissionStatus() {
      try {
        const submission = await getSubmission(
          this.selectedTeam.id,
          this.selectedMilestone.id,
        )
        this.submission = submission.data
        this.hasSubmission = !!submission.data
        this.hasFile =
          submission.data && submission.data.submission ? true : false
        console.log('File found: ', this.hasFile)
      } catch (error) {
        this.hasSubmission = false
        this.hasFile = false
      }
    },

    handleMilestoneChange(value) {
      this.selectedMilestone = this.milestones.find(
        milestone => milestone.id === value,
      )
      console.log('Selected Milestone:', {
        id: this.selectedMilestone.id,
        title: this.selectedMilestone.title,
        description: this.selectedMilestone.description,
        due_date: this.selectedMilestone.due_date,
      })
      this.checkDeadline(); // Update the deadline status
      this.$nextTick(() => {
        this.refreshFeedbacks()
        this.fetchSubmissionStatus()
      })
    },

    handleTeamChange(value) {
      this.selectedTeam = this.teams.find(team => team.id === value)
      console.log('Selected Team:', {
        id: this.selectedTeam.id,
        team_name: this.selectedTeam.team_name,
      })
      this.$nextTick(() => {
        this.refreshFeedbacks()
        this.fetchSubmissionStatus()
      })
    },

    refreshFeedbacks() {
      this.$refs.feedbacksComponent.fetchFeedbacks()
    },

    toggleHeadingEdit() {
      this.editingHeading = !this.editingHeading
      if (this.editingHeading) {
        this.editedHeading = this.selectedMilestone.title
      }
    },
    async saveHeading() {
      try {
        const updatedMilestone = {
          ...this.selectedMilestone,
          title: this.editedHeading.trim(),
        }
        await updateMilestone(
          this.selectedMilestone.project,
          this.selectedMilestone.id,
          updatedMilestone,
        )
        this.selectedMilestone.title = this.editedHeading.trim()
        this.editingHeading = false
        success("Success", "Milestone title updated successfully")
      } catch (err) {
        error("Error", "Error updating milestone title")
        console.error('Error updating milestone title:', err)
      }
    },
    toggleDescriptionEdit() {
      this.editingDescription = !this.editingDescription
      if (this.editingDescription) {
        this.editedDescription = this.selectedMilestone.description
      }
    },
    async saveDescription() {
      try {
        const updatedMilestone = {
          ...this.selectedMilestone,
          description: this.editedDescription.trim(),
        }
        await updateMilestone(
          this.selectedMilestone.project,
          this.selectedMilestone.id,
          updatedMilestone,
        )
        this.selectedMilestone.description = this.editedDescription.trim()
        this.editingDescription = false
        success("Success", "Milestone description updated successfully")
      } catch (err) {
        error("Error", "Error updating milestone description")
        console.error('Error updating milestone description:', err)
      }
    },
    editFeedback(index) {
      this.$set(this.feedbackList[index], 'editing', true)
      this.$set(
        this.feedbackList[index],
        'editedText',
        this.feedbackList[index].text,
      )
    },
    saveFeedback(index) {
      const feedback = this.feedbackList[index]
      feedback.text = feedback.editedText.trim()
      feedback.editing = false
    },
    async handleFileUpload(event) {
      const files = event.target.files
      if (files.length) {
        const formData = new FormData()
        formData.append('submission', files[0])
        formData.append('milestone_id', this.selectedMilestone.id)
        formData.append('team_id', this.selectedTeam.id)

        try {
          if (this.hasSubmission) {
            await updateSubmission(
              this.selectedTeam.id,
              this.selectedMilestone.id,
              formData,
            )
            success("Success", "File updated successfully")
          } else {
            await createSubmission(formData)
            success("Success", "File uploaded successfully")
          }
          await this.fetchSubmissionStatus()
          event.target.value = '' // Reset the file input
        } catch (err) {
          error("Error", "Error uploading file")
          console.error('Error uploading file:', err)
        }
      }
    },
    async downloadAllFiles() {
      try {
        console.log(
          'Attempting to download files for team:',
          this.selectedTeam.id,
          'milestone:',
          this.selectedMilestone.id,
        )
        const response = await getSubmissionFile(
          this.selectedTeam.id,
          this.selectedMilestone.id,
        )
        const teamName = this.selectedTeam.team_name.replace(/\s+/g, '_')
        const milestoneTitle = this.selectedMilestone.title.replace(/\s+/g, '_')
        const url = window.URL.createObjectURL(
          new Blob([response.data], { type: 'application/zip' }),
        )
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${teamName}_-_${milestoneTitle}.zip`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        console.log('File downloaded successfully')
      } catch (error) {
        console.error('Error downloading file:', error)
      }
    },
    async deleteAllSubmissions() {
      const formData = new FormData()
      formData.append('milestone_id', this.selectedMilestone.id)
      formData.append('team_id', this.selectedTeam.id)

      try {
        await updateSubmission(
          this.selectedTeam.id,
          this.selectedMilestone.id,
          formData,
        )
        success("Success", "Submission deleted successfully")
        await this.fetchSubmissionStatus()
        document.querySelector('input[type="file"]').value = '' // Reset the file input
      } catch (err) {
        error("Error", "Error deleting submission")
        console.error('Error deleting submission:', err)
      }
    },
    async fetchReport() {
      this.$store.commit('showLoader')
      try {
        const response = await fetchGenAIReport(this.submission.id)
        this.pdfURL = URL.createObjectURL(
          new Blob([response.data], { type: 'text/html' }),
        )
        this.showPDF = true
      } catch (error) {
        console.error('Error fetching GenAI report:', error)
      } finally {
        this.$store.commit('hideLoader')
      }
    },
    closePDF() {
      this.showPDF = false // Hide the PDF viewer
      this.pdfURL = null // Clean up the URL
    },
    navigateToCreateMilestone() {
      this.$router.push({ name: 'CreateMilestone' })
    },
    deleteFeedback(index) {
      this.feedbackList.splice(index, 1)
    },
    addFeedback() {
      if (this.newFeedback.trim()) {
        this.feedbackList.push({
          text: this.newFeedback.trim(),
          username: this.username,
        })
        this.newFeedback = ''
      } else {
        alert('Feedback cannot be empty.')
      }
    },
    checkDeadline() {
      const today = new Date()
      const deadlineDate = new Date(this.selectedMilestone.due_date)
      const diffInDays = Math.ceil(
        (deadlineDate - today) / (1000 * 60 * 60 * 24),
      )
      this.isDeadlineNear = diffInDays > 0 && diffInDays <= 3
    },
    async saveRubrics() {
      try {
        const updatedMilestone = {
          ...this.selectedMilestone,
          rubrics: this.editedRubrics,
        }
        await updateMilestone(
          this.selectedMilestone.project,
          this.selectedMilestone.id,
          updatedMilestone,
        )
        this.selectedMilestone.rubrics = this.editedRubrics
        this.showRubricsModal = false
        this.isEditingRubrics = false
        success("Success", "Rubrics saved successfully")
      } catch (err) {
        error("Error", "Error saving rubrics")
        console.error('Error saving rubrics:', err)
      }
    },
    closeRubricsModal() {
      this.editedRubrics = this.selectedMilestone.rubrics; // Reset editedRubrics to current rubrics
      this.showRubricsModal = false
      this.isEditingRubrics = false
    },
    toggleDeadlineEdit() {
      this.editingDeadline = !this.editingDeadline
      if (this.editingDeadline) {
        this.editedDeadline = this.selectedMilestone.due_date.split('T')[0]
      }
    },
    async saveDeadline() {
      try {
        const updatedMilestone = {
          ...this.selectedMilestone,
          due_date: new Date(this.editedDeadline).toISOString().split('.')[0] + 'Z', // Remove milliseconds and add 'Z'
        }
        await updateMilestone(
          this.selectedMilestone.project,
          this.selectedMilestone.id,
          updatedMilestone,
        )
        this.selectedMilestone.due_date = updatedMilestone.due_date
        this.editingDeadline = false
        this.checkDeadline() // Update the deadline status
        success("Success", "Milestone deadline updated successfully")
      } catch (err) {
        error("Error", "Error updating milestone deadline")
        console.error('Error updating milestone deadline:', err)
      }
    },
    confirmDeleteMilestone() {
      if (confirm(`Are you sure you want to delete "${this.selectedMilestone.title}"?`)) {
        this.deleteMilestone();
      }
    },
    async deleteMilestone() {
      try {
        const projectId = this.$route.params.projectId;
        const milestoneId = this.selectedMilestone.id;
        await deleteMilestone(projectId, milestoneId);
        success("Success", "Milestone deleted successfully!");
        await this.fetchMilestones(); // Fetch the updated list of milestones
        this.selectNearestUpcomingMilestone(); // Select the default (latest upcoming) milestone
        this.$refs.feedbacksComponent.fetchFeedbacks(); // Refresh feedbacks
        await this.fetchSubmissionStatus(); // Refresh submission status
      } catch (error) {
        console.error("Error deleting milestone:", error);
        error("Error", "Failed to delete milestone.");
      }
    },
  },
}
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
  border-top: 16px solid rgba(52, 152, 219, 8); /* Translucent border-top */
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
  background: rgba(255, 255, 255, 0.8); /* Translucent background */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.custom-select {
  background-color: rgb(82, 88, 126);
}
</style>
