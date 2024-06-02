<template>
  <DetailA ref="detail"> </DetailA>
  <div class="container">
    <div class="card-container">
      <el-card
        v-for="item in filterInfo"
        :key="item"
        style="width: 30%; min-height: 400px; margin: 1.6%"
      >
        <div class="header">
          <el-avatar :size="50" :src="circleUrl" />
          <div class="row">
            <div class="row1">
              <p style="font-size: larger; margin-right: 10px; font-weight: 600">门诊号</p>
              <p>{{ item.office }}</p>
            </div>
            <div class="row2">
              <p>猫猫就诊医院</p>
            </div>
          </div>
          <p style="color: darkblue; margin-left: 60px">{{ item.state }}</p>
        </div>
        <el-divider class="divider" />
        <div class="content">
          <div class="line">
            <p>订单号：</p>
            <p>{{ item.orderNum }}</p>
          </div>
          <div class="line">
            <p>费用：</p>
            <p>{{ item.price }}</p>
          </div>
          <div class="line">
            <p>就诊人：</p>
            <p>{{ item.name }}</p>
          </div>
          <div class="line">
            <p>电子就医卡号：</p>
            <p>{{ item.cardNum }}</p>
          </div>
          <div class="line">
            <p>科室地址：</p>
            <p>{{ item.position }}</p>
          </div>
          <div class="line">
            <p>预约时间：</p>
            <p>{{ item.time }}</p>
          </div>
          <div class="line">
            <p>排队号：</p>
            <p>{{ item.line }}</p>
          </div>
        </div>
        <div class="neirong">
          <el-icon class="jinggao"><Warning /></el-icon>
          <p>&nbsp;实际就诊时间以医院安排为准！</p>
        </div>
        <el-divider class="divider" />
        <div class="button">
          <el-button type="primary" plain @click="showPrescriptionDetails(item)" class="xiang"
            >显示详情</el-button
          >
          <el-button type="primary" plain v-if="item.state === '已预约'" @click="cancel(item)"
            >取消挂号</el-button
          >
        </div>
      </el-card>
    </div>
    <el-footer height="30px" align="center" class="footer">SE_GROUP_6</el-footer>
  </div>
</template>
<script>
import DetailA from './DetailA.vue'
import { ElMessage } from "element-plus"

export default {
  name: 'HistoryA',
  props: {
    filterInfo: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    }
  },
  components: {
    DetailA
  },
  methods: {
    showPrescriptionDetails(item) {
      this.$refs.detail.openModal(item)
    },
    cancelRegister(item) {
      return new Promise((resolve, reject) => {
        let ts = this
        let requestData = {
          action: 'cancelRegister',
          id: item.id
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
    cancel(item) {
      this.cancelRegister(item).then(() => {
        ElMessage({
          type: 'info',
          message: '取消挂号成功 ╮(╯▽╰)╭',
          showClose: true
        })
      })
    }
  }
}
</script>
<style scoped>
.neirong {
  display: flex;
  flex-direction: row;
  align-items: center;
  color: red;
}
.button {
  display: flex;
  justify-content: flex-end;
}
.container {
  position: absolute;
  top: 630px;
  width: 100%;
  min-height: 50vh;
  background-color: white;
}
.header {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.row1 {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.row {
  max-height: 100%;
  display: flex;
  flex-direction: column;
}
p {
  line-height: 0.1; /* 降低行高，根据需要调整该值 */
}
.content {
  display: flex;
  flex-direction: column;
}
.line {
  display: flex;
  flex-direction: row;
}
.el-avatar {
  margin-right: 10px;
}
.card-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
}
.footer {
  position: relative;
  width: 100%;
  background-color: rgb(8, 3, 88);
  color: white;
  font-size: 17px;
  line-height: 30px;
  margin-top: 10px;
}
</style>
