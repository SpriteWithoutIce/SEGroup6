<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="content">
        <h3>处方明细</h3>
        <div v-for="item in form.medicine" :index="item" class="card">
          <p style="margin-left: 15px">{{ item.name }}</p>
          <p style="font-size: smaller; margin-left: 15px">单价：{{ item.price }}</p>
          <el-divider class="divider" />
          <div class="line">
            <p style="margin-left: 15px">疗程：</p>
            <p>{{ item.times }}</p>
          </div>
          <div class="line">
            <p style="margin-left: 15px">数量：</p>
            <p>{{ item.cnt }}</p>
          </div>
          <div class="m"></div>
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
  name: 'DetailB',
  data() {
    return {
      isVisible: false,
      form: {
        office: '',
        time: '',
        patient: '',
        doctor: '',
        medicine: [{ name: '金莲花软件囊', times: 3, cnt: 1, price: '' }]
      }
    }
  },
  methods: {
    openModal(item) {
      this.isVisible = true
      document.body.style.overflow = 'hidden' // 禁止滚动
      this.form.office = item.office
      this.form.time = item.time
      this.form.doctor = item.doctor
      this.form.patient = item.patient
      this.form.medicine = item.medicine
    },
    closeModal() {
      this.isVisible = false
      document.body.style.overflow = '' // 恢复滚动
    }
  }
}
</script>
<style scoped>
.divider {
  margin: 10px 0;
  width: 92%;
  transform: translateX(-50%);
  left: 50%;
}
.card {
  width: 100%;
}
.m {
  background-color: rgb(228, 228, 228);
  width: 100%;
  height: 5px;
  margin-top: 12px;
  margin-bottom: 12px;
}
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
  width: 100%;
  flex-direction: row;
}
.button {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
p {
  line-height: 1.6; /* 调整行间距 */
  margin: 0; /* 移除默认的外边距 */
}
.head {
  background-color: blue;
  height: 80px;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 5px;
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
  overflow-y: auto;
  max-height: 400px;
  max-width: 500px; /* 设置最大宽度为800像素 */
  width: 100%;
  background-color: #fff;
  border-radius: 5px;
  display: flex; /* 使用Flexbox布局 */
  flex-direction: column; /* 设置为垂直方向的布局 */
  justify-content: flex-start; /* 垂直居中所有子元素 */
  align-items: center;
}
</style>
