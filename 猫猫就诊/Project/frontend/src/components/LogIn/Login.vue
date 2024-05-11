<template>
  <div class="modal-background" v-if="loginVisible">
    <div class="modal-container">
      <el-form :model="loginForm" :rules="rules" ref="loginForm" class="form" label-width="auto"
        style="max-width: 600px">
        <el-form-header class="form-header">猫猫就诊个人信息认证</el-form-header>
        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="loginForm.idCard"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="loginForm.name"></el-input>
        </el-form-item>
      </el-form>
      <div class="button-group">
        <el-button type="primary" @click="handleLogin">确认</el-button>
        <el-button @click="cancelModal">取消</el-button>
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
        idCard: '',
        name: '',
      },
      rules: {
        idCard: [
          { required: true, message: '请输入身份证号', trigger: 'blur' },
          { pattern: /^\d{6,20}$/, message: '身份证号必须为6~20位数字', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ]
      },
      users: [
        { idCard: '22373334', name: '周其顺' },
        { idCard: '09876543210987654321', name: 'Bob' }
      ]
    };
  },
  methods: {
    openModal () {
      this.loginForm.idCard = '';
      this.loginForm.name = '';
      this.loginVisible = true;
      document.body.style.overflow = 'hidden'; // 禁止滚动
    },
    closeModal () {
      this.loginVisible = false;
      document.body.style.overflow = '';
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
          const existingUser = this.users.find(user => user.idCard === this.loginForm.idCard);
          if (existingUser) {
            if (existingUser.name === this.loginForm.name) {
              ElMessage({
                showClose: true,
                message: "登录成功 (๑˃̵ᴗ˂̵)",
                type: "success",
              });
              // 登录成功后的逻辑...
              this.closeModal();
            } else {
              ElMessage({
                type: "info",
                message: "(╯°□°）╯︵ ┻━┻",
                showClose: true,
              });
            }
          } else {
            this.users.push({
              idCard: this.loginForm.idCard,
              name: this.loginForm.name
            });
            ElMessage({
              showClose: true,
              message: "新用户已添加并登录成功 (≧▽≦)",
              type: "success",
            });
            // 登录成功后的逻辑...
            this.closeModal();
          }
        } else {
          ElMessage({
            type: "info",
            message: "信息错误 ╮(╯▽╰)╭",
            showClose: true,
          });
          console.log('登录信息错误');
        }
      });
    }
  }
};
</script>

<style scoped>
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

.form-header {
  display: flex;
  justify-content: center;
  font-size: 24px;
  /* 字体大小 */
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}
</style>
