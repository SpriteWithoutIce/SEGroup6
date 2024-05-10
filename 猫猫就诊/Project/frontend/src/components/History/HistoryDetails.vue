<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <h2>处方信息</h2>
      <div class="flex-container">
        <p>姓名：</p>
        <div>{{ form.name }}</div>
      </div>
      <div class="flex-container">
        <p>性别：</p>
        <div>{{ form.gender }}</div>
      </div>
      <div class="flex-container">
        <p>就诊日期：</p>
        <div>{{ form.date }}</div>
      </div>
      <el-divider class="divider" />

      <div class="button-group">
          <el-button @click="closeModal">退出</el-button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'PrescriptionDetails',
  data () {
    return {
      isVisible: false,
      form: {
        name: '',
        date: new Date().toISOString().substr(0, 10),
        gender: [],
      },
      advice:'',
      medicinesDB: [
        { name: '阿司匹林', stock: 100, price: 2.5 },
        { name: '头孢', stock: 50, price: 10.0 },
        { name: '布洛芬', stock: 80, price: 5.0 },
        // 可以添加更多药物数据
      ]
    };
  },
  computed: {
    totalPrice () {
      return this.form.medicines.reduce((total, medicine) => total + parseFloat(medicine.totalPrice || 0), 0).toFixed(2);
    }
  },
  methods: {
    openModal (row) {
      this.isVisible = true;
      document.body.style.overflow = 'hidden'; // 禁止滚动
      this.form.name = row.name;
      this.form.gender = row.sex;
    },
    closeModal () {
      this.isVisible = false;
      document.body.style.overflow = ''; // 恢复滚动
    },
    calculatePrice (medicine) {
      const selectedMedicine = this.medicinesDB.find(med => med.name === medicine.name);
      if (selectedMedicine) {
        medicine.price = selectedMedicine.price;
        medicine.totalPrice = (selectedMedicine.price * medicine.quantity).toFixed(2);
      }
    },

    querySearch (queryString, cb) {
      //投影做检索
      var medicines = this.medicinesDB.map(item => ({ value: item.name }));  // 现在每个条目都是一个对象，包含 value 属性
      console.log(medicines);
      var results = queryString ? medicines.filter(this.createFilter(queryString)) : medicines;
      console.log(results);
      cb(results);
    },

    createFilter (queryString) {
      return (medicine) => {
        return medicine.value.toLowerCase().includes(queryString.toLowerCase());
      };
    },

    handleSelect (item) {
      var selectedMedicine = this.medicinesDB.find(med => med.name === item);
      if (selectedMedicine) {
        this.form.medicines[this.form.medicines.length - 1].price = selectedMedicine.price;
        this.calculatePrice(this.form.medicines[this.form.medicines.length - 1]);
      }
    },
  }
};
</script>



<style scoped>
h2{
  text-align: center; /* 仅在水平方向上居中文本 */
}
.flex-container {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
}
.namelable {
  padding-left: 0px;
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
  max-width: 400px; /* 设置最大宽度为800像素 */
  width: 100%; 
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  display: flex; /* 使用Flexbox布局 */
  flex-direction: column; /* 设置为垂直方向的布局 */
  justify-content: center; /* 垂直居中所有子元素 */
}

.button-group {
  margin-top: 20px;
  text-align: center;
}

.delete-button {
  width: 14%;
  text-align: left;
}

.form-header {
  align-items: center;
  font-size: 24px;
  /* 字体大小 */
  font-weight: bold;
  /* 字体加粗 */
  color: #333;
  /* 字体颜色 */
  margin-bottom: 50px;
  /* 下边距 */
}
</style>
