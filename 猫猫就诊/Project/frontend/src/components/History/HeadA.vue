<script setup></script>

<template>
  <div class="head-container">
    <div class="logo"></div>
    <el-button color="#DBA979" :dark="isDark" plain class="loginButton"
      >登录</el-button
    >
    <el-button color="#DBA979" :dark="isDark" plain class="signButton"
      >注册</el-button
    >
  </div>
</template>

<style scoped>
.logo {
  background-image: url("@/utils/logo.png");
  background-repeat: no-repeat;
  background-size: cover;
  height: 100px;
  width: 200px;
  margin-left: 20px;
}
.loginButton {
  margin-left: 1000px;
}
.head-container {
  display: flex;
  align-items: center; /* 垂直居中 */
  position: absolute;
  top: 0;
  left: 0;
  max-height: 90px;
  width: 100%;
  background-color: white;
}
</style>
