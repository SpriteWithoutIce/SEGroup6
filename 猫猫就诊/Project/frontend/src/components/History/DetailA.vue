<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <h2>处方信息</h2>
      <el-button @click="closeModal">退出</el-button>
    </div>
  </div>
</template>
<script>
export default{
  name: 'DetailA',
  data(){
    return{
      isVisible:false,
    }
  },
  methods:{
    openModal () {
      this.isVisible = true;
      document.body.style.overflow = 'hidden'; // 禁止滚动
    },
    closeModal () {
      this.isVisible = false;
      document.body.style.overflow = ''; // 恢复滚动
    },
  }
}

</script>
<style scoped>
.modal-background {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 8;
}
.modal-container {
  max-width: 400px; /* 设置最大宽度为800像素 */
  width: 100%; 
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  display: flex; /* 使用Flexbox布局 */
  flex-direction: column; /* 设置为垂直方向的布局 */
  justify-content: center; /* 垂直居中所有子元素 */
}
</style>
