<script setup></script>

<template>
  <div class="sign-container">
    <div class="neirong">
      <el-icon class="jinggao"><Warning /></el-icon>
      <p>详细信息以医院出具的单据为准！</p>
    </div>
  </div>
</template>

<style scoped>
.neirong {
  position: relative;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.jinggao {
  position: absolute;
  left: 15%;
  color: red;
}
p {
  position: absolute;
  left: 25%;
  color: red;
}
.sign-container {
  position: absolute;
  top: 510px;
  height: 35px;
  width: 400px;
  background-color: rgb(232, 232, 238);
  border-radius: 35px;
  left: 50%;
  transform: translateX(-50%);
}
</style>
