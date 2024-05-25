<!--药物录入细节-->
<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="content">
        <h3>添加药品</h3>

        <div class="upload">
          <p style="margin-bottom: 20px; font-size: 14px; font-weight: 500; color: grey">
            点击导入本地药物图片
          </p>
          <el-upload
            v-model:file-list="fileList"
            class="upload-demo"
            action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :on-success="handleSuccess"
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
          <p style="margin-left: 15px">药品名：</p>
          <el-input
            v-model="info.name"
            style="width: 240px"
            placeholder="请输入药品名称"
            clearable
          />
        </div>
        <div class="line">
          <p style="margin-left: 15px">药品类型：</p>
          <el-radio-group v-model="radio">
            <el-radio :value="3">中药</el-radio>
            <el-radio :value="6">中成药</el-radio>
            <el-radio :value="9">西药</el-radio>
          </el-radio-group>
        </div>
        <div class="line">
          <p style="margin-left: 15px">价格：</p>
          <el-input v-model="info.price" style="width: 240px" placeholder="请输入单价" clearable />
        </div>
        <div class="line">
          <p style="margin-left: 15px">库存：</p>
          <el-input v-model="info.num" style="width: 240px" placeholder="请输入库存" clearable />
        </div>
        <div class="line">
          <p style="margin-left: 15px">适应症状：</p>
          <el-input
            v-model="info.use"
            style="width: 240px"
            placeholder="用逗号分隔(例如：感冒，头痛)"
            type="textarea"
            clearable
          />
        </div>
      </div>
      <div class="button">
        <el-button @click="closeModal" plain>取消</el-button>
        <el-button @click="closeModal" type="primary">确定</el-button>
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from 'vue'
export default {
  name: 'DetailC',
  data() {
    return {
      fileList: ref([
        {
          name: 'food.jpeg',
          url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        }
      ]),
      isVisible: false,
      inputName: '',
      radio: '',
      info: [
        {
          name: '',
          type: '',
          use: '',
          price: '',
          num: ''
        }
      ]
    }
  },
  methods: {
    handleSuccess(response, file, fileList) {
      // 假设后端API返回了文件上传成功的响应
      if (response.success) {
        // 更新fileList，添加新上传的文件信息
        this.fileList.push({
          name: file.name,
          url: response.data.url // 假设后端返回文件的URL
          // 其他需要的属性...
        })
      } else {
        // 处理错误情况
        console.error('文件上传失败:', response.message)
      }
    },
    // 合并之前的handleRemove函数
    handleRemove(uploadFile, uploadFiles) {
      console.log(uploadFile, uploadFiles)
    },
    // 合并之前的handlePreview函数
    handlePreview(file) {
      console.log(file)
    },
    openModal(row) {
      this.isVisible = true
      document.body.style.overflow = 'hidden' // 禁止滚动
      this.info.name = row.name
      if (row.type === '中药') {
        this.radio = 3
      } else if (row.type === '中成药') {
        this.radio = 6
      } else {
        this.radio = 9
      }
      this.info.use = row.use
      this.info.price = row.price
      this.info.num = row.num
      console.log(`传入的name是：${this.info.name}`)
    },
    closeModal() {
      this.isVisible = false
      document.body.style.overflow = '' // 恢复滚动
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
