<!-- 显示医生排班 -->
<template>  
  <Header :squares2="squares2" />
  <div class="notice-box" style="height: 1000px;">
    <div class="container2">
      <router-link :to="{
        path:'/AppointmentRegistration4',
        query:{
          name:info.name,
          paymentType:info.paymentType,
          department:info.department,
          inumber:info.inumber,
        }}" class="button2 button-prev" style="text-decoration: none;">上一步</router-link>
      <router-link 
        :to="{
          path:'/AppointmentRegistration6',
          query:{
            info_doctor:JSON.stringify(info)
          }
        }" class="button2 button-next" style="text-decoration: none; " v-if="checked">
        下一步
      </router-link>
    </div>
    
    <!-- 顶部日期块 -->  
    <div class="date-blocks">
      <button   
        class="date-block"   
        v-for="(day, index) in nextSevenDays"   
        :key="index"  
        :class="{noSelected:dayStatus[index].status!='empty'}"
        @mouseover="hoverButton"
        @click="clickButton(day)"
      > 
        <div>{{ day.date }}</div>  
        <div v-if="index==0">今天</div> 
        <div v-else-if="index==1">明天</div> 
        <div v-else>{{ day.dayOfWeek }}</div>  
        <div v-if="dayStatus[index].status=='none'">无排班</div>
        <div v-else-if="dayStatus[index].status=='full'">约满</div>
        <div v-else>有号</div>
      </button> 
    </div>  
  
    <!-- 底部医生介绍 -->  
    <div class="doctor-intro">  
      <div   
        v-for="(doctor,doctorIndex) in doctors"   
        :key="doctorIndex"  
      >  
        <div v-if="doctorHasScheduleForDate(doctor, selectedDate)" class="doctor-item">
          <div class="doctor-header"> 
            <img :src="doctor.avatar" alt="" class="avatar">
            <div class="info">  
              <div class="name">{{ doctor.name }}</div>  
              <div class="title">{{ doctor.title }}</div>  
              <div class="research">{{ doctor.research }}</div>  
            </div>  
          </div>  
          <div class="schedule">  
            <div v-for="(daySchedule, dayIndex) in doctor.schedule"   
                    :key="dayIndex">
              <div v-if="dayHasScheduleForDate(daySchedule,selectedDate)">
                <button class="schedule-item1" v-if="daySchedule.status!='empty'">
                  <div class="time-label">{{ daySchedule.time }}
                  </div>  
                  <div>
                    <div class="status">约满</div> 
                  </div>
                </button>
                <button v-else @click="isClick(doctor.name,daySchedule.time,dayIndex,doctorIndex)"
                  @mouseover="hoverButton"  
                  @mouseout="mouseoutButton" 
                  class="schedule-item"
                  :class="{ check : doctor.name===selectDoctor && daySchedule.time===selectDate}">
                  <div class="time-label">{{ daySchedule.time }}</div>  
                  <div>
                    <div class="status" style="color: blue;">余&nbsp;{{ daySchedule.number }}</div> 
                  </div>
                </button>
              </div> 
            </div>  
          </div>  
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
        { hovered: false, active: true ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      nextSevenDays: [],
      dayStatus:[
        {'status':'none'},
        {'status':'none'},
        {'status':'none'},
        {'status':'none'},
        {'status':'none'},
        {'status':'none'},
        {'status':'none'},
      ],
      selectedDate: null,
      selectDoctor:'',
      selectDate:'',
      today: new Date(),
      doctors: [  
        
      ],  
      isHovered:[false,false,false,false,false,false,false,false,false,false],
      info:{
        name:'',
        paymentType:'',
        department:'',
        inumber:'',
        info_time:'',
        doctor:{},
        day_index:'',
      },
    };  
  }  ,
  methods: {  
    getDutyData() {
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          action: 'getNextSevenDaysDuty',
          department: this.$route.query.department,
        };
        console.log(requestData.department)
        this.$axios.post('/api/duty/next_seven_days/', requestData)
          .then(function (response) {
            ts.doctors = response.data['duty'];
            console.log(ts.doctors);
            resolve();
          })
          .catch(function (error) {
            console.log(error);
            reject(error);
          });
      });
    },
    isClick(doctor,time,dayIndex,doctorIndex){
      this.info.info_time=time;
      this.checked=true;
      this.selectDoctor=doctor;
      this.selectDate=time;
      this.info.day_index=dayIndex;
      this.info.doctor=this.doctors[doctorIndex];
    },
    locatenextSevenDays() {  
      const days = [];  
      for (let i = 0; i < 7; i++) {  
        const date = new Date(this.today);  
        date.setDate(this.today.getDate() + i);  
        days.push({  
          date: this.formatDate(date),
          dayOfWeek: this.formatDayOfWeek(date),
        });  
      }  
      return days;  
    },    
    formatDate(date) {  
      const mm = String(date.getMonth() + 1).padStart(2, '0');  
      const dd = String(date.getDate()).padStart(2, '0');  
      return `${mm}-${dd}`;  
    },  
    formatDayOfWeek(date) {  
      const days = ['日', '一', '二', '三', '四', '五', '六'];  
      return `周${days[date.getDay()]}`;  
    },  
    clickButton(day){
      this.selectedDate=day.date
    },
    doctorHasScheduleForDate(doctor, date) {  
      return doctor.schedule.some(item => item.time.includes(date));  
    }, 
    dayHasScheduleForDate(daySchedule, date) {  
      return daySchedule.time.includes(date);  
    },  
    hoverButton() {  
    },  
    mouseoutButton() {  
    },
    checkTime(timeString) {  
      const [datePart, timeOfDay] = timeString.split('(');  
      const [month, day] = datePart.split('-').map(str => parseInt(str, 10));  
      const isMorning = timeOfDay.includes('上午');  
      const time = isMorning ? '08:00:00' : '14:00:00'; 
 
      const compareDate = new Date();  
      compareDate.setMonth(month - 1);
      compareDate.setDate(day);  
      compareDate.setHours(...time.split(':').map(Number));  
      compareDate.setMinutes(0);  
      compareDate.setSeconds(0);  
      compareDate.setMilliseconds(0);  

      const now = new Date();   
      if (compareDate.getDate() !== now.getDate() || compareDate.getMonth() !== now.getMonth()) {  
        return true;
      }   
      if (now > compareDate) {  
        return false;
      }  
      return true;  
    },
  },
  mounted() {
    console.log(this.$route.query.department)
    console.log(this.$route.query.paymentType)
    this.getDutyData().then(() => {
      console.log("111");
      console.log(this.doctors);
      this.nextSevenDays = this.locatenextSevenDays();
      for (let i = 0; i < this.nextSevenDays.length; i++) {
        const day = this.nextSevenDays[i].date;
        this.dayStatus[i].status = 'none';
        this.doctors.forEach(doctor => {
          doctor.schedule.forEach(scheduleItem => {
            if (scheduleItem.time.includes(day)) {
              if(i==0){
                const [datePart, timeOfDay] = scheduleItem.time.split('(');  
                const [month, day] = datePart.split('-').map(str => parseInt(str, 10));  
                const isMorning = timeOfDay.includes('上午');  
                const time = isMorning ? '08:00:00' : '14:00:00'; 
                const compareDate = new Date();  
                compareDate.setMonth(month - 1); 
                compareDate.setDate(day);  
                compareDate.setHours(...time.split(':').map(Number));  
                compareDate.setMinutes(0);  
                compareDate.setSeconds(0);  
                compareDate.setMilliseconds(0);  
                const now = new Date(); 
                if (now > compareDate) {  
                  scheduleItem.status = 'full'
                }
              }
              if (scheduleItem.status === 'full' && this.dayStatus[i].status != 'empty') {
                this.dayStatus[i].status = 'full';
              } else if (scheduleItem.status === 'empty') {
                this.dayStatus[i].status = 'empty';
              }
            }
            console.log(this.dayStatus[i].status);
          });
        });
      }
    })
    // console.log("111");
    // console.log(this.doctors);
    // this.nextSevenDays = this.locatenextSevenDays();
    // for (let i = 0; i < this.nextSevenDays.length; i++) {
    //   const day = this.nextSevenDays[i].date;
    //   this.dayStatus[i].status = 'none';
    //   this.doctors.forEach(doctor => {
    //     doctor.schedule.forEach(scheduleItem => {
    //       if (scheduleItem.time.includes(day)) {
    //         if (scheduleItem.status === 'full' && this.dayStatus[i].status != 'empty') {
    //           this.dayStatus[i].status = 'full';
    //         } else if (scheduleItem.status === 'empty') {
    //           this.dayStatus[i].status = 'empty';
    //         }
    //       }
    //       console.log(this.dayStatus[i].status);
    //     });
    //   });
    //   this.info.name = this.$route.query.name;
    //   this.info.paymentType = this.$route.query.paymentType;
    //   this.info.department = this.$route.query.department;
    //   console.log(this.doctors);
    // }
  },
  created(){
    this.info.name = this.$route.query.name;
    this.info.paymentType = this.$route.query.paymentType;
    this.info.department = this.$route.query.department;
    this.info.inumber=this.$route.query.inumber;
    console.log(this.info.department)
  }
}
</script>  
  
<style scoped>  

.notice-box {  
  background-color: #f5f5f5;
  border-left: 30px solid #fff;
  border-right: 30px solid #fff; 
  padding: 20px;
  padding-bottom: 50px;
  margin: 10px;
  box-sizing: border-box;
}  

.container2 {  
  display: flex;  
  flex-wrap: wrap;  
  justify-content: center;  
  margin-bottom: 20px;
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

.date-blocks {  
  display: flex;  
  justify-content: space-around;  
  margin-bottom: 20px;  
}  
  
.date-block {  
  width: 120px;  
  text-align: center;  
  border: 1px solid #ccc;  
  padding: 10px;  
  margin: 0 5px;  
}  
.date-block:hover{
  background-color: #003366;
  color: white;
}
.date-block.noSelected{
  color: #999;
}
.doctor-intro {  
  display: flex;  
  flex-direction: column;
  justify-content: center;
}  
  
.doctor-item {  
  width: 600px;
  margin: 10px auto;
  border: 1px solid #ccc;  
  padding: 15px;  
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  
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
  margin-right: 10px;  
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
  
.schedule {  
  margin-top: 15px;  
}  
  
.schedule-item {  
  display: flex;  
  justify-content: space-between;  
  align-items: center;  
  margin-bottom: 5px;  
  border: 1px solid #999;
  background-color: white;
  height: 35px;
  border-radius: 5px;
  width: 550px;
} 
.schedule-item1 {  
  display: flex;  
  justify-content: space-between;  
  align-items: center;  
  margin-bottom: 5px;  
  border: 1px solid #999;
  background-color: white;
  height: 35px;
  border-radius: 5px;
  width: 550px;
}  
.schedule-item:hover {
  background-color: #85c400;
  color: white;
  cursor: pointer;
}
.schedule-item.check{
  background-color: #85c400;
  color: white;
}
.time-label {  
  padding-left: 10px;
}  
  
.status {  
  color: #666;  
  padding-right: 20px;
}  
.status.有号 {  
  color: green;  
}  
  
.status.约满 {  
  color: red;  
}  
  
.status.无排班 {  
  color: #999;  
}  
</style>