// lyx 这是干嘛用的？
// zjh 把组件打包后export，方便在router/index.js里面import
import HeaderNavigation from "./Navigation/HeaderNavigation.vue";
import MakePrescription from "./Prescription/MakePrescription.vue";
import PrescriptionDetails from "./Prescription/PrescriptionDetails.vue";
import Navbar from "./Navigation/Navbar.vue";
import BillList from "./Bills/BillList.vue";
import BillDetails from "./Bills/BillDetails.vue";
import PatientA from "./History/PatientA.vue";
export {HeaderNavigation, MakePrescription, PrescriptionDetails, Navbar, BillList, BillDetails,PatientA}