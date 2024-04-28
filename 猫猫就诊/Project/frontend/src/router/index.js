import { createRouter, createWebHistory } from 'vue-router'
import {HeaderNavigation, MakePrescription, PrescriptionDetails, Navbar, BillList, BillDetails} from '../components/index.js'
import { compileScript } from 'vue/compiler-sfc'

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
      component: MakePrescription
    }
  ]
})

export default router
