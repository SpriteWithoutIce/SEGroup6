<template>
  <div class="modal-background" v-if="loginVisible">
    <div class="modal-container">
      <div class="top-section">
        <img src="../../assets/navigation/banner1.jpg" alt="背景图片" class="background-image">
        <!-- Place cancel button in the top right corner -->
        <div class="cancel-btn" @click="cancelModal">
          <div class="cancel-icon">X</div>
        </div>
      </div>
      <!-- 想在这里插入一个空区域让两边分割 -->
      <div class="mid-section">

      </div>
      <div class="bottom-section">
        <el-form :model="loginForm" :rules="rules" ref="loginForm" class="form" label-width="auto">
          <el-form-item label="身份证号" prop="idCard" class="input-item">
            <el-input v-model="loginForm.idCard"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="name" class="input-item">
            <el-input v-model="loginForm.name" type="password"></el-input>
          </el-form-item>
          <div class="checkbox-group">
            <el-checkbox v-model="loginForm.remember">记住密码</el-checkbox>
            <el-checkbox v-model="loginForm.autoLogin">自动登录</el-checkbox>
          </div>
        </el-form>
        <div class="button-group">
          <el-button type="primary" @click="handleLogin" class="input-item2">登录</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
export default {
  data () {
    return {
      loginVisible: false,
      loginForm: {
        idCard: "",
        name: "",
        remember: false,
        autoLogin: false,
      },
      rules: {
        idCard: [
          { required: true, message: "请输入账号", trigger: "blur" },
          { pattern: /^\d{6,20}$/, message: "账号必须为6~20位数字", trigger: "blur" },
        ],
        name: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
    };
  },
  methods: {
    openModal () {
      this.loginForm.idCard = "";
      this.loginForm.name = "";
      this.loginVisible = true;
      document.body.style.overflow = "hidden"; // 禁止滚动
    },
    closeModal () {
      this.loginVisible = false;
      document.body.style.overflow = "";
    },
    cancelModal () {
      ElMessage({
        type: "info",
        message: "取消登录 ╮(╯▽╰)╭",
        showClose: true,
      });
      this.closeModal();
    },
    handleLogin () {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          // 验证通过后的逻辑...
          ElMessage({
            showClose: true,
            message: "登录成功 (๑˃̵ᴗ˂̵)",
            type: "success",
          });
          this.closeModal();
        } else {
          ElMessage({
            type: "info",
            message: "信息错误 ╮(╯▽╰)╭",
            showClose: true,
          });
        }
      });
    },
  },
};
</script>

<style scoped>
.modal-background {
  position: fixed;
  top: 0;
  left: 0;
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
  width: 600px;
  height: 400px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-section {
  height: 33%;
  background-color: #f0f0f0;
  position: relative;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bottom-section {
  height: 67%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  /* Center align all child elements horizontally */
}

.checkbox-group {
  display: flex;
  justify-content: space-between;
  width: 100%;
  /* Ensure checkboxes take full width */
}

.button-group {
  margin-top: 20px;
  text-align: center;
  width: 100%;
}

.cancel-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  cursor: pointer;
  border-radius: 50%;
  background-color: #007bff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cancel-btn:hover {
  background-color: #000fb397;
}

.cancel-icon {
  font-size: 20px;
  color: #fff;
}

.input-item2 {
  align-self: center;
  width: 50%;
}
</style>
