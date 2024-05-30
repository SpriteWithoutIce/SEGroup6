<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <el-form :model="form" class="form" label-width="auto" style="max-width: 600px">
        <div class="form-header">处方开具</div>
        <el-form-item label="姓名" class="namelable">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="就诊日期">
          <el-date-picker v-model="form.date" type="date"></el-date-picker>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio value="男">男</el-radio>
            <el-radio value="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-for="(medicine, index) in form.medicines" :key="index">
          <el-autocomplete v-model="medicine.name" :trigger-on-focus="false" :fetch-suggestions="querySearch"
            placeholder="药物名称或症状" @select="handleSelect(index)" :show-all="true"></el-autocomplete>
          <el-input-number v-model="medicine.quantity" :min="0" :step="1" placeholder="数量"
            @change="calculatePrice(medicine)"></el-input-number>
          <el-row>
            <el-col :span="12">
              <el-input v-model="medicine.totalPrice" disabled placeholder="总价" style="margin-left: 10px;"></el-input>
            </el-col>
          </el-row>
          <el-button type="danger" icon="el-icon-delete" @click="removeMedicine(index)" v-if="form.medicines.length > 1"
            class="delete-button">删除药物</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="addMedicine" type="primary">添加药物</el-button>
        </el-form-item>
        <el-form-item label="医师建议">
          <el-input type="textarea" v-model="form.advice"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="totalPrice" disabled placeholder="总价"></el-input>
        </el-form-item>
      </el-form>
      <div class="button-group">
        <el-button @click="submitForm" type="primary">提交</el-button>
        <el-button @click="cancelModal">退出</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
export default {
  name: 'PrescriptionDetails',
  data () {
    return {
      isVisible: false,
      form: {
        name: '',
        date: new Date().toISOString().substr(0, 10),
        gender: '',
        advice: '',
        medicines: [{ name: '', quantity: 0, price: 0, totalPrice: 0 }]
      },
      medicinesDB: [
        // { name: '布洛芬', stock 改成num: 80, price: 5.0, use: ['发热', '炎症'] }
        // 可以添加更多药物数据
      ]
    };
  },
  computed: {
    totalPrice () {
      return this.form.medicines
        .reduce((total, medicine) => total + parseFloat(medicine.totalPrice || 0), 0)
        .toFixed(2);
    }
  },
  methods: {
    getMedicineData () {
      return new Promise((resolve, reject) => {
        let ts = this;
        this.$axios.get('/api/medicine/list/')
          .then(function (response) {
            ts.medicinesDB = response.data['medicine'];
            console.log(ts.medicinesDB);
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
      });
    },
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
    cancelModal () {
      ElMessage({
        type: "info",
        message: "取消提交 ╮(╯▽╰)╭",
        showClose: true
      });
      this.closeModal();
    },
    submitForm () {
      ElMessage({
        showClose: true,
        message: "提交成功 ╰(*°▽°*)╯",
        type: "success"
      });
      console.log('提交表单', this.form);
      this.closeModal();
    },
    addMedicine () {
      this.form.medicines.push({ name: '', quantity: 0, price: 0, totalPrice: 0 });
    },
    removeMedicine (index) {
      this.form.medicines.splice(index, 1);
    },
    calculatePrice (medicine) {
      const selectedMedicine = this.medicinesDB.find(med => med.name === medicine.name);
      if (selectedMedicine) {
        medicine.price = selectedMedicine.price;
        medicine.totalPrice = (selectedMedicine.price * medicine.quantity).toFixed(2);
      }
    },
    querySearch (queryString, cb) {
      const medicines = this.medicinesDB.map(item => ({
        value: item.name,
        symptoms: item.use
      }));
      const results = queryString
        ? medicines.filter(this.createFilter(queryString))
        : medicines;
      cb(results);
    },
    createFilter (queryString) {
      return medicine => {
        const nameMatch = medicine.value.toLowerCase().includes(queryString.toLowerCase());
        const symptomMatch = medicine.symptoms.some(symptom =>
          symptom.toLowerCase().includes(queryString.toLowerCase())
        );
        return nameMatch || symptomMatch;
      };
    },
    handleSelect (index) {
      return item => {
        const selectedMedicine = this.medicinesDB.find(med => med.name === item.value);
        if (selectedMedicine) {
          const medicine = this.form.medicines[index];
          medicine.name = selectedMedicine.name;
          medicine.price = selectedMedicine.price;
          this.calculatePrice(medicine);
        }
      };
    }
  },

  mounted () {
    this.getMedicineData().then(() => {
    });
  }
};
</script>

<style scoped>
.namelable {
  padding-left: 0px;
}

.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 8;
}

.modal-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
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
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}
</style>
