<!-- 预约须知 -->
<template>  
  <!-- 上面的四个框 -->
  <div class="containerlyh" style="display: flex; justify-content: center; align-items: center; height: 180px;">  
    <router-link 
      v-for="(square, index) in squares"  
      :key="index"  
      :to="link[index]"
      class="square"  
      :class="{ 'square-hovered': (square.hovered || index===1) }"  
      @mouseover="square.hovered = true"  
      @mouseout="square.hovered = false">
      {{ info[index] }}  
    </router-link>
  </div>  
  <!-- 下面的8个块 -->
  <div>  
    <div class="container2" style="display: flex; justify-content: center; align-items: center;">  
      <div  
        v-for="(square, index) in squares2"  
        :key="index"  
        class="square2"  
        :class="{ 'square-active2': square.active }"  
        @mouseover="square.hovered = true"  
        @mouseout="square.hovered = false"  
        @click="toggleSquare(index)"  
      >  
        {{ info2[index] }}  
      </div>  
    </div>  
  </div>  
  <!-- 就诊须知内容 -->
  <div class="notice-box">  
    <h2>温 馨 提 示</h2>  
    <p>尊敬的就诊者：</p>  
    <p>您好！我院门诊已实行就诊新流程，敬请注意如下事项：</p>  
    <p style="font-weight: bold;">重点：每日上午的号需在当日8:00前挂，下午的号须在当日14:00前挂</p>
    <p>一、进入院区请正确佩戴口罩。体温≥37.3℃者请到发热门诊就诊。急危重症患者请到急诊就诊。</p>  
    <p>二、按照医院整体改造施工计划，东川门诊4楼大部分区域开始围蔽改造。部分康复科及心中医门诊继续安排在4楼新区出诊，请留意指引标识或咨询现场导诊人员。</p>  
    <p>三、原板房门诊已关停。东川儿科、肝胆内科已分别搬到东川门诊3楼及5楼，东川心理精神科已搬到伟伦楼4楼继续开诊，请留意现场指引。</p> 
    <p>四、心外科、心儿科门诊已搬迁到东川门诊5楼开诊，请留意现场指引。</p>
    <p>五、普通门诊预约后无需先缴诊查费，就诊后交费时一并收取诊查费。但若有欠费（注：看病或咨询后没有开药或开具检验/检查者，也需缴诊查费），在您补交欠费前，将无法预约下次门诊。</p>
    <p>六、请于预约时段前10分钟到自助机或分诊台报到（初诊未实名、越秀区公医及省市直医保门特患者须到分诊台人工报到），请勿过早聚集在医院内候诊。如过时未报到，预约号会自动失效（详见预约手机短信或现场预约凭条内容指引）。</p>
    <p>七、报到后请留意诊间门前叫号屏，可扫码查阅实时排序信息并候诊。</p>
    <p>八、失约管理：累计失约次数超过3次，系统会自动暂停您线上预约挂号功能（但不影响现场挂号），需凭本人身份证明到挂号窗口办理恢复手续。</p>
    <p>九、官网、官微、5G互联网医院、自助机、现场、电话、诊间预约挂号期限统一为14天。</p>  
  </div>  
  <!-- 打勾&按钮 -->
  <div>
    <div class="button-container">
      <router-link v-if="checked" @click="nextSquare" class="router-button" to="/AppointmentRegistration2">
        下一步
      </router-link>
    </div>
    <div class="checkbox-container" style="text-align: center; margin-top: 20px;">  
      <input type="checkbox" id="checkbox" v-model="checked" />  
      <label for="checkbox">我已阅读并同意《个人隐私收集声明》</label>  
    </div>  
    
  </div>
</template>  
  
<script>  
export default {  
  data() {  
    return {  
      squares: [  
        { hovered: false },  
        { hovered: true },  
        { hovered: false },  
        { hovered: false }  
      ] ,
      info: [
        "出诊查询","网上预约看诊","预约流程","医生查询"
      ],
      checked: false,  
      currentSquareIndex: 0,  
      squares2: [  
        { hovered: false, active: true },  
        { hovered: false, active: false },  
        { hovered: false, active: false },  
        { hovered: false, active: false },  
        { hovered: false, active: false },  
        { hovered: false, active: false },  
        { hovered: false, active: false },  
        { hovered: false, active: false }  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      link:['/TableSearch','/AppointmentRegistration','/Picture','/DoctorSearch'],

    };  
  }  ,
  methods: {  
    toggleSquare(index) {  
      this.currentSquareIndex = index;   
      this.currentSquareIndex = 1;
      this.checked = false;
    },  
    nextSquare(){

    }
  }  
};  
</script>  
  
<style scoped>  
.containerlyh {  
  flex-wrap: wrap;  
  height: 300px;
  margin: auto auto;
}  
  
.square {  
  font-size: large;
  width: 150px;  
  height: 120px;  
  display: flex;  
  justify-content: center;  
  align-items: center;  
  margin: 0 10px;  
  border-radius: 10px;
  background-color: #e5ecff;  
  color: #000000;  
  cursor: pointer;  
  border: none;
  transition: background-color 0.3s, color 0.3s; /* 添加过渡效果 */  
  text-decoration: none;
}  
  
.square-hovered {  
  background-color: #003366;  
  color: #FFFFFF;  
}  

.container2 {  
  display: flex;  
  flex-wrap: wrap;  
  justify-content: center;  
}  
  
.square2 {  
  width: 120px;  
  height: 50px;  
  display: flex;  
  justify-content: center;  
  align-items: center;  
  margin: 0 10px 10px 0;  
  background-color: #e0e0e0;  
  color: #808080;  
  cursor: pointer;  
  transition: background-color 0.3s, color 0.3s;  
}  
  
.square-hovered2 {  
  background-color: #003366;  
  color: #FFFFFF;  
}  
  
.square-active2 {  
  background-color: orange;  
  color: white;  
}  
  
.checkbox-container {  
  width: 100%;  
  padding: 10px;  
  box-sizing: border-box;  
}  
  
.router-button {  
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
  background-color: #003366; 
  color: #fcfcfc;
  text-decoration: none;
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
.notice-box h2 {  
  text-align: center;
  margin-bottom: 20px;
}  
.notice-box p {  
  margin-bottom: 10px;
}  
</style>