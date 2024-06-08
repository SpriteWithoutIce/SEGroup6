<!-- 选择科室 -->
<template>  
  <Header :squares2="squares2" />
  <div class="notice-box">  
    <div class="department-selector">  
      <div class="left-buttons">  
        <button  
          v-for="department in departments"  
          :key="department.id"  
          :class="{ active: selectedDepartment === department.id }"  
          @click="selectDepartment(department.id)"  
          class="round-button"  
        >  
          {{ department.name }}  
        </button>  
      </div>  
    
      <div class="right-buttons">  
        <div class="selected-department-container">  
          <div style="height: 30px;">您选择的科室为：</div>
          <div class="sub-department-titles selected-department-title" style="width: 200px;height: 30px;">  
            {{ selectedDepartmentName }}  
          </div>  
          <div class="container2">  
            <router-link 
              :to="{
                path:'/AppointmentRegistration3',
                query:{
                  select:this.selected
                }
              }"
              class="button2 button-prev">上一步</router-link>
            <router-link 
              :to="{
                path:'/AppointmentRegistration5',
                query:{
                  name:info.name,
                  paymentType:info.paymentType,
                  inumber:info.inumber,
                  department:selectedDepartmentName
                }
              }" class="button2 button-next"  v-if="checked">
              下一步
            </router-link>
          </div> 
        </div>   
        <div class="sub-department-titles">  
          <div class="sub-department-title-chinese" v-if="selectedDepartment">{{ getSubDepartmentsName(selectedDepartment)[0].subname }}</div>  
          <div class="sub-department-title-english" v-if="selectedDepartment">{{ getSubDepartmentsName(selectedDepartment)[0].enbame }}</div>  
        </div>   
        <div class="sub-department-buttons">  
          <button  
            v-for="subDepartment in getSubDepartments(selectedDepartment)"  
            :key="subDepartment.id"  
            class="square-button"  
            @mouseover="hoverButton"  
            @mouseout="mouseoutButton"
            @click="selectSubDepartment(subDepartment.id)"  
            :class="{ selected: selectedSubDepartment === subDepartment.id && selectedDepartmentRight===selectedDepartment}"
          >  
            {{ subDepartment.name }}  
          </button>  
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
        { hovered: false, active: true ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
      departments: [  
        { id: 'internal', name: '内科' },  
        { id: 'surgical', name: '外科' },  
        { id: 'medical_tech', name: '医技科室' },  
      ],  
      selectedDepartment: 'internal',  
      hoveredButton: 'internal',  
      selectedDepartmentName: '', // 用于存储选中的部门名称
      selectedDepartmentRight:'',
      selectedSubDepartment: '',
      selectedSubDepartmentName:'',
      info:{
        name:'',
        paymentType:'',
        inumber:'',
      },
      selected:0,
    };  
  }  ,
  methods: {  
    selectDepartment(id) {  
      this.selectedDepartment = id;  
    },  
    selectSubDepartment(id){
      this.selectedDepartmentName=this.getSubDepartments(this.selectedDepartment)[id-1].name
      
      this.selectedDepartmentRight=this.selectedDepartment
      this.selectedSubDepartment=this.getSubDepartments(this.selectedDepartment)[id-1].id
      this.checked=true
    },
    getSubDepartmentsName(departmentId){
      if (departmentId === 'internal'){
        return [{subname:'内科系统',enbame:'Internal Medician System'}]
      }
      else if(departmentId === 'surgical'){
        return [{subname:'外科系统',enbame:'Surgical System'}]
      }
      else if(departmentId === 'medical_tech'){
        return [{subname:'医技科室',enbame:'Medical Technology Department'}]
      }
    },
    // 这里是要显示在屏幕上的科室名字，是固定的
    getSubDepartments(departmentId) {  
      if (departmentId === 'internal') {  
        return [  
          { id: 1, name: '心血管内科' },  
          { id: 2, name: '呼吸与危重症医学科' },  
          { id: 3, name: '内分泌科' },  
          { id: 4, name: '肾内科' },  
          { id: 5, name: '血液内科' },
          { id: 6, name: '消化科' },
          { id: 7, name: '风湿免疫科' },
          { id: 8, name: '老年内科' },
          { id: 9, name: '神经内科' },
          { id: 10, name: '感染疾病科' },
          { id: 11, name: '急诊科' },
          { id: 12, name: '皮肤科' },
          { id: 13, name: '中医科' },
          { id: 14, name: '职业病科' },
          { id: 15, name: '肿瘤放疗科' },
          { id: 16, name: '肿瘤化疗与放射病科' },
          { id: 17, name: '儿科' },
          { id: 18, name: '体检中心' },
          { id: 19, name: '全科医学科' },
        ];  
      }  
      else if (departmentId === 'surgical') {  
        return [  
          { id: 1, name: '普通外科' },  
          { id: 2, name: '骨科' },  
          { id: 3, name: '泌尿外科' },  
          { id: 4, name: '胸外科' },  
          { id: 5, name: '心脏外科' },
          { id: 6, name: '神经外科' },
          { id: 7, name: '整形科' },
          { id: 8, name: '介入血管外科' },
          { id: 9, name: '危重医学科' },
          { id: 10, name: '运动医学科' },
          { id: 11, name: '康复医学科' },
          { id: 12, name: '妇产科' },
          { id: 13, name: '生殖医学科' },
          { id: 14, name: '眼科' },
          { id: 15, name: '耳鼻喉科' },
          { id: 16, name: '口腔科' },
          { id: 17, name: '麻醉科' },
          { id: 18, name: '疼痛医学中心' },
        ];  
      }  
      else if (departmentId === 'medical_tech'){
        return [  
          { id: 1, name: '放射科' },  
          { id: 2, name: '超声医学科' },  
          { id: 3, name: '核医学科' },  
          { id: 4, name: '检验科' },  
          { id: 5, name: '输血科' },
          { id: 6, name: '药剂科' },
          { id: 7, name: '手术室' },
          { id: 8, name: '病理科' },
          { id: 9, name: '病案科' },
          { id: 10, name: '临床营养科' },
        ];  
      }
    },  
    hoverButton() {  
    },  
    mouseoutButton() {  
    },  
  }  ,
  created(){
    this.info.name=this.$route.query.name;
    this.info.paymentType=this.$route.query.paymentType;
    this.selected=this.$route.query.selected;
    this.info.inumber=this.$route.query.number;
  }
};  
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
.department-selector {  
  display: flex;  
  justify-content: space-between;  
  align-items: flex-start;  
  height: 100vh;
}  
  
.left-buttons {  
  width: 200px; 
  display: flex;  
  flex-direction: column;  
  padding: 10px;  
  padding-left: 100px;
}  
  
.right-buttons {  
  flex-grow: 1;
  display: flex;  
  flex-wrap: wrap;
  padding: 10px;  
  justify-content: center;
  gap: 10px;
}  
  
.round-button {  
  width: 100px;
  height: 100px;
  border-radius: 50px;  
  padding: 10px 20px;  
  margin: 20px 0;  
  background-color: #fff;  
  border: none;  
  cursor: pointer;  
  transition: background-color 0.3s ease;  
}  
  
.round-button.active {  
  background-color: #ddd;  
}  
  
.square-button {  
  border-radius: 0;  
  padding: 10px 20px;  
  margin: 5px;  
  background-color: #fff;  
  border: none;  
  cursor: pointer;  
  transition: background-color 0.3s ease;  
  flex: 0 0 calc(20% - 10px);
  border: 2px dashed #003366;
}  
  
.square-button:hover {  
  background-color: #78291e;
  color: white;
}  
.square-button.selected {  
  background-color: orange;
  color: white;
}

.sub-department-title {  
  text-align: center;
  padding: 10px 0;
  font-size: 18px;
  font-weight: bold;
}
.sub-department-titles {  
  text-align: center;
  margin-bottom: 10px; 
}  
  
.sub-department-title-chinese,  
.sub-department-title-english {  
  font-size: 18px;
  font-weight: bold; 
}  
.sub-department-buttons{
  flex-grow: 1; 
  display: flex;  
  flex-wrap: wrap; 
  padding: 10px;  
  justify-content: center;
  gap: 10px;
}
.selected-department-container {  
  width: 100%;
  margin-bottom: 10px; 
  justify-content: center;
  display: flex;
  align-items: center; 
}  
  
.selected-department-title {  
  border: 1px solid #ccc;  
  padding: 5px 10px; 
  display: inline-block; 
}
.container2 {  
  display: flex;  
  flex-wrap: wrap;  
  justify-content: center;  
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