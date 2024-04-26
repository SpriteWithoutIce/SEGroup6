<template>
  <BillDetails ref="BillDetails"> </BillDetails>
  <HeaderNavigation />
  <BillList />
  <NavBar />
</template>

<script>
import BillDetails from './components/Bills/BillDetails.vue'
import BillList from './components/Bills/BillList.vue'
import HeaderNavigation from './components/HeaderNavigation.vue';
import NavBar from './components/Navigation/Navbar.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    BillDetails,
    BillList,
    HeaderNavigation,
  },
  methods: {
    showBillDetails () {
      this.$refs.billDetails.openModal();
    }
  }
}
</script>

<style>
#app {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
