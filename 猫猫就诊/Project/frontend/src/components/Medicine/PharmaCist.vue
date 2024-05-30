<!--药物+医生信息录入总的-->
<template>
  <div class="container">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane label="药物录入" name="first">
        <MedicineA></MedicineA>
      </el-tab-pane>
      <el-tab-pane label="医生录入" name="second">
        <DoctorA></DoctorA>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import type { TabsPaneContext } from 'element-plus'
import MedicineA from './MedicineA.vue'
import DoctorA from './DoctorA.vue'

const activeName = ref('first')

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}
</script>

<style>
.el-tabs {
  margin-left: 10px; /* 调整左边距 */
  margin-right: 10px;
}
.demo-tabs > .el-tabs__content {
  color: #6b778c;
}
.container {
  position: relative;
  top: 0;
  width: 100%;
  min-height: 100vh;
  background-color: white;
}
</style>
