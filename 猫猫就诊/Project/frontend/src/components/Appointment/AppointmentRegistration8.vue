<template>  
  <Header :squares2="squares2"/> 
  <div class="notice-box" style="height: 1400px;">  
    <!-- 上一步/下一步 -->
    
    <div style="width: 800px;margin: 20px auto;"> 
      <div class="subline">您好，您已预约成功。订单详情如下</div>
      <div class="subline">
        <div>就诊人：</div>
        <div class="detail">{{ info1.name }}</div>
      </div>
      <div class="subline">
        <div>医生：</div>
        <div class="detail">{{ info1.doctorName }}</div>
      </div>
      <div class="subline">
        <div>就诊医院：</div>
        <div class="detail">猫猫就诊</div>
      </div>
      <div class="subline">
        <div>科室：</div>
        <div class="detail">{{ info1.department }}</div>
      </div>
      <div class="subline">
        <div>就诊时段：</div>
        <div class="detail">2024-{{ info1.time }}&nbsp;{{ info1.starttime }}-{{ info1.endtime }}</div>
      </div>
      <div class="subline">
        <div class="detail">建议到诊时间：</div>
        <div class="detail">{{ timeBeforeTenMinutes(info1.starttime) }}</div>
      </div>
      <div class="subline">
        <div>医事服务费：</div>
        <div class="detail" v-if="this.info1.paymentType=='医保'">0元</div>
        <div class="detail" v-else>{{ info1.cost }}元</div>
      </div>
      <div class="subline">
        <div>就诊序号：</div>
        <div class="detail">{{ info1.number }}</div>
      </div>
      <div class="subline">
        <div>挂号时间：</div>
        <div>{{ currentTime }}</div>
      </div>
      <div class="subline">
        <div>温馨提示：</div>
      </div>
      <div>
        <div style="margin: 5px auto;">
        (1)医保患者请携带挂号凭证(电子就医卡二维码)和医保卡，到自助机或挂号/预约取号窗口缴费取号，再去分诊台分诊。(取号时间:上午号时间11:30前、下午号16:30前)
        </div>
        <div style="margin: 5px auto;">
        (2)非医保患者请携带挂号凭证(电子就医卡二维码)，无需取号即可去分诊台分诊。
        </div>
        <div style="margin: 5px auto;">
          (3)所有挂号在就诊当日上午号12:00前、下午号17:00前有效，过有效时间后不再安排就诊及退费。
        </div>
        <div style="margin: 5px auto;">
          倡导文明绿色出行，共享单车请入栏停放。如需驾车,中大型轿车及SUV车型沿道路最内侧的排队通道进入，标准尺寸小型轿车工作日8-16时周末8-12时可直接进入医院。
        </div>
      </div>
      
    </div>
    <div class="container2">  
      <router-link :to="{
        path: '/AppointmentRegistration7',
        query:{
          info:JSON.stringify(info1.info_last)
        }}" class="button2 button-prev" style="text-decoration: none;">上一步</router-link>
      <button class="button2 button-next" @click="submit">确认</button>  
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
      checked: false,  
      currentSquareIndex: 0,  
      squares2: [  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: true ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      form:{
        address:'北医三院',
        selectTimeTable:{time: '05-09(上午)', startTime:"08:00", endTime:"08:10"},
        order:100,
        people: {
          name: '林艺涵',  
          gender:'女',
          idType:'身份证',
          phone:'18518559617',
          number:'370883200503160423',
        },
        isMedicalInsurance:true,
        doctor:'医生A',
        department:'心血管内科',
        num:15,
      },
      currentTime: '',
      info1:{},
    };  
  }  ,
  
  methods: {  
    timeBeforeTenMinutes(timeStr) {  
      // 假设时间字符串格式为 HH:mm  
      var [hoursStr, minutesStr] = timeStr.split(':').map(Number);  
      var hours = hoursStr;  
      var minutes = minutesStr - 10; // 减去10分钟  
  
      // 处理分钟数小于0的情况  
      if (minutes < 0) {  
        hours -= 1; // 如果分钟数为负，则小时数减1  
        minutes += 60; // 并且分钟数加上60  
      }  
  
      // 格式化小时和分钟为两位数  
      const formattedHours = String(hours).padStart(2, '0');  
      const formattedMinutes = String(minutes).padStart(2, '0');  
  
      // 返回格式化后的时间字符串  
      return `${formattedHours}时${formattedMinutes}分`;  
    },
    updateCurrentTime() {  
      const now = new Date();  
      const formattedDateTime = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;  
      this.currentTime = formattedDateTime;  
    },
    
  },
  created(){
    this.updateCurrentTime();  
    const orderStr = this.$route.query.order;  
    if (orderStr) {  
      this.info1 = JSON.parse(orderStr);  
    }
    
  },
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
.subline{
  display: flex;
  height: 30px;
  margin: 5px auto;
}
.detail{
  color: #1736ff;
}
</style>