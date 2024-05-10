<!--患者的历史查询页面-->
<script setup>
import CarouselA from './CarouselA.vue';
import HeadA from './HeadA.vue';
import SearchA from './SearchA.vue';
import SignA from './SignA.vue';
import InputA from './InputA.vue';
import HistoryA from './HistoryA.vue';
</script>

<template>
  <div class="container">
    <scroll>
      <div class="all-container" width="100%">
        <SearchA></SearchA>
        <SignA></SignA>
        <InputA />
        <HistoryA></HistoryA>
      </div>
    </scroll>
  </div>
</template>

<style scoped>
.container{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
