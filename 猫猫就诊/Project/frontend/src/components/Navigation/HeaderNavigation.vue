<!-- 开侧边栏比如bingAI,会由于元素缩放问题（问题在旋转动画那里）导致关停 -->
<!-- 感觉把边上那个按钮去掉吧,主要是图片不好看的原因 -->
<!-- 功能修改成点击可以切换图片，图片也会进行轮播 https://blog.csdn.net/boxuestudio/article/details/129099623-->
<template>
  <div>
    <el-header class="header-nav">
      <nav>
        <!-- 导航链接可以根据需要添加 -->
        <!-- 这是需要加路由的，路由应该放在index里边 -->
        <a href="#unknown">首页</a>
        <a href="#unknown">登录</a>
        <a href="#unknown">联系我们</a>
        <a href="#unknown">关于</a>
      </nav>
      <!-- 下边这段肯定可以简化 -->
      <!-- 改了会出bug导致的 -->
      <div class="clickable-images">
        <a href="#link1" class="image-link" @mouseover="showSurroundImage(1)" @mouseleave="hideSurroundImage()">
          <img class="designed-icon" src="../../assets/navigation/list1.1.png" alt="Image 1">
          <img class="Surround-image" src="../../assets/navigation/list1_bg.png" alt="Surround Image 1">
        </a>
        <RouterLink to="/PatientA" class="image-link" @mouseover="showSurroundImage(2)" @mouseleave="hideSurroundImage()">
          <img class="designed-icon" src="../../assets/navigation/list1.2.png" alt="Image 2">
          <img class="Surround-image" src="../../assets/navigation/list1_bg.png" alt="Surround Image 2">
        </RouterLink>
        <RouterLink to="/PatientA" class="image-link" @mouseover="showSurroundImage(3)" @mouseleave="hideSurroundImage()">
          <img class="designed-icon" src="../../assets/navigation/list1.2.png" alt="Image 2">
          <img class="Surround-image" src="../../assets/navigation/list1_bg.png" alt="Surround Image 2">
        </RouterLink>
        <RouterLink to="/Prescription" class="image-link" @mouseover="showSurroundImage(4)"
          @mouseleave="hideSurroundImage()">
          <img class="designed-icon" src="../../assets/navigation/list1.3.png" alt="Image 3">
          <img class="Surround-image" src="../../assets/navigation/list1_bg.png" alt="Surround Image 3">
        </RouterLink>
        <RouterLink to="/Bill" class="image-link" @mouseover="showSurroundImage(5)" @mouseleave="hideSurroundImage()">
          <img class="designed-icon" src="../../assets/navigation/list1.4.png" alt="Image 4">
          <img class="Surround-image" src="../../assets/navigation/list1_bg.png" alt="Surround Image 4">
        </RouterLink>
      </div>
    </el-header>
    <RouterView />
  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'
import BillList from '../Bills/BillList.vue'
import PatientA from '../History/PatientA.vue'
import Prescription from '../Prescription/MakePrescription.vue'

export default {
  name: 'HeaderNavigation',
  data () {
    return {
      WebURL: "http://localhost:8080",
      currentIndex: 0,
      images: ['/static/img/navigation/banner1.jpg', '/static/img/navigation/banner2.jpg', '/static/img/navigation/banner3.jpg'],
    };
  },
  mounted () {
    setInterval(this.changeBackground, 5000); // Change background every 5 seconds
  },
  components: {
    RouterLink,
    RouterView
  },
  methods: {
    changeBackground () {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
      let elements = document.getElementsByClassName('header-nav');
      for (let i = 0; i < elements.length; i++) {
        elements[i].style.transition = 'background-image 2s ease-in-out';
        elements[i].style.backgroundImage = 'url(' + this.images[this.currentIndex] + ')';
      }
    },
    showSurroundImage (index) {
      const SurroundImage = document.querySelector(`.clickable-images a:nth-child(${index}) .Surround-image`);
      if (SurroundImage) {
        SurroundImage.style.opacity = 1;
        SurroundImage.style.animation = 'spin 10s linear infinite';
      }
    },
    hideSurroundImage () {
      const SurroundImages = document.querySelectorAll('.Surround-image');
      SurroundImages.forEach(image => {
        image.style.opacity = 0;
        image.style.transform = 'rotate(0deg)';
      });
    },

    /*下边的代码都是想实现图片轮播*/
  },
}
</script>

<style>
/* 进行图片缩放的代码 非常奇怪，不知道哪里跳错了，没弄错参数，问题是开了侧边栏，需要网页全屏才能看的清楚*/
@keyframes zoom {
  0% {
    background-size: 105%;
  }

  100% {
    background-size: 100%;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.header-nav {
  background-color: #333;
  color: white;
  padding: 0;
  text-align: center;
  background-image: url('../../assets/navigation/banner1.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  min-height: 390px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  align-items: flex-start;
  padding-right: 0px;
  animation: zoom 2s ease-in-out;
  position: relative;
  margin-top: 0;
}

/*添加logo 的代码*/
.header-nav::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 30px;
  width: 300px;
  height: 150px;
  background-image: url('../../assets/navigation/logo.png');
  background-size: cover;
  background-repeat: no-repeat;
  /*图层拉高，否则会被after影响到*/
  z-index: 5;
}

.header-nav nav {
  display: flex;
  z-index: 1;
}

/*控制边角导航栏选项的*/
.header-nav nav a {
  color: white;
  padding: 14px 20px;
  text-decoration: none;
  font-size: 17px;
  position: relative;
  width: 4em;
  text-align: center;
}

/*导航栏蓝色下划线代码*/
.header-nav nav a::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  height: 2px;
  width: 100%;
  background-color: rgba(13, 65, 153, 0.941);
  transform: translateX(-50%) scaleX(0);
  transition: transform 0.3s;
}

.header-nav nav a:hover::after {
  transform: translateX(-50%) scaleX(0.5);
}

/*灰色透明区域 并不适合覆盖顶部选项*/
.header-nav::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 100%;
  height: 80px;
  /* 设置灰色透明矩形区域的高度 */
  background-color: rgba(255, 255, 255, 0.7);
  /* 设置灰色透明 */
  z-index: 1;
  /* 确保在导航链接之上 */
}

.header-nav nav {
  display: flex;
  z-index: 0;
}

.header-nav nav a:hover {
  color: rgb(246, 242, 242);
}

/*注意底部灰色阴影的图层是1*/
.clickable-images {
  position: absolute;
  bottom: 3px;
  left: 0;
  width: 100%;
  height: 90px;
  /* 与灰色透明矩形区域高度相同 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

/*调整灰色矩形内可点击元素距离*/
.clickable-images a {
  margin: 0 95px;

  position: relative;
}

.image-link {
  position: relative;
}

/*非常困惑的一点就是clickable里边设置过的元素，在子类元素里边再设置会被无视，好反常识？？？*/
.clickable-images img {
  /*width: 30px;
  height: 30px;
  */
  position: absolute;
  transition: all 0.3s ease;
}

/*父类是clickable images 所以找着那个来定位*/
/*下边两个是并列等级的设置*/
.Surround-image {
  opacity: 0;
  position: absolute;
  width: 80px;
  height: 80px;
  top: -30px;
  left: -17.5px;
  z-index: 2;
}

.designed-icon {
  width: 60px;
  height: 60px;
  position: absolute;
  top: -20px;
  left: -10px;
  z-index: 4;
}
</style>