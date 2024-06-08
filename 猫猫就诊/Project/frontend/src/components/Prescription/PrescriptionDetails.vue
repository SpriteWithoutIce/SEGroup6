<!-- 开具处方的具体实现逻辑界面 -->
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
          <el-input-number v-model="medicine.cnt" :min="0" :step="1" placeholder="数量"
            @change="calculatePrice(medicine)">药物数</el-input-number>
          <el-form-item label="疗程">
            <el-input-number v-model="medicine.times" :min="0"></el-input-number>
          </el-form-item>
          <el-button type="danger" icon="el-icon-delete" @click="removeMedicine(index)" v-if="form.medicines.length > 1"
            class="delete-button">删除药物</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="addMedicine" type="primary">添加药物</el-button>
        </el-form-item>
        <el-form-item label="上传图片" type="primary">
          <input type="file" @change="handleImageUpload">
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
        <el-button @click="generateReport" type="success">生成报告</el-button>
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
      image: null,
      totalPrice: 0,
      form: {
        id: "",/*这里的id是问诊单号*/
        name: '',
        date: new Date().toISOString().substr(0, 10), /*就诊日期 年月日*/
        gender: '',
        advice: '',
        medicines: [{ name: '', cnt: 0, price: 0, times: 0, totalPrice: 0 }]
      },
      medicinesDB: [
      ]
    };
  },
  computed: {
    totalPrice () {
      this.totalPrice = this.form.medicines
        .reduce((total, medicine) => total + parseFloat(medicine.totalPrice || 0), 0)
        .toFixed(2);


      return this.form.medicines
        .reduce((total, medicine) => total + parseFloat(medicine.totalPrice || 0), 0)
        .toFixed(2);
    }
  },
  methods: {
    writeBackPrescriptionDetailsData () {
      return new Promise((resolve, reject) => {
        let ts = this;
        let requestData = {
          /*问诊单字段：单号+开具的药物+时间+医师建议+总价*/
          id: this.form.id,
          medicines: this.form.medicines,
          suggestion: this.form.advice,
          totalPrice: this.totalPrice,
          action: "addTreatmentData"
        };
        console.log("写回处方前的数据" + requestData.id + " " + requestData.totalPrice + " " + requestData.medicines + " " + requestData.suggestion);
        this.$axios.post('/api/prescriptionDetailsWriteBack/', requestData)
          .then(function (response) {
            console.log(response.data['msg']);
            resolve(); 
          })
          .catch(function (error) {
            console.log(error);
            console.log("Prescription Details Write Back Failed")
            reject(error); 
          });
      });
    },
    handleImageUpload (event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    getMedicineData () {
      return new Promise((resolve, reject) => {
        let ts = this;
        this.$axios.get('/api/medicine/list/')
          .then(function (response) {
            ts.medicinesDB = response.data['medicine'];
            console.log(ts.medicinesDB);
            resolve(); 
          })
          .catch(function (error) {
            console.log(error);
            reject(error); 
          });
      });
    },
    openModal (row) {
      this.form.id = row.Id;
      this.isVisible = true;
      document.body.style.overflow = 'hidden'; // 禁止滚动
      this.form.name = row.name;
      this.form.gender = row.sex;
      console.log("打开订单时的列的信息" + this.form.id + " " + this.form.name);
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
      console.log('Submitting form:', this.form); // 打印整个表单状态
      ElMessage({
        showClose: true,
        message: "提交成功 ╰(*°▽°*)╯",
        type: "success"
      });
      console.log('提交表单 完成' + this.form);
      this.writeBackPrescriptionDetailsData();
      this.form.advice = "";
      this.form.date = "";
      this.form.gender = "";
      this.form.id = "";
      this.form.medicines = [{ name: '', cnt: 0, price: 0, times: 0, totalPrice: 0 }];
      this.form.name = "";
      this.totalPrice = 0;
      this.closeModal();
    },
    addMedicine () {
      this.form.medicines.push({ name: '', cnt: 0, price: 0, times: 0, totalPrice: 0 });
    },
    removeMedicine (index) {
      this.form.medicines.splice(index, 1);
    },
    calculatePrice (medicine) {
      const selectedMedicine = this.medicinesDB.find(med => med.name === medicine.name);
      if (selectedMedicine) {
        medicine.price = selectedMedicine.price;
        medicine.totalPrice = (selectedMedicine.price * medicine.cnt).toFixed(2);
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
        const symptomMatch = medicine.symptoms.toLowerCase().includes(queryString.toLowerCase());
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
    },
    generateReport () {
      // 插入标题
      const title = "<h2 style='font-family: 宋体;font-size: 24px;'>猫猫就诊报告</h2>";
      const image = this.image ? `<img src="${this.image}" alt="就诊图片" style="max-width: 100%;">` : '';
      const reportContent = `
    <p style='font-family: 宋体;font-size: 14px;'>
      姓名: ${this.form.name} <br/>
      就诊日期: ${this.form.date} <br/>
      性别: ${this.form.gender} <br/>
      药物列表: <br/>
      ${this.form.medicines.map(med => `  - ${med.name}: ${med.cnt} 个，总价: ¥${med.totalPrice}`).join('<br/>')}
      <br/>
      医师建议: <br/>
      ${this.form.advice} <br/>
      总价: ¥${this.totalPrice}
    </p>
  `;

      // 整合标题和报告内容
      const fullReportContent = title + image + reportContent;
      const blob = new Blob([fullReportContent], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${this.form.name}-就诊报告.html`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      URL.revokeObjectURL(url);

      ElMessage({
        showClose: true,
        message: "报告生成成功 ╰(*°▽°*)╯",
        type: "success"
      });
    },
  },
  mounted () {
    this.getMedicineData().then(() => {
    });
  },
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
