import { createRouter, createWebHistory } from 'vue-router'
import {
  HeaderNavigation, MakePrescription, PrescriptionDetails, Navbar, BillList, BillDetails, AppointmentRegistration, AppointmentRegistration2,
  AppointmentRegistration3, AppointmentRegistration4, AppointmentRegistration5, AppointmentRegistration6, AppointmentRegistration7, AppointmentRegistration8, TableSearch,  DoctorSearch, Picture, PatientA, PresA, MedicineA,PharmaCist
} from '../components/index.js'
import { compileScript } from 'vue/compiler-sfc'
import ReadOnlyVue from '@/components/Main/ReadOnlyVue.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      // 这里是默认路由，后续根据情况修改
      redirect: '/Main',
    },
    {
      path: '/Main',
      name: 'Main',
      component: ReadOnlyVue
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
    },
    {
      path: '/PatientA',
      name: 'PatientA',
      component: PatientA
    },
    {
      path: '/PresA',
      name: 'PresA',
      component: PresA
    },
    {
      path: '/AppointmentRegistration',
      name: 'AppointmentRegistration',
      component: AppointmentRegistration
    },
    {
      path: '/AppointmentRegistration2',
      name: 'AppointmentRegistration2',
      component: AppointmentRegistration2
    },
    {
      path: '/AppointmentRegistration3',
      name: 'AppointmentRegistration3',
      component: AppointmentRegistration3
    },
    {
      path: '/AppointmentRegistration4',
      name: 'AppointmentRegistration4',
      component: AppointmentRegistration4
    },
    {
      path: '/AppointmentRegistration5',
      name: 'AppointmentRegistration5',
      component: AppointmentRegistration5
    },
    {
      path: '/AppointmentRegistration6',
      name: 'AppointmentRegistration6',
      component: AppointmentRegistration6
    },
    {
      path: '/AppointmentRegistration7',
      name: 'AppointmentRegistration7',
      component: AppointmentRegistration7
    },
    {
      path: '/AppointmentRegistration8',
      name: 'AppointmentRegistration8',
      component: AppointmentRegistration8
    },
    {
      path: '/TableSearch',
      name: 'TableSearch',
      component: TableSearch
    },
    {
      path: '/DoctorSearch',
      name: 'DoctorSearch',
      component: DoctorSearch
    },
    {
      path: '/Picture',
      name: 'Picture',
      component: Picture
    },
    {
      path: '/MedicineA',
      name: 'MedicineA',
      component: MedicineA
    },
    {
      path: '/PharmaCist',
      name: 'PharmaCist',
      component: PharmaCist
    },
  ]
})

export default router
