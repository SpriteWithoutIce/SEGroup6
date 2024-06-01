<template>
  <!-- 侧边抽屉 -->
  <div class="myDrawer">
    <el-drawer v-model="table" title="消息列表" direction="rtl" size="40%" >
      <!-- 折叠面板实现消息种类分类 -->
      <div class="demo-collapse">
        <el-collapse v-model="activeNames">
          <el-collapse-item name="1" class="collapseItem1">
            <template #title>
              &nbsp;&nbsp;&nbsp;<el-icon><Calendar /></el-icon>&nbsp;&nbsp;预约通知
            </template>
            <div class="messageList">
              <el-table :data="resMes" style="width: 100%" :row-class-name="tableRowClassName">
                <el-table-column type="expand">
                  <template #default="props">
                    <div v-if="props.row.type == '预约成功'" m="4" class="mesBody">
                      <p>尊敬的患者:</p>
                      <p>您好！您已<b>成功预约</b>了我院的挂号服务。以下是您的预约详情：</p>
                      <strong>
                        <p m="t-0 b-2">- 预约编号: {{ props.row.id }}</p>
                        <p m="t-0 b-2">- 预约科室: {{ props.row.department }}</p>
                        <p m="t-0 b-2">- 预约医生: {{ props.row.doctor }}</p>
                        <p m="t-0 b-2">- 预约就诊时间: {{ props.row.time }}</p>
                      </strong>
                      <p>
                        请您准时到达，并携带<b>有效身份证件及相关病历资料</b>。
                        <br />感谢您选择我院，祝您身体健康！
                      </p>
                      <p style="text-align: right">
                        猫猫就诊ฅ 预约挂号服务中心<br />
                        {{ props.row.timetamp }}
                      </p>
                    </div>
                    <div v-if="props.row.type == '取消预约'" m="4" class="mesBody">
                      <p>尊敬的患者:</p>
                      <p>您好！我们收到了您的<b>预约挂号取消</b>请求。以下是已取消的预约信息：</p>
                      <strong>
                        <p m="t-0 b-2">- 预约编号: {{ props.row.id }}</p>
                        <p m="t-0 b-2">- 预约科室: {{ props.row.department }}</p>
                        <p m="t-0 b-2">- 预约医生: {{ props.row.doctor }}</p>
                        <p m="t-0 b-2">- 预约就诊时间: {{ props.row.time }}</p>
                      </strong>
                      <p>
                        请您注意，若未来需要再次预约，<b>请提前通过我院官网进行预约</b>。
                        <br />感谢您的理解与合作，祝您身体健康！
                      </p>
                      <p style="text-align: right">
                        猫猫就诊 预约挂号服务中心<br />
                        {{ props.row.timetamp }}
                      </p>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="已读?">
                  <template #default="props">
                    <div v-if="props.row.read === false">
                      <el-button class="pay-button" @click="readMes(props.row)">确认</el-button>
                    </div>
                    <!-- 使用 v-else显示文本 -->
                    <div v-else class="butAbanText">已读</div>
                  </template>
                </el-table-column>
                <el-table-column label="类型" prop="type" />
                <el-table-column label="患者姓名" prop="name" />
                <el-table-column label="就诊时间" prop="time" />
              </el-table>
            </div>
          </el-collapse-item>

          <el-collapse-item name="2" class="collapseItem2">
            <template #title>
              &nbsp;&nbsp;&nbsp;<el-icon><Money /></el-icon>&nbsp;&nbsp;处方缴费通知
            </template>
            <div class="messageList">
              <!-- <el-table :data="billMes" style="width: 100%" :row-class-name='success'> -->
              <el-table :data="billMes" style="width: 100%" :row-class-name="tableRowClassName">
                <el-table-column type="expand">
                  <template #default="props">
                    <div m="4" v-if="props.row.type == '处方缴费提醒'" class="mesBody">
                      <p>尊敬的患者:</p>
                      <p>您好！您在我院的就诊处方<b>即将到达缴费截止时间</b>。处方详情如下：</p>
                      <strong>
                        <p m="t-0 b-2">- 处方编号: {{ props.row.id }}</p>
                        <p m="t-0 b-2">- 开具科室: {{ props.row.department }}</p>
                        <p m="t-0 b-2">- 开具医生: {{ props.row.doctor }}</p>
                        <p m="t-0 b-2">- 开具时间: {{ props.row.time }}</p>
                      </strong>
                      <p>
                        请您<b>在30分钟内完成缴费</b>，以免影响您的就诊计划。
                        <br />感谢您的配合，祝您身体健康！
                      </p>
                      <router-link to="/Bill" @click="turnToBill">缴费入口</router-link>
                      <p style="text-align: right">
                        猫猫就诊 缴费服务中心<br />
                        {{ props.row.timetamp }}
                      </p>
                    </div>
                    <div m="4" v-if="props.row.type == '处方缴费成功'" class="mesBody">
                      <p>尊敬的患者:</p>
                      <p>您好！您在我院的就诊处方<b>缴费成功</b>。处方详情如下：</p>
                      <strong>
                        <p m="t-0 b-2">- 处方编号: {{ props.row.id }}</p>
                        <p m="t-0 b-2">- 开具科室: {{ props.row.department }}</p>
                        <p m="t-0 b-2">- 开具医生: {{ props.row.doctor }}</p>
                        <p m="t-0 b-2">- 开具时间: {{ props.row.time }}</p>
                      </strong>
                      <p>
                        感谢您对我们医院的信任与支持。如有任何疑问或需要进一步的帮助，请随时联系我们。祝您身体健康！
                      </p>
                      <p style="text-align: right">
                        猫猫就诊 缴费服务中心<br />
                        {{ props.row.timetamp }}
                      </p>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="已读?">
                  <template #default="props">
                    <div v-if="props.row.read === false">
                      <el-button class="pay-button" @click="readMes(props.row)">确认</el-button>
                    </div>
                    <!-- 使用 v-else显示文本 -->
                    <div v-else class="butAbanText">已读</div>
                  </template>
                </el-table-column>
                <el-table-column label="类型" prop="type" />
                <el-table-column label="患者姓名" prop="name" />
                <el-table-column label="开具时间" prop="time" />
              </el-table>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import notIcon from './notIcon.vue'
import { GlobalState } from '../../global.js';
import { ElNotification } from 'element-plus'
export default {
  props:['msg'],
  data() {
    return {
      activeNames: ['1', '2'],
      table: false,
      timer: null,
      unreadCount: 0,
      firstLoad: true,
      resMes: [
        // {
        //   type: '预约成功',
        //   name: '小黄',
        //   department: '精神科',
        //   doctor: '李医生',
        //   time: '2024-5-12',
        //   id: '03230802',
        //   timetamp: '2024-5-11 23:59:59', //用MySQL中的DATETIME类型就可以
        //   read: false
        // },
        // {
        //   type: '取消预约',
        //   name: '小黄',
        //   department: '精神科',
        //   doctor: '李医生',
        //   time: '2024-5-12',
        //   id: '03230802',
        //   timetamp: '2024-5-11 23:59:59',  //用MySQL中的DATETIME类型就可以
        //   read: false
        // }
      ],
      oriBillMes: [
        // {
        //   type: '处方缴费提醒',
        //   name: '小黄',
        //   department: '精神科',
        //   doctor: '李医生',
        //   time: '2024-5-12',
        //   id: '03230802',
        //   timetamp: '2024-5-11 23:59:59',  //用MySQL中的DATETIME类型就可以
        //   price: 200,
        //   read: false
        // },
        // {
        //   type: '处方缴费成功',
        //   name: '小黄',
        //   department: '精神科',
        //   doctor: '李医生',
        //   time: '2024-5-12',
        //   id: '03230802',
        //   timetamp: '2024-5-11 23:59:59',  //用MySQL中的DATETIME类型就可以
        //   price: 200,
        //   read: false
        // }
      ],
      billMes:[],
    }
  },
  methods: {
    countUnread() {
      // 计算resMes中read为false的数量
      const unreadResMesCount = this.resMes.filter((item) => item.read === false).length
      // 计算billMes中read为false的数量
      const unreadBillMesCount = this.billMes.filter((item) => item.read === false).length
      this.unreadCount = unreadResMesCount + unreadBillMesCount
      if(this.unreadCount > 0 && this.firstLoad === true && this.msg === "true") {
          this.checkNewMsg();
          this.firstLoad = false;
      }
      // 返回两个数量的总和
      // this.$emit('getUnreadCount', unreadResMesCount + unreadBillMesCount)
      this.$emit('update:result', this.unreadCount)
    },
    // post请求，请求数据体中包含用户证件号identityNum
    // url为api/notice/list/
    // 返回数据为resMes和billMes两个字典数组
    getMesData(){
      return new Promise((resolve, reject) => {
        let ts = this;
        this.$axios.post('api/notice/list/', {identity_num: GlobalState.identityNum, action: "getMesData"})
          .then(function (response) {
            ts.resMes = response.data['resMes'];
            ts.oriBillMes = response.data['billMes'];
            ts.payOverTimeQuery();
            console.log(ts.resMes);
            console.log(ts.billMes);
            ts.countUnread();
            resolve(); // 数据获取完成，resolve Promise
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
          console.log('MesDrawer发送的请求参数:', {identity_num: GlobalState.identityNum});
      });
    },
    openDrawer() {
      this.getMesData();
      this.table = true;
    },
    turnToBill() {
      this.table = false
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
      })
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.read === false) {
        return 'warning-row'
      } else if (row.read === true) {
        return 'success-row'
      }
      return ''
    },
    /* done TODO
      1.根据当前用户id和row对应的消息id更改对应消息的阅读状态（未读->已读） 【link-backend！】
      2.重新获取消息，刷新界面
    */
    readMes(row) {
      return new Promise((resolve, reject) => {
        let ts = this;
        //TODO:需要后端在Notice的api里添加action"readMes"，根据传入的item_id找到对应数据将其item['isRead']改为true，不用后端返回更新后的数据，前端直接再调用一次getMesData()就可以
        this.$axios.post('api/notice/list/', {action: "readMes", item_id: row.item_id})
          .then(function (response) {
            ts.getMesData().then(() => {
                resolve(); // 数据获取完成，resolve Promise
            })
          })
          .catch(function (error) {
            console.log(error);
            reject(error); // 数据获取失败，reject Promise
          });
      });
    },
    payOverTimeQuery(){
      this.billMes = [];
      // 获取当前时间的时间戳（毫秒）
      const nowUtcTimestamp = Date.now();
      // 北京时区相对于 UTC 的偏移量（8小时 * 60分钟 * 60秒 * 1000毫秒）
      const beijingUtcOffset = 8 * 60 * 60 * 1000;
      // 将 UTC 时间戳转换为北京时区的时间戳
      const now = nowUtcTimestamp + beijingUtcOffset;
      // 遍历 oriBillMes 数组
      this.oriBillMes.forEach(item => {
        // 将字符串形式的时间戳转换为数字类型的时间戳（毫秒）
        const timetamp = new Date(item.timetamp).getTime();
        // 检查 type 是否为 '处方缴费提醒' 并且 timetamp 时间距离当前时间是否大于30分钟
        // bug 时间戳格式待定
        if ((item.type === '处方缴费提醒' && (now - timetamp) > 30 * 60 * 1000)||item.type === '处方缴费成功') {
          // 如果条件满足，将 item 添加到 billMes 数组
          this.billMes.push(item);
        }
      });
    },
    checkNewMsg(){
      ElNotification({
        icon: notIcon,
        title: '未读消息提示',
        message: '猫猫提示您，有新消息啦，请及时查看哦(>^ω^<)',
        duration: 6000,
        offset: 50
      })
    },
    mounted() {
      if (GlobalState.identityNum === '0') {
        console.log("未登录");
        return;
      }
      this.getMesData().then(() => {
        this.intervalId = setInterval(this.payOverTimeQuery, 30000);
      })
    },
    beforeDestroy() {
      // 组件销毁时清除定时器
      clearInterval(this.intervalId);
    }
  }
}
</script>

<style scoped>
::v-deep .el-drawer{
  background: url("../../assets/message/message-back.jpg");
  background-size: cover;
}
::v-deep .el-drawer__title {
  font-size: 22px;
  font-weight: bold;
  text-shadow: 2px 2px 3px rgba(13, 65, 153, 0.941);
  text-align: left;
  color:rgb(255, 254, 254)
}
::v-deep .el-collapse-item__header{
  font-size: 14px;
  font-weight: bold;
  color:grey
}
.mesBody{
  margin: 20px;
}
.collapseItem1,.collapseItem2{
  padding: 3px;
  background: linear-gradient(#f0f0f0, #fff);
  border: 1px solid #ccc;
  box-shadow: 
    2px 2px 5px rgba(0, 0, 0, 0.3), 
    inset -2px -2px 5px rgba(255, 255, 255, 0.6), 
    inset 2px 2px 5px rgba(0, 0, 0, 0.3);
}
.collapseItem1{
  margin-bottom:10px
}
.el-table >>> .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table >>> .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
