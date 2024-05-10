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
.img1 {
  width: 100%;
  background-image: url("@/utils/1.jpg");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}
.img2 {
  width: 100%;
  background-image: url("@/utils/2.jpg");
  background-position: bottom;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
}
.img3 {
  width: 100%;
  background-image: url("@/utils/3.jpg");
  background-position: 0% 90%;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
}
.img4 {
  width: 100%;
  background-image: url("@/utils/4.jpg");
  background-position: 0% 90%;
  background-size: cover;
  background-repeat: no-repeat;
  display: flex;
}
</style>
