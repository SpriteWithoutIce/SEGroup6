<!--患者的历史查询页面-->
<script setup>
import CarouselA from './CarouselA.vue';
import HeadA from './HeadA.vue';
import SearchA from './SearchA.vue';
import SignA from './SignA.vue';
import InputA from './InputA.vue';
import MakePrescription from '@/components/Prescription/MakePrescription.vue';
</script>

<template>
  <scroll>
    <div class="all-container" width="100%">
      <HeadA></HeadA>
      <CarouselA class="carousel-class" />
      <SearchA />
      <SignA></SignA>
      <InputA />
      <MakePrescription></MakePrescription>
    </div>
  </scroll>
</template>

<style scoped></style>
