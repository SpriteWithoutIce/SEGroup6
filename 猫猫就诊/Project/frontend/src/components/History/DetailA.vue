<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="head">
        <p style="margin-left: 15px; font-size: larger; color: white">{{ form.state }}</p>
        <p v-if="form.state === '已预约'" style="margin-left: 15px; font-size: small; color: white">
          请在约定时间前往就诊
        </p>
      </div>
      <div class="content">
        <h3>就诊信息</h3>
        <div class="line">
          <p style="margin-left: 15px">就诊科室：</p>
          <p>{{ form.office }}</p>
        </div>
        <div class="line">
          <p style="margin-left: 15px">科室地址：</p>
          <p>{{ form.position }}</p>
        </div>
        <div class="line">
          <p style="margin-left: 15px">医生：</p>
          <p>{{ form.doctor }}</p>
        </div>
        <div class="line">
          <p style="margin-left: 15px">预约时间：</p>
          <p>{{ form.time }}</p>
        </div>
        <div class="y">
          <el-icon class="w"><Bell /></el-icon>
          <p class="w">就诊时间以医生实际看诊叫号顺序为准</p>
        </div>
        <div class="line">
          <p style="margin-left: 15px">排队号：</p>
          <p>{{ form.line }}</p>
        </div>
        <div class="line">
          <p style="margin-left: 15px">就诊人：</p>
          <p>{{ form.name }}</p>
        </div>
        <div class="line">
          <p style="margin-left: 15px">电子就医卡号：</p>
          <p>{{ form.cardNum }}</p>
        </div>
      </div>
      <div class="m"></div>
      <div class="content">
        <h3>订单信息</h3>
        <div class="line">
          <p style="margin-left: 15px">订单号：</p>
          <p>{{ form.orderNum }}</p>
        </div>
        <div class="line">
          <p style="margin-left: 15px">费用：</p>
          <p>现场待支付医事服务费{{ form.price }}</p>
        </div>
      </div>
      <div class="button">
        <el-button v-if="form.state === '已预约'" @click="cancelModal">取消挂号</el-button>
      </div>
      <div class="button">
        <el-button @click="closeModal">退出</el-button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import { ElMessage } from 'element-plus'
export default {
  name: 'DetailA',
  data() {
    return {
      isVisible: false,
      form: {
        id: '',
        office: '',
        orderNum: '',
        price: '',
        name: '',
        cardNum: '',
        position: '',
        time: '',
        line: '',
        state: '',
        doctor: ''
      }
    }
  },
  methods: {
    cancelRegister() {
      return new Promise((resolve, reject) => {
        let ts = this
        let requestData = {
          action: 'cancelRegister',
          id: this.form.id
        }
        this.$axios
          .post('/api/registers/cancel/', requestData)
          .then(function (response) {
            console.log(response.data['msg'])
            resolve() // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error)
            reject(error) // 数据获取失败，reject Promise
          })
      })
    },
    openModal(item) {
      this.isVisible = true
      document.body.style.overflow = 'hidden' // 禁止滚动
      this.form.id = item.id //传入id对预约进行标识
      this.form.office = item.office
      this.form.orderNum = item.orderNum
      this.form.price = item.price
      this.form.name = item.name
      this.form.cardNum = item.cardNum
      this.form.line = item.line
      this.form.position = item.position
      this.form.time = item.time
      this.form.state = item.state
      this.form.doctor = item.doctor
    },
    closeModal() {
      this.isVisible = false
      document.body.style.overflow = '' // 恢复滚动
    },
    cancelModal() {
      this.cancelRegister().then(() => {
        ElMessage({
          type: 'info',
          message: '取消挂号成功 ╮(╯▽╰)╭',
          showClose: true
        })
        // 关闭弹窗
        this.closeModal()
      })
    }
  }
}
</script>
<style scoped>
.w {
  color: rgb(252, 191, 50);
}
.y {
  position: relative;
  background-color: rgb(244, 244, 194);
  width: 90%;
  height: 30px;
  transform: translateX(-50%);
  left: 50%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.m {
  background-color: rgb(228, 228, 228);
  width: 100%;
  height: 5px;
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
