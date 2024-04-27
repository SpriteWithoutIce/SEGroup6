import { createRouter, createWebHistory } from 'vue-router'
import BillList from '../components/Bills/BillList.vue'
import Prescription from '../components/Prescription/MakePrescription.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      // 这里是默认路由，后续根据情况修改
      redirect: '/Bill',
    },
    {
      path: '/Bill',
      name: 'Bill',
      component: BillList
    },
    {
      path: '/Prescription',
      name: 'Prescription',
      component: Prescription
    }
  ]
})

export default router
