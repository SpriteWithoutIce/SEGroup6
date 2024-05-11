<template>
  <div class="input-container">
    <div class="chaxun">
      <el-input
        v-model="input4"
        style="width: 300px; height: 40px"
        placeholder="请输入就诊日期 或 就诊科室"
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
        >查询</el-button
      >
      <p>{{ input4 }}</p>
    </div>
  </div>
</template>
<script></script>
<style scoped>
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
