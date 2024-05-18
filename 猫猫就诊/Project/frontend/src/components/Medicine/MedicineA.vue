<template>
  <div class="container">
    <div class="m">
      <p style="margin-left: 50px; font-weight: bold; margin-right: 10px">首页</p>
      <el-icon><DArrowRight /></el-icon>
      <p style="font-weight: bold; margin-left: 10px">药品管理</p>
    </div>
    <div class="card-container">
      <el-card style="height: 650px; width: 95%">
        <el-input
          v-model="input4"
          style="width: 400px; height: 40px"
          placeholder="请输入药物名称"
          class="shuru"
        >
          <template #prefix>
            <el-icon class="el-input__icon"><search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" plain style="height: 40px; margin-left: 10px"
          >+新建药物类型</el-button
        >
        <el-table :data="ftableData" style="width: 95%; max-height: 480px">
          <el-table-column prop="name" label="药物名称" width="180" />
          <el-table-column prop="type" label="药物种类" width="180" />
          <el-table-column prop="price" label="药物价格" width="180" />
          <el-table-column prop="use" label="适应症状" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
                修改
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)"
                plain
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
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
      </el-card>
    </div>
    <el-footer height="30px" align="center" class="footer">SE_GROUP_6</el-footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
const handleEdit = (index, row) => {
  // 编辑操作的逻辑
  console.log('Edit row:', row)
}

const handleDelete = (index, row) => {
  // 删除操作的逻辑
  console.log('Delete row:', row)
}
const pagination = ref({
  total: 0,
  currentPage: 1,
  pageSize: 9
})
const tableData = [
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '感冒冲剂',
  //   type: '中药',
  //   use: '感冒',
  //   price: '5.00'
  // },
  // {
  //   name: '阿司匹林片',
  //   type: '西药',
  //   use: '缓解疼痛，如头痛、牙痛，降低发热体温，预防血栓形成',
  //   price: '2.50'
  // },
  // {
  //   name: '布洛芬缓释胶囊',
  //   type: '西药',
  //   use: '减轻中度疼痛，如关节炎、扭伤等，缓解炎症',
  //   price: '15.00'
  // },
  // {
  //   name: '维生素C片',
  //   type: '保健品',
  //   use: '补充维生素C，增强免疫力，促进铁的吸收',
  //   price: '8.00'
  // },
  // {
  //   name: '胰岛素注射液',
  //   type: '生物制品',
  //   use: '治疗糖尿病，调节血糖水平',
  //   price: '35.00'
  // },
  // {
  //   name: '蒙脱石散',
  //   type: '中药',
  //   use: '治疗腹泻，缓解胃肠道不适',
  //   price: '10.00'
  // }
]

const getMedicineData = () => {
  $axios.get('/api/medicine/list/')
    .then(response => {
      tableData = response.data['medicine'];
      pagination.value.total = tableData.length // 更新总条目数
      console.log("Medicine data fetched:", tableData.value);
    })
    .catch(error => {
      console.error("Error fetching medicine data:", error);
    })
}

const ftableData = computed(() => {
  const start = (pagination.value.currentPage - 1) * pagination.value.pageSize
  const end = start + pagination.value.pageSize
  console.log(`值是：${pagination.value.total}`)
  return tableData.slice(start, end)
})

// 处理当前页码改变的事件
const handleCurrentChange = (e) => {
  pagination.value.currentPage = e
  // filteredBillsDiv 会自动更新，因为是一个 computed 属性
}
onMounted(() => {
  getMedicineData()
  handleCurrentChange(1)
})
</script>
<style scoped>
.page {
  position: absolute;
  bottom: 5%;
  transform: translateX(-50%);
  left: 50%;
}
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}
.m {
  background-color: rgb(228, 228, 228);
  width: 100%;
  height: 50px;
  display: flex;
  flex-direction: row;
  align-items: center;
}
.card-container {
  position: relative;
  top: 40px;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 650px;
}
.el-card {
  position: relative;
  transform: translateX(-50%);
  left: 50%;
}
.el-table {
  position: relative;
  transform: translateX(-50%);
  left: 50%;
  margin-top: 50px;
}
.container {
  position: relative;
  top: 0;
  width: 100%;
  min-height: 100vh;
  background-color: white;
}
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  background-color: rgb(8, 3, 88);
  color: white;
  font-size: 17px;
  line-height: 30px;
}
</style>
