<!--患者处方查询页面-->
<template>
  <DetailB ref="detail"> </DetailB>
  <div class="container">
    <div class="card-container">
      <el-card
        v-for="item in filterInfo"
        :key="item"
        style="width: 30%; min-height: 00px; margin: 1.6%"
      >
        <div class="header">
          <div class="row">
            <div class="row1">
              <p style="margin-right: 10px; font-weight: 600">门诊号</p>
              <p>{{ item.office }}</p>
            </div>
            <div style="font-size: small">
              <p>{{ item.time }}</p>
            </div>
            <div style="font-size: small">
              <p>患者：{{ item.patient }}</p>
            </div>
            <div style="font-size: small">
              <p>医生：{{ item.doctor }}</p>
            </div>
          </div>
        </div>
        <el-divider class="divider" />
        <div class="content">
          <div class="line">
            <p>诊断：</p>
            <p>{{ item.advice }}</p>
            <el-button type="primary" plain @click="showPrescriptionDetails(item)" class="xiang"
              >展开处方</el-button
            >
          </div>
        </div>
        <div class="button"></div>
      </el-card>
    </div>
    <el-footer height="30px" align="center" class="footer">SE_GROUP_6</el-footer>
  </div>
</template>
<script>
import DetailB from './DetailB.vue'
export default {
  name: 'PHistory',
  props: {
    filterInfo: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      info: []
    }
  },
  components: {
    DetailB
  },
  methods: {
    showPrescriptionDetails(item) {
      this.$refs.detail.openModal(item)
    }
  }
}
</script>
<style scoped>
.el-button.xiang {
  position: absolute;
  right: 0; /* 或者使用具体的像素值 */
  top: 50%;
  transform: translateY(-50%); /* 垂直居中 */
}
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
  position: relative;
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
