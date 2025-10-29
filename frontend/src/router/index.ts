import CarModel from '@/components/car-price/CarModel.vue';
import { createRouter, createWebHistory } from 'vue-router';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/models/car-price", component: CarModel }
  ],
});

export default router;
