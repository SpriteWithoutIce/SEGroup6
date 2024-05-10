<script setup></script>

<template>
  <div class="search-container">
    <div class="wenzi">
      <p class="guahao">挂号查询</p>
      <p class="back">首页 > 挂号查询</p>
    </div>
    <el-divider class="divider" />
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
</style>
