<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <div class="head">
        <p style="margin-left:15px;font-size:larger;color:white;">{{ form.state }}</p>
        <p  v-if="form.state === '已预约'" style="margin-left:15px;font-size:small;color:white;">请在约定时间前往就诊</p>
      </div>
      <el-button  v-if="form.state === '已预约'" class="button">取消挂号</el-button>
      <el-button @click="closeModal" class="button">退出</el-button>
    </div>
  </div>
</template>
<script>
export default{
  name: 'DetailA',
  data(){
    return{
      isVisible:false,
      form:{office:"",orderNum:"",price:"",name:"",cardNum:"",position:"",time:"",line:'',state:''},
    }
  },
  methods:{
    openModal (item) {
      this.isVisible = true;
      document.body.style.overflow = 'hidden'; // 禁止滚动
      this.form.office=item.office;
      this.form.orderNum=item.orderNum;
      this.form.price=item.price;
      this.form.name=item.name;
      this.form.cardNum=item.cardNum;
      this.form.line=item.line;
      this.form.position=item.position;
      this.form.time=item.time;
      this.form.state=item.state;
    },
    closeModal () {
      this.isVisible = false;
      document.body.style.overflow = ''; // 恢复滚动
    },
  }
}

</script>
<style scoped>
.button{
  width:100%;
}
p {
  line-height: 0.1; /* 降低行高，根据需要调整该值 */
}
.head{
  background-color: blue;
  height:80px;
  width:100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 8px;
}
.modal-background {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 8;
}
.modal-container {
  max-width: 500px; /* 设置最大宽度为800像素 */
  width: 100%; 
  background-color: #fff;
  border-radius: 8px;
  display: flex; /* 使用Flexbox布局 */
  flex-direction: column; /* 设置为垂直方向的布局 */
  justify-content: center; /* 垂直居中所有子元素 */
  align-items: center;
}
</style>
