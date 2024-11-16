<script setup>
import Button from 'primevue/button'
</script>
<template>
  <DataTable
    :value="tableData"
    v-model:editingRows="editingRows"
    editMode="row"
    @row-edit-save="onRowEditSave"
    stripedRows
    paginator
    :rows="10"
    :rowsPerPageOptions="[10, 20, 50]"
    size="large"
    :globalFilterFields="['global']"
  >
    <template #header>
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-xl font-bold">{{ tableTitle }}</span>
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
          :disabled="data[field].choices"
          v-model="data[field]"
          fluid
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
        <Button icon="pi pi-search" class="p-button-secondary" rounded></Button>
      </template>
    </Column>
  </DataTable>
</template>

<script>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { FilterMatchMode } from '@primevue/core/api'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import Tag from 'primevue/tag'

export default {
  name: 'GenericTable',
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
      loading: true,
      editingRows: [],
    }
  },
  props: {
    tableData: {
      type: Array,
      required: true,
    },
    columns: {
      type: Array,
      required: true,
    },
    tableTitle: {
      type: String,
    },
    editable: {
      type: Boolean,
      default: true,
    },
    severity: {
      type: Object,
      required: false
    },
    allowView: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    onRowEditSave(event) {
      this.$emit('row-edit-save', event)
    },
    exportCSV() {
      this.$refs.dt.exportCSV()
    },
  },
  components: {
    DataTable,
    Column,
    InputIcon,
    InputText,
    IconField,
    Button,
    Tag,
  },
}
</script>

<style></style>
