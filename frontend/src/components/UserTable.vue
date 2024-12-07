<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Users</h1>
    <DataTable
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
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" fluid />
        </template>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
      </Column>
      <Column :field="'role'" :header="'Role'" sortable removableSort>
        <template #editor="{ data, field }">
          <Dropdown
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
      <Column :field="'email'" :header="'Email'" sortable removableSort>
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" fluid />
        </template>
        <template #body="{ data, field }">
          <span>{{ data[field] }}</span>
        </template>
      </Column>
      <Column :field="'created_at'" :header="'CreatedAt'" sortable>
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
            @click="() => $router.push(`/user/${data.id}/details`)"
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
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import { DatePicker } from 'primevue';
import { FilterMatchMode, FilterOperator } from '@primevue/core/api';
import { getUsers, updateUser } from '../api/user';
import { formatDate } from '../utils/dateUtils';

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
  },
  data() {
    return {
      users: [], // Populated from the API
      columns: [
        { field: 'username', header: 'Username' },
        { field: 'role', header: 'Role' },
        { field: 'created_at', header: 'CreatedAt', type: 'date' },
        { field: 'email', header: 'Email' },
      ],
      roles: [
      { label: 'Instructor', value: 'Instructor' },
      { label: 'TA', value: 'TA' },
      { label: 'Student', value: 'Student' },
    ],
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        username: { value: null, matchMode: FilterMatchMode.CONTAINS },
        role: { value: null, matchMode: FilterMatchMode.CONTAINS },
        email: { value: null, matchMode: FilterMatchMode.CONTAINS },
        created_at: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
        },
      },
      loading: true, // Tracks loading state
      editingRows: [], // Tracks rows in edit mode
      editable: true, // Enables row editing
      allowView: true, // Enables detail view buttons
    };
  },
  async created() {
    try {
      this.loading = true
      const response = await getUsers()
      if (response.success) {
        console.log(response)
        this.users = response.users
        this.loading = false
      } else {
        console.error('Failed to fetch users:', response.message)
        this.loading = false
      }
    } catch (error) {
      console.error('Error fetching users:', error)
      this.loading = false
    }
  },
  methods: {
    onRowEditSave(event) {
      const user = event.data;
      updateUser(user.id, user)
        .then((response) => {
          if (response.success) {
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'User updated successfully',
              life: 3000,
            });
          } else {
            this.$toast.add({
              severity: 'error',
              summary: 'Error',
              detail: response.message,
              life: 3000,
            });
          }
        })
        .catch((error) => {
          console.error('Error updating user:', error);
          this.$toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to update user',
            life: 3000,
          });
        });
    },
    exportCSV() {
      this.$refs.dt.exportCSV();
    },
    formatDate,
  },
};
</script>

<style scoped>
</style>