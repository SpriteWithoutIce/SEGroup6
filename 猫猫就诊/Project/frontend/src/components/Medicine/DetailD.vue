<!--医生录入细节-->
<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="content">
        <h3>录入医生</h3>
        <div class="upload">
          <p style="margin-bottom: 20px; font-size: 14px; font-weight: 500; color: grey">
            点击导入本地医生照片
          </p>
          <el-upload
            v-model:file-list="fileList"
            class="upload-demo"
            action="/api/doctors/uploadAvatar/"
            :before-upload="handleBeforeUpload"
            :on-success="handleSuccess"
            :on-preview="handlePreview"
            :before-remove="handleBeforeRemove"
            :on-remove="handleRemove"
            list-type="picture"
          >
            <el-button type="primary">Click to upload</el-button>
            <template #tip>
              <div class="el-upload__tip">jpg/png files with a size less than 500kb</div>
            </template>
          </el-upload>
        </div>

        <el-divider />
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
          <p style="margin-left: 15px">医生编号：</p>
          <el-input v-model="info.id" style="width: 240px" placeholder="请输入医生编号" clearable />
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
          id: '',
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
          id: this.info.id,
          department: this.info.office,
          title: this.info.title,
          cost: this.info.cost,
          research: this.info.research,
          avatar_name: this.fileList.length === 0 ? '' : this.fileList[0].name,
          action: this.sign == 'add' ? 'addDoctor' : 'alterDoctor'
        }
        this.$axios
          .post('/api/doctors/setData/', requestData)
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
    removePhoto() {
      return new Promise((resolve, reject) => {
        axios
          .post('/api/doctors/removeAvatar/', {
            id: this.info.id,
            avatar_name: this.fileList[0].name,
            action: 'removeAvatar'
          })
          .then((response) => {
            console.log('删除成功:', response.data)
            resolve()
          })
          .catch((error) => {
            console.error('删除失败:', error)
            reject(error)
          })
      })
    },
    handleBeforeUpload(file) {
      if (this.fileList.length === 0) {
        file.formData = { id: this.info.id }
        return true
      } else {
        this.removePhoto().then(() => {
          file.formData = { id: this.info.id }
          return true
        })
      }
    },
    handleSuccess(res) {
      // if (response.data['msg'] == "Successfully uploaded photo") {
      //   this.fileList[0].name = data['name'];
      //   this.fileList[0].url = data['url'];
      // } else {
      //   console.error('文件上传失败');
      // }
      if (this.fileList.length === 0) {
        this.fileList.push({ name: res.name, url: res.url })
      } else {
        this.fileList = []
        this.fileList.push({ name: res.name, url: res.url })
      }
      console.log(this.fileList)
    },
    handleBeforeRemove() {
      this.removePhoto().then(() => {
        return true
      })
    },
    // 合并之前的handleRemove函数
    handleRemove() {
      this.fileList = []
    },
    // 合并之前的handlePreview函数
    handlePreview(file) {
      console.log(file)
    },
    openModal(row, sign) {
      this.isVisible = true
      document.body.style.overflow = 'hidden' // 禁止滚动
      this.info.name = row.name
      this.info.id = row.id
      this.info.office = row.office
      this.info.title = row.title
      this.info.cost = row.cost
      this.info.research = row.research
      this.sign = sign
      this.fileList = []
      if (row.avatar_name !== undefined && row.avatar_name != '')
        this.fileList.push({ name: row.avatar_name, url: '/api/doctor/avatar/' + row.avatar_name })
      console.log(`传入的sign是：${this.sign}`)
    },
    closeModal() {
      if (this.fileList.length !== 0 && this.sign == 'add') {
        this.removePhoto().then(() => {
          this.isVisible = false
          document.body.style.overflow = '' // 恢复滚动
          this.$emit('updateData') // 触发自定义事件
        })
      } else {
        this.isVisible = false
        document.body.style.overflow = '' // 恢复滚动
        this.$emit('updateData') // 触发自定义事件
      }
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
