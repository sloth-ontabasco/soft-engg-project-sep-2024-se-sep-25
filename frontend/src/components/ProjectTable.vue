<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Projects</h1>
    <DataTable
      :value="projects"
      v-model:editingRows="editingRows"
      v-model:filters="filters"
      filterDisplay="row"
      :loding="loading"
      editMode="row"
      @row-edit-save="onRowEditSave"
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
          <div class="text-end pb-4">
            <Button
              icon="pi pi-external-link"
              label="Export"
              class="p-button-secondary"
              @click="exportCSV($event)"
            />
          </div>
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
            dateFormat="yy-mm-dd'T'HH:mm:ss"
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
      <Column
        :rowEditor="editable"
        style="width: 10%; min-width: 8rem"
        bodyStyle="text-align:center"
      ></Column>
      <Column v-if="allowView" class="w-24 !text-end">
        <template #body="{ data }">
          <Button
            @click="() => $router.push(`/project/${data.id}/milestonesubmission`)"
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
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { FilterMatchMode, FilterOperator } from '@primevue/core/api'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import Button from 'primevue/button'
import { getProjects, updateProject } from '../api/project'
import { DatePicker } from 'primevue'

export default {
  name: 'ProjectTable',
  components: {
    DataTable,
    Column,
    InputIcon,
    InputText,
    IconField,
    Button,
    DatePicker,
  },
  data() {
    return {
      projects: [],
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
    }
  },
  async created() {
    try {
      this.loading = true
      const response = await getProjects()
      if (response.success) {
        this.projects = response.data
        this.loading = false
      } else {
        console.error('Failed to fetch projects:', response.message)
        this.loading = false
      }
    } catch (error) {
      console.error('Error fetching projects:', error)
      this.loading = false
    }
  },
  methods: {
    onRowEditSave(event) {
      console.log('row edit save', event)
      const project = event.data
      updateProject(project.id, project.data)
        .then(response => {
          if (response.success) {
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Project updated successfully',
              life: 3000,
            })
          } else {
            this.$toast.add({
              severity: 'error',
              summary: 'Error',
              detail: response.message,
              life: 3000,
            })
          }
        })
        .catch(error => {
          console.error('Error updating project:', error)
          this.$toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to update project',
            life: 3000,
          })
        })
    },
    exportCSV() {
      this.$refs.dt.exportCSV()
    },
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toISOString().slice(0, 19)
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
