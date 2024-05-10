<!--患者的历史查询页面-->
<script setup>
import CarouselA from './CarouselA.vue';
import HeadA from './HeadA.vue';
import SearchA from './SearchA.vue';
import SignA from './SignA.vue';
import InputA from './InputA.vue';
import PHistory from './PHistory.vue';
</script>

<template>
  <div class="container">
    <scroll>
      <div class="all-container" width="100%">
        <div class="search-container">
            <div class="wenzi">
                <p class="guahao">处方查询</p>
                <p class="back">首页 > 处方查询</p>
        </div>
        <el-divider class="divider" />
     </div>
        <SignA></SignA>
        <InputA />
        <PHistory></PHistory>
      </div>
    </scroll>
  </div>
</template>

<style scoped>
.wenzi {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row; /* 将组件横向排列 */
  align-items: center;
}
.guahao {
  position: absolute;
  font-size: 25px;
  left: 50%;
  transform: translateX(-50%);
}
p {
  color: #e9c874;
}
.back {
  font-size: 15px;
  position: absolute;
  left: 80%;
}
p {
  font-weight: bold;
}
.divider {
  position: absolute;
  width: 50%;
  left: 25%;
  top: 55%;
}
.search-container {
  position: absolute;
  top: 400px;
  height: 90px;
  width: 800px;
  background-color: white;
  box-shadow: 0 4px 8px rgb(212, 206, 206);
  border-radius: 35px;
  transform: translateX(-50%);
  left: 50%;
}
.container{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
