<!-- 填写就诊人信息 -->
<template>  
  <Header :squares2="squares2" />
  <!-- 就诊须知内容 -->
  <div class="notice-box">  
    <div class="container2" style="margin-bottom: 50px;">  
      <router-link to="/AppointmentRegistration2" class="button2 button-prev">上一步</router-link>
      <router-link 
        :to="{
          path:'/AppointmentRegistration4',
          query:{
            name:formData.name,
            number:formData.number,
            paymentType:formData.paymentType,
            selected:select
          }
        }" class="button2 button-next" @click="submit" v-if="isformed()">
        下一步
      </router-link>
    </div> 
    <!-- 首诊信息 -->
    <div class="container3" v-if="first">
    <form @submit.prevent="submitForm">  
      <div class="form-group">  
        <input type="text" id="name" name="name" class="form-control" placeholder="请输入姓名" v-model="formData.name">  
        <select id="paymentType" name="paymentType" class="form-control" placeholder="支付类型" v-model="formData.paymentType">  
          <option value="" disabled selected>请选择支付类型</option>
          <option value="医保">医保</option>  
          <option value="非医保">非医保</option>  
        </select>  
      </div>  
      <div class="form-group">  
        <select id="gender" name="gender" class="form-control" placeholder="性别" v-model="formData.gender">  
          <option value="" disabled selected>性别</option>
          <option value="男">男</option>  
          <option value="女">女</option>  
        </select>  
        <input type="date" id="birthday" name="birthday" class="form-control" placeholder="出生日期" v-model="formData.birthday">  
      </div>  
      <div class="form-group">  
        <select id="idType" name="idType" class="form-control" placeholder="证件类型" v-model="formData.idType">
          <option value="" disabled selected>请选择证件类型</option>
          <option value="身份证">身份证</option>  
          <option value="医保卡">医保卡</option>  
          <option value="诊疗卡">诊疗卡</option>
          <option value="护照">护照</option>
          <option value="军官证">军官证</option>
          <option value="港澳通行证">港澳通行证</option>
        </select>  
        <input type="tel" id="phone" name="phone" class="form-control" placeholder="联系电话" v-model="formData.phone">  
      </div>   
      <div class="form-group">
        <input type="text" id="number" name="number" class="form-control" placeholder="请输入证件号" v-model="formData.number"> 
      </div>
      <div class="form-group">
        <input type="text" id="addr" name="addr" class="form-control" placeholder="请输入住址" v-model="formData.addr"> 
      </div>
    </form>  
    </div>
    <!-- 复诊信息 -->
    <div class="container3" v-if="second">
    <form @submit2.prevent="submitForm2">  
      <div class="form-group">  
        <input type="text" id="name" name="name" class="form-control" placeholder="请输入姓名" v-model="formData.name">  
        <select id="gender" name="gender" class="form-control" placeholder="性别" v-model="formData.gender">  
          <option value="" disabled selected>性别</option>
          <option value="男">男</option>  
          <option value="女">女</option>  
        </select>  
      </div>  
      <div class="form-group">  
        <select id="idType" name="idType" class="form-control" placeholder="证件类型" v-model="formData.idType">
          <option value="" disabled selected>请选择证件类型</option>
          <option value="身份证">身份证</option>  
          <option value="医保卡">医保卡</option>  
          <option value="诊疗卡">诊疗卡</option>
          <option value="护照">护照</option>
          <option value="军官证">军官证</option>
          <option value="港澳通行证">港澳通行证</option>
        </select>  
        <input type="tel" id="phone" name="phone" class="form-control" placeholder="联系电话" v-model="formData.phone"> 
      </div>  
      <div class="form-group">
        <input type="text" id="number" name="number" class="form-control" placeholder="请输入证件号" v-model="formData.number"> 
      </div>
    </form>  
    </div>
    <!-- 打勾&按钮 -->
    <div>
      <div class="checkbox-container" style="text-align: center; margin-top: 20px;">  
        <input type="checkbox" id="checkbox" v-model="checked" />  
        <label for="checkbox">我已阅读并同意《个人隐私收集声明》</label>  
      </div>  
    </div>
  </div>  
</template>  
  
<script>  
import Header from './Appointments/AppointmentHeader.vue'
export default {  
  components: {
    Header,
  },
  data() {  
    return {  
      squares: [  
        { hovered: false },  
        { hovered: true },  
        { hovered: false },  
        { hovered: false }  
      ] ,
      info: [
        "出诊查询","网上预约看诊","预约流程","取消预约"
      ],
      checked: false,  
      currentSquareIndex: 0,  
      squares2: [  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: true ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      first: 0,
      second: 0,
      select:0,
      formData:{
        queryFirst:0,
        name:'',
        paymentType:'',
        gender:'',
        birthday:'',
        idType:'',
        phone:'',
        number:'',
        addr:'',
      }
    };  
  }  ,
  methods: { 
    setPatientData() {
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          name: this.formData.name,
          paymentType: this.formData.paymentType,
          gender: this.formData.gender,
          birthday: this.formData.birthday,
          idType: this.formData.idType,
          phone: this.formData.phone,
          number: this.formData.number,
          addr: this.formData.addr,
        };
        this.$axios.post('/api/patient/add/', requestData)
          .then(function (response) {
            console.log(response.data['msg']);
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
      });
    },
    toggleSquare(index) {  
      this.currentSquareIndex = index;   
      this.currentSquareIndex = 1;
      this.checked = false;
    },  
    nextSquare(){

    },
    
    submitForm() {  
      console.log(this.formData);
    } ,
    submit(){
      console.log(this.formData)
      if(this.first==1)
        this.setPatientData();
    },
    submitForm2() {  
      console.log(this.form2);
    }, 
    isformed(){
      if(this.first==1){
        if(!this.checked)
          return false;
        return Object.keys(this.formData)  
        .filter(key => key !== 'queryFirst')
        .every(key => this.formData[key] !== '');
      }
      else{
        if(!this.checked)
          return false;
        if(this.formData.name=='') return false;
        if(this.formData.gender=='') return false;
        if(this.formData.idType=='') return false;
        if(this.formData.number=='') return false;
        if(this.formData.phone=='') return false;
        return true;
      }
    }
  },
  created(){
    this.select=this.$route.query.select
    if(this.$route.query.select==0){
      this.first=1;
      this.formData.queryFirst=1;
    }
    else
      this.second=1;
  }
};  
</script>  
  
<style scoped>  
.container2 {  
  display: flex;  
  flex-wrap: wrap;  
  justify-content: center;  
}  
.container3 {  
  display: flex;  
  flex-direction: column;  
  align-items: center; 
  justify-content: center; 
  height: 40vh;
  margin: 0;
}  
button {  
  margin: auto auto;  
  padding: 5px 10px;  
  background-color: #003366;  
  color: #FFFFFF;  
  width: 150px;
  height: 50px;
  border-radius: 10px;
}  
.button-container {
  display: flex;  
  justify-content: center;  
  align-items: center;  
}

.notice-box {  
  background-color: #f5f5f5; 
  border-left: 30px solid #fff;
  border-right: 30px solid #fff;
  padding: 20px;
  margin: 10px;
  box-sizing: border-box;
}  

.square-done {
  background-color: #003366;  
  color: #FFFFFF;
}

.form-group {  
  display: flex;  
  flex-direction: row;  
  justify-content: space-between;  
  margin-bottom: 20px; 
  width: 500px;
  height: 50px; 
  border-radius: 25px;
}  
.form-control {  
  flex: 1;  
  margin-right: 10px;  
  border-radius: 25px;
  border: none;
  padding: 0 10px;
}  
.form-control:last-child {  
  margin-right: 0;  
}  
.button2 {  
  border: none;
  font-size: large;
  width: 150px;  
  height: 50px;  
  display: flex;  
  justify-content: center;  
  align-items: center;  
  margin: 0 10px;  
  border-radius: 10px;
  background-color: #fcfcfc;  
  color: #000000;  
  cursor: pointer;  
  transition: background-color 0.3s, color 0.3s;
  text-decoration: none;
}  
.button-next {  
  background-color: #003366;
  color: #fcfcfc; 
}  
.button-prev {  
  background-color: #e5ecff;
  color: #003366;
}  
.button:hover {  
  opacity: 0.8;
}  

.checkbox-container {  
  width: 100%;  
  padding: 10px;  
  box-sizing: border-box;  
}  
</style>