<!--患者的历史查询页面-->
<script setup>
import CarouselA from './CarouselA.vue';
import HeadA from './HeadA.vue';
import SearchA from './SearchA.vue';
import SignA from './SignA.vue';
import InputA from './InputA.vue';
import CheckHistory from './CheckHistory.vue';
import HistoryA from './HistoryA.vue';
</script>

<template>
  <scroll>
    <div class="all-container" width="100%">
      <HeadA></HeadA>
      <CarouselA/>
      <SearchA></SearchA>
      <SignA></SignA>
      <InputA />
      <HistoryA></HistoryA>
    </div>
  </scroll>
</template>

<style scoped></style>
