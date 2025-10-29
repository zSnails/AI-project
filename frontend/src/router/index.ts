import BikeTollModel from '@/components/bike-toll/BikeTollModel.vue';
import CarModel from '@/components/car-price/CarModel.vue';
import CirrhosisModel from '@/components/cirrhosis/CirrhosisModel.vue';
import FaceRecognition from '@/components/face-recognition/FaceRecognition.vue';
import HepatitisModel from '@/components/hepatitis/HepatitisModel.vue';
import StrokeModel from '@/components/stroke/StrokeModel.vue';
import { createRouter, createWebHistory } from 'vue-router';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/models/car-price", component: CarModel },
    { path: "/models/bike-toll", component: BikeTollModel },
    { path: "/models/cirrhosis", component: CirrhosisModel },
    { path: "/models/hepatitis", component: HepatitisModel },
    { path: "/models/stroke", component: StrokeModel },
    { path: "/models/face-recognition", component: FaceRecognition },
  ],
});

export default router;
