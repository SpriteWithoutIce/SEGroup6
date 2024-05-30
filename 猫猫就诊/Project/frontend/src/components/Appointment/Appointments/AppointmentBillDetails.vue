<template>
  <div class="modal-background" v-if="isVisible">
    <div class="modal-container">
      <el-form
        :model="form"
        class="form"
        label-width="auto"
        style="max-width: 600px"
      >
        <el-form-header class="form-header">缴费详情</el-form-header>
        <el-form-item label="类型">
          {{ form.type }}
        </el-form-item>
        <el-form-item label="具体事由">
          {{ form.issue }}
        </el-form-item>
        <el-form-item label="费用（元）">
          {{ form.price }}
        </el-form-item>
        <el-form-item label="创建时间">
          {{ form.date }}
        </el-form-item>
        <div class="button-group">
          <!-- 确认缴费按钮 -->
          <el-button @click="submitForm" type="primary" :plain="true"
            >确认缴费</el-button
          >
          <!-- 取消缴费按钮 -->
          <el-button @click="cancelModal">取消</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";

export default {
  name: "BillDetails",
  data() {
    return {
      isVisible: false,
      form: {
        type: "",
        issue: "",
        price: 0,
        date: "",
        id: 0,
      },
    };
  },
  methods: {
    // 触发弹窗（在父组件中引用）
    openModal(row) {
      this.isVisible = true;
      document.body.style.overflow = "hidden"; // 禁止滚动
      this.form.type = row.type;
      this.form.issue = row.issue;
      this.form.price = row.price;
      this.form.date = row.date;
      this.form.id = row.id;
    },
    // 关闭弹窗
    closeModal() {
      this.isVisible = false;
      document.body.style.overflow = ""; // 恢复滚动
    },
    // 取消按钮触发
    cancelModal() {
      ElMessage({
        type: "info",
        message: "取消缴费 ╮(╯▽╰)╭",
        showClose: true,
      });
      // 关闭弹窗
      this.closeModal();
    },
    // 确认缴费
    submitForm () {
      // 修改数据库
      this.$emit('billDetailsUpdated', true);
      ElMessage({
        showClose: true,
        message: "缴费成功 ╰(*°▽°*)╯",
        type: "success",
      });
      // 提交后关闭弹窗
      this.closeModal();
    },
  },
};
</script>

<style scoped>
.form {
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.el-form-item {
  margin-bottom: 15px;
}

.el-form-item__label {
  font-weight: bold;
}

.el-form-item__content {
  font-size: 14px;
}

.modal-background {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 8;
}

.modal-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
}

.button-group {
  margin-top: 20px;
  text-align: center;
}

.delete-button {
  width: 14%;
  text-align: left;
}

.form-header {
  display: flex;
  justify-content: center;
  font-size: 24px;
  /* 字体大小 */
  font-weight: bold;
  /* 字体加粗 */
  color: #333;
  /* 字体颜色 */
  margin-bottom: 20px;
  /* 下边距 */
}
</style>
