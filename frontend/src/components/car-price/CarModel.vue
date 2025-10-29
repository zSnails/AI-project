<script setup lang="ts">
import { ref } from "vue";
import carNameData from "@/components/car-price/all_car_names_codes.json";
const fuelTypes = [
  {"name": "CNG","code": 0},
  {"name": "Diesel","code": 1},
  {"name": "Petrol","code": 2},
];

let prediction = ref<number>(0);

async function submit(form: any) {
  const formData = new FormData(form.target as unknown as HTMLFormElement);
  const params = new URLSearchParams(formData as unknown as any);
  const response = await fetch(`http://localhost:8080/api/models/car-price?${params.toString()}`, { method: "GET" });
  const result = await response.json();
  prediction.value = result.prediction;
}
</script>
<template>
  <div>
    <h1 class="title">Final Prediction</h1>
    <h2 class="subtitle">${{ prediction * 1000 }}</h2>
    <form @submit.prevent="submit">
      <div class="field">
        <label for="car-name-code" class="label">Car Name</label>
        <div class="control">
          <select class="select" name="car-name-code" id="car-name-code" required>
            <option v-for="(row, idx) in carNameData" :key="idx" :value="row.code">{{row.name}}</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="present-price" class="label">Present Price</label>
        <div class="controle">
          <input type="number" class="input" name="present-price" placeholder="2.5k" required
          step="0.01">
        </div>
      </div>
      <div class="field">
        <label for="kms-driven" class="label">Kms Driven</label>
        <div class="controle">
          <input type="number" class="input" name="kms-driven" placeholder="0" required>
        </div>
      </div>
      <div class="field">
        <label for="fuel-type-code" class="label">Fuel Type</label>
        <div class="control">
          <select class="select" name="fuel-type-code" id="fuel-type-code" required>
            <option v-for="(row, idx) in fuelTypes" :key="idx" :value="row.code">{{row.name}}</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="seller-type-code" class="label">Seller Type</label>
        <div class="control">
          <select class="select" name="seller-type-code" id="seller-type-code" required>
            <option :value="0">Dealer</option>
            <option :value="1">Individual</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="transmission-type-code" class="label">Transmission Type</label>
        <div class="control">
          <select class="select" name="transmission-type-code" id="transmission-type-code" required>
            <option :value="0">Automatic</option>
            <option :value="1">Manual</option>
          </select>
        </div>
      </div>
      <input type="number" :value="0" hidden required/>
      <div class="field is-group">
        <div class="control">
          <button type="submit" class="button is-link">Submit</button>
        </div>
      </div>
    </form>
  </div>
</template>
