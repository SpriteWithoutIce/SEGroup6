<template>
  <div class="modal-background" v-if="loginVisible">
    <img src="../../assets/LogIn/碳治郎1.png" alt="中心图片" class="center-image">
    <div class="modal-container">
      <div class="top-section">
        <img src="../../assets/navigation/banner2.jpg" alt="背景图片" class="background-image">
        <div class="cancel-btn" @click="cancelModal">
          <div class="cancel-icon">X</div>
        </div>
      </div>
      <div class="mid-section"></div>
      <div class="bottom-section" v-if="isLogin">
        <el-form :model="loginForm" :rules="rules" ref="loginForm" class="form" label-width="auto">
          <el-form-item label="身份证号" prop="idCard" class="input-item">
            <el-input v-model="loginForm.idCard"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password" class="input-item">
            <el-input v-model="loginForm.password" type="password"></el-input>
          </el-form-item>
          <el-select v-model="loginForm.userType" placeholder="身份选择" class="input-item3">
            <el-option label="医生" value="医生"></el-option>
            <el-option label="普通用户" value="普通用户"></el-option>
            <el-option label="管理员" value="管理员"></el-option>
          </el-select>
        </el-form>
        <div class="button-group">
          <el-button type="primary" @click="handleLogin" class="input-item2">登录</el-button>
        </div>
      </div>
      <div class="bottom-section" v-if="notLogin">
        <div class="user-info">
          <title>当前用户信息</title>
          <p>身份证号：{{ receivedidCard }}</p>
          <p>用户类型：{{ receivedtype }}</p>
        </div>
        <div class="button-group">
          <el-button type="danger" @click="logout" class="input-item2">退出登录</el-button>
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
      receivedidCard: "",
      receivedtype: "",
      loginVisible: false,
      isLogin: "",
      notLogin: "",
      loginForm: {
        idCard: "",
        password: "",
        userType: "",
        remember: false,
        autoLogin: false,
      },
      users: [],

      rules: {
        idCard: [
          { required: true, message: "请输入账号", trigger: "blur" },
          { pattern: /^\d{6,20}$/, message: "账号必须为6~20位数字", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
    };
  },
  methods: {
    openModal (id, type) {
      this.receivedidCard = id;
      this.receivedtype = type;
      if (id != "") {
        this.isLogin = false;
        this.notLogin = true;
      }
      else {
        this.isLogin = true;
        this.notLogin = false;
      }
      //在这里读取把User数组中的数据更新为数据库的内容
      this.loginForm.idCard = "";
      this.loginForm.password = "";
      this.loginVisible = true;
      document.body.style.overflow = "hidden";
    },
    closeModal () {
      this.loginVisible = false;
      document.body.style.overflow = "";
    },
    cancelModal () {
      ElMessage({
        type: "info",
        message: "取消 ╮(╯▽╰)╭",
        showClose: true,
      });
      this.closeModal();
    },
    handleLogin () {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          const { idCard, password, userType } = this.loginForm;
          let user = this.findUser(idCard);

          if (user) {
            if (user.password === password) {
              ElMessage({
                showClose: true,
                message: "登录成功 (๑˃̵ᴗ˂̵)",
                type: "success",
              });
              this.$emit('update:currentUserCard', this.loginForm.idCard);
              this.$emit('update:currentUserType', this.loginForm.userType);
              this.closeModal();
            } else {
              ElMessage({
                showClose: true,
                message: "密码错误 ╮(╯▽╰)╭",
                type: "error",
              });
            }
          } else {
            //下边一个语句是把新的数据存在了本地的User数组中，得写回数据库
            this.users.push({ id: idCard, password, userType });
            ElMessage({
              showClose: true,
              message: "注册成功并已登录 (๑˃̵ᴗ˂̵)",
              type: "success",
            });
            this.$emit('update:currentUserCard', this.loginForm.idCard);
            this.$emit('update:currentUserType', this.loginForm.userType);
            this.closeModal();
          }
        } else {
          ElMessage({
            type: "info",
            message: "信息错误 ╮(╯▽╰)╭",
            showClose: true,
          });
        }
      });
    },
    logout () {
      this.receivedidCard = '';
      this.currentUserType = '';
      this.$emit('update:currentUserCard', this.loginForm.idCard);
      this.$emit('update:currentUserType', this.loginForm.userType);
      this.isLogin = false;
      this.notLogin = true;
      this.closeModal();
      ElMessage({
        type: 'success',
        message: '已退出登录 (๑˃̵ᴗ˂̵)',
        showClose: true,
      });
    },
    findUser (idCard) {
      return this.users.find((user) => user.id === idCard);
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

.center-image {
  position: absolute;
  top: 32%;
  width: 7%;
  z-index: 3;
}

.mid-section {
  height: 15vh;
}

.bottom-section {
  z-index: 5;
  height: 67%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.checkbox-group {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.button-group {
  margin-top: 20px;
  text-align: center;
  width: 100%;
}

.cancel-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 18px;
  height: 18px;
  cursor: pointer;
  border-radius: 50%;
  background-color: #007bff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cancel-btn:hover {
  background-color: #07070e97;
}

.cancel-icon {
  font-size: 12px;
  color: #fff;
}

.input-item2 {
  align-self: center;
  width: 40%;
  height: 40px;
}

.input-item3 {
  left: 28%;
  width: 70%;
  height: 40px;
}
</style>