<!--患者的挂号查询页面-->
<template>
  <div class="container">
    <scroll>
      <div class="all-container" width="100%">
        <SearchA></SearchA>
        <SignA></SignA>
        <div class="input-container">
          <div class="chaxun">
            <el-input
              v-model="input4"
              style="width: 300px; height: 40px"
              placeholder="请输入就诊日期(例:05-09) 或 就诊科室"
              class="shuru"
            >
              <template #prefix>
                <el-icon class="el-input__icon"><search /></el-icon>
              </template>
            </el-input>
            <el-button
              color="#DBA979"
              :dark="isDark"
              plain
              class="searchButton"
              style="width: 80px; height: 40px"
              @click="commitSearch"
              >查询</el-button
            >
            <p>{{ input4 }}</p>
          </div>
        </div>
        <HistoryA :filterInfo="filterInfo"></HistoryA>
      </div>
    </scroll>
  </div>
</template>
<script setup>
import SearchA from './SearchA.vue'
import SignA from './SignA.vue'
import HistoryA from './HistoryA.vue'
import { ref, onMounted, computed } from 'vue'
const input4 = ref('')
const info = ref([
  {
    office: '心血管门诊',
    orderNum: 'w0023',
    price: '0.00元',
    name: 'buaa',
    cardNum: '001741',
    position: '门诊楼三层内科二诊区',
    time: '2024-05-14 下午 14:10-14:20',
    line: '37',
    state: '已预约',
    doctor: '王玉'
  },
  {
    office: '心血管门诊',
    orderNum: 'w0024',
    price: '0.00元',
    name: 'buaa',
    cardNum: '001741',
    position: '门诊楼三层内科二诊区',
    time: '2024-05-15 下午 14:10-14:20',
    line: '38',
    state: '已就诊',
    doctor: '王玉'
  },
  {
    office: '心血管门诊',
    orderNum: 'w0025',
    price: '0.00元',
    name: 'hhh',
    cardNum: '001742',
    position: '门诊楼三层内科二诊区',
    time: '2024-05-16 下午 14:10-14:20',
    line: '39',
    state: '已预约',
    doctor: '王玉'
  },
  {
    office: '心血管门诊',
    orderNum: 'w0026',
    price: '0.00元',
    name: 'hhh',
    cardNum: '001742',
    position: '门诊楼三层内科二诊区',
    time: '2024-05-17 下午 14:10-14:20',
    line: '40',
    state: '已预约',
    doctor: '王玉'
  },
  {
    office: '心血管门诊',
    orderNum: 'w0026',
    price: '0.00元',
    name: 'hhh',
    cardNum: '001742',
    position: '门诊楼三层内科二诊区',
    time: '2024-05-17 下午 14:10-14:20',
    line: '40',
    state: '已预约',
    doctor: '王玉'
  },
  {
    office: '心血管门诊',
    orderNum: 'w0026',
    price: '0.00元',
    name: 'hhh',
    cardNum: '001742',
    position: '门诊楼三层内科二诊区',
    time: '2024-05-17 下午 14:10-14:20',
    line: '40',
    state: '已预约',
    doctor: '王玉'
  },
  {
    office: '心血管门诊',
    orderNum: 'w0026',
    price: '0.00元',
    name: 'hhh',
    cardNum: '001742',
    position: '门诊楼三层内科二诊区',
    time: '2024-05-17 下午 14:10-14:20',
    line: '40',
    state: '已预约',
    doctor: '王玉'
  }
])
const commitSearch = () => {
  console.log(`查询内容是：${input4.value}`)
  // commitSearch 现在不需要做任何操作，因为 filterInfo 已经是计算属性
  // 它会自动响应 input4.value 的变化
}
const filterInfo = computed(() => {
  return info.value.filter((item) => {
    const dateInItem = item.time.split(' ')[0]
    return input4.value ? dateInItem === input4.value : true
  })
})
</script>

<style scoped>
.container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.chaxun {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row; /* 将组件横向排列 */
  align-items: center;
}
.shuru {
  position: absolute;
  left: 0%;
}
.searchButton {
  position: absolute;
  left: 80%;
}
.input-container {
  position: absolute;
  top: 570px;
  height: 50px;
  width: 400px;
  background-color: white;
  transform: translateX(-50%);
  display: flex;
  flex-direction: row;
  align-items: center;
  left: 50%;
}
</style>
