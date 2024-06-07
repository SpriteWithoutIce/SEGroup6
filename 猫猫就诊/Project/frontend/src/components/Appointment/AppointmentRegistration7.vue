<template>  
  <Header :squares2="squares2"/> 
  <BillDetails @billDetailsUpdated="onBillDetailsUpdated" ref="BillDetails"> </BillDetails>
  <div class="notice-box" style="height: 1500px;">  
   
    <!-- 上一步/下一步 -->
    <div class="container2">  
      <router-link :to="{
        path: '/AppointmentRegistration6',
        query:{
          info_doctor:JSON.stringify(info_last.info_doctor)
        }
        }" class="button2 button-prev" style="text-decoration: none;">上一步</router-link>
      <router-link :to="{
          path:'/AppointmentRegistration8',
          query:{
            order:JSON.stringify(info)
          }}" class="button2 button-next" @click="submit" v-if="billstatus">确认</router-link>
      <div class="container2" v-if="!billstatus">
        <el-button @click="showBillDetails()"
          >缴费</el-button>
      </div>  
    </div> 
    <p>倒计时: {{ countDown }}</p> 
    <div class="doctor-item">
      <div class="doctor-header"> 
        <img :src="info.doctorAvatar" alt="" class="avatar">
        <div class="info">  
          <div class="name">{{ info.doctorName }}</div>  
          <div class="title">{{ info.doctorTitle }}</div>  
          <div class="research">{{ info.doctorRearch }}</div>  
        </div>  
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊院区：</div>
        <div class="detail-item ">猫猫就诊</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">科室：</div>
        <div class="detail-item ">{{ info.department }}</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊日期：</div>
        <div class="detail-item ">2024-{{ info.time }}</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊时间：</div>
        <div class="detail-item ">{{ info.starttime }}-{{ info.endtime }}</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">医事服务费：</div>
        <div class="detail-item ">{{ info.cost }}元</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊人：</div>
        <div class="detail-item ">{{ info.name }}</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">*支付类型（请选择）：</div>
        <div style="display: flex;justify-content: space-around; height: 50px;" class="detail-item ">
          <div >{{ isMedicalInsurance ? '医保' : '非医保' }}</div>
          <span class="toggle-arrow" @click="togglePaymentType">▶</span>
        </div>
      </div>
    </div>
    
    
  </div>  
</template>  
  
<script>  
import BillDetails from './Appointments/AppointmentBillDetails.vue'
import Header from './Appointments/AppointmentHeader.vue'
import { GlobalState } from '../../global.js';
export default {  
  inject: ['$identity_num'],
  components: {
    Header,
  },
  data() {  
    return {  
      countDown: 20, // 3分钟 = 180秒  
      intervalId: null,  
      checked: false,  
      currentSquareIndex: 0,  
      squares2: [  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: true ,done: false},  
        { hovered: false, active: false ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      selectTime:1,
      isMedicalInsurance:true,
      billstatus:false,
      info:{
        name:'',//就诊人
        paymentType:'',
        department:'',
        time:'',//日期05-30
        starttime:'',//开始时间
        endtime:'',
        number:'',//挂号序号
        doctorName:'',//医生名字
        doctorTitle:'',//医生title
        doctorAvatar:'',//医生头像
        doctorRearch:'',//医生领域
        cost:'',//医生的挂号费
        inumber:'',//患者的证件号
        identity_num: this.$identityNum,
        info_last:{},
        doctor_id:'',
      },
      info_last:{},
    };  
  }  ,
  components: {
    BillDetails
  },
  methods: {  
    submit(){
      this.setAppointmentData().then(() =>{})
      // console.log(this.form)
    },
    selectTimeSlot(index){
      this.selectTime=index
      this.checked=true
    }, 
    togglePaymentType() {  
      this.isMedicalInsurance = !this.isMedicalInsurance; // 切换支付类型  
      if(this.isMedicalInsurance)
        this.info.paymentType='医保';
      else
        this.info.paymentType='非医保';
    },
    showBillDetails() {
      const now = new Date(); 
      const formattedDateTime = `${now.getFullYear()}年${String(now.getMonth() + 1).padStart(2, '0')}月${String(now.getDate()).padStart(2, '0')}日`;  
      var row={
        type:'挂号',
        issue:'挂号费',
        price:this.info.cost,
        date:formattedDateTime
      };
      if(this.isMedicalInsurance){
        row.price=0;
      }
      console.log(row)
      this.$refs.BillDetails.openModal(row)
    },
    onBillDetailsUpdated(dataFromChild) {
      this.billstatus=dataFromChild;
      return dataFromChild;
    },
    setAppointmentData() {
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          name:this.info.name,//就诊人
          paymentType:this.info.paymentType,
          department:this.info.department,
          time:this.info.time,//日期05-30
          starttime:this.info.starttime,//开始时间
          endtime:this.info.endtime,
          number:this.info.number,//挂号序号
          doctorId:this.info.doctor_id,
          doctorName:this.info.doctorName,//医生名字
          doctorTitle:this.info.doctorAvatar,//医生title
          doctorAvatar:this.info.doctorAvatar,//医生头像
          doctorRearch:this.info.doctorRearch,//医生领域
          cost:this.info.cost,//医生的挂号费
          inumber:this.info.inumber,//患者的证件号
          identity_num: GlobalState.identityNum,
          id:this.info.doctor_id,
        };
        console.log(requestData)
        requestData = {
          name:this.info.name,//就诊人
          paymentType:this.info.paymentType,
          department:this.info.department,
          time:this.info.time,//日期05-30
          starttime:this.info.starttime,//开始时间
          endtime:this.info.endtime,
          number:this.info.number,//挂号序号
          doctorId:this.info.doctor_id,
          doctorName:this.info.doctorName,//医生名字
          doctorTitle:this.info.doctorAvatar,//医生title
          doctorAvatar:this.info.doctorAvatar,//医生头像
          doctorRearch:this.info.doctorRearch,//医生领域
          cost:this.info.cost,//医生的挂号费
          inumber:this.info.inumber,//患者的证件号
          identity_num: GlobalState.identityNum,
          id:this.info.doctor_id,
          action:"addRegisterData"
        };
        if(this.info.paymentType=='医保')
          requestData.cost=0;
        // 这里的api
        this.$axios.post('/api/appointment/add/', requestData)
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
    
    navigateToOtherPage() {  
      // 假设你正在使用Vue Router  
      this.$router.push('/AppointmentRegistration');  
    },  
    cancel(){
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          number:this.info.number,
          time:this.info_time,
          starttime:this.info_startTime,
          doctorId:this.info.doctor_id,
          action:"unlockRegister"
        };
        this.$axios.post('/api/register/unlock/', requestData)
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
  },
  beforeDestroy() {  
    // 在组件销毁前清除定时器，避免内存泄漏  
    clearInterval(this.intervalId);  
  },  
  created(){
    const info_Str = this.$route.query.info;  
    if (info_Str) {  
      this.info_last = JSON.parse(info_Str);  
    }
    this.info.info_last=this.info_last;
    this.info.name=this.info_last.name;
  
    this.info.paymentType=this.info_last.paymentType;
    if(this.info.paymentType=='非医保')
      this.isMedicalInsurance=false;
    else{
      this.info.paymentType='医保';
    }
    this.info.department=this.info_last.department;
    this.info.time=this.info_last.time;
    this.info.starttime=this.info_last.starttime;
    this.info.endtime=this.info_last.endtime;
    this.info.number=this.info_last.number;
    this.info.doctorName=this.info_last.doctorName;
    this.info.doctorTitle=this.info_last.doctorTitle;
    this.info.doctorAvatar=this.info_last.doctorAvatar;
    this.info.doctorRearch=this.info_last.doctorRearch;
    this.info.cost=this.info_last.cost;
    this.info.inumber=this.info_last.inumber;
    this.info.doctor_id=this.info_last.doctor_id;
    console.log(this.info.info_last)
    console.log(this.info)
    this.intervalId = setInterval(() => {  
      if (this.countDown > 0) {  
        this.countDown--;  
      } else {  
        // 倒计时结束，跳转到其他页面  
        this.cancel();
        this.navigateToOtherPage();  
        
        clearInterval(this.intervalId); // 清除定时器  
      }  
    }, 1000); // 每秒更新一次  
  }
};  
</script>  
  
<style scoped>  
.container2 {  
  display: flex;  
  flex-wrap: wrap;  
  justify-content: center;  
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
.notice-box {  
  background-color: #f5f5f5; /* 浅灰色背景 */  
  border-left: 30px solid #fff;
  border-right: 30px solid #fff; /* 白色边框 */  
  padding: 20px; /* 内边距 */  
  margin: 10px; /* 外边距 */  
  margin-bottom: 100px;
  box-sizing: border-box; /* 确保边框和内边距包含在元素的总宽度和高度内 */  
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
  transition: background-color 0.3s, color 0.3s; /* 添加过渡效果 */  
  text-decoration: none;
}  
.button-next {  
  background-color: #003366; /* 浅蓝色 */  
  color: #fcfcfc; /* 深蓝色 */  
}  
.button-prev {  
  background-color: #e5ecff; /* 深蓝色 */  
  color: #003366; /* 白色 */  
}  
.button:hover {  
  opacity: 0.8; /* 鼠标悬停时透明度降低 */  
}  
.doctor-header {  
  display: flex;  
  align-items: center;  
  margin-bottom: 10px;  
}  
  
.avatar {  
  width: 60px;  
  height: 60px;  
  border-radius: 50%;  
  background-size: cover;  
  background-position: center;  
  margin-right: 50px;  
}  
.info {  
  flex: 1;  
}  
  
.name {  
  font-size: 18px;  
  font-weight: bold;  
  margin-bottom: 5px;  
}  
  
.title, .research {  
  font-size: 14px;  
}  

.doctor-item {  
  width: 800px;
  margin: 10px auto; /* 如果垂直排列，通常只需要上下边距 */
  border: 1px solid #ccc;  
  padding: 15px;  
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  
} 

.button-container {  
  width: 900px;
  margin: 20px auto;
  display: flex;  
  flex-wrap: wrap;  
  justify-content: flex-start; /* 水平方向对齐方式，这里使用默认即可 */  
}  
  
.button-row {  
  display: flex;  
  margin-bottom: 10px; /* 可选，用于按钮行之间的间距 */  
}  

.button-down {  
  width: 120px;
  height: 100px;  
  display: flex;  
  flex-direction: column; /* 垂直排列文字 */  
  justify-content: center; /* 垂直居中文字 */  
  align-items: center; /* 水平居中文字（在这个场景里其实不需要，但保持一致性）*/  
  text-align: center; /* 水平居中文字内容 */  
  border: none; /* 去除默认边框 */  
  background-color: #eee; /* 示例背景色 */  
  cursor: pointer; /* 鼠标悬停时变为小手形状 */  
  color: black;
  margin-left: 50px;
  margin-right: 50px;
}  
.selected{
  color: #1736ff;
  background-color: #d4e1ff;
  border: 1px solid #1736ff;
} 
span {  
  margin-top: 5px; /* 上下排列的文字之间的间距 */  
}
.detail{
  height: 50px;
  border: 1px solid #ccc; 
  background-color: white;
  align-items: center;
  line-height: 50px;
}
.detail-container {  
  display: flex;  
  justify-content: space-between; /* 可选：在 div 之间添加一些空间 */  
  height: 50px;
  border: 1px solid #ccc; 
  background-color: white;
  align-items: center;
  line-height: 50px;
}  
  
.detail-item {  
  flex: 1; /* 让 div 均匀地占用可用空间 */  
  margin: 1%; /* 添加一些外边距以防止它们紧挨着 */  
  background-color: white; /* 可选：添加一个背景色以便于查看 */  
}  
.toggle-arrow {  
    margin-left: auto; /* 将箭头推到右边 */  
    cursor: pointer; /* 鼠标悬停时显示小手图标，表示可点击 */  
}

.pay-button {
  background-color: whitesmoke;
  margin-left: -10px;
  max-width: 75px;
}
</style>