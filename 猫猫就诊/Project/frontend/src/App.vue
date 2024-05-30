<script setup>
import HeaderNavigation from './components/Navigation/HeaderNavigation.vue';
import NavBar from './components/Navigation/Navbar.vue'
import readOnlyVue from './components/Main/ReadOnlyVue.vue'
import PatientA from './components/History/PatientA.vue';
import PresA from './components/History/PresA.vue';
</script>

<template>
  <div id="app">
    <!-- <HeaderNavigation></HeaderNavigation> -->
    <NavBar></NavBar>
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
