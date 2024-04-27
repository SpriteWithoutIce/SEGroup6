<template>
  <div class="carousel-container">
    <el-carousel indicator-position="outside" autoplay="false" interval="0">
      <el-carousel-item class="img1"> </el-carousel-item>
      <el-carousel-item class="img2"> </el-carousel-item>
      <el-carousel-item class="img3"> </el-carousel-item>
      <el-carousel-item class="img4"> </el-carousel-item>
    </el-carousel>
  </div>
</template>
<script></script>
<style>
.carousel-container {
  position: absolute;
  top: 90px;
  left: 0;
  width: 100%;
  min-height: 400px;
}
.el-carousel__item {
  width: 100%;
  min-height: 400px;
}
.el-carousel__item p {
  font-size: 28px;
  color: rgb(58, 57, 57);
  opacity: 0.75;
  min-height: 400px;
}
.img1 {
  width: 100%;
  background-image: url("../utils/5.jpg");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
}
.img2 {
  width: 100%;
  background-image: url("../utils/6.jpg");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
}
.img3 {
  width: 100%;
  background-image: url("../utils/7.jpg");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
}
.img4 {
  width: 100%;
  background-image: url("../utils/8.jpg");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
}
</style>
