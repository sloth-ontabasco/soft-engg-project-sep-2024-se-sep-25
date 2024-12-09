<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Users</h1>
    <DataTable
      ref="dt"
      :value="users"
      v-model:editingRows="editingRows"
      v-model:filters="filters"
      filterDisplay="row"
      :loading="loading"
      editMode="row"
      @row-edit-save="onRowEditSave"
      stripedRows
      paginator
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      size="large"
      :globalFilterFields="['global', 'username', 'role', 'email', 'created_at']"
    >
      <template #header>
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="text-xl font-bold">Users</span>
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
      <Column :field="'username'" :header="'Userame'" sortable removableSort>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
      </Column>
      <Column :field="'email'" :header="'Email'" sortable removableSort>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
      </Column>
      <Column :field="'role'" :header="'Role'" sortable removableSort>
        <template #editor="{ data, field }">
          <Select
            v-model="data[field]"
            :options="roles"
            optionLabel="label"
            placeholder="Select a role"
          />
        </template>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
      </Column>
      <Column
        :rowEditor="editable"
        style="width: 10%; min-width: 8rem"
        bodyStyle="text-align:center"
      ></Column>
    </DataTable>
  </div>
</template>

<script>
import { ref } from 'vue'
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import Select from 'primevue/select';
import Button from 'primevue/button';
import { error, success, info } from '../utils/toast'
import { DatePicker } from 'primevue';
import { FilterMatchMode } from '@primevue/core/api';

const dt = ref();

export default {
  name: 'UserTable',
  components: {
    DataTable,
    Column,
    InputIcon,
    InputText,
    IconField,
    Button,
    DatePicker,
    Select,
  },
  data() {
    return {
      columns: [
        { field: 'username', header: 'Username' },
        { field: 'role', header: 'Role' },
        { field: 'email', header: 'Email' },
      ],
      roles: [
        { label: 'Instructor', value: 'instructor' },
        { label: 'TA', value: 'ta' },
        { label: 'Student', value: 'student' },
      ],
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        username: { value: null, matchMode: FilterMatchMode.CONTAINS },
        email: { value: null, matchMode: FilterMatchMode.CONTAINS },
        role: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
      loading: true,
      editingRows: [],
      editable: true,
    };
  },
  computed: {
    // Fetch users directly from Vuex store
    users() {
      return this.$store.state.users;
    },
  },
  async mounted() {
    // Dispatch an action to fetch users from the API
    try {
      this.loading = true;
      await this.$store.dispatch('getAllUsers');
      info('Success', 'Users fetched successfully')
      this.loading = false;
    } catch (error) {
      console.error('Error fetching users:', error);
      this.loading = false;
    }
  },
  methods: {
    onRowEditSave(event) {
      const user = event.newData;
      user.role = user.role.value;

      // Dispatch the Vuex action to update the user
      this.$store.dispatch('updateUserAction', {
        id: user.id,
        details: user,
      });
      success('Success', 'User role updated successfully')
    },
    exportCSV() {
      this.$refs.dt.exportCSV();
    },
  },
};
</script>

<style scoped>
</style>
