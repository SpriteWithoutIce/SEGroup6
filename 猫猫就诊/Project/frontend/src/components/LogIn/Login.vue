<template>
  <div class="modal-background" v-if="loginVisible">
    <!-- <img src="../../assets/LogIn/碳治郎1.png" alt="中心图片" class="center-image"> -->
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
          <el-form-item label="身份" prop="idCard" class="input-item3">
            <el-select v-model="loginForm.userType" placeholder="身份选择" class="input-item3">
              <el-option label="医生" value="医生"></el-option>
              <el-option label="普通用户" value="普通用户"></el-option>
              <el-option label="管理员" value="管理员"></el-option>
            </el-select>
          </el-form-item>
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
          <RouterLink to="/Main">
            <el-button type="danger" @click="logout" class="input-item2">退出登录</el-button>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CryptoJS from 'crypto-js';
import { ElMessage } from "element-plus";
import { inject } from 'vue'
export default {
  data () {
    return {
      identityNum: inject('$identity_num'),

      receivedidCard: "",
      receivedtype: "",
      loginVisible: false,
      isLogin: "",
      notLogin: "",
      loginForm: {
        idCard: "",
        userType: "",
        password: "",
        remember: false,
        autoLogin: false,
      },
      // 不需要users，使用一条返回信息即可
      // users: [],
      msg: "",

      rules: {
        idCard: [
          { required: true, message: "请输入账号", trigger: "blur" },
          { pattern: /^\d{6,20}$/, message: "账号必须为6~20位数字", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
    };
  },
  mounted () {
    /*this.getUsersData();*/
  },
  methods: {
    writeBackUserData () {
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          identityNum: this.loginForm.idCard,
          userType: this.loginForm.userType,
          password: this.loginForm.password,//这里也要SHA吗？
        };
        this.$axios.post('/api/loginWriteBack/', requestData)
          .then(function (response) {
            console.log(response.data['msg']);
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            console.log("Login Write Back Failed")
            reject(error); // 数据获取失败，reject Promise
          });
      });
    },
    getUserData (idCard, password, userType) {
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          idCard: idCard,
          password: CryptoJS.SHA256(password).toString(),
          userType: userType
        };
        this.$axios.post('/api/login/', requestData)
          .then(function (response) {
            ts.msg = response.data['msg'];
            console.log(ts.msg);
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
      });
    },
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
          // let user = this.findUser(idCard);
          // 不能从数据库直接读用户信息，不安全
          // 把用户证件号和使用SHA256加密后的密码传入后端进行比对
          // ElMessage({
          //   showClose: true,
          //   message: "登录成功 (๑˃̵ᴗ˂̵)",
          //   type: "success",
          // });


          // /*连数据库注释下边四行*/
          // this.identityNum = idCard;
          // this.$emit('update:currentUserCard', this.loginForm.idCard);
          // this.$emit('update:currentUserType', this.loginForm.userType);
          // this.closeModal();

          this.getUserData(idCard, password, userType).then(() => {
            if (this.msg === "Successfully Login") {
              ElMessage({
                showClose: true,
                message: "登录成功 (๑˃̵ᴗ˂̵)",
                type: "success",
              });
              this.identityNum = idCard;
              this.$emit('update:currentUserCard', this.loginForm.idCard);
              this.$emit('update:currentUserType', this.loginForm.userType);
              this.closeModal();
            } else if (this.msg === "Wrong Password") {
              ElMessage({
                showClose: true,
                message: "密码错误或用户类型错误 ╮(╯▽╰)╭",
                type: "error",
              });
            } else {
              //下边一个语句是把新的数据存在了本地的User数组中，得写回数据库
              // this.users.push({ id: idCard, password, userType });
              /*writeback是新增的写回数据库*/
              writeBackUserData();
              ElMessage({
                showClose: true,
                message: "注册成功并已登录 (๑˃̵ᴗ˂̵)",
                type: "success",
              });
              this.identityNum = idCard;
              this.$emit('update:currentUserCard', this.loginForm.idCard);
              this.$emit('update:currentUserType', this.loginForm.userType);
              this.closeModal();
            }
          })
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
      this.identityNum = '0';
      this.receivedidCard = '';
      this.currentUserType = '';
      this.loginForm.userType = '';
      this.$emit('update:currentUserCard', "");
      this.$emit('update:currentUserType', "");
      this.isLogin = false;
      this.notLogin = true;
      this.closeModal();
      ElMessage({
        type: 'success',
        message: '已退出登录 (๑˃̵ᴗ˂̵)',
        showClose: true,
      });

      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth',
      });
    },
    // findUser (idCard) {
    //   return this.users.find((user) => user.id === idCard);
    // },
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
  width: 100%;
  height: 40px;
}
</style>