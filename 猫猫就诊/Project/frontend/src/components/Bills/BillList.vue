<template>
  <!-- 注意调用的位置 -->
  <div>
  <BillDetails @update:payStatus="updatePayStatus" ref="BillDetails"> </BillDetails>
  <el-container style="height: 100vh" class="container-header">
    <el-container>
      <el-aside width="200px">
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
        <el-main class="main">
          <div>
            <!-- :data 属性接收一个数组，该数组包含了所有要显示的数据对象 -->
            <el-table :data="filteredBills">
              <!-- 设置 prop 属性 - Element UI 自动将该属性对应字段的数据渲染到表格的每一行中 -->
              <el-table-column prop="type" label="类型"> </el-table-column>
              <el-table-column prop="issue" label="具体事由"> </el-table-column>
              <el-table-column prop="price" label="费用（元）"> </el-table-column>
              <el-table-column prop="date" label="创建时间"> </el-table-column>
              <el-table-column style="textalign: right" label="操作">
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
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[10, 20, 30, 40]"
              :page-size="pageSize"
              :total="totalItems"
              :hide-on-single-page="false"
              layout="total, sizes, prev, pager, next, jumper"
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
import BillDetails from './BillDetails.vue'
export default {
  data() {
    return {
      desc: '缴费列表统计',
      bill: [
        {
          id: 1,
          type: '挂号',
          issue: '皮肤科挂号',
          price: 10,
          date: '2024年3月15日',
          payStatus: true
        },
        {
          id: 2,
          type: '处方',
          issue: '眼科问诊处方药品开具',
          price: 200,
          date: '2024年2月15日',
          payStatus: false
        },
        {
          id: 3,
          type: '挂号',
          issue: '全科挂号',
          price: 5,
          date: '2024年1月15日',
          payStatus: false
        }
      ],
      filteredBills: []
    }
  },
  components: {
    BillDetails
  },
  methods: {
    showBillDetails(row) {
      this.$refs.BillDetails.openModal(row)
    },
    selectFunc(payStatus) {
      // 根据传入的 payStatus 筛选患者数据
      this.filteredBills = this.bill.filter((stu) => {
        return stu.payStatus === payStatus
      })
    },
    // bug：这里目前无法从根本上实现属性的修改，页面一重新挂载就会恢复，后续链接后端时再修正逻辑
    updatePayStatus(id) {
      // 找到 bill 数组中对应的对象，并更新 payStatus
      const index = this.bill.findIndex((item) => item.id === id)
      if (index !== -1) {
        this.bill[index].payStatus = true
      }
      // 更新 filteredBills
      this.selectFunc(false)
    }
  },
  mounted() {
    // 默认是未缴费页面
    this.selectFunc(false)
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

.pay-button {
  background-color: whitesmoke;
  margin-left: -10px;
  max-width: 75px;
}

.butAbanText {
  font-size: 6px;
  color: rgba(128, 128, 128, 0.847);
}

/*页尾*/
.footer {
  background-color: rgb(8, 3, 88);
  color: white;
  font-size: 17px;
  line-height: 30px;
}
</style>
