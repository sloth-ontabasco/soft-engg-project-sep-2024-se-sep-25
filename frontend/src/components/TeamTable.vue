<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Teams</h1>
    <Toolbar class="mb-6">
      <template #start>
        <Button label="New" icon="pi pi-plus" class="mr-2" @click="openNew" />
      </template>
    </Toolbar>

    <Dialog
      v-model:visible="newTeamVisible"
      :style="{ width: '450px' }"
      header="Team Details"
      :modal="true"
    >
      <div class="flex flex-col gap-6">
        <div>
          <label for="team_name" class="block font-bold mb-3">Team Name</label>
          <InputText
            id="team_name"
            v-model.trim="team.team_name"
            required
            autofocus
            :invalid="submitted && !team.team_name"
          />
          <small v-if="submitted && !team.team_name" class="text-red-500">
            Team Name is required.
          </small>
        </div>
        <div>
          <label for="members" class="block font-bold mb-3">Members (Email)</label>
          <MultiSelect
            id="members"
            v-model="team.members"
            :options="allMembers"
            filter
            optionLabel="email"
            optionValue="id"
            placeholder="Select Members"
            class="w-full md:w-20rem"
          />
        </div>
        <div class="flex justify-end gap-2">
          <Button label="Cancel" icon="pi pi-times" text @click="() => (newTeamVisible = false)" />
          <Button label="Save" icon="pi pi-check" @click="saveTeam" />
        </div>
      </div>
    </Dialog>

    <DataTable
    ref="dt"
      :value="teams"
      v-model:filters="filters"
      filterDisplay="row"
      :loding="loading"
      stripedRows
      paginator
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      size="large"
      :globalFilterFields="['global', 'team_name', 'member_count', 'created_at']"
      class="mt-4"
    >
      <template #header>
        <div class="flex items-center justify-between">
          <span class="text-xl font-bold">Teams</span>
          <div class="flex gap-2">
            <InputText
              v-model="filters['global'].value"
              placeholder="Search by keyword"
              class="w-full md:w-20rem"
            />
          </div>
        </div>
      </template>

      <template #empty> No data found. </template>
      <template #loading> Loading data... Please wait. </template>

      <Column :field="'team_name'" :header="'Team Name'" sortable>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" />
        </template>
      </Column>
      <Column :field="'members'" :header="'Member Count'" sortable>
        <template #body="{ data }">
          <span>{{ data.member_count }}</span>
        </template>
      </Column>
      <Column :field="'created_at'" :header="'Created Date'" sortable>
        <template #body="{ data, field }">
          <span>{{ formatDate(data[field]) }}</span>
        </template>
      </Column>
      <Column :field="'project_status'" :header="'Status'" sortable>
        <template #body="{ data }">
          <span>{{ data.project_status }}</span>
        </template>
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" />
        </template>
      </Column>
      <Column>
        <template #body="{ data }">
          <Button
            icon="pi pi-pencil"
            class="p-button-secondary"
            rounded
            @click="openEdit(data)"
          ></Button>
        </template>
      </Column>
      <Column>
        <template #body="{ data }">
          <Button
            icon="pi pi-trash"
            class="p-button-warning"
            rounded
            @click.stop="confirmDelete(data)"
          ></Button>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import { ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import { Toolbar, MultiSelect } from 'primevue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import { getProjectTeams, createTeam, updateTeam, deleteTeam } from '../api/team'
import { mapGetters } from 'vuex'
import { success, error } from '../utils/toast'
import { formatDate } from '../utils/dateUtils'

const dt = ref()

export default {
  name: 'TeamsTable',
  components: {
    DataTable,
    Column,
    InputText,
    Textarea,
    Toolbar,
    MultiSelect,
    Dialog,
    Button,
  },
  data() {
    return {
      teams: [],
      team: {
        team_name: '',
        members: '',
      },
      columns: [
        { field: 'team_name', header: 'Team Name' },
        { field: 'member_count', header: 'Member Count' },
        { field: 'created_at', header: 'Created Date' },
        { field: 'project_status', header: 'Project Status' },
      ],
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        team_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
        project_status: { value: null, matchMode: FilterMatchMode.CONTAINS },
        created_at: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
        },
      },
      loading: true,
      newTeamVisible: false,
      submitted: false,
      filters: {
        global: { value: null },
      },
    }
  },
  computed: {
    ...mapGetters(['allStudents']),
    allMembers() {
      return [...this.allStudents]
    },
  },
  async mounted() {
    await this.fetchTeams()
  },
  methods: {
    async fetchTeams() {
      this.loading = true
      try {
        const response = await getProjectTeams(this.$route.params.projectId)
        if (response) {
          this.teams = response
          console.log(this.teams)
          success('Success', 'Teams fetched successfully')
        }
      } catch (err) {
        error('Error', 'Failed to fetch teams')
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    openNew() {
      this.submitted = false
      this.team = { team_name: '', members: '' }
      this.newTeamVisible = true
    },
    async saveTeam() {
      this.submitted = true
      if (!this.team.team_name || !this.team.members) return
      try {
        const members = this.team.members.split(',').map((email) => email.trim())
        const response = await createTeam({
          team_name: this.team.team_name,
          members,
        })
        if (response.success) {
          this.teams.push(response.data)
          success('Success', 'Team created successfully')
          this.newTeamVisible = false
        }
      } catch (err) {
        error('Error', 'Failed to create team')
        console.error(err)
      }
    },
    openEdit(data) {
      this.team = { ...data, members: data.members.join(', ') }
      this.newTeamVisible = true
    },
    async editTeam() {
      this.team.members = this.team.members.split(',').map(member => member.trim());
      updateTeam(this.team.id, this.team)
        .then(response => {
          if (response.success) {
            this.teams = this.teams.map(team => {
              if (team.id === this.team.id) {
                return this.team;
              }
              return team;
            });
            success('Success', 'Team updated successfully');
            this.newTeamVisible = false;
          } else {
            error('Error', response.message);
            this.newTeamVisible = false;
          }
        })
        .catch(error => {
          console.error('Error updating team:', error);
          error('Error', 'Failed to update team');
          this.newTeamVisible = false;
        });
    },
    async confirmDelete(team) {
      if (confirm(`Are you sure you want to delete team "${team.team_name}"?`)) {
        try {
          const response = await deleteTeam(team.id)
          if (response.success) {
            this.teams = this.teams.filter((t) => t.id !== team.id)
            success('Success', 'Team deleted successfully')
          }
        } catch (err) {
          error('Error', 'Failed to delete team')
          console.error(err)
        }
      }
    },
    formatDate(date) {
      return formatDate(date)
    },
  },
}
</script>

<style scoped>
.p-4 {
  padding: 1rem;
}
.text-2xl {
  font-size: 1.5rem;
}
.font-bold {
  font-weight: bold;
}
.mb-4 {
  margin-bottom: 1rem;
}
</style>