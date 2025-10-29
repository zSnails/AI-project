import CarModel from "@/components/car-price/CarModel.vue";
import AguacateModel from "@/components/aguacate/AguacateModel.vue";
import BitcoinModel from "@/components/bitcoin/BitcoinModel.vue";
import VinoModel from "@/components/vino/VinoModel.vue";
import TelecomModel from "@/components/telecom/TelecomModel.vue";
import GrasaModel from "@/components/grasa/GrasaModel.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/models/car-price", component: CarModel },
    { path: "/models/aguacate", component: AguacateModel },
    { path: "/models/bitcoin", component: BitcoinModel },
    { path: "/models/vino", component: VinoModel },
    { path: "/models/telecomunicaciones", component: TelecomModel },
    { path: "/models/grasa", component: GrasaModel },
  ],
});

export default router;
