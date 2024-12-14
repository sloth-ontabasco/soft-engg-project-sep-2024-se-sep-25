<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Main Content -->
    <main class="flex-1 p-10">
      <!-- Breadcrumb Navigation -->
      <nav class="text-sm text-gray-600 mb-5">
        <router-link :to="'/projects'" class="hover:underline">All Projects</router-link>
        / <a href="#" class="hover:underline">SE Sept 2024</a> /

        <Select v-model="selectedMilestone" :options="milestones" optionLabel="title" optionValue="id"
          :defaultValue="selectedMilestone.id" @update:modelValue="handleMilestoneChange"
          class="w-full md:w-56 custom-select" />
        <template v-if="canEdit">
          /
          <Select v-model="selectedTeam" :options="teams" optionLabel="team_name" optionValue="id"
            :defaultValue="selectedTeam.id" @update:modelValue="handleTeamChange"
            class="w-full md:w-56 custom-select" />
        </template>
      </nav>

      <!-- Add Milestone Button -->
      <div v-if="canEdit" class="mb-5">
        <button @click="navigateToCreateMilestone" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Add Milestone
        </button>
      </div>

      <div class="flex justify-end mb-5">
        <!-- Github Button -->
        <button ref="githubButton" @click="loginWithGithub"
          class="bg-gray-800 text-white py-2 px-4 rounded-lg hover:bg-gray-700 transition duration-200">
          Link GitHub
        </button>
      </div>
      <!-- Header -->
      <div class="group flex items-center justify-between">
        <div>
          <h1 v-if="!editingHeading" class="text-black text-3xl font-bold mb-5">
            Milestone - {{ selectedMilestone.title }}
          </h1>
          <input v-else type="text" v-model="editedHeading" class="border p-2 rounded text-3xl font-bold mb-5"
            @keyup.enter="saveHeading" />
        </div>
        <i v-if="canEdit" @click="toggleHeadingEdit"
          class="fa fa-edit text-blue-500 hover:text-blue-700 cursor-pointer"></i>
      </div>

      <div class="group flex items-center justify-between">
        <div>
          <p v-if="!editingDescription" class="text-gray-700 mb-5">
            Use the options below to manage files and review feedback for
            {{ selectedMilestone.title }} for {{ selectedTeam.team_name }}.
            <br />
            {{ selectedMilestone.description || 'No description' }}
          </p>
          <textarea v-else v-model="editedDescription"
            class="w-full max-w-full p-2 border rounded focus:outline-none focus:ring mb-5"
            @keyup.enter="saveDescription"></textarea>
        </div>
        <i v-if="canEdit" @click="toggleDescriptionEdit"
          class="fa fa-edit text-blue-500 hover:text-blue-700 cursor-pointer"></i>
      </div>

      <div class="group flex items-center justify-between">
        <div>
          <div :class="[
            'inline-block px-6 py-3 rounded-lg text-sm font-semibold',
            isDeadlineNear
              ? 'bg-red-500 text-white animate-pulse'
              : 'bg-white text-black',
          ]" style="margin-left: 0">
            Deadline: {{ formattedDeadline }}
          </div>
          <input v-if="editingDeadline" type="date" v-model="editedDeadline"
            class="border p-2 rounded text-sm font-semibold mb-5" @change="saveDeadline" />
        </div>
        <i v-if="canEdit" @click="toggleDeadlineEdit"
          class="fa fa-edit text-blue-500 hover:text-blue-700 cursor-pointer"></i>
      </div>
      <br />
      <br />

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
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
              <label v-if="!hasFile && !canEdit"
                class="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600">
                <i class="fas fa-upload"></i> Upload
                <!-- Upload Icon -->
                <input type="file" accept=".zip" class="hidden" @change="handleFileUpload" />
              </label>
              <button v-if="hasFile" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                @click="downloadAllFiles">
                <i class="fas fa-download"></i> Download
                <!-- Download Icon -->
              </button>
              <button v-if="hasFile && !canEdit" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                @click="deleteAllSubmissions">
                <i class="fas fa-trash-alt"></i> Delete
                <!-- Delete Icon -->
              </button>
              <button v-if="canEdit" :disabled="!hasFile" class="bg-gray-400 text-white px-4 py-2 rounded" :class="{
                'bg-sky-500 hover:bg-sky-400': isMilestoneSubmitted,
                'opacity-50 hover:bg-sky-500': !hasFile,
              }" @click="fetchReport">
                <i class="fas fa-robot"></i> GenAI Report
                <!-- GenAI Icon -->
              </button>
              <button v-if="canEdit" :disabled="!hasFile" @click="showRubricsModal = true"
                class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none flex items-center"
                :class="{ 'opacity-50 hover:bg-blue-500': !hasFile }">
                <i class="fa fa-edit mr-2"></i> Rubrics for AI
              </button>
            </div>
          </div>
          <!-- PDF Viewer Modal -->
          <div v-if="showPDF"
            class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-75 flex justify-center items-center z-50">
            <div class="bg-white p-4 rounded shadow-lg w-4/5 h-4/5 relative">
              <button class="absolute top-2 right-2 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                @click="closePDF">
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
          <div v-if="isGitHubLinked">
            <p style="color: black;">Chosen Repository:</p>
            <select v-model="selectedRepo" @change="handleRepoChange" class="w-full md:w-56 custom-select">
              <option v-for="repo in repos" :key="repo" :value="repo">{{ repo }}</option>
            </select>
            <div v-if="commits.length > 0" class="mt-5 commits-container">
              <h3 class="text-black text-md font-bold mb-3">Commits:</h3>
              <ul>
                <li v-for="commit in commits" :key="commit.sha" class="mb-2">
                  <p style="color: black;"><strong>Message:</strong> {{ commit.message }}</p>
                  <p style="color: black;"><strong>Author:</strong> {{ commit.author }}</p>
                  <p style="color: black;"><strong>Date:</strong> {{ new Date(commit.date).toLocaleString() }}</p>
                </li>
              </ul>
            </div>
          </div>
          <div v-else>
            <p style="color: black;">Please link your GitHub account to view repositories.</p>
          </div>
        </div>
      </div>
      <!-- Rubrics Section -->

      <!-- Modal for Rubrics -->
      <div v-if="showRubricsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg w-1/3 shadow-lg">
          <h3 class="text-lg font-bold mb-4">
            {{ isEditingRubrics ? 'Edit Rubrics' : 'Add Rubrics' }}
          </h3>
          <form @submit.prevent="saveRubrics">
            <div class="mb-4">
              <label for="rubrics" class="block font-medium text-gray-700">Rubrics</label>
              <textarea v-model="editedRubrics" id="rubrics"
                class="w-full border border-gray-300 rounded p-2"></textarea>
            </div>
            <div class="flex justify-end">
              <button type="button" @click="closeRubricsModal"
                class="bg-gray-300 text-gray-700 py-2 px-4 rounded mr-2 hover:bg-gray-400 focus:outline-none">
                Cancel
              </button>
              <button type="submit"
                class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none">
                Save
              </button>
            </div>
          </form>
        </div>
      </div>
      <!-- Feedback Section -->
      <Feedbacks v-if="selectedMilestone.id && selectedTeam.id" :projectId="$route.params.projectId" :user="user"
        :selectedMilestone="selectedMilestone" :selectedTeam="selectedTeam" ref="feedbacksComponent" />
    </main>
  </div>
</template>

<script>
import Feedbacks from './Feedbacks.vue'
import { getProjectMilestones, updateMilestone } from '../api/milestone'
import { getProjectTeams } from '../api/team'
import { getGithubRepos, getGithubCommits } from '../api/github' // Import the API method to fetch repos and commit data

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
      isGitHubLinked: false,
      repos: [],
      selectedRepo: '',
      commits: [],
      feedbackList: [
        {
          text: 'Ensure all required files are uploaded before the deadline.',
          username: 'TA John',
          editing: false,
          editedText: '',
        },
        {
          text: 'Contact your TA for further clarifications.',
          username: 'TA Jane',
          editing: false,
          editedText: '',
        },
      ],
      newFeedback: '',
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
    ...mapState(['user']),
    canEdit() {
      return this.user && ['instructor', 'ta', 'admin'].includes(this.user.role)
    },
    formattedDeadline() {
      if (!this.selectedMilestone.due_date) return 'No deadline'
      const date = new Date(this.selectedMilestone.due_date)
      const day = String(date.getDate()).padStart(2, '0')
      const month = String(date.getMonth() + 1).padStart(2, '0') // Months are zero-based
      const year = date.getFullYear()
      return `${day}-${month}-${year}`
    },
  },
  // eslint-disable-next-line no-dupe-keys
  async mounted() {
    await this.fetchMilestones()
    await this.fetchTeams()
    await this.fetchGithubRepos()
    this.checkGithubLogin()
    if (this.selectedMilestone.id && this.selectedTeam.id) {
      this.$refs.feedbacksComponent.fetchFeedbacks()
      await this.fetchSubmissionStatus()
    }
    this.checkDeadline()
  },
  methods: {
    // Method to handle GitHub login redirect,
    loginWithGithub() {
      // Redirect to the backend GitHub login route to initiate OAuth flow
      window.location.href = import.meta.env.VITE_SERVER_BASE_URL + '/github/' + this.selectedTeam['id'] + '/login'; // Adjust if needed
    },
    checkGithubLogin() {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.has('githubLoginSuccess') || this.repos.length > 0) {
        const githubButton = this.$refs.githubButton;
        githubButton.style.backgroundColor = 'green';
        githubButton.disabled = true;
        githubButton.innerText = 'GitHub Linked';
        this.isGitHubLinked = true;
        this.fetchGithubRepos(); // Fetch repos if GitHub is linked
      }
    },
    async fetchGithubRepos() {
      try {
        const response = await getGithubRepos(this.selectedTeam['id']);
        this.repos = response.data.repos;
      } catch (error) {
        console.error('Error fetching GitHub repositories:', error);
      }
    },
    async handleRepoChange() {
      console.log('Selected Repo:', this.selectedRepo);
      // Handle repo change logic here
      try {
        const response = await getGithubCommits(this.selectedTeam['id'], this.selectedRepo);
        this.commits = response['commits'];
      } catch (error) {
        console.error('Error fetching GitHub repositories:', error);
      }
    },
    async fetchMilestones() {
      try {
        const milestones = await getProjectMilestones(
          this.$route.params.projectId,
        )
        this.milestones = Array.isArray(milestones) ? milestones : []
        if (this.milestones.length > 0) {
          this.selectedMilestone = this.milestones[0] // Select the first milestone by default
          console.log(this.selectedMilestone.title)
        }
      } catch (error) {
        console.error('Error fetching milestones:', error)
      }
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
          console.log('kdjwcksdjch')
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
        success('Success', 'Milestone title updated successfully')
      } catch (err) {
        error('Error', 'Error updating milestone title')
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
        success('Success', 'Milestone description updated successfully')
      } catch (err) {
        error('Error', 'Error updating milestone description')
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
            success('Success', 'File updated successfully')
          } else {
            await createSubmission(formData)
            success('Success', 'File uploaded successfully')
          }
          await this.fetchSubmissionStatus()
          event.target.value = '' // Reset the file input
        } catch (err) {
          error('Error', 'Error uploading file')
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
        success('Success', 'Submission deleted successfully')
        await this.fetchSubmissionStatus()
        document.querySelector('input[type="file"]').value = '' // Reset the file input
      } catch (err) {
        error('Error', 'Error deleting submission')
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
        success('Success', 'Rubrics saved successfully')
      } catch (err) {
        error('Error', 'Error saving rubrics')
        console.error('Error saving rubrics:', err)
      }
    },
    closeRubricsModal() {
      this.editedRubrics = this.selectedMilestone.rubrics // Reset editedRubrics to current rubrics
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
          due_date:
            new Date(this.editedDeadline).toISOString().split('.')[0] + 'Z', // Remove milliseconds and add 'Z'
        }
        await updateMilestone(
          this.selectedMilestone.project,
          this.selectedMilestone.id,
          updatedMilestone,
        )
        this.selectedMilestone.due_date = updatedMilestone.due_date
        this.editingDeadline = false
        success('Success', 'Milestone deadline updated successfully')
      } catch (err) {
        error('Error', 'Error updating milestone deadline')
        console.error('Error updating milestone deadline:', err)
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
  background: rgba(0, 0, 0, 0.8);
  /* Translucent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loader {
  border: 16px solid rgba(243, 243, 243, 0.7);
  /* Translucent border */
  border-radius: 50%;
  border-top: 16px solid rgba(52, 152, 219, 0.8);
  /* Translucent border-top */
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
  background: rgba(255, 255, 255, 0.8);
  /* Translucent background */
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

.commits-container {
  max-height: 100px; /* Set a fixed height */
  overflow-y: auto; /* Make it scrollable */
}

.commits-list {
  list-style-type: none; /* Remove default list styling */
  padding: 0; /* Remove default padding */
  margin: 0; /* Remove default margin */
}
</style>
