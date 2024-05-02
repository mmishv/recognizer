import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import LoanCalculator from '@/pages/FormulaRecognizer.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Loan Calculator',
    component: LoanCalculator
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router
