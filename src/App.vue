<script setup>
import BillList from './components/Bills/BillList.vue'
import HeaderNavigation from './components/HeaderNavigation.vue';
import NavBar from './components/Navigation/Navbar.vue'
</script>

<template>
  <HeaderNavigation />
  <!-- <BillList /> -->
  <NavBar />
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
