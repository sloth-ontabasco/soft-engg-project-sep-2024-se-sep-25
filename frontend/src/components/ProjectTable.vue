<template>
  <GenericTable
    :tableData="projects"
    :columns="columns"
    tableTitle="Projects"
    :editable="true"
    :severity="severity"
  ></GenericTable>
</template>

<script>
import GenericTable from './GenericTable.vue'

export default {
  name: 'ProjectTable',
  components: {
    GenericTable,
  },
  data() {
    return {
      projects: [
        {
          id: 1,
          name: 'Project 1',
          createdOn: '2024-11-28 16:00:00',
          submissionBy: '2024-12-28 16:00:00',
          studentsEnrolled: 100,
          taAssigned: 10,
          status: {
            choices: {
              value: 'In Progress',
              severity: 'info',
            },
          },
        },
        {
          id: 2,
          name: 'Project 2',
          createdOn: '2024-11-28 16:00:00',
          submissionBy: '2024-12-28 16:00:00',
          studentsEnrolled: 100,
          taAssigned: 10,
          status: {
            choices: {
              value: 'In Progress',
              severity: 'info',
            },
          },
        },
        {
          id: 3,
          name: 'Project 3',
          createdOn: '2024-11-28 16:00:00',
          submissionBy: '2024-12-28 16:00:00',
          studentsEnrolled: 100,
          taAssigned: 10,
          status: {
            choices: {
              value: 'Not Started',
              severity: 'danger',
            },
          },
        },
      ],
      columns: [
        { field: 'name', header: 'Name' },
        { field: 'createdOn', header: 'Created On' },
        { field: 'submissionBy', header: 'Submission By' },
        { field: 'studentsEnrolled', header: 'Students Enrolled' },
        { field: 'taAssigned', header: 'TA Assigned' },
        { field: 'status.choices.value', header: 'Status', severity: 'status.choices.severity' },
      ],
      severity: {
        'Not Started': 'danger',
        'In Progress': 'info',
      },
    }
  },
}
</script>
