<script setup>
import { RouterView } from 'vue-router'
import { Toast } from 'primevue';
</script>

<template>
  <Toast/>
  <RouterView />

</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  height: 100%;
  width: 100%;
}
</style>