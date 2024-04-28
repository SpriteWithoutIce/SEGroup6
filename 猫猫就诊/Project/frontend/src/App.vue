<script setup>
import HeaderNavigation from './components/Navigation/HeaderNavigation.vue';
import NavBar from './components/Navigation/Navbar.vue'
</script>

<template>
  <div id="app">
    <HeaderNavigation />
    <NavBar />
  </div>
</template>

<style>
#app {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
