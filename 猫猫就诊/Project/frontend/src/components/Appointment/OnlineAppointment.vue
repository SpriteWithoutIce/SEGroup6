<template>
  <div style="height: 300px;width: auto;align-items: center;display: flex; flex-direction: column;">占位</div>
  <div id="appMenu" class="infoSubNav">
    <div class="display: flex; flex-direction: column;">
      <ul class="ul">
        <li id="search" class="li li667"><a href="https://www.gdghospital.org.cn/czcx/index.html"><i></i><span>出诊查询</span></a></li> 
        <li id="predict" class="li li81 on"><a href="https://www.gdghospital.org.cn/OnlineAppointment/index.html"><i></i><span>网上预约挂号</span></a></li> 
        <li id="guide1" class="li li82"><a href="https://www.gdghospital.org.cn/AppointmentGuide/index.html"><i></i><span>门诊预约指南</span></a></li> 
        <li id="guide2" class="li li83"><a href="https://www.gdghospital.org.cn/ScheduleProcess/index.html"><i></i><span>预约检查流程</span></a></li> 
        <li class="li licancel btn_li"><a href="javascript:"><i></i><span>取消预约</span></a></li> 
      </ul>
    </div>
    <div id="app" style="display: flex; flex-direction: column;">
      <ul style="display: flex; flex-direction: row;">
        <li class="li2on"><span>就诊需知</span></li> 
        <li class="li"><span>挂号类别</span></li> 
        <li class="li"><span>填写预约信息</span></li> 
        <li class="li"><span>选择科室</span></li> 
        <li class="li"><span>选择医生</span></li> 
        <li class="li"><span>选择时间地点</span></li> 
        <li class="li"><span>核对预约信息</span></li> 
        <li class="li"><span>预约成功</span></li>
      </ul> 
      <div class="clear"></div>
      </div> 
  </div>
  
    

  



</template>

<script>

</script>

<style>
.infoSubNav {display: flex; flex-direction: column;}
.infoSubNav .ul{font-size: 0;text-align: center;margin-bottom: 80px;overflow: hidden;}
.infoSubNav .ul>li{display: inline-block;vertical-align: top;margin: 2px 24px;}
.infoSubNav .ul>li>a{display: block;overflow: hidden;background: #f3f6fa;font-size: 16px;color: #333;padding: 30px 32px;line-height: 22px;border-radius: 5px;}
.infoSubNav .ul>li i{display: block;margin: 0 auto 15px;width: 32px;height: 32px;background: center no-repeat;}
.infoSubNav .ul>li>a:hover{color: #fff;background: #1a4e95;}
.infoSubNav .ul>li.on>a{color: #fff;background: #1a4e95;}

.li2on span{background-color: #ff8900;color: #fff;}
</style>