<template>
    <GenericTable
      :tableData="users"
      :columns="columns"
      tableTitle="Users"
      :editable="true"
      :allowView="false"
    ></GenericTable>
  </template>
  
  <script>
  import GenericTable from './GenericTable.vue'
  
  export default {
    name: 'UserTable',
    components: {
      GenericTable,
    },
    data() {
      return {
        users: [
          {
            id: 1,
            name: 'John Doe',
            role: 'Admin',
            joinDate: '2023-01-15',
            email: 'john.doe@example.com',
          },
          {
            id: 2,
            name: 'Jane Smith',
            role: 'User',
            joinDate: '2023-02-20',
            email: 'jane.smith@example.com',
          },
          {
            id: 3,
            name: 'Alice Johnson',
            role: 'Moderator',
            joinDate: '2023-03-10',
            email: 'alice.johnson@example.com',
          },
        ],
        columns: [
          { field: 'name', header: 'User Name' },
          { field: 'role', header: 'Role' },
          { field: 'joinDate', header: 'Join Date' },
          { field: 'email', header: 'Email' },
        ],
      }
    },
  }
  </script>
  
  <style scoped>
  </style>