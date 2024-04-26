import { HeaderNavigation, MakePrescription, PrescriptionDetails, Navbar } from "../components/index.js"

export default new Router({
    routes: [
        {
            path: '/',
            name: 'main',
            component: HeaderNavigation, MakePrescription, PrescriptionDetails, Navbar
        }
    ]
})