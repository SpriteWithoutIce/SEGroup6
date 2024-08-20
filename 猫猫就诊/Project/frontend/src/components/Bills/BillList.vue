<!--
BillList.vue 组件用于展示就诊账单的列表界面。

该组件的主要功能包括：
1. 列出用户所有猫猫的就诊账单记录，包括账单编号、就诊日期、总金额等关键信息。
2. 提供分页功能，允许用户查看不同页码的账单记录。
3. 允许用户对账单进行筛选，如按日期范围、就诊医生等条件进行筛选。
4. 提供跳转到账单详情页面的功能，通过点击某个账单项，用户可以查看该账单的详细信息。

组件内部通过异步请求获取账单数据，并根据获取到的数据进行渲染。它使用了Vue的列表渲染指令`v-for`来展示账单列表，并使用Vue Router进行页面跳转。
此外，组件还包含了一些用于处理分页、筛选等交互逻辑的方法。
通过此组件，用户可以方便地查看和管理猫猫的就诊账单列表，从而更好地了解和管理宠物的健康状况。
-->

<template>
  <!-- 注意调用的位置 -->
  <div>
    <BillDetails @update:payStatus="updatePayStatus" ref="BillDetails"> </BillDetails>
    <el-container class="componentBody">
      <el-container>
        <el-aside>
          <!-- 下边的部分是选择菜单 -->
          <!-- @select="selectFunc" 表示当 <el-menu> 上的某个菜单项被选中时，会触发 selectFunc 方法 -->
          <!-- :unique-opened="true" 表示同时只能展开一个子菜单 -->
          <el-menu class="aside my-menu" default-active="1" :unique-opened="true">
            <el-sub-menu index="1">
              <template #title>
                <span>缴费列表</span>
              </template>
              <el-menu-item index="1" @click="selectFunc(false)">未缴费</el-menu-item>
              <el-menu-item index="2" @click="selectFunc(true)">已缴费</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-aside>
        <el-container>
          <!-- 插入一个空标题，让表格内容和菜单内容间距看起来更舒适 -->
          <el-header height="30px" style="padding: 0; margin: 0"></el-header>
          <el-main class="el-main">
            <div class="main">
              <!-- :data 属性接收一个数组，该数组包含了所有要显示的数据对象 -->
              <el-table :data="filteredBillsDiv" class="el-table">
                <!-- 设置 prop 属性 - Element UI 自动将该属性对应字段的数据渲染到表格的每一行中 -->
                <el-table-column prop="type" label="类型"> </el-table-column>
                <el-table-column prop="department" label="开具科室"> </el-table-column>
                <el-table-column prop="price" label="费用（元）"> </el-table-column>
                <el-table-column prop="date" label="创建时间"> </el-table-column>
                <el-table-column style="text-align: right" label="操作">
                  <!-- scope实现插槽，允许在父组件中定义插槽的内容，但是在子组件的作用域内访问数据 -->
                  <template #default="scope">
                    <!-- 使用 v-if来判断是否显示按钮 -->
                    <div v-if="scope.row.payStatus === false">
                      <el-button class="pay-button" @click="showBillDetails(scope.row)"
                        >缴费</el-button
                      >
                    </div>
                    <!-- 使用 v-else显示文本 -->
                    <div v-else class="butAbanText">已缴费，无需操作</div>
                  </template>
                </el-table-column>
              </el-table>
              <!-- 分页组件，目前不显示？ -->
              <el-pagination
                class="page"
                :current-page="pagination.currentPage"
                :page-size="pagination.pageSize"
                :total="pagination.total"
                :pager-count="3"
                background
                layout="prev, pager, next, total"
                @update:current-page="handleCurrentChange"
              >
              </el-pagination>
            </div>
          </el-main>
          <el-footer height="30px" align="center" class="footer">SE_GROUP_6</el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { inject } from 'vue'
import { GlobalState } from '../../global.js';
import BillDetails from './BillDetails.vue'
export default {
  // inject: ['$identity_num'],
  created() {
    // this.identityNum = this.$identity_num;
    this.identityNum = GlobalState.identityNum;
    console.log("BillList获取的identityNum为：",this.identityNum); 
  },
  data() {
    return {
      identityNum: 0,
      desc: '缴费列表统计',
      bill: [],
      pagination: {
        total: 0,
        currentPage: 1,
        pageSize: 10
      },
      filteredBills: [],
      filteredBillsDiv: []
    }
  },
  components: {
    BillDetails
  },
  methods: {
    getBillsData() {
      return new Promise((resolve, reject) => {
        let ts = this;
        //已完成 注意：需要前端传入当前登录用户的证件号
        this.$axios.post('/api/bills/list/', {identity_num: this.identityNum, action: "getBillsData"})
          .then(function (response) {
            ts.bill = response.data['bill'];
            console.log(ts.bill);
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
          console.log('BillList发送的请求参数:', {identity_num: this.identityNum});
      });
    },
    handleCurrentChange(e) {
      this.pagination.currentPage = e
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.filteredBillsDiv = this.filteredBills.slice(start, end)
      this.pagination.total = this.filteredBills.length
    },
    showBillDetails(row) {
      this.$refs.BillDetails.openModal(row)
    },
    selectFunc(payStatus) {
      // 根据传入的 payStatus 筛选患者数据
      this.filteredBills = this.bill.filter((stu) => {
        return stu.payStatus === payStatus
      }),
      this.handleCurrentChange(1)
    },
    changeBillStatus(id) {
      return new Promise((resolve, reject) => {
        let ts = this;
        //已完成 注意：需要前端传入当前登录用户的证件号
        this.$axios.post('/api/bills/list/', {identity_num: this.identityNum, action: "changeBillStatus", item_id: id})
          .then(function (response) {
            ts.bill = response.data['bill'];
            console.log(ts.bill);
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
      });
    },
    updatePayStatus(id) {
      // 找到 bill 数组中对应的对象，并更新 payStatus
      // const index = this.bill.findIndex((item) => item.id === id)
      // if (index !== -1) {
      //   this.bill[index].payStatus = true
      // }
      this.changeBillStatus(id).then(() => {
        // 更新 filteredBills
        this.selectFunc(false)
      })
    }
  },
  mounted() {
    this.getBillsData().then(() => {
      // 默认是未缴费页面
      this.selectFunc(false)
      //分页初始化
      this.handleCurrentChange(1)
    });
  }
}
</script>

<style scoped>
.componentBody {
  height: 100vh;
}
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
  width: clamp(130px, 30vw, 230px);
}

.el-aside {
  width: clamp(130px, 30vw, 230px);
}

.my-menu .el-menu-item.is-active {
  color: black;
  background-color: cornflowerblue;
  opacity: 0.5;
  width: clamp(130px, 30vw, 230px);
}

/*标题的下划线*/
.subHeader {
  /*background-color: cornflowerblue*/
  background-color: black;
}

/*问诊列表*/
.el-main {
  display: flex;
  flex-direction: column;
  background-color: white;
  background-image: url(../../assets/prescription/prescription_bg.png);
  background-size: cover;
}

.main {
  justify-content: space-between;
  display: flex;
  height: 100%;
  flex-direction: column;
}

.pay-button {
  background-color: whitesmoke;
  margin-left: -10px;
  max-width: 75px;
}

/* .butAbanText {
  font-size: 6px;
  color: rgba(128, 128, 128, 0.847);
} */

/*页尾*/
.footer {
  background-color: rgb(8, 3, 88);
  color: white;
  font-size: 17px;
  line-height: 30px;
}
</style>
