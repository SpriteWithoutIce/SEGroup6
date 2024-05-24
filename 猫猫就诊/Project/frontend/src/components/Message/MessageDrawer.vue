<template>
  <!-- 侧边抽屉 -->
  <div class="myDrawer">
    <el-drawer v-model="table" title="消息列表" direction="rtl" size="40%">
      <!-- 折叠面板实现消息种类分类 -->
      <div class="demo-collapse">
        <el-collapse v-model="activeNames" @change="handleChange">
          <el-collapse-item title="预约通知" name="1" class="collapseItem">
            <div class="messageList">
              <el-table :data="resMes" style="width: 100%" :row-class-name="tableRowClassName">
                <el-table-column type="expand">
                  <template #default="props">
                    <div v-if="props.row.type == '预约成功'" m="4">
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
                    <div v-if="props.row.type == '取消预约'" m="4">
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

          <el-collapse-item title="缴费通知" name="2">
            <div class="messageList">
              <!-- <el-table :data="billMes" style="width: 100%" :row-class-name='success'> -->
              <el-table :data="billMes" style="width: 100%" :row-class-name="tableRowClassName">
                <el-table-column type="expand">
                  <template #default="props">
                    <div m="4" v-if="props.row.type == '处方缴费提醒'">
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
                    <div m="4" v-if="props.row.type == '处方缴费成功'">
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
                <el-table-column label="时间" prop="time" />
              </el-table>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-drawer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeNames: ['1', '2'],
      table: false,
      timer: null,
      resMes: [
        {
          type: '预约成功',
          name: '小黄',
          department: '精神科',
          doctor: '李医生',
          time: '2024-5-12',
          id: '03230802',
          timetamp: '2024-5-11',
          read: true
        },
        {
          type: '取消预约',
          name: '小黄',
          department: '精神科',
          doctor: '李医生',
          time: '2024-5-12',
          id: '03230802',
          timetamp: '2024-5-11',
          read: false
        }
      ],
      billMes: [
        {
          type: '处方缴费提醒',
          name: '小黄',
          department: '精神科',
          doctor: '李医生',
          time: '2024-5-12',
          id: '03230802',
          timetamp: '2024-5-11',
          price: 200,
          read: false
        },
        {
          type: '处方缴费成功',
          name: '小黄',
          department: '精神科',
          doctor: '李医生',
          time: '2024-5-12',
          id: '03230802',
          timetamp: '2024-5-11',
          price: 200,
          read: false
        }
      ]
    }
  },
  methods: {

    // post请求，请求数据体中包含用户证件号identity_num
    // url为api/notice/list/
    // 返回数据为resMes和billMes两个字典数组
    openDrawer() {
      this.table = true
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
    countUnread() {
      // 计算resMes中read为false的数量
      const unreadResMesCount = this.resMes.filter((item) => item.read === false).length
      // 计算billMes中read为false的数量
      const unreadBillMesCount = this.billMes.filter((item) => item.read === false).length
      // 返回两个数量的总和
      // this.$emit('getUnreadCount', unreadResMesCount + unreadBillMesCount)
      this.$emit('update:result', unreadResMesCount + unreadBillMesCount)
    },
    readMes(row) {
      row.read = true;
      this.countUnread();
    }
  }
}
</script>

<style scoped>
.el-table >>> .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table >>> .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
