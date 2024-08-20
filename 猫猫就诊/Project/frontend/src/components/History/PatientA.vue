<!--患者的挂号查询页面-->
<template>
  <el-container style="height: 100vh">
    <scroll>
      <div class="all-container" width="100%">
        <div class="search-container">
          <div class="wenzi">
            <p class="guahao">挂号查询</p>
            <p class="back">首页 > 挂号查询</p>
          </div>
          <el-divider class="divider" />
        </div>
        <SignA></SignA>
        <div class="input-container">
          <div class="chaxun">
            <el-input
              v-model="input4"
              style="width: 300px; height: 40px"
              placeholder="请输入就诊日期(例:2024-05-09) 或 科室"
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
  </el-container>
</template>
<script setup>
import SearchA from './SearchA.vue'
import SignA from './SignA.vue'
import HistoryA from './HistoryA.vue'
import axios from 'axios'
import { GlobalState } from '../../global.js'
// GlobalState.identityNum;
import { ref, onMounted, computed, inject } from 'vue'
const input4 = ref('')
const info = ref([])

// const identityNum = inject('$identity_num')

const getRegistersData = () => {
  return new Promise((resolve, reject) => {
    let requestData = {
      action: 'getRegistersData',
      identity_num: GlobalState.identityNum
    }
    axios
      .post('/api/registers/list/', requestData)
      .then((response) => {
        info.value = response.data['registers']
        console.log('Registers data fetched:', info.value)
        resolve() // 数据获取完成，resolve Promise
      })
      .catch((error) => {
        console.error('Error fetching registers data:', error)
        reject(error) // 数据获取失败，reject Promise
      })
  })
}

const commitSearch = () => {
  console.log(`查询内容是：${input4.value}`)
}
const filterInfo = computed(() => {
  return info.value.filter((item) => {
    // 检查 input4 的第一个字符是否为数字
    if (/^\d/.test(input4.value)) {
      // 如果是数字，按照 time 字段进行过滤
      const dateInItem = item.time.split(' ')[0]
      return dateInItem === input4.value
    } else {
      // 如果不是数字，按照 office 字段进行过滤
      return input4.value ? item.office === input4.value : true
    }
  })
})
onMounted(() => {
  if (GlobalState.identityNum == '0') {
    console.log('未登录')
    return
  }
  getRegistersData().then(() => {})
})
</script>

<style scoped>
.wenzi {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  /* 将组件横向排列 */
  align-items: center;
}
p {
  color: #e9c874;
}

.back {
  font-size: 15px;
  position: absolute;
  left: 80%;
}

p {
  font-weight: bold;
}
.divider {
  position: absolute;
  width: 50%;
  left: 25%;
  top: 55%;
}
.guahao {
  position: absolute;
  font-size: 25px;
  left: 50%;
  transform: translateX(-50%);
}
.search-container {
  position: absolute;
  top: 400px;
  height: 90px;
  width: 800px;
  background-color: white;
  box-shadow: 0 4px 8px rgb(212, 206, 206);
  border-radius: 35px;
  transform: translateX(-50%);
  left: 50%;
}
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
