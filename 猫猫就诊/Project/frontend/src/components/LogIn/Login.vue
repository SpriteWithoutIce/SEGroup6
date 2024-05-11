<template>
  <div class="modal-background" v-if="loginVisible">
    <div class="modal-container">
      <el-form :model="loginForm" :rules="rules" ref="loginForm" class="form" label-width="auto" style="max-width: 600px">
        <el-form-header class="form-header">登录</el-form-header>
        <el-form-item label="身份证号" class="idCardLabel">
          <el-input v-model="loginForm.idCard"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="loginForm.password" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div class="button-group">
        <el-button type="primary" @click="handleLogin">登录</el-button>
        <el-button @click="cancelModal">取消</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
export default {
  data() {
    return {
      loginVisible: false,
      loginForm: {
        idCard: '',
        password: ''
      },
      rules: {
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 15, message: '密码长度在 5 到 15 个字符', trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    openModal() {
      this.loginVisible = true;
      document.body.style.overflow = 'hidden'; // 禁止滚动
    },
    closeModal() {
      this.loginVisible = false;
      document.body.style.overflow = ''; // 恢复滚动
    },
    cancelModal () {
      ElMessage({
        type: "info",
        message: "取消登录 ╮(╯▽╰)╭",
        showClose: true,
      }),
        this.closeModal();
    },
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          alert('登录成功');
          // 登录成功后的逻辑...
          this.closeModal();
        } else {
          console.log('登录信息错误');
        }
      });
    }
  }
};
</script>

<style scoped>
.idCardLabel {
  padding-left: 0px;
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
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
}

.button-group {
  margin-top: 20px;
  text-align: center;
}

.delete-button {
  width: 14%;
  text-align: left;
}

.form-header {
  display: flex;
  justify-content: center;
  font-size: 24px;
  /* 字体大小 */
  font-weight: bold;
  /* 字体加粗 */
  color: #333;
  /* 字体颜色 */
  margin-bottom: 20px;
  /* 下边距 */
}


</style>
