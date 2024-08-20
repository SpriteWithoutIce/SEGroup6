<!-- 选择排队号 -->
<template>  
  <Header :squares2="squares2"/> 
  <div class="notice-box" style="height: 1400px;">  
    <!-- 上一步/下一步 -->
    <div class="container2">  
      <router-link :to="{
        path:'/AppointmentRegistration5',
        query:{
          name:info.name,
          paymentType:info.paymentType,
          department:info.department,
          inumber:info.inumber,
        }}" class="button2 button-prev" style="text-decoration: none;">上一步</router-link>
      <router-link 
        :to="{
          path:'/AppointmentRegistration7',
          query:{
            info:JSON.stringify(info_detail)
          }
        }" @click="submit" class="button2 button-next" style="text-decoration: none; " v-if="checked">
        下一步</router-link>
    </div> 
    <div class="doctor-item">
      <div class="doctor-header"> 
        <img :src="doctors[0].avatar" alt="" class="avatar">
        <div class="info">  
          <div class="name">{{ doctors[0].name }}</div>  
          <div class="title">{{ doctors[0].title }}</div>  
          <div class="research">{{ doctors[0].research }}</div>  
        </div>  
      </div>
    </div>
    
    <div class="button-container">  
      <div v-for="(timeSlot, index) in doctors[0].schedule[this.info_doctor.day_index].emptytime" :key="index" class="button-row">  
        <button  
          v-if="timeSlot.status === 'empty' && (this.info_time.match(/\(.*?\)/) || [])[0]=='(上午)'"  
          @click="selectTimeSlot(index,timetable_1[timeSlot.number-1].startTime,timetable_1[timeSlot.number-1].endTime)" 
          class="button-down" 
          :class="{selected:selectTime===index}"
        >  
          {{ timetable_1[timeSlot.number-1].startTime }} - {{ timetable_1[timeSlot.number-1].endTime }}  
          <span>{{ index+1 }}&nbsp;号</span>  
        </button>
        <button  
          v-if="timeSlot.status === 'empty' && (this.info_time.match(/\(.*?\)/) || [])[0]=='(下午)'"  
          @click="selectTimeSlot(index,timetable_2[timeSlot.number-1].startTime,timetable_2[timeSlot.number-1].endTime)" 
          class="button-down" 
          :class="{selected:selectTime===index}"
        >  
          {{ timetable_2[timeSlot.number-1].startTime }} - {{ timetable_2[timeSlot.number-1].endTime }}  
          <span>{{ index+1 }}&nbsp;号</span>  
        </button>  
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
        { hovered: false, active: true ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      selectTime:1,
      // 这里的是排班表，每10分钟一个号，医生只存储号的编号，不用存储具体的时间
      timetable_1:[
            {startTime:"08:00",endTime:"08:10"},
            {startTime:"08:10",endTime:"08:20"},
            {startTime:"08:20",endTime:"08:30"},
            {startTime:"08:30",endTime:"08:40"},
            {startTime:"08:40",endTime:"08:50"},
            {startTime:"08:50",endTime:"09:00"},
            {startTime:"09:00",endTime:"09:10"},
            {startTime:"09:10",endTime:"09:20"},
            {startTime:"09:20",endTime:"09:30"},
            {startTime:"09:30",endTime:"09:40"},
            {startTime:"09:40",endTime:"09:50"},
            {startTime:"09:50",endTime:"10:00"},
            {startTime:"10:00",endTime:"10:10"},
            {startTime:"10:10",endTime:"10:20"},
            {startTime:"10:20",endTime:"10:30"},
            {startTime:"10:30",endTime:"10:40"},
            {startTime:"10:40",endTime:"10:50"},
            {startTime:"10:50",endTime:"11:00"},
            {startTime:"11:00",endTime:"11:10"},
            {startTime:"11:10",endTime:"11:20"},
      ],
      timetable_2:[
            {startTime:"14:00",endTime:"14:10"},
            {startTime:"14:10",endTime:"14:20"},
            {startTime:"14:20",endTime:"14:30"},
            {startTime:"14:30",endTime:"14:40"},
            {startTime:"14:40",endTime:"14:50"},
            {startTime:"14:50",endTime:"15:00"},
            {startTime:"15:00",endTime:"15:10"},
            {startTime:"15:10",endTime:"15:20"},
            {startTime:"15:20",endTime:"15:30"},
            {startTime:"15:30",endTime:"15:40"},
            {startTime:"15:40",endTime:"15:50"},
            {startTime:"15:50",endTime:"16:00"},
            {startTime:"16:00",endTime:"16:10"},
            {startTime:"16:10",endTime:"16:20"},
            {startTime:"16:20",endTime:"16:30"},
            {startTime:"16:30",endTime:"16:40"},
            {startTime:"16:40",endTime:"16:50"},
            {startTime:"16:50",endTime:"17:00"},
            {startTime:"17:00",endTime:"17:10"},
            {startTime:"17:10",endTime:"17:20"},
      ],
      doctors: [],
      info_doctor:{},
      info:{
        name:'',
        paymentType:'',
        department:'',
        inumber:'',
      },
      info_time:'',
      timeOfDay:'',
      info_startTime:'',
      info_endTime:'',
      info_number:0,
      info_detail:{
        name:'',
        paymentType:'',
        department:'',
        inumber:'',
        time:'',
        starttime:'',
        endtime:'',
        number:'',
        doctorName:'',
        doctorTitle:'',
        doctorAvatar:'',
        doctorRearch:'',
        cost:'',
        info_doctor:{},
        doctor_id:'',
      }
    };  
  }  ,
  methods: {  
    nextSquare(){

    },
    selectTimeSlot(index,start,end){
      this.selectTime=index
      this.checked=true
      this.info_startTime=start
      this.info_endTime=end
      this.info_number=index+1
      this.info_detail.starttime=this.info_startTime
      this.info_detail.endtime=this.info_endTime
      this.info_detail.number=this.info_number
    },
    displayTime() {  
      this.timeOfDay = (this.info_time.match(/\(.*?\)/) || []);
      if (timeOfDay == '(下午)') {  
        return 1; 
      } else if (timeOfDay == '(上午)' || !timeOfDay) { 
        return 0;
      }  
      return '未知的时间';  
    },  
    submit(){
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          number:this.info_number,
          time:this.info_time,
          starttime:this.info_startTime,
          doctorId:this.info_detail.doctor_id,
          action:"lockRegister"
        };
        this.$axios.post('/api/register/lock/', requestData)
          .then(function (response) {
            console.log(response.data['msg']);
            resolve();
          })
          .catch(function (error) {
            console.log(error);
            reject(error);
          });
      });
    }
  }  ,
  created(){
    const info_doctor_Str = this.$route.query.info_doctor;  
    if (info_doctor_Str) {  
      this.info_doctor = JSON.parse(info_doctor_Str);  
    }
    console.log(this.info_doctor)
    this.info.name=this.info_doctor.name;
    this.info.paymentType=this.info_doctor.paymentType;
    this.info.department=this.info_doctor.department;
    this.info_time=this.info_doctor.info_time;
    this.info.inumber=this.info_doctor.inumber;
    this.doctors[0]=this.info_doctor.doctor;

    this.info_detail.doctor_id=this.doctors[0].id;
    this.info_detail.name=this.info.name;
    this.info_detail.paymentType=this.info.paymentType;
    this.info_detail.department=this.info.department;
    this.info_detail.inumber=this.info.inumber;
    this.info_detail.time=this.info_time;
    this.info_detail.doctorName=this.doctors[0].name;
    this.info_detail.doctorTitle=this.doctors[0].title;
    this.info_detail.doctorAvatar=this.doctors[0].avatar;
    this.info_detail.doctorRearch=this.doctors[0].research;
    this.info_detail.cost=this.doctors[0].cost;
    this.info_detail.info_doctor=this.info_doctor;
    if((this.info_time.match(/\(.*?\)/) || [])[0]=='(上午)'){
      var i=0;
      for(i=0;i<20;i++){
        if(this.doctors[0].schedule[0].emptytime[i].status=='empty'){
          this.info_detail.starttime=this.timetable_1[i].startTime;
          this.info_detail.endtime=this.timetable_1[i].endTime;
          break;
        }
      }
      
    }
    else{
      var i=0;
      for(i=0;i<20;i++){
        if(this.doctors[0].schedule[0].emptytime[i].status=='empty'){
          this.info_detail.starttime=this.timetable_2[i].startTime;
          this.info_detail.endtime=this.timetable_2[i].endTime;
          break;
        }
      }
    }
    console.log(this.info_detail)
    console.log(this.info_detail.doctor_id)
    console.log(this.info_doctor)
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
  background-color: #f5f5f5;
  border-left: 30px solid #fff;
  border-right: 30px solid #fff; 
  padding: 20px; 
  margin: 10px;
  margin-bottom: 100px;
  box-sizing: border-box; 
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
  margin: 10px auto;
  border: 1px solid #ccc;  
  padding: 15px;  
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  
} 

.button-container {  
  width: 900px;
  margin: 20px auto;
  display: flex;  
  flex-wrap: wrap;  
  justify-content: flex-start;
}  
  
.button-row {  
  display: flex;  
  margin-bottom: 10px; 
}  

.button-down {  
  width: 120px;
  height: 100px;  
  display: flex;  
  flex-direction: column; 
  justify-content: center;
  align-items: center;
  text-align: center;
  border: none;
  background-color: #eee;
  cursor: pointer;
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
  margin-top: 5px;
}
</style>