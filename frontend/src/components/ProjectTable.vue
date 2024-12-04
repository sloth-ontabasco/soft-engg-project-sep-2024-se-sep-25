<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Projects</h1>
    <DataTable
      :value="projects"
      v-model:editingRows="editingRows"
      editMode="row"
      @row-edit-save="onRowEditSave"
      stripedRows
      paginator
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      size="large"
      :globalFilterFields="['title', 'description']"
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
      <Column
        v-for="col of columns"
        :key="col.field"
        :field="col.field"
        :header="col.header"
        removableSort
      >
        <template #editor="{ data, field }">
          <InputText
            v-if="col.type !== 'date'"
            v-model="data[field]"
            fluid
          />
          <DatePicker v-else id="datepicker-24h" v-model="data[field]" showTime hourFormat="24" fluid 
            dateFormat="yy-mm-dd'T'HH:mm:ss"/>

        </template>
        <template #body="{ data, field }">
          <span v-if="col.type === 'date'">{{ formatDate(data[field]) }}</span>
          <span v-else>{{ data[field] }}</span>
        </template>
      </Column>
      <Column
        :rowEditor="editable"
        style="width: 10%; min-width: 8rem"
        bodyStyle="text-align:center"
      ></Column>
      <Column v-if="allowView" class="w-24 !text-end">
        <template #body="{ data }">
          <Button icon="pi pi-search" class="p-button-secondary" rounded></Button>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { FilterMatchMode } from '@primevue/core/api'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import Button from 'primevue/button'
import { getProjects } from '../api/project'
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
    DatePicker
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
      },
      loading: true,
      editingRows: [],
      editable: true,
      allowView: true,
    }
  },
  async created() {
    try {
      const response = await getProjects()
      if (response.success) {
        this.projects = response.data
      } else {
        console.error('Failed to fetch projects:', response.message)
      }
    } catch (error) {
      console.error('Error fetching projects:', error)
    }
  },
  methods: {
    onRowEditSave(event) {
      this.$emit('row-edit-save', event)
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
