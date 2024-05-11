<template>
  <div>
    <el-header class="readOnlybg">
      <img src='../../assets/main/logo.png' class="logo" alt="Logo">
      <img src='../../assets/main/1.jpg' class="square1">
      <img src='../../assets/main/2.jpg' class="square2">
      <img src='../../assets/main/3.jpg' class="square3">
      <img src='../../assets/main/4.jpg' class="square4">
    </el-header>
  </div>
</template>
<style>
@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
.logo {
  opacity: 1;
  position: absolute;
  width: 600px;
  height: 600px;
  top: 40px;
  left: 140px;
  z-index: 2;
  animation: rotate 10s linear infinite; 
}
.readOnlybg {
  background-color: #333;
  color: white;
  background-image: url('../../assets/main/readOnlybg.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  opacity: 0.6;
  min-height: 690px;
  animation: zoom 2s ease-in-out;
  position: relative;
}
.square1
{
  position: absolute;
  width:200px;
  height:200px;
  top:150px;
  right:300px;
}
.square2
{
  position: absolute;
  width:200px;
  height:200px;
  top:150px;
  right:80px;
}
.square3
{
  position: absolute;
  width:200px;
  height:200px;
  top:370px;
  right:300px;
}
.square4
{
  position: absolute;
  width:200px;
  height:200px;
  top:370px;
  right:80px;
}
</style>