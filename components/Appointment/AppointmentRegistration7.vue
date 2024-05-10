<template>  
  <Header :squares2="squares2"/> 
  
  <div class="notice-box" style="height: 1500px;">  
    <!-- 上一步/下一步 -->
    <div class="container2">  
      <button class="button2 button-next" @click="submit">确认</button>  
    </div> 
    <div class="doctor-item">
      <div class="doctor-header"> 
        <img :src="doctor.avatar" alt="" class="avatar">
        <div class="info">  
          <div class="name">{{ doctor.name }}</div>  
          <div class="title">{{ doctor.title }}</div>  
          <div class="research">{{ doctor.research }}</div>  
        </div>  
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊院区：</div>
        <div class="detail-item ">猫猫就诊</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">科室：</div>
        <div class="detail-item ">{{ department }}</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊日期：</div>
        <div class="detail-item ">2024-{{ this.selectTimeTable.time }}</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊时间：</div>
        <div class="detail-item ">{{ this.selectTimeTable.startTime }}-{{ this.selectTimeTable.endTime }}</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">医事服务费：</div>
        <div class="detail-item ">{{ doctor.cost }}元</div>
      </div>
      <div class="detail-container">
        <div class="detail-item ">就诊人：</div>
        <div class="detail-item ">林艺涵</div>
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
      selectTimeTable:{time: '05-09(上午)', startTime:"08:00", endTime:"08:10"},
      isMedicalInsurance:true,
      doctor:{  
          name: '医生A',  
          title: '主任医师',  
          avatar: 'img/lsy.jpg', // 头像URL  
          research: '生物信息', // 主要研究方向  
          schedule: [  
            {time: '05-09(上午)',status:'empty', number: 10},
          ],  
          cost:100,
          emptytime:[
            {number: 1,status:'empty'},
            {number: 2,status:'full'},
            {number: 3,status:'empty'},
            {number: 4,status:'empty'},
            {number: 5,status:'full'},
            {number: 6,status:'empty'},
            {number: 7,status:'full'},
            {number: 8,status:'full'},
            {number: 9,status:'empty'},
            {number: 10,status:'full'},
            {number: 11,status:'full'},
            {number: 12,status:'full'},
            {number: 13,status:'empty'},
            {number: 14,status:'empty'},
            {number: 15,status:'full'},
            {number: 16,status:'empty'},
            {number: 17,status:'empty'},
            {number: 18,status:'full'},
            {number: 19,status:'empty'},
            {number: 20,status:'full'},
          ],
          
        },
      department:'心血管内科',
      people: {
        name: '林艺涵',  
        gender:'女',
        idType:'身份证',
        phone:'18518559617',
        number:'370883200503160423',
      },
      form:{
        address:'',
        selectTimeTable:{},
        order:0,
        people: this.people,
        isMedicalInsurance:this.isMedicalInsurance,
        doctorname:'',
        department:'心血管内科',
      },
    };  
  }  ,
  methods: {  
    submit(){
      this.form.address='猫猫就诊';
      this.form.selectTimeTable=this.selectTimeTable;
      this.form.order=this.doctor.cost;
      this.form.people=this.people;
      this.form.isMedicalInsurance=this.isMedicalInsurance;
      this.form.doctorname=this.doctor.name;
      // console.log(this.form)
    },
    selectTimeSlot(index){
      this.selectTime=index
      this.checked=true
    }, 
    togglePaymentType() {  
      this.isMedicalInsurance = !this.isMedicalInsurance; // 切换支付类型  
    },
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
</style>