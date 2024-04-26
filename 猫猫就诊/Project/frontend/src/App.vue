<template>
  <PrescriptionDetails ref="prescriptionDetails"> </PrescriptionDetails>
  <HeaderNavigation />
  <MakePrescription />
  <NavBar />
</template>

<script>
import PrescriptionDetails from './components/Prescription/PrescriptionDetails.vue'
import MakePrescription from './components/Prescription/MakePrescription.vue'
import HeaderNavigation from './components/HeaderNavigation.vue';
import NavBar from './components/Navigation/Navbar.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    PrescriptionDetails,
    MakePrescription,
    HeaderNavigation,
  },
  methods: {
    showPrescriptionDetails () {
      this.$refs.prescriptionDetails.openModal();
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
