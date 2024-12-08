<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Projects</h1>
    <Toolbar class="mb-6">
      <template #start>
        <Button label="New" icon="pi pi-plus" class="mr-2" @click="openNew" />
      </template>

      <template #end>
        <Button
          label="Export"
          icon="pi pi-upload"
          severity="secondary"
          @click="exportCSV($event)"
        />
      </template>
    </Toolbar>

    <Dialog
      v-model:visible="newProjectVisible"
      :style="{ width: '450px' }"
      header="Project Details"
      :modal="true"
    >
      <div class="flex flex-col gap-6">
        <div>
          <label for="Title" class="block font-bold mb-3">Name</label>
          <InputText
            id="name"
            v-model.trim="project.title"
            required="true"
            autofocus
            :invalid="submitted && !project.title"
            fluid
          />
          <small v-if="submitted && !project.title" class="text-red-500"
            >Title is required.</small
          >
        </div>
        <div>
          <label for="description" class="block font-bold mb-3"
            >Description</label
          >
          <Textarea
            id="description"
            v-model="project.description"
            :invalid="submitted && !project.description"
            required="true"
            rows="3"
            cols="20"
            fluid
          />
          <small v-if="submitted && !project.title" class="text-red-500"
            >description is required.</small
          >
        </div>
        <div>
          <label for="deadline" class="block font-bold mb-3"
            >Project Deadline</label
          >
          <DatePicker
            id="deadline"
            dateFormat="yy-mm-dd"
            showTime
            hourFormat="24"
            fluid
            v-model="project.deadline"
          ></DatePicker>
        </div>
        <div>
          <label for="mentors" class="block font-bold mb-3">Mentors</label>
          <MultiSelect
            id="mentors"
            v-model="project.mentors"
            :options="allMentors"
            filter
            optionLabel="email"
            optionValue="id"
            placeholder="Select Mentors"
            class="w-full md:w-20rem"
          />
        </div>
        <Button
          label="Cancel"
          icon="pi pi-times"
          text
          @click="() => (newProjectVisible = false)"
        />
        <Button
          label="Save"
          icon="pi pi-check"
          @click="
            () => {
              project.id ? editProject() : saveProject()
            }
          "
        />
      </div>
    </Dialog>

    <DataTable
      ref="dt"
      :value="projects"
      v-model:filters="filters"
      filterDisplay="row"
      :loding="loading"
      stripedRows
      paginator
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      size="large"
      :globalFilterFields="['global', 'title', 'description', 'deadline']"
    >
      <template #header>
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="text-xl font-bold">Projects</span>
          <IconField>
            <InputIcon>
              <i class="pi pi-search" style="color: white" />
            </InputIcon>
            <InputText
              v-model="filters['global'].value"
              placeholder="Keyword Search"
            />
          </IconField>
        </div>
      </template>
      <template #empty> No data found. </template>
      <template #loading> Loading data... Please wait. </template>
      <Column :field="'title'" :header="'Title'" removableSort>
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" fluid />
        </template>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
      </Column>
      <Column :field="'description'" :header="'Description'" removableSort>
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" fluid />
        </template>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
      </Column>
      <Column :field="'deadline'" :header="'Deadline'" sortable>
        <template #editor="{ data, field }">
          <DatePicker
            id="datepicker-24h"
            v-model="data[field]"
            showTime
            hourFormat="24"
            fluid
            dateFormat="dd/mm/yy HH:mm:ss"
          />
        </template>
        <template #body="{ data, field }">
          <span>{{ formatDate(data[field]) }}</span>
        </template>
        <template #filter="{ filterModel }">
          <DatePicker
            v-model="filterModel.value"
            dateFormat="mm/dd/yy"
            placeholder="mm/dd/yyyy"
          />
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
      <Column v-if="allowView" class="w-24 !text-end">
        <template #body="{ data }">
          <Button
            @click="
              () => $router.push(`/project/${data.id}/milestonesubmission`)
            "
            icon="pi pi-search"
            class="p-button-secondary"
            rounded
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
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import { Toolbar, MultiSelect } from 'primevue'
import { Dialog } from 'primevue'
import Button from 'primevue/button'
import { getProjects, updateProject, createProject } from '../api/project'
import { DatePicker, Textarea } from 'primevue'
import { error, success, info } from '../utils/toast'
import { mapGetters } from 'vuex'
import { formatDate } from '../utils/dateUtils'
// eslint-disable-next-line no-unused-vars
const dt = ref()

export default {
  name: 'ProjectTable',
  components: {
    DataTable,
    Column,
    MultiSelect,
    InputIcon,
    InputText,
    // eslint-disable-next-line vue/no-reserved-component-names
    Textarea,
    IconField,
    // eslint-disable-next-line vue/no-reserved-component-names
    Button,
    DatePicker,
    Toolbar,
    // eslint-disable-next-line vue/no-reserved-component-names
    Dialog,
  },
  data() {
    return {
      projects: [],
      project: {
        title: '',
        description: '',
        deadline: null,
      },
      columns: [
        { field: 'title', header: 'Title' },
        { field: 'description', header: 'Description' },
        { field: 'deadline', header: 'Deadline', type: 'date' },
      ],
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        title: { value: null, matchMode: FilterMatchMode.CONTAINS },
        description: { value: null, matchMode: FilterMatchMode.CONTAINS },
        deadline: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
        },
      },
      loading: true,
      editingRows: [],
      editable: true,
      allowView: true,
      newProjectVisible: false,
      submitted: false,
    }
  },
  computed: {
    ...mapGetters(['allTAs', 'allInstructors']),
    allMentors() {
      return [...this.allTAs, ...this.allInstructors]
    },
  },
  created() {
    this.loading = true
    getProjects()
      .then(response => {
        if (response.success) {
          this.projects = response.data
          info('Success', 'Projects fetched successfully')
          this.loading = false
        } else {
          console.error('Failed to fetch projects:', response.message)
          error('Error', 'Failed to fetch projects')
          this.loading = false
        }
      })
      .catch(error => {
        console.error('Failed to fetch projects:', error)
        error('Error', 'Failed to fetch projects')
        this.loading = false
      })
  },
  methods: {
    openNew() {
      this.submitted = false
      this.newProjectVisible = true
    },
    openEdit(project) {
      this.project = { ...project }
      this.submitted - false
      this.newProjectVisible = true
    },
    async saveProject() {
      this.newProjectVisible = false
      this.project.deadline = formatDate(this.project.deadline)
      const res = await createProject(this.project)
      if (res.success) {
        success('Success', 'Project created successfully')
        console.log(res.data)
        this.projects.push(res.data)
      } else {
        error('Error', res.message)
      }
      this.submitted = true
    },
    async editProject() {
      this.project.deadline = formatDate(this.project.deadline)
      updateProject(this.project.id, this.project)
        .then(response => {
          if (response.success) {
            this.projects = this.projects.map(project => {
              if (project.id === this.project.id) {
                return this.project
              }
              return project
            })
            success('Success', 'Project updated successfully')

            this.newProjectVisible = false
          } else {
            error('Error', response.message)

            this.newProjectVisible = false
          }
        })
        .catch(error => {
          console.error('Error updating project:', error)
          error('Error', 'Failed to update project')

          this.newProjectVisible = false
        })
    },
    exportCSV() {
      this.$refs.dt.exportCSV()
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
