<!--患者的处方查询页面-->
<template>
  <!-- <div class="container"> -->
  <el-container style="height: 100vh">
    <scroll>
      <div class="all-container" width="100%">
        <div class="search-container">
          <div class="wenzi">
            <p class="guahao">处方查询</p>
            <p class="back">首页 > 处方查询</p>
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
                <el-icon class="el-input__icon">
                  <search />
                </el-icon>
              </template>
            </el-input>
            <el-button
              color="#DBA979"
              :dark="isDark"
              plain
              class="searchButton"
              style="width: 80px; height: 40px"
              >查询</el-button
            >
            <p>{{ input4 }}</p>
          </div>
        </div>
        <PHistory :filterInfo="filterInfo"></PHistory>
      </div>
    </scroll>
  </el-container>
</template>
<script setup>
import CarouselA from './CarouselA.vue'
import HeadA from './HeadA.vue'
import SearchA from './SearchA.vue'
import SignA from './SignA.vue'
import InputA from './InputA.vue'
import PHistory from './PHistory.vue'
import axios from 'axios'
import { ref, onMounted, computed, getCurrentInstance } from 'vue'

const {proxy} = getCurrentInstance()

const getTreatmentsData = () => {
  return new Promise((resolve, reject) => {
    axios.post('/api/treatments/list/', {identity_num: proxy.appContext.config.globalProperties.$identity_num })
    .then((response) => {
      info.value = response.data['treatments']
      console.log('Treatments data fetched:', info.value)
      resolve() // 数据获取完成，resolve Promise
    }).catch((error) => {
      console.error('Error fetching treatments data:', error)
      reject(error) // 数据获取失败，reject Promise
    })
  })
}

const input4 = ref('')
const info = ref([
  // {
  //   office: '心血管门诊', //科室
  //   time: '2024-05-14 下午 14:10-14:20', //就诊时间
  //   patient: 'buaa', //患者姓名
  //   doctor: '士小信', //医生
  //   advice: '心跳过快', //医生诊断(比较短,不是很长的那种建议)
  //   medicine: [
  //     { name: '金莲花软件囊', time: 3, cnt: 1, use: '口服', price: '5.98' }, //time:疗程,cnt:开的药的数量,use:使用方法,price:单价
  //     { name: '复方鲜竹沥液', time: 3, cnt: 2, use: '口服', price: 1.09 },
  //     { name: '复方鲜竹沥液', time: 3, cnt: 2, use: '口服', price: 1.09 }
  //   ]
  // },
  // {
  //   office: '心血管门诊',
  //   orderNum: 'w0024',
  //   patient: 'buaa',
  //   doctor: '士小信',
  //   price: '0.00元',
  //   name: 'buaa',
  //   cardNum: '001741',
  //   position: '门诊楼三层内科二诊区',
  //   time: '2024-05-15 下午 14:10-14:20',
  //   line: '38',
  //   state: '已就诊',
  //   advice: '',
  //   medicine: []
  // },
  // {
  //   office: '心血管门诊',
  //   orderNum: 'w0025',
  //   patient: 'buaa',
  //   doctor: '士小信',
  //   price: '0.00元',
  //   name: 'hhh',
  //   cardNum: '001742',
  //   position: '门诊楼三层内科二诊区',
  //   time: '2024-05-16 下午 14:10-14:20',
  //   line: '39',
  //   state: '已预约',
  //   advice: '',
  //   medicine: []
  // },
  // {
  //   office: '心血管门诊',
  //   orderNum: 'w0026',
  //   patient: 'buaa',
  //   doctor: '士小信',
  //   price: '0.00元',
  //   name: 'hhh',
  //   cardNum: '001742',
  //   position: '门诊楼三层内科二诊区',
  //   time: '2024-05-17 下午 14:10-14:20',
  //   line: '40',
  //   state: '已预约',
  //   advice: '',
  //   medicine: []
  // },
  // {
  //   office: '心血管门诊',
  //   orderNum: 'w0026',
  //   patient: 'buaa',
  //   doctor: '士小信',
  //   price: '0.00元',
  //   name: 'hhh',
  //   cardNum: '001742',
  //   position: '门诊楼三层内科二诊区',
  //   time: '2024-05-17 下午 14:10-14:20',
  //   line: '40',
  //   state: '已预约',
  //   advice: '',
  //   medicine: []
  // },
  // {
  //   office: '心血管门诊',
  //   orderNum: 'w0026',
  //   patient: 'buaa',
  //   doctor: '士小信',
  //   price: '0.00元',
  //   name: 'hhh',
  //   cardNum: '001742',
  //   position: '门诊楼三层内科二诊区',
  //   time: '2024-05-17 下午 14:10-14:20',
  //   line: '40',
  //   state: '已预约',
  //   advice: '',
  //   medicine: []
  // },
  // {
  //   office: '心血管门诊',
  //   orderNum: 'w0026',
  //   patient: 'buaa',
  //   doctor: '士小信',
  //   price: '0.00元',
  //   name: 'hhh',
  //   cardNum: '001742',
  //   position: '门诊楼三层内科二诊区',
  //   time: '2024-05-17 下午 14:10-14:20',
  //   line: '40',
  //   state: '已预约',
  //   advice: '',
  //   medicine: []
  // }
])
const commitSearch = () => {
  console.log(`查询内容是：${input4.value}`)
  // commitSearch 现在不需要做任何操作，因为 filterInfo 已经是计算属性
  // 它会自动响应 input4.value 的变化
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
  getTreatmentsData().then(() => {
  })
})
</script>
<style scoped>
.chaxun {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  /* 将组件横向排列 */
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

.wenzi {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  /* 将组件横向排列 */
  align-items: center;
}

.guahao {
  position: absolute;
  font-size: 25px;
  left: 50%;
  transform: translateX(-50%);
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

/*.container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
*/
</style>
