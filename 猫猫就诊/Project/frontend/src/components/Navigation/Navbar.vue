<template>
  <div class="navbar" :class="{ sticky: isSticky }">
    <messagedrawer ref="messageBox" class="messageBox" />
    <RouterLink to="/Main" @click="returnTop" class="white-bold">首页</RouterLink>
    <a href="#" class="white-bold">登录</a>
    <a class="white-bold" @click="openMessageBox">消息</a>
    <a @click="returnTop" class="white-bold">回到顶部</a>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import messagedrawer from '../Message/MessageDrawer.vue'

export default {
  name: 'NavBar',
  setup () {
    const isSticky = ref(false)

    const checkScroll = () => {
      isSticky.value = window.scrollY > 200
    }

    onMounted(() => {
      window.addEventListener('scroll', checkScroll)
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', checkScroll)
    })

    return { isSticky }
  },
  components: {
    messagedrawer
  },
  methods: {
    returnTop () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    },
    openMessageBox () {
      this.$refs.messageBox.openDrawer()
    }
  }
}
</script>

<style scoped>
.navbar {
  width: 100%;
  height: 70px;
  transition: all 0.2s;
  opacity: 0;
  background-color: #78291e;
  /* 设置背景色为深蓝色 */
}

.navbar.sticky::before {
  content: '';
  position: absolute;
  top: -14px;
  left: 40px;
  width: 210px;
  height: 105px;
  background-image: url('../../assets/navigation/logo.png');
  background-size: cover;
  background-repeat: no-repeat;
  z-index: 6;
  visibility: visible;
}

@media (max-width: 700px) {
  .navbar.sticky::before {
    visibility: hidden;
  }
}

.navbar.sticky {
  text-align: right;
  color: white;
  position: fixed;
  top: 0;
  opacity: 1;
  z-index: 5;
}

.white-bold {
  text-decoration: none;
  position: relative;
  top: 21px;
  right: 20px;
  font-size: 17px;
  font-weight: bold;
  color: white;
  padding: 14px 20px;
  width: 4em;
  /* 调整文本之间的间距 */
}

.white-bold::after {
  content: '';
  position: absolute;
  top: 40px;
  left: 50%;
  bottom: 0;
  height: 3px;
  width: 130%;
  background-color: rgba(13, 65, 153, 0.941);
  transform: translateX(-50%) scaleX(0);
  transition: transform 0.3s;
}

.white-bold:hover::after {
  transform: translateX(-50%) scaleX(0.5);
}
</style>
