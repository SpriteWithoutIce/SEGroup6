<script setup>
import { ref, onMounted } from 'vue';
import MyHead from './components/head.vue'

const tagList = ref(['全部事项', '待付款', '已付款', '待处理', '已完成']);
const curIndex = ref(0);
const orderList = ref([
  {
    id: 1,
    createtime: '2023-04-01',
    params: { type:'挂号费', name: '事项1', price: 100 },
    state: 0,
  },
]);

function changeIndex(i) {
  curIndex.value = i;
  // 根据 curIndex 过滤 orderList 的逻辑可以在这里实现
}

// 如果需要在组件加载时执行某些逻辑，可以在 onMounted 钩子中实现
onMounted(() => {
  // 例如，获取初始的订单列表
});
</script>

<template>
  <div class="MyOrder">
    <!-- 事项的标签列表 -->
    <ul class="tagList">
      <li
        :class="{ selected: curIndex === index }"
        v-for="(item, index) in tagList"
        :key="'tag' + index"
        @click="changeIndex(index)"
      >
        {{ item }}
      </li>
    </ul>

    <!-- 事项列表 -->
    <div class="orderBox">
      <div class="orderTableHeader">
        <span>费用类型</span>
        <span>具体事项</span>
        <span>应付金额</span>
        <span>交易操作</span>
      </div>
      <ul class="orderList">
        <li v-for="item in orderList" :key="'order' + item.id">
          <div class="orderHeader">
            <span class="orderTime">{{ item.createtime }}</span>
            <span class="orderId">{{ '记录号：' + item.id }}</span>
            <span class="state">{{ tagList[item.state + 1] }}</span>
          </div>
          <div class="orderDetail">
            <span class="type">{{ item.params.type }}</span>
            <span class="name">{{ item.params.name }}</span>
            <span class="price">{{ '￥' + item.params.price }}</span>
            <!-- 条件渲染按钮，根据订单状态显示不同的按钮 -->
            <span class="mybutton"><button v-if="item.state === 0" @click="confirmPay(item.id)">确认付款</button></span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped lang="less">
@import './assets/css/var.less';
.MyOrder {
  // 订单标签列表样式
  .tagList {
    // 标签列表项样式
    display: flex;
    justify-content: space-between; // 元素间平均分布，两端对齐
    padding: 0;
    list-style: none; // 移除列表项前的默认标记
    li {
      flex: 1;
      text-align: center;
      font-weight: 550;
      font-size: 18px;
      cursor: pointer;
      padding: 10px 20px;
      border-right: 2px solid #000;
      // 最后一个标签列表项不需要后面的竖线
      &:last-child {
        border-right: none;
      }
    }
    // 选中的标签列表项样式
    .selected {
      color: @thirdColor;
      border-bottom: 2px solid @thirdColor;
    }
  }
  // 订单盒子样式
  .orderBox {
    margin-top: 20px;
    .orderTableHeader {
      display: flex;
      justify-content: space-between;
      background-color: #f5f5f5;
      border: 1px solid @borderColor;
      color: @fontDefaultColor;
      font-size: 14px;
      // 订单表格头部字段样式
      span {
        padding-top: 14px;
        padding-bottom: 14px;
        text-align: center;
        flex: 1;
      }
      span:nth-child(2) {
        flex: 2;
      }
    }
    // 订单列表样式
    .orderList {
      padding: 0;
      list-style: none; // 移除列表项前的默认标记
      li {
        border: 1px solid @borderColor;
        font-size: 13px;
        margin-top: 10px;
        .orderHeader {
          display: flex;
          align-items: center;
          background-color: #f1f1f1;
          padding: 10px 14px;
          .orderTime {
            font-weight: 600;
          }
          .orderId,.state {
            margin-left: 14px;
          }
        }
        .orderDetail {
          display: flex;
          justify-content: space-between;
          align-items: center;
          min-height: 80px;
          text-align: center;
          button {
            width: 70px;
            height: 30px;
            border-radius: 3px;
            background-color: @thirdColor;
            color: white;
            border: none;
          }
          span {
            padding-top: 14px;
            padding-bottom: 14px;
            text-align: center;
            flex: 1;
          }
          span:nth-child(2) {
            flex: 2;
          }
        }
      }
    }
  }
}

.selected {
  color: #333;
  font-weight: bold;
}
</style>
