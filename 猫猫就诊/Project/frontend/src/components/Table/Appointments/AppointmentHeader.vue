<template>  
  <!-- 上面的四个框 -->
  <div class="container" style="display: flex; justify-content: center; align-items: center; height: 180px;">  
    <div  
      v-for="(square, index) in squares"  
      :key="index"  
      class="square"  
      :class="{ 'square-hovered': (selected==index) || square.hovered}"  
      @mouseover="square.hovered = true"  
      @mouseout="square.hovered = false"  
    >  
      {{ info[index] }}  
    </div>  
  </div>  
</template>  
  
<script>  
export default {  
  props: {  
    squares2: {  
      type: Array,  
      required: true, // 如果父组件没有传递这个 prop，则抛出警告  
    },  
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
      checked: false,  
      currentSquareIndex: 0,  
      selected:0,
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