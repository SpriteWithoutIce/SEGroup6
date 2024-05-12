<template>
  <!-- 注意调用的位置 -->
  <PrescriptionDetails ref="prescriptionDetails"> </PrescriptionDetails>
  <!-- 设置标题 -->
  <el-container style="height: 100vh;">
    <el-container>
      <el-aside width="200px">
        <!-- 下边的部分是选择菜单 -->
        <el-menu class="aside my-menu" default-active="1" :unique-opened="true">
          <el-sub-menu index="1">
            <template #title>
              <span>问诊列表</span>
            </template>
            <el-menu-item index="1" @click="selectFunc('1')">今日</el-menu-item>
            <el-menu-item index="2" @click="selectFunc('2')">昨日</el-menu-item>
            <el-menu-item index="3" @click="selectFunc('3')">更早</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      <el-container>
        <!-- 在这里插入了一个空标题，让表格内容和菜单内容间距看起来舒服点 -->
        <el-header height="30px" style="padding:0;margin:0">
        </el-header>
        <el-main class="main">
          <div>
            <!-- filtered没问题，current出现了问题 -->
            <el-table :data="currentPatients">
              <el-table-column prop="Id" label="单号">
              </el-table-column>
              <el-table-column prop="name" label="姓名">
              </el-table-column>
              <el-table-column prop="age" label="年龄">
              </el-table-column>
              <el-table-column prop="sex" label="性别">
              </el-table-column>
              <el-table-column prop="date" style="background-color:black" label="问诊时间">
              </el-table-column>
              <el-table-column style="text-align: right" label="操作">
                <template #default="scope">
                  <el-button class="prescribe-button" @click="showPrescriptionDetails(scope.row)">开具处方</el-button>
                </template>
              </el-table-column>
            </el-table>
            <!-- 分页组件 -->
            <el-pagination class="page" :current-page="pagination.currentPage" :page-size="pagination.pageSize"
              :total="pagination.total" :pager-count="3" background layout="prev, pager, next, total"
              @update:current-page="handleCurrentChange">
            </el-pagination>
          </div>
        </el-main>


        <el-footer height="30px" align="center" class="footer">SE_GROUP_6</el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import PrescriptionDetails from './PrescriptionDetails.vue'
export default {
  data () {
    return {
      desc: "问诊列表统计",
      //注意，函数里有日期比较逻辑，所以务必注意后端的日期数据格式！！！
      // 把patients设置成数据库读取的内容就好
      patient: [
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        // {
        //   Id: '1',
        //   name: '秋子夜',
        //   age: '18',
        //   sex: '男',
        //   date: '2024年5月10日',
        // },
        {
          Id: '1',
          name: '秋子夜',
          age: '18',
          sex: '男',
          date: '2024年5月10日',
        },

      ],
      //这里设置数据初始化
      filteredPatients: [
      ],
      currentPatients: [],
      pagination: {
        total: 0,
        currentPage: 1,
        pageSize: 10,
      },
    }
  },
  components: {
    PrescriptionDetails,
  },
  methods: {
    handleCurrentChange (e) {
      this.pagination.currentPage = e;
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize;
      const end = start + this.pagination.pageSize;
      this.currentPatients = this.filteredPatients.slice(start, end);
      this.pagination.total = this.filteredPatients.length;
      console.log("看看这里能读吗1")
      console.log(this.patient);
    },
    getTreatmentsData: function () {
      let ts = this;
      this.$axios.get('/api/treatments/list/')
        .then(function (response) {
          ts.patient = response.data['treatments'];
        })
        .catch(function (error) {
          console.log(error);
        })
      console.log("看看这里能读吗2")
      console.log(this.patient);
    },


    showPrescriptionDetails (row) {
      this.$refs.prescriptionDetails.openModal(row);
    },
    selectFunc (index) {
      let today = new Date();
      today.setHours(0, 0, 0, 0); // Set time to midnight
      let yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);

      switch (index) {
        case '1':
          // 今日
          this.filteredPatients = this.patient.filter(stu => {
            let parts = stu.date.split('年').join('-').split('月').join('-').split('日').join('').split('-');
            let stuDate = new Date(parts[0], parts[1] - 1, parts[2]);
            stuDate.setHours(0, 0, 0, 0);
            return stuDate.toDateString() === today.toDateString();
          });
          this.handleCurrentChange(1);
          break;
        case '2':
          // 昨日
          this.filteredPatients = this.patient.filter(stu => {
            let parts = stu.date.split('年').join('-').split('月').join('-').split('日').join('').split('-');
            let stuDate = new Date(parts[0], parts[1] - 1, parts[2]);
            stuDate.setHours(0, 0, 0, 0);
            return stuDate.toDateString() === yesterday.toDateString();
          });
          this.handleCurrentChange(1);
          break;
        case '3':
          // 更早
          this.filteredPatients = this.patient.filter(stu => {
            let parts = stu.date.split('年').join('-').split('月').join('-').split('日').join('').split('-');
            let stuDate = new Date(parts[0], parts[1] - 1, parts[2]);
            stuDate.setHours(0, 0, 0, 0);
            return stuDate < yesterday;
          });
          this.handleCurrentChange(1);
          break;
      }
      console.log(this.filteredPatients);
    },
  },
  mounted () {
    /*this.getTreatmentsData();*/
    // 等待 DOM 更新后再执行筛选逻辑
    //唉我真吐了，1记得加上单引号
    this.selectFunc('1');
    this.handleCurrentChange(1);
  }
}
</script>



<style scoped>
.page {
  margin-top: 2vh;
  justify-content: center;
  margin-bottom: 1vh;
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
