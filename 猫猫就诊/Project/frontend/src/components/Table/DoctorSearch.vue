<!-- 医生查询 -->
<template>  
  <div class="containerlyh" style="display: flex; justify-content: center; align-items: center; height: 180px;">  
    <router-link 
      v-for="(square, index) in squares"  
      :key="index"  
      :to="link[index]"
      class="square"  
      :class="{ 'square-hovered': (square.hovered || index==3) }"  
      @mouseover="square.hovered = true"  
      @mouseout="square.hovered = false">
      {{ info[index] }}  
    </router-link>
  </div>
  
  
  <div class="container2">  
    <div class="input-container" style="width: 500px;height: 100px;margin: auto auto;">
      <div class="chaxun">  
        <el-autocomplete  
          v-model="search"  
          :fetch-suggestions="querySearch"  
          placeholder="请输入医生姓名"  
          @select="handleSelect"  
          style="width: 300px; height: 40px"
        >  
          <template #default="{ item }">  
            <div class="el-input__icon">{{ item.name }}</div>  
          </template>  
          
        </el-autocomplete>  
        <el-button
          color="#DBA979"
          :dark="isDark"
          plain
          class="searchButton"
          style="width: 80px; height: 40px"
          >查询</el-button
        >
        <p>{{ search }}</p>
      </div>  
    </div>

    <div class="doctor-intro">  
      <div   
        v-for="doctor in filteredDoctors(square_selected)"   
        :key="doctor.name"  
        class="doctor-item"
      >  
        <div class="doctor-header"> 
          <img :src="doctor.avatar" alt="" class="avatar">
          <div class="info">  
            <div style="display: flex;  align-items: center;">
              <div class="name">{{ doctor.name }}</div>  
              <div style="font-size: 12px;">{{ doctor.title }}</div>  
            </div>
            <div class="research">{{ doctor.research }}</div>  
          </div>  
        </div>  
      </div>
    </div>
    <!-- 圆形按钮 -->  
    <div class="circle-buttons">  
      <button  
        v-for="(label, index) in departmentLetters"  
        :key="index"  
        :class="{ selected: isActive(index) }"  
        @click="selectDepartment(index)"  
      >  
        {{ label }}  
      </button>  
    </div>  
    
    <!-- 方形按钮 -->  
    <div class="square-buttons">  
      <div  
        v-for="(department, index) in filteredDepartments"  
        :key="index"  
        @click="square_select(department.id)"
      >  
        <button class="department-button" :class="{'department-button-selected':department.id==square_selected}">{{ department.name }}</button>  
      </div>  
    </div> 
    
    
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
        { hovered: false },  
        { hovered: true }  
      ] ,
      info: [
        "出诊查询","网上预约看诊","预约流程","医生查询"
      ],
      link:['/TableSearch','/AppointmentRegistration','/Picture','/DoctorSearch'],

      departments: [  
        { id:0, name: '心血管内科', pinyin:'Xinxueguanneike' },  
        { id:1, name: '呼吸与危重症医学科' ,pinyin:'Huxi'},  
        { id:2, name: '内分泌科' ,pinyin:'Neifenmi'},  
        { id:3, name: '肾内科' ,pinyin:'Shenneike'},  
        { id:4, name: '血液内科' ,pinyin:'Xueye'},
        { id:5, name: '消化科' ,pinyin:'Xiaohua'},
        { id:6, name: '风湿免疫科' ,pinyin:'Fengshi'},
        { id:7, name: '老年内科' ,pinyin:'Laonian'},
        { id:8, name: '神经内科' ,pinyin:'Shenjing'},
        { id:9, name: '感染疾病科' ,pinyin:'Ganran'},
        { id:10, name: '急诊科' ,pinyin:'Jizhen'},
        { id:11, name: '皮肤科' ,pinyin:'Pifu'},
        { id:12, name: '中医科' ,pinyin:'Zhongyi'},
        { id:13, name: '职业病科' ,pinyin:'Zhiye'},
        { id:14, name: '肿瘤放疗科' ,pinyin:'Zhongliu'},
        { id:15, name: '肿瘤化疗与放射病科' ,pinyin:'Zhongliu'},
        { id:16, name: '儿科' ,pinyin:'Erke'},
        { id:17, name: '体检中心' ,pinyin:'Tijian'},
        { id:18, name: '全科医学科' ,pinyin:'Quanke'},
        { id:19, name: '普通外科' ,pinyin:'Puwai'},  
        { id:20, name: '骨科' ,pinyin:'Guke'},  
        { id:21, name: '泌尿外科' ,pinyin:'Miniao'},  
        { id:22, name: '胸外科' ,pinyin:'Xiongwai'},  
        { id:23, name: '心脏外科' ,pinyin:'Xinwai'},
        { id:24, name: '神经外科' ,pinyin:'Shenwai'},
        { id:25, name: '整形科' ,pinyin:'Zhengxing'},
        { id:26, name: '介入血管外科' ,pinyin:'Jieru'},
        { id:27, name: '危重医学科' ,pinyin:'Weizhong'},
        { id:28, name: '运动医学科' ,pinyin:'Yundong'},
        { id:29, name: '康复医学科' ,pinyin:'Kangfu'},
        { id:30, name: '妇产科' ,pinyin:'Fuchan'},
        { id:31, name: '生殖医学科' ,pinyin:'Shengzhi'},
        { id:32, name: '眼科' ,pinyin:'Yanke'},
        { id:33, name: '耳鼻喉科' ,pinyin:'Erbihou'},
        { id:34, name: '口腔科' ,pinyin:'Kouqiang'},
        { id:35, name: '麻醉科' ,pinyin:'Mazui'},
        { id:36, name: '疼痛医学中心' ,pinyin:'Tengtong'},
        { id:37, name: '放射科' ,pinyin:'Fangshe'},  
        { id:38, name: '超声医学科' ,pinyin:'Chaosheng'},  
        { id:39, name: '核医学科' ,pinyin:'He'},  
        { id:40, name: '检验科' ,pinyin:'Jianyan'},  
        { id:41, name: '输血科' ,pinyin:'Shuxue'},
        { id:42, name: '药剂科' ,pinyin:'Yaoji'},
        { id:43, name: '手术室' ,pinyin:'Shoushu'},
        { id:44, name: '病理科' ,pinyin:'Bingli'},
        { id:45, name: '病案科' ,pinyin:'Bingan'},
        { id:46, name: '临床营养科' ,pinyin:'Linchuang'}, 
      ],
      doctors: [  
        
      ],     
      departmentLetters: ['ALL', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],  

      selectedLetterIndex: -1, 
      square_selected:-1, 
      select:false,

      search:'',
      search_name_id:-1,
    };  
  }  ,
  computed: {   
    filteredDepartments() {   
      if (this.selectedLetterIndex === -1) {    
        return this.departments;  
      } else {   
        const letter = this.departmentLetters[this.selectedLetterIndex].toUpperCase();  
        return this.departments.filter(department =>  
          department.pinyin[0].toUpperCase() === letter  
        );  
      }  
    }
  },  
  methods: {    
    selectDepartment(index) { 
      if(index==0)
        this.selectedLetterIndex=-1; 
      else
        this.selectedLetterIndex = index;  
    },  
    isActive(index) {  
      if(index==0)
        return this.selectedLetterIndex===-1;
      return this.selectedLetterIndex === index;  
    },  
    square_select(index){
      this.square_selected=index;
      this.select=true;
      this.search_name_id=-1;
    },
    filteredDoctors(id) {  
      if(this.search_name_id!=-1){
        return this.doctors.filter(doctor =>
          doctor.name==this.doctors[this.search_name_id-1].name
        );
      }
      else if(this.square_selected!=-1){
        return this.doctors.filter(doctor =>
          doctor.department==this.departments[this.square_selected].name
        );
      }
      
    },  
    querySearch(queryString, cb) {   
      console.log(queryString)
      const results = this.doctors.filter(doctor =>  
        doctor.name.includes(queryString)  
      ); 
      console.log(results)
      cb(results);  
    },  
    handleSelect(item) {  
      this.search_name_id=item.id;
      console.log(item);  
      input.value = item.name;
    },
    getDutyData() {
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          action: 'getDoctorsData',
        };
        this.$axios.post('api/doctors/list/', requestData)
          .then(function (response) {
            ts.doctors = response.data['doctors'];
            console.log(ts.doctors);
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
      });
    }, 
  },
  mounted(){
    this.getDutyData();
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
  transition: background-color 0.3s, color 0.3s; /* 添加过渡效果 */  
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
  width: 200px; /* 假设有10px的间距 */  
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