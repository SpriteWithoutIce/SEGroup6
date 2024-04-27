<template>  
  <Header :squares2="squares2" />
  <!-- 就诊须知内容 -->
  <div class="notice-box">  
    <form>  
      <div class="form-group">  
        <label for="name">姓名:</label>  
        <input type="text" id="name" name="name" class="form-control" placeholder="请输入姓名">  
        <label for="paymentType">支付类型:</label>  
        <select id="paymentType" name="paymentType" class="form-control">  
          <option value="医保">医保</option>  
          <option value="非医保">非医保</option>  
        </select>  
      </div>  
      <div class="form-group">  
        <label for="gender">性别:</label>  
        <select id="gender" name="gender" class="form-control">  
          <option value="男">男</option>  
          <option value="女">女</option>  
        </select>  
        <label for="birthday">生日:</label>  
        <input type="date" id="birthday" name="birthday" class="form-control">  
      </div>  
      <div class="form-group">  
        <label for="idType">证件类型:</label>  
        <select id="idType" name="idType" class="form-control">  
          <option value="身份证">身份证</option>  
          <option value="绿卡">绿卡</option>  
          <!-- 可以继续添加其他选项 -->  
        </select>  
        <label for="phone">电话:</label>  
        <input type="tel" id="phone" name="phone" class="form-control" placeholder="请输入电话">  
      </div>  
      <button type="submit">提交</button>  
    </form>  
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
        { hovered: false, active: true ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false},  
        { hovered: false, active: false ,done: false}  
      ]  ,
      info2:[
        "就诊须知","挂号类别","填写预约信息","选择科室","选择医生","选择时间地点","核对预约信息","预约成功"
      ],
    };  
  }  ,
  methods: {  
    toggleSquare(index) {  
      this.currentSquareIndex = index;   
      this.currentSquareIndex = 1;
      this.checked = false; // 重置打勾状态  
    },  
    nextSquare(){

    }
  }  
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
  transition: background-color 0.3s, color 0.3s; /* 添加过渡效果 */  
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
  background-color: #f5f5f5; /* 浅灰色背景 */  
  border-left: 30px solid #fff;
  border-right: 30px solid #fff; /* 白色边框 */  
  padding: 20px; /* 内边距 */  
  margin: 10px; /* 外边距 */  
  box-sizing: border-box; /* 确保边框和内边距包含在元素的总宽度和高度内 */  
}  

.square-done {
  background-color: #003366;  
  color: #FFFFFF;
}

.form-group {  
  display: flex;  
  flex-direction: row;  
  justify-content: space-between;  
  margin-bottom: 10px;  
}  
.form-control {  
  flex: 1;  
  margin-right: 10px;  
}  
.form-control:last-child {  
  margin-right: 0;  
}  
</style>