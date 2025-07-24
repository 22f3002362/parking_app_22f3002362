<script setup>
import { RouterView } from 'vue-router'
// import NewNavbar from './components/NewNavbar.vue'
</script>

<template>
  <div id="app">
    <!-- <NewNavbar /> -->
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
#app {
  width: 100%;
  min-height: 100vh;
}

.main-content {
  min-height: 100vh;
}

/* Ensure navbar is above content */
header.header {
  position: relative;
  z-index: 100;
}

/* Ensure proper page transitions */
.router-view {
  width: 100%;
}

/* Reset any potential conflicting styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}
</style>

