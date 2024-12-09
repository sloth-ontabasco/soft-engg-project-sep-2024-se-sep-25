<template>
    <GenericTable
      :tableData="teams"
      :columns="columns"
      tableTitle="Teams"
      :editable="true"
      :allowView="false"
    ></GenericTable>
  </template>
  
  <script>
  import GenericTable from './GenericTable.vue'
  
  export default {
    name: 'TeamsTable',
    components: {
      GenericTable,
    },
    data() {
      return {
        teams: [
          {
            id: 1,
            name: 'Team Alpha',
            memberCount: 10,
            createdDate: '2023-01-15',
            status: {
              choices: {
                value: 'Active',
                severity: 'success',
              },
            },
          },
          {
            id: 2,
            name: 'Team Beta',
            memberCount: 8,
            createdDate: '2023-02-20',
            status: {
              choices: {
                value: 'Inactive',
                severity: 'danger',
              },
            },
          },
          {
            id: 3,
            name: 'Team Gamma',
            memberCount: 12,
            createdDate: '2023-03-10',
            status: {
              choices: {
                value: 'Pending',
                severity: 'warning',
              },
            },
          },
        ],
        columns: [
          { field: 'name', header: 'Team Name' },
          { field: 'memberCount', header: 'Member Count' },
          { field: 'createdDate', header: 'Created Date' },
          { field: 'status.choices.value', header: 'Status' },

        ],
      }
    },
  }
  </script>
  
  <style scoped>
  </style>