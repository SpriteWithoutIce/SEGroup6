<template>
  <!-- 注意调用的位置 -->
  <PrescriptionDetails ref="prescriptionDetails"> </PrescriptionDetails>
  <!-- 设置标题 -->
  <el-container style="height: 100vh;">
    <el-container>
      <el-aside width="200px">
        <!-- 下边的部分是选择菜单 -->
        <el-menu class="aside my-menu" @select="selectFunc" default-active="1" :unique-opened="true">
          <el-sub-menu index="1">
            <template #title>
              <span>问诊列表</span>
            </template>
            <el-menu-item index="1">今日</el-menu-item>
            <el-menu-item index="2">昨日</el-menu-item>
            <el-menu-item index="3">更早</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      <el-container>
        <!-- 在这里插入了一个空标题，让表格内容和菜单内容间距看起来舒服点 -->
        <el-header height="30px" style="padding:0;margin:0">
        </el-header>
        <el-main class="main">
          <div>
            <el-table :data="filteredPatients">
              <!-- 可以加上一个问诊号 -->
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
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
              :current-page="currentPage" :page-sizes="[10, 20, 30, 40]" :page-size="pageSize"
              layout="total, sizes, prev, pager, next, jumper" :total="totalItems" :hide-on-single-page="false">
            </el-pagination>
          </div>
        </el-main>


        <el-footer height="30px" align="center" class="footer">SE_GROUP_6</el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
// import instance from '../../axios';
import PrescriptionDetails from './PrescriptionDetails.vue'
export default {
  data () {
    return {
      desc: "问诊列表统计",
      //注意，函数里有日期比较逻辑，所以务必注意后端的日期数据格式！！！
      // 把stus设置成数据库读取的内容就好
      patient: [
        {
          name: "小王",
          age: 18,
          sex: "男",
          date: "2024年4月27日"
        }, {
          name: "小张",
          age: 17,
          sex: "男",
          date: "2024年2月15日"
        }, {
          name: "小秋",
          age: 16,
          sex: "女",
          date: "2024年1月15日"
        }
      ],
      //这里设置数据初始化
      filteredPatients: [
      ],
    }
  },
  components: {
    PrescriptionDetails,
  },
  methods: {
    // getPatientsData () {
    //   instance.axios.get('/patients', {})
    //     .then(res => {
    //       const data = res.data;
    //       this.patient = data;
    //       console.log('Fetched users data:', data);
    //     })
    //     .catch(error => {
    //       console.error('Error fetching users data:', error);
    //     });
    // },
    getPatientsData: function () {

      this.$axios.get('/api/patients/list/')
        .then(function (response) {
          this.patient = response.data;
        })
        .catch(function (error) {
          console.log(error);
        })
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
          break;
        case '2':
          // 昨日
          this.filteredPatients = this.patient.filter(stu => {
            let parts = stu.date.split('年').join('-').split('月').join('-').split('日').join('').split('-');
            let stuDate = new Date(parts[0], parts[1] - 1, parts[2]);
            stuDate.setHours(0, 0, 0, 0);
            return stuDate.toDateString() === yesterday.toDateString();
          });
          break;
        case '3':
          // 更早
          this.filteredPatients = this.patient.filter(stu => {
            let parts = stu.date.split('年').join('-').split('月').join('-').split('日').join('').split('-');
            let stuDate = new Date(parts[0], parts[1] - 1, parts[2]);
            stuDate.setHours(0, 0, 0, 0);
            return stuDate < yesterday;
          });
          break;
      }
      console.log(this.filteredPatients);
    },
  },
  mounted () {
    this.getPatientsData();
    // 等待 DOM 更新后再执行筛选逻辑
    //唉我真吐了，1记得加上单引号
    this.$nextTick(() => {
      this.selectFunc('1');
    });
  }
}
</script>



<style scoped>
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
