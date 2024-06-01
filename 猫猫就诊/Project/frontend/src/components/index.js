// lyx 这是干嘛用的？
// zjh 把组件打包后export，方便在router/index.js里面import
import HeaderNavigation from "./Navigation/HeaderNavigation.vue";
import MakePrescription from "./Prescription/MakePrescription.vue";
import PrescriptionDetails from "./Prescription/PrescriptionDetails.vue";
import Navbar from "./Navigation/Navbar.vue";
import BillList from "./Bills/BillList.vue";
import BillDetails from "./Bills/BillDetails.vue";

import ReadOnlyVue from "./Main/ReadOnlyVue.vue";
import PatientA from "./History/PatientA.vue";
import PresA from "./History/PresA.vue";
import MedicineA from "./Medicine/MedicineA.vue";
import PharmaCist from "./Medicine/PharmaCist.vue";
import AppointmentRegistration from "./Appointment/AppointmentRegistration.vue";
import AppointmentRegistration2 from "./Appointment/AppointmentRegistration2.vue";
import AppointmentRegistration3 from "./Appointment/AppointmentRegistration3.vue";
import AppointmentRegistration4 from "./Appointment/AppointmentRegistration4.vue";
import AppointmentRegistration5 from "./Appointment/AppointmentRegistration5.vue";
import AppointmentRegistration6 from "./Appointment/AppointmentRegistration6.vue";
import AppointmentRegistration7 from "./Appointment/AppointmentRegistration7.vue";
import AppointmentRegistration8 from "./Appointment/AppointmentRegistration8.vue";
import TableSearch from "./Table/TableSearch.vue";
import DoctorSearch from "./Table/DoctorSearch.vue";
import Picture from "./Table/Picture.vue"
export {
  ReadOnlyVue, HeaderNavigation, MakePrescription, PrescriptionDetails, Navbar, BillList, BillDetails, AppointmentRegistration, AppointmentRegistration2,
  AppointmentRegistration3, AppointmentRegistration4, AppointmentRegistration5, AppointmentRegistration6, AppointmentRegistration7, AppointmentRegistration8, TableSearch,  DoctorSearch, Picture, PatientA, PresA, MedicineA,PharmaCist
}
