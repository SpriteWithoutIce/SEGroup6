<!--药物录入细节-->
<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="content">
        <h3>录入医生</h3>
        <div class="line">
          <p style="margin-left: 15px">姓名：</p>
          <el-input
            v-model="info.name"
            style="width: 240px"
            placeholder="请输入医生姓名"
            clearable
          />
        </div>
        <div class="line">
          <p style="margin-left: 15px">科室：</p>
          <el-input
            v-model="info.office"
            style="width: 240px"
            placeholder="请输入工作科室"
            clearable
          />
        </div>
        <div class="line">
          <p style="margin-left: 15px">职称：</p>
          <el-input v-model="info.title" style="width: 240px" placeholder="请输入职称" clearable />
        </div>
        <div class="line">
          <p style="margin-left: 15px">出诊费：</p>
          <el-input
            v-model="info.cost"
            style="width: 240px"
            placeholder="请输入单次出诊费"
            clearable
          />
        </div>
        <div class="line">
          <p style="margin-left: 15px">主要研究方向：</p>
          <el-input
            v-model="info.research"
            style="width: 240px"
            placeholder="用逗号分隔(例如：病理学，生物医学)"
            type="textarea"
            clearable
          />
        </div>
      </div>
      <div class="button">
        <el-button @click="closeModal" plain>取消</el-button>
        <el-button @click="setDataAndCloseModal" type="primary">确定</el-button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import { ref } from 'vue'
export default {
  name: 'DetailC',
  data() {
    return {
      fileList: [],
      isVisible: false,
      sign: '',
      inputName: '',
      radio: '',
      info: [
        //医生的信息
        {
          name: '',
          office: '',
          title: '',
          cost: '',
          research: ''
        }
      ]
    }
  },
  methods: {
    setDoctorData() {
      return new Promise((resolve, reject) => {
        let ts = this
        let requestData = {
          name: this.info.name,
          department: this.info.office,
          title: this.info.title,
          cost: this.info.cost,
          research: this.info.research,
          action: this.sign == 'add' ? 'addDoctor' : 'alterDoctor'
        }
        this.$axios
          .post('/api/doctor/setData/', requestData)
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
    openModal(row, sign) {
      this.isVisible = true
      document.body.style.overflow = 'hidden' // 禁止滚动
      this.info.name = row.name
      this.info.office = row.office
      this.info.title = row.title
      this.info.cost = row.cost
      this.info.research = row.research
      this.sign = sign
      this.fileList = []
      console.log(`传入的sign是：${this.sign}`)
    },
    closeModal() {
      this.isVisible = false
      document.body.style.overflow = '' // 恢复滚动
      this.$emit('updateData') // 触发自定义事件
    },
    setDataAndCloseModal() {
      this.setDoctorData().then(() => {
        this.isVisible = false
        document.body.style.overflow = '' // 恢复滚动
        this.$emit('updateData') // 触发自定义事件
      })
    }
  }
}
</script>

<style scoped>
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
  margin-left: 15px;
  margin-top: 10px;
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
<style scoped>
.upload {
  position: relative;
  display: flex;
  flex-direction: column;
  margin-left: 15px;
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
  margin-top: 10px;
}
.button {
  width: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-bottom: 15px;
  margin-top: 20px;
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
