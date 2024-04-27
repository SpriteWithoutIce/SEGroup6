<script setup>
import CarouselA from "@/views/CarouselA.vue";
import HeadA from "@/views/HeadA.vue";
import SearchA from "@/views/SearchA.vue";
import SignA from "@/views/SignA.vue";
import InputA from "@/views/InputA.vue";
import MakePrescription from "@/components/Prescription/MakePrescription.vue";
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
