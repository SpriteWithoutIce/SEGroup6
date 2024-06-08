<!-- 选择首诊复诊 -->
<template>  
  <Header :squares2="squares2"/> 
  
  <!-- 首诊/复诊 -->
  <div class="notice-box" style="height: 400px;">  
    <!-- 上一步/下一步 -->
    <div class="container2">  
      <router-link to="/AppointmentRegistration" class="button2 button-prev">上一步</router-link>
      <router-link :to="{path:'/AppointmentRegistration3',query:{select:selected}}" class="button2 button-next" v-if="checked">下一步</router-link>
    </div> 
    <div class="containerlyh" style="display: flex; justify-content: center; align-items: center; height: 180px;">
      <div  
        v-for="(square, index) in squares3"  
        :key="index"  
        class="square3"  
        :class="{ 'square3-hovered': (square.hovered || index==selected) }"  
        @mouseover="square.hovered = true"  
        @mouseout="square.hovered = false"  
        @click="clickbutton(index)"
      >  
        {{ treat[index] }}  
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
      selected:-1,
      currentSquareIndex: 0,  
      squares2: [  
        { hovered: false, active: false ,done: true},  
        { hovered: false, active: true ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      squares3: [  
        { hovered: false, active: false },  
        { hovered: false, active: false },  
      ]  ,
      treat:["首诊","复诊"]
    };  
  }  ,
  methods: {  
    toggleSquare(index) {  
      this.currentSquareIndex = index;   
      this.currentSquareIndex = 1;
      this.checked = false;
    },  
    nextSquare(){

    },
    clickbutton(index){
      this.checked=true;
      this.selected=index;
    },
  }  ,
};  
</script>  
  
<style scoped>  
.container {  
  flex-wrap: wrap;  
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
  transition: background-color 0.3s, color 0.3s;
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

.square3 {  
  font-size: large;
  width: 150px;  
  height: 140px;  
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

.square3-hovered {  
  background-color: #003366;  
  color: #FFFFFF;  
}  
.square-done {
  background-color: #003366;  
  color: #FFFFFF;
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
</style>