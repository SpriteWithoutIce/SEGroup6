<!--药物管理系统-->
<template>
  <DetailD ref="detail" @updateData="refreshDoctorData"> </DetailD>
  <div class="container">
    <div class="m">
      <p style="margin-left: 50px; font-weight: bold; margin-right: 10px">首页</p>
      <el-icon><DArrowRight /></el-icon>
      <p style="font-weight: bold; margin-left: 10px">医生管理</p>
    </div>
    <div class="card-container">
      <el-card style="height: 660px; width: 95%">
        <el-input
          v-model="input4"
          style="width: 300px; height: 40px"
          placeholder="请输入医生姓名"
          class="shuru"
        >
          <template #prefix>
            <el-icon class="el-input__icon"><search /></el-icon>
          </template>
        </el-input>
        <el-button
          type="primary"
          plain
          style="height: 40px; margin-left: 10px"
          @click="showPrescriptionDetails('', 'add')"
          >+录入医生</el-button
        >
        <el-table :data="ftableData" style="width: 95%; max-height: 480px">
          <el-table-column prop="name" label="姓名" width="150" />
          <el-table-column prop="id" label="医生编号" width="150" />
          <el-table-column prop="office" label="科室" width="150" />
          <el-table-column prop="title" label="职称" width="150" />
          <el-table-column prop="cost" label="出诊费" width="150" />
          <el-table-column prop="research" label="主要研究方向" />

          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="showPrescriptionDetails(scope.row, 'alter')">
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
import { ref, computed, onMounted, watch } from 'vue'
import DetailD from './DetailD.vue'
import axios from 'axios'
const detail = ref(null)
const input4 = ref('')
const showPrescriptionDetails = (row, sign) => {
  // 假设DetailD组件有一个名为openModal的方法
  detail.value.openModal(row, sign)
}
// closeModal后刷新数据
const refreshDoctorData = () => {
  getDoctorData().then(() => {
    updateTotal()
    handleCurrentChange(pagination.value.currentPage)
  })
}
const handleEdit = (index, row) => {
  // 编辑操作的逻辑
  console.log('Edit row:', row)
}

const handleDelete = (index, row) => {
  // 删除操作的逻辑
  deleteDoctor(row).then(() => {})
}
const pagination = ref({
  total: 0,
  currentPage: 1,
  pageSize: 9
})
const tableData = ref([])

const filterData = computed(() => {
  return input4.value
    ? tableData.value.filter((item) => item.name.includes(input4.value))
    : tableData.value
})

// 更新分页总数的方法
const updateTotal = () => {
  pagination.value.total = filterData.value.length
}

// 观察 input4 的变化，当输入改变时更新过滤数据和分页总数
watch(input4, () => {
  updateTotal()
})
const getDoctorData = () => {
  return new Promise((resolve, reject) => {
    axios
      .get('/api/doctors/list/')
      .then((response) => {
        tableData.value = response.data['doctors']
        pagination.value.total = tableData.value.length // 更新总条目数
        console.log('Doctor data fetched:', tableData.value)
        resolve() // 数据获取完成，resolve Promise
      })
      .catch((error) => {
        console.error('Error fetching doctor data:', error)
        reject(error) // 数据获取失败，reject Promise
      })
  })
}
const deleteDoctor = (row) => {
  return new Promise((resolve, reject) => {
    axios
      .post('/api/doctors/delete/', { id: row.id, action: 'deleteDoctor' })
      .then((response) => {
        tableData.value = response.data['doctors']
        pagination.value.total = tableData.value.length // 更新总条目数
        console.log('Doctor data deleted')
        resolve() // 数据获取完成，resolve Promise
      })
      .catch((error) => {
        console.error('Error deleting doctor data:', error)
        reject(error) // 数据获取失败，reject Promise
      })
  })
}
const ftableData = computed(() => {
  const start = (pagination.value.currentPage - 1) * pagination.value.pageSize
  const end = start + pagination.value.pageSize
  //pagination.value.total = filterData.value.length
  return filterData.value.slice(start, end)
})
// 处理当前页码改变的事件
const handleCurrentChange = (e) => {
  pagination.value.currentPage = e
}
onMounted(() => {
  getDoctorData().then(() => {
    updateTotal()
    handleCurrentChange(1)
  })
})
</script>
<style scoped>
.warn {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  height: 100%;
}
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
  height: 660px;
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
