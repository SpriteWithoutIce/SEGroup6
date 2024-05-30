<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="content">
        <h1>系统介绍</h1>
        <h3>一.预约挂号</h3>
        <div class="line">
          <p style="margin-left: 15px">
            本系统提供医生的查询，方便用户看本诊所总共有哪些医生。用户能够在挂号页面选择想要的科室、医生和时间段进行挂号预约，每天凌晨00:00放号，可以进行复诊操作。
          </p>
        </div>
        <h3>二.处方开具</h3>
        <div class="line">
          <p style="margin-left: 15px">
            医生可以根据患者的症状开具对应的处方。开具处方的时候医生要能够根据症状或者名字查询药物。同时每个药物应该有价格，医生开具处方后要能自动结算价格。
          </p>
        </div>
        <h3>三.历史记录查询</h3>
        <div class="line">
          <p style="margin-left: 15px">
            患者能查询自己的挂号和问诊记录，得到挂号信息和处方单子。医生能够查询自己名下挂号的患者，和自己开具的单子。
          </p>
        </div>
        <h3>四.药物登记&医生登记</h3>
        <div class="line">
          <p style="margin-left: 15px">
            药剂师可以把药物和医生录入到后端系统，药物信息包含：名字，种类，适应症状和价格等等。
          </p>
        </div>
        <h3>五.通知系统</h3>
        <div class="line">
          <p style="margin-left: 15px">
            患者能够收到一些特定的通知，如预约成功，预约被取消了，一定时间内没缴费会发缴费等通知。
          </p>
        </div>
        <h3>六.缴费系统</h3>
        <div class="line">
          <p style="margin-left: 15px">患者能够通过该系统缴纳医疗费用。</p>
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
  data() {
    return {
      isVisible: false
    }
  },
  methods: {
    openModal(item) {
      this.isVisible = true
      document.body.style.overflow = 'hidden' // 禁止滚动
      this.form.office = item.office
      this.form.time = item.time
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
.h1 {
  position: relative;
  text-align: center;
  margin-left: 20px;
}
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
  width: 90%;
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
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 8;
}
.modal-container {
  overflow-y: auto;
  max-height: 500px;
  max-width: 700px; /* 设置最大宽度为800像素 */
  width: 100%;
  background-image: url('../../utils/blue.jpg');
  opacity: 0.8;
  border-radius: 5px;
  display: flex; /* 使用Flexbox布局 */
  flex-direction: column; /* 设置为垂直方向的布局 */
  justify-content: flex-start; /* 垂直居中所有子元素 */
  align-items: center;
}
</style>
