<template>  
  <Header :squares2="squares2" />
  <div class="notice-box" style="height: 1000px;">
    <div class="container2">
      <router-link to="/AppointmentRegistration3" class="button2 button-prev" style="text-decoration: none;">上一步</router-link>
      <router-link 
        :to="{
          path:'/AppointmentRegistration6',
          query:{
            name:info.name,
            paymentType:info.paymentType,
            department:info.department,
            time:info_time
          }
        }" class="button2 button-next" v-if="checked" style="text-decoration: none;">
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
        v-for="doctor in doctors"   
        :key="doctor.name"  
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
                <button v-else @click="isClick(doctor.name,daySchedule.time)"
                  @mouseover="hoverButton"  
                  @mouseout="mouseoutButton" 
                  class="schedule-item"
                  :class="{ check : doctor.name===selectDoctor && daySchedule.time===selectDate}">
                  <div class="time-label">{{ daySchedule.time }}</div>  
                  <div>
                    <div class="status" style="color: blue;">余&nbsp;{{ daySchedule.number }}</div> 
                  </div>
                </button>
                <!-- <router-link to="/AppointmentRegistration6" v-else @mouseover="isHovered[dayIndex] = true "   
                  @mouseleave="isHovered[dayIndex] = false" 
                  class="schedule-item" :style="isHovered[dayIndex]? 'color: blue; background-color: #85c400;color:white;' : 'color: blue;'">
                  <div class="time-label">{{ daySchedule.time }}</div>  
                  <div>
                    <div class="status" style="color: blue;">余&nbsp;{{ daySchedule.number }}</div> 
                  </div>
                </router-link> -->
                <!-- <button v-else @mouseover="isHovered[dayIndex] = true "   
                  @mouseleave="isHovered[dayIndex] = false" 
                  class="schedule-item" :style="isHovered[dayIndex]? 'color: blue; background-color: #85c400;color:white;' : 'color: blue;'">
                  <div class="time-label">{{ daySchedule.time }}</div>  
                  <div>
                    <div class="status" style="color: blue;">余&nbsp;{{ daySchedule.number }}</div> 
                  </div>
                </button> -->
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
      today: new Date(), // 今天的日期  
      doctors: [  
        {  
          id:0,
          name: '医生A',  
          title: '主任医师',  
          avatar: 'img/lsy.jpg', // 头像URL  
          research: '生物信息', // 主要研究方向  
          schedule: [  
            {time: '05-11(上午)',status:'empty', number: 10},
            {time: '05-12(下午) ',status: 'full'},
          ],  
          cost:100,
        },
        {  
          id:1,
          name: '医生B',  
          title: '副主任医师',  
          avatar: 'img/touxiang.png', // 头像URL  
          research: '生物信息', // 主要研究方向  
          schedule: [  
            {time: '05-13(上午)',status:'full'},
            {time: '05-12(下午) ',status: 'empty',number:5},
          ],  
          cost:60,
        }, 
        {  
          id:2,
          name: '医生C',  
          title: '副主任医师',  
          avatar: 'img/touxiang (1).png', // 头像URL  
          research: '生物信息', // 主要研究方向  
          schedule: [  
            {time: '05-11(上午)',status:'full'},
            {time: '05-14(下午) ',status: 'full'},
          ],  
          cost:60,
        }, 
        // ... 其他医生数据  
      ],  
      isHovered:[false,false,false,false,false,false,false,false,false,false],
      info:{
        name:'',
        paymentType:'',
        department:'',
      },
      info_time:'',
    };  
  }  ,
  methods: {  
    isClick(doctor,time){
      this.info_time=time;
      this.checked=true;
      this.selectDoctor=doctor;
      this.selectDate=time;
    },
    // 计算接下来7天的日期和周几  
    locatenextSevenDays() {  
      const days = [];  
      for (let i = 0; i < 7; i++) {  
        const date = new Date(this.today);  
        date.setDate(this.today.getDate() + i);  
        days.push({  
          date: this.formatDate(date), // 格式化的日期字符串  
          dayOfWeek: this.formatDayOfWeek(date), // 周几的字符串  
        });  
      }  
      return days;  
    },  
    // 日期格式化函数  
    formatDate(date) {  
      // 根据需要格式化日期，例如 "05-02"  
      const mm = String(date.getMonth() + 1).padStart(2, '0');  
      const dd = String(date.getDate()).padStart(2, '0');  
      return `${mm}-${dd}`;  
    },  
    // 周几格式化函数  
    formatDayOfWeek(date) {  
      // 根据需要返回周几的字符串，例如 "周一"  
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
  },  
  created() {
    this.nextSevenDays=this.locatenextSevenDays()
    for (let i = 0; i < this.nextSevenDays.length; i++) {  
      const day = this.nextSevenDays[i].date;
      console.log(day)
      this.dayStatus[i].status='none';
      this.doctors.forEach(doctor => {  
        doctor.schedule.forEach(scheduleItem => {  
          if (scheduleItem.time.includes(day)) {  
            if (scheduleItem.status === 'full' && this.dayStatus[i].status!='empty') {  
              this.dayStatus[i].status='full';
            } else if (scheduleItem.status === 'empty') {  
              this.dayStatus[i].status='empty';
            }  
          }  
        });  
      });
    }
    this.info.name=this.$route.query.name;
    this.info.paymentType=this.$route.query.paymentType;
    this.info.department=this.$route.query.department;
  }
};  
</script>  
  
<style scoped>  

.notice-box {  
  background-color: #f5f5f5; /* 浅灰色背景 */  
  border-left: 30px solid #fff;
  border-right: 30px solid #fff; /* 白色边框 */  
  padding: 20px; /* 内边距 */  
  padding-bottom: 50px;
  margin: 10px; /* 外边距 */  
  box-sizing: border-box; /* 确保边框和内边距包含在元素的总宽度和高度内 */  
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
  background-color: #003366; /* 这里使用了:hover伪类，而不是Vue方法 */  
  color: white;
}
.date-block.noSelected{
  color: #999;
}
.doctor-intro {  
  display: flex;  
  flex-direction: column;
  justify-content: center;
  /* flex-wrap: wrap;  
  justify-content: space-around;   */
}  
  
.doctor-item {  
  width: 600px; /* 如果你想要每个元素占据整行宽度，可以设置为100% */  
  margin: 10px auto; /* 如果垂直排列，通常只需要上下边距 */
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
  /* font-weight: bold;   */
  padding-left: 10px;
}  
  
.status {  
  /* font-style: italic;   */
  color: #666;  
  padding-right: 20px;
}  
  
/* 根据状态设置不同的背景色或颜色 */  
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