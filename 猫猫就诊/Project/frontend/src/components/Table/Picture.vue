<!-- 预约流程 -->
<template>  
  <div class="containerlyh" style="display: flex; justify-content: center; align-items: center; height: 180px;">  
    <router-link 
      v-for="(square, index) in squares"  
      :key="index"  
      :to="link[index]"
      class="square"  
      :class="{ 'square-hovered': (square.hovered || index==2) }"  
      @mouseover="square.hovered = true"  
      @mouseout="square.hovered = false">
      {{ info[index] }}  
    </router-link>
  </div>
  
  
  <div class="container2">  
    <img src="/static/img/appointment/img.png" alt="" style="width: 40%;">
    
  </div>  
</template>  
  
<script>  
import Header from './Appointments/AppointmentHeader.vue'
import { ref } from 'vue';  
export default {  
  components: {
    Header,
  },
  data() {  
    
    return {  
      squares: [  
        { hovered: false },  
        { hovered: false },  
        { hovered: true },  
        { hovered: false }  
      ] ,
      info: [
        "出诊查询","网上预约看诊","预约流程","医生查询"
      ],
      link:['/TableSearch','/AppointmentRegistration','/Picture','/DoctorSearch'],

      
    };  
  }  ,
  
  methods: {  
    
  },
  created(){
    
  }
};  
</script>  
  
<style scoped>  
.container2{
  display: flex; 
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.containerlyh {  
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

.circle-buttons {  
  display: flex;  
  justify-content: space-between;  
  width: 1000px;
  margin: auto auto;
  font-size: medium;
}  
  
.circle-buttons button {  
  border: none;  
  border-radius: 17px;  
  width: 34px;
  height: 34px; 
  padding: auto 5px;
  color: black;
  background-color: #e5ecff;  
  cursor: pointer;  
}  
  
.circle-buttons button.selected {  
  background-color: #003366;  
  color: white;
}  
  
.square-buttons {  
  display: flex;  
  flex-wrap: wrap;  
  padding-left: 100px;
  width:1000px;
  margin: 10px auto;
}  
  
.department-button {  
  display: flex;  
  justify-content: center;  
  align-items: center;  
  width: 200px;
  margin: 10px;  
  background-color: white;  
  padding: 10px;  
  border: 1px solid gray;
  text-align: center; 
  cursor: pointer;
}  
  
.department-button button {  
  width: 100%;  
  text-align: center;  
  border: none;
  background-color: white;
  cursor: pointer;
}  
.department-button-selected{
  background-color: orange;

}

.doctor-intro {  
  display: flex;  
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
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
  margin-right: 20px;
}  
  
.title, .research {  
  font-size: 14px;  
}  

.doctor-item {    
  border: 1px solid #ccc; 
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px;  
  margin: 10px; 
  width: 500px;  
  text-align: center;
}  

.searchTable {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px auto;
  width: 200px;
}

.chaxun {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.shuru {
  position: relative;
}
.searchButton {
  position: relative;
  margin-left:10px;
}
.input-container {
  background-color: white;
  display: flex;
  flex-direction: row; 
  align-items: center;
  
}
</style>