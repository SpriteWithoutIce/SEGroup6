<!-- 导航栏代码部分 -->
<template>
  <div>
    <messagedrawer ref="messageBox" class="messageBox" @update:result="getUnreadCount" />
    <Login @update:refresh="refreshPage" @update:currentUserCard="updateUserCard" @update:messagebox="updateMessagebox"
      @update:currentUserType="updateUserType" ref="Login"></Login>
    <Sign ref="Sign"> </Sign>
    <el-header class="header-nav" @click="changeBackgroundOnClick">
      <nav>
        <RouterLink to="/Main">已自动不老实</RouterLink>
        <a href="#unknown" @click="showLogin()">登录</a>
        <a @click="openMessageBox">消息</a><el-badge :value="unreadCount" class="item"
          v-if="unreadCount !== 0"></el-badge>
        <a href="#unknown" @click="showSign()">系统介绍</a>
      </nav>
      <div class="clickable-images">
        <template v-for="(image, index) in getClickableImages()">
          <!-- RouterLink里边必须加一个跳转地址 -->
          <RouterLink class="image-link" to="/Main" @mouseover="showSurroundImage(index + 1)"
            @mouseleave="hideSurroundImage()" @click.prevent="handleImageClick(image.link, $event)">
            <img class="designed-icon" :src="image.icon" :alt="image.alt" />
            <img class="Surround-image" src="../../assets/navigation/list1_bg.png" alt="Surround Image" />
          </RouterLink>
        </template>
      </div>
    </el-header>
    <RouterView />
  </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router'
// import Navbar from './Navbar.vue'
import Login from '../LogIn/Login.vue'
import Sign from '../LogIn/Sign.vue'
import BillList from '../Bills/BillList.vue'
import PatientA from '../History/PatientA.vue'
import Prescription from '../Prescription/MakePrescription.vue'
import messagedrawer from '../Message/MessageDrawer.vue'
import { GlobalState } from '../../global.js';
import VueCookies from 'vue-cookies';
export default {
  name: 'HeaderNavigation',
  data () {
    return {
      date: new Date(),
      WebURL: 'http://localhost:8080',
      currentIndex: 0,
      images: [
        '/static/img/navigation/banner1.jpg',
        '/static/img/navigation/banner2.jpg',
        '/static/img/navigation/banner3.jpg'
      ],
      unreadCount: 0,
      intervalId: null,
      currentUser: {
        userType: '',
        idCard: '',
        password: ''
      }
    }
  },
  mounted () {
    this.checkLoginStatus()
    this.intervalId = setInterval(this.updateMessagebox, 30000);
    console.log("HeaderNavigation 定时器已加载");
    this.startBackgroundRotation()
  },
  beforeDestroy () {
    this.stopBackgroundRotation()
    clearInterval(this.intervalId)
  },
  components: {
    // Navbar,
    Login,
    Sign,
    RouterLink,
    RouterView,
    messagedrawer
  },
  methods: {
    checkLoginStatus () {
      const idCard = VueCookies.get('idCard');
      console.log("HeaderNavigationcookies" + idCard);
      const userType = VueCookies.get('userType');

      if (idCard && userType) {
        GlobalState.identityNum = idCard;
        this.updateMessagebox();
        console.log("刷新后的全局身份" + GlobalState.identityNum);
        this.currentUser.userType = userType;
        this.currentUser.idCard = idCard;
      }
    },
    handleImageClick (link, event) {
      if (this.currentUser.userType === '') {
        this.showLogin()
      } else {
        this.$router.push(link)
      }
    },
    refreshPage () {
      this.currentUser.idCard = ''
      this.currentUser.userType = ''
      this.currentUser.password = ''
      console.log('HeaderNavigarion refreshPage done')
      this.$forceUpdate()
    },
    updateUserCard (id) {
      this.currentUser.idCard = id
      console.log('用户id更新完毕')
    },
    updateUserType (userType) {
      this.currentUser.userType = userType
      this.$forceUpdate()
      console.log('用户类型更新完毕')
    },
    updateMessagebox () {
      this.$refs.messageBox.getMesData();
    },
    showLogin () {
      this.$refs.Login.openModal(this.currentUser.idCard, this.currentUser.userType)
    },
    showSign () {
      this.$refs.Sign.openModal()
    },
    startBackgroundRotation () {
      this.intervalId = setInterval(this.changeBackground, 5000)
    },
    stopBackgroundRotation () {
      clearInterval(this.intervalId)
    },
    changeBackground () {
      this.currentIndex = (this.currentIndex + 1) % this.images.length
      let elements = document.getElementsByClassName('header-nav')
      for (let i = 0; i < elements.length; i++) {
        elements[i].style.transition = 'background-image 2s ease-in-out'
        elements[i].style.backgroundImage = 'url(' + this.images[this.currentIndex] + ')'
      }
    },
    changeBackgroundOnClick () {
      this.stopBackgroundRotation()
      this.changeBackground()
      this.startBackgroundRotation()
    },
    showSurroundImage (index) {
      const SurroundImage = document.querySelector(
        `.clickable-images a:nth-child(${index}) .Surround-image`
      )
      if (SurroundImage) {
        SurroundImage.style.opacity = 1
        SurroundImage.style.animation = 'spin 10s linear infinite'
      }
    },
    hideSurroundImage () {
      const SurroundImages = document.querySelectorAll('.Surround-image')
      SurroundImages.forEach((image) => {
        image.style.opacity = 0
        image.style.transform = 'rotate(0deg)'
      })
    },
    openMessageBox () {
      this.$refs.messageBox.openDrawer()
    },
    getUnreadCount (cnt) {
      this.unreadCount = cnt
      this.$emit('update:unreadCount', cnt)
    },
    getClickableImages () {
      const defaultClickHandler = () => {
        this.showLogin()
      }
      switch (this.currentUser.userType) {
        case '医生':
          return [
            { link: '/PatientA', icon: '/static/img/navigation/list1_2.png', alt: 'Image 2' },
            { link: '/PresA', icon: '/static/img/navigation/list1_5.png', alt: 'Image 5' },
            { link: '/Prescription', icon: '/static/img/navigation/list1_3.png', alt: 'Image 3' }
          ]
        case '普通用户':
          return [
            {
              link: '/AppointmentRegistration',
              icon: '/static/img/navigation/list1_1.png',
              alt: 'Image1'
            },
            { link: '/PatientA', icon: '/static/img/navigation/list1_2.png', alt: 'Image 2' },
            { link: '/PresA', icon: '/static/img/navigation/list1_5.png', alt: 'Image 5' },
            { link: '/Bill', icon: '/static/img/navigation/list1_4.png', alt: 'Image 4' }
          ]
        case '管理员':
          return [
            { link: '/PharmaCist', icon: '/static/img/navigation/信息录入.png', alt: 'Image 2' }
          ]
        default:
          return [
            {
              link: '/AppointmentRegistration',
              icon: '/static/img/navigation/list1_1.png',
              alt: 'Image1'
            },
            { link: '/PharmaCist', icon: '/static/img/navigation/信息录入.png', alt: 'Image 2' },
            { link: '/PresA', icon: '/static/img/navigation/list1_5.png', alt: 'Image 5' },
            { link: '/Bill', icon: '/static/img/navigation/list1_4.png', alt: 'Image 4' }
          ]
      }
    }
  }
}
</script>

<style>
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

.item {
  margin-top: 10px;
  margin-left: -25px;
  margin-right: 25px;
}

.header-nav {
  background-color: #333;
  color: white;
  padding: 0;
  text-align: center;
  background-image: url('../../assets/navigation/list1_1.png');
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
  animation: zoom 1.5s ease-in-out;
  position: relative;
  margin-top: 0;
}

/*添加logo 的代码*/
.header-nav::before {
  content: '';
  position: absolute;
  top: 25px;
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
  padding: 14px 8px;
  text-decoration: none;
  font-size: 17px;
  position: relative;
  width: 4em;
  text-align: center;
  font-weight: bold;
  text-shadow: 2px 2px 2px rgba(13, 65, 153, 0.941);
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

.header-nav::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 100%;
  height: 80px;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 1;
}

.header-nav nav {
  display: flex;
  z-index: 0;
}

.header-nav nav a:hover {
  color: rgb(246, 242, 242);
}

.clickable-images {
  position: absolute;
  bottom: 3px;
  left: 0;
  width: 100%;
  height: 90px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.clickable-images a {
  margin: 0 9vw;

  position: relative;
}

.image-link {
  position: relative;
}

a:hover {
  cursor: pointer;
}

.clickable-images img {
  position: absolute;
  transition: all 0.3s ease;
}

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
