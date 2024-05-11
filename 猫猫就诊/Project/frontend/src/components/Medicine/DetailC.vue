<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="content">
        <h3>就诊信息</h3>
        <div class="line">
          <p style="margin-left: 15px">就诊科室：</p>
          <p>hello</p>
        </div>
      </div>
      <div class="button">
        <el-button @click="closeModal">退出</el-button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'DetailC',
  data() {
    return {
      isVisible: false
    }
  },
  methods: {
    openModal(row) {
      this.isVisible = true
      document.body.style.overflow = 'hidden' // 禁止滚动
    },
    closeModal() {
      this.isVisible = false
      document.body.style.overflow = '' // 恢复滚动
    }
  }
}
</script>
<style scoped>
.el-button {
  height: 40px;
}
h3 {
  line-height: 0.1; /* 降低行高，根据需要调整该值 */
  margin-left: 15px;
}
.content {
  margin-top: 10px;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  justify-content: center;
}
.line {
  display: flex;
  flex-direction: row;
}
.button {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
p {
  line-height: 0.1; /* 降低行高，根据需要调整该值 */
}
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
  max-width: 500px; /* 设置最大宽度为800像素 */
  width: 100%;
  background-color: #fff;
  border-radius: 5px;
  display: flex; /* 使用Flexbox布局 */
  flex-direction: column; /* 设置为垂直方向的布局 */
  justify-content: center; /* 垂直居中所有子元素 */
  align-items: center;
}
</style>
