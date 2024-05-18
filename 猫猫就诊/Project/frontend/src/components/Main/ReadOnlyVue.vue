<template>
  <el-container style="height: 88vh;">
    <div class="flowing-background"></div>
    <!-- <img src='../../assets/main/divider.jpg' class="divider"> -->
    <el-header class="Header">
      <img src='../../assets/main/readOnlybg.jpg' class="bg">
      <!-- <img src='../../assets/main/title.png' class="title"> -->
      <img src='../../assets/main/subtitle.png' class="subtitle">
      <img src='../../assets/main/logo.png' class="logo" alt="Logo">
      <div class="zqssquare1"></div>
      <div class="zqssquare2"></div>
      <div class="zqssquare3"></div>
      <div class="zqssquare4"></div>
    </el-header>
  </el-container>
  <el-footer height="30px" align="center" class="footer">SE_GROUP_6</el-footer>
</template>

<style>
/*也就是说卡顿被我调整成了100s*一次，消除卡顿需要对高度px进行调整*/
  .flowing-background {
    width: 100%;
    height: 8vh; 
    background-image: url('../../assets/main/divider.jpg');
    background-repeat: repeat-y; 
    background-size: cover; 
    animation: flow 100s linear infinite;
  }
  @keyframes flow {
    0% {
      background-position: 0 0; /* 初始位置 */
    }
    100% {
      background-position: 0 -100vh; /* 向上移动100vh */
    }
  }
  @keyframes rotate {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  .divider{
    width:100%;
  }
  .Header{
    position:relative;
    height:100vh;
  }
  .logo {
    opacity: 0.5;
    position: relative;
    width: 440px;
    height: 440px;
    top: 80px;
    left: 150px;
    z-index: 2;
    animation: rotate 50s linear infinite; 
  }
  .title{
    position: absolute;
    opacity:1;
    z-index:3;
    top:0px;
    left:60px;
    width:260px;
  }
  .subtitle{
    position: absolute;
    opacity:1;
    z-index:3;
    top:0px;
    right:220px;
    width:180px;
  }
  .bg{
    position: absolute;
    top: 0;
    left: 0;
    background-color: #333;
    color: white;
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0.4;
    width: 100%;
    height: 650px;
  }
  .zqssquare1, .zqssquare2, .zqssquare3, .zqssquare4 {
    border-radius: 5px; /* 添加圆角框 */
    position: absolute;
    width: 230px;
    height: 230px;
    transition: transform 1.5s ease; /* 添加过渡效果 */
  }

  .zqssquare1 {
    top: 80px;
    right: 330px;
    background-image: url('../../assets/main/1.jpg'); /* 默认背景图片 */
  }

  .zqssquare2 {
    top: 80px;
    right: 80px;
    background-image: url('../../assets/main/2.jpg');
  }

  .zqssquare3 {
    top: 330px;
    right: 330px;
    background-image: url('../../assets/main/3.jpg'); /* 默认背景图片 */
  }

  .zqssquare4 {
    top: 330px;
    right: 80px;
    background-image: url('../../assets/main/4.jpg'); /* 默认背景图片 */
  }

  .zqssquare1:hover,
  .zqssquare2:hover,
  .zqssquare3:hover,
  .zqssquare4:hover {
    transform: scale(1.1); /* 悬停时放大 */
  }

  .zqssquare1:hover::before,
  .zqssquare2:hover::before,
  .zqssquare3:hover::before,
  .zqssquare4:hover::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.5); /* 半透明白色遮罩 */
    transition: background-image 0.8s ease; /* 添加过渡效果 */
    z-index: 1;
  }

  .zqssquare1:hover::before {
    background-image: url('../../../static/img/main/change1.png'); /* 悬停时的背景图片 */
  }
  .zqssquare2:hover::before {
    background-image: url('../../../static/img/main/change2.png'); /* 悬停时的背景图片 */
  }
  .zqssquare3:hover::before {
    background-image: url('../../../static/img/main/change3.png'); /* 悬停时的背景图片 */
  }
  .zqssquare4:hover::before {
    background-image: url('../../../static/img/main/change4.png'); /* 悬停时的背景图片 */
  }
  .footer {
    position: relative;
    background-color: rgb(8, 3, 88);
    color: white;
    font-size: 17px;
    line-height: 30px;
  
  }
</style>
