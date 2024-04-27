<template>
  <!-- 注意调用的位置 -->
  <PrescriptionDetails ref="prescriptionDetails"> </PrescriptionDetails>
  <!-- 设置标题 -->
  <el-container style="height: 100vh" class="form-container">
    <el-container>
      <el-container>
        <!-- 在这里插入了一个空标题，让表格内容和菜单内容间距看起来舒服点 -->
        <el-header height="30px" style="padding: 0; margin: 0"> </el-header>
        <el-main class="main">
          <div>
            <el-table :data="filteredPatients">
              <!-- 可以加上一个问诊号 -->
              <el-table-column prop="name" label="姓名"> </el-table-column>
              <el-table-column prop="age" label="年龄"> </el-table-column>
              <el-table-column prop="sex" label="性别"> </el-table-column>
              <el-table-column
                prop="date"
                style="background-color: black"
                label="问诊时间"
              >
              </el-table-column>
              <el-table-column style="text-align: right" label="操作">
                <template #default="scope">
                  <el-button
                    class="prescribe-button"
                    @click="showPrescriptionDetails(scope.row)"
                    >开具处方</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
            <!-- 分页组件 -->
            <el-pagination
              :pager-count="10"
              class="page"
              :current-page="pagination.currentPage"
              :page-size="pagination.pageSize"
              :total="pagination.total"
              layout="prev, pager, next ,total"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-main>

        <el-footer height="30px" align="center" class="footer"
          >SE_GROUP_6</el-footer
        >
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import PrescriptionDetails from "./PrescriptionDetails.vue";
export default {
  data() {
    return {
      desc: "问诊列表统计",
      //注意，函数里有日期比较逻辑，所以务必注意后端的日期数据格式！！！
      // 把stus设置成数据库读取的内容就好
      patient: [
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日",
        },
        {
          name: "小张",
          age: 17,
          sex: "男",
          date: "2024年2月15日",
        },
        {
          name: "小秋",
          age: 16,
          sex: "女",
          date: "2024年1月15日",
        },
      ],
      pagination: {
        total: 0,
        currentPage: 1,
        pageSize: 10,
      },
      //这里设置数据初始化
      filteredPatients: [],
    };
  },
  components: {
    PrescriptionDetails,
  },
  methods: {
    showPrescriptionDetails(row) {
      this.$refs.prescriptionDetails.openModal(row);
    },
    handleCurrentChange(e) {
      this.pagination.currentPage = e;
      const start = (this.pagination.currentPage - 1) * 10;
      const end = start + 10;
      this.filteredPatients = this.patient.slice(start, end);
    },
  },
  mounted() {
    //分页初始化
    this.pagination.total = this.patient.length;
    this.handleCurrentChange(1);
    console.log("Patient data loaded:", this.patient);
    // 等待 DOM 更新后再执行筛选逻辑
    //唉我真吐了，1记得加上单引号
    this.$nextTick(() => {
      this.selectFunc("1");
      console.log("here");
      console.log("Filtered patients after DOM update:", this.filteredPatients);
    });
  },
};
</script>

<style scoped>
.page {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 5%;
}
.form-container {
  position: absolute;
  top: 600px;
  left: 0;
  width: 100%;
  background-color: white;
}
.header {
  font-size: 30px;
  line-height: 80px;
  background-color: #f1f1f1;
}

/*菜单栏*/
.aside {
  background-color: wheat;
}

.my-menu .el-menu-item.is-active {
  color: black;
  background-color: cornflowerblue;
  opacity: 0.5;
}

/*标题的下划线*/
.subHeader {
  /*background-color: cornflowerblue*/
  background-color: black;
}

/*问诊列表*/
.main {
  background-color: white;
  background-image: url(../../assets/prescription/prescription_bg.png);
}

.prescribe-button {
  background-color: whitesmoke;
  margin-left: -10px;
  max-width: 75px;
}

/*页尾*/
.footer {
  background-color: rgb(8, 3, 88);
  color: white;
  font-size: 17px;
  line-height: 30px;
}
</style>
