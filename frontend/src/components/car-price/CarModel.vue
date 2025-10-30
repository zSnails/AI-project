<script setup lang="ts">
import { ref } from 'vue';
import carNameData from '@/components/car-price/all_car_names_codes.json';

const fuelTypes = [
  { name: 'CNG', code: 0 },
  { name: 'Diesel', code: 1 },
  { name: 'Petrol', code: 2 },
];

const prediction = ref<number | null>(null);
const isLoading = ref(false);
const requestUrl = ref<string | null>(null);
const rawResponse = ref<unknown>(null);
const resultAt = ref<string | null>(null);

function apiUrl(path: string) {
  if (/^https?:\/\//.test(path)) return path;
  return `http://localhost:8080${path}`;
}

async function submit(form: Event) {
  isLoading.value = true;
  try {
    const formData = new FormData(form.target as HTMLFormElement);
    const params = new URLSearchParams(formData as unknown as never);
    requestUrl.value = `${apiUrl('/api/models/car-price')}?${params.toString()}`;
    const response = await fetch(requestUrl.value, { method: 'GET' });
    const result = await response.json();
    rawResponse.value = result;
    prediction.value = result.prediction;
    resultAt.value = new Date().toLocaleString();
  } finally {
    isLoading.value = false;
  }
}
</script>
<template>
  <div class="model-card card">
    <div class="card-content">
      <div class="columns">
        <div class="column is-half">
          <h1 class="title">Car Price — Predicción</h1>
          <h2 class="subtitle">{{ prediction !== null ? (prediction * 1000).toFixed(2) : '—' }}</h2>
          <form @submit.prevent="submit">
            <div class="field">
              <label for="car-name-code" class="label">Car Name</label>
              <div class="control">
                <select class="select" name="car-name-code" id="car-name-code" required>
                  <option v-for="(row, idx) in carNameData" :key="idx" :value="row.code">{{ row.name }}</option>
                </select>
              </div>
            </div>
            <div class="field">
              <label for="present-price" class="label">Present Price</label>
              <div class="control">
                <input type="number" class="input" name="present-price" placeholder="2.5k" required step="0.01" />
              </div>
            </div>
            <div class="field">
              <label for="kms-driven" class="label">Kms Driven</label>
              <div class="control">
                <input type="number" class="input" name="kms-driven" placeholder="0" required />
              </div>
            </div>
            <div class="field">
              <label for="fuel-type-code" class="label">Fuel Type</label>
              <div class="control">
                <select class="select" name="fuel-type-code" id="fuel-type-code" required>
                  <option v-for="(row, idx) in fuelTypes" :key="idx" :value="row.code">{{ row.name }}</option>
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
              <label for="transmission-code" class="label">Transmission Type</label>
              <div class="control">
                <select class="select" name="transmission-code" id="transmission-code" required>
                  <option :value="0">Automatic</option>
                  <option :value="1">Manual</option>
                </select>
              </div>
            </div>
            <input type="number" value="0" hidden name="owner" required />
            <div class="field is-group">
              <div class="control">
                <button type="submit" class="button is-link" :class="{ 'is-loading': isLoading }">Consultar</button>
              </div>
            </div>
          </form>
        </div>
        <div class="column is-half">
          <div class="box">
            <p><strong>URL:</strong> <code v-if="requestUrl">{{ requestUrl }}</code></p>
            <p v-if="resultAt" class="is-size-7 has-text-grey">Resultado: {{ resultAt }}</p>
            <div v-if="rawResponse">
              <p class="has-text-weight-semibold">Respuesta</p>
              <pre class="raw-box">{{ JSON.stringify(rawResponse, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.model-card {
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(10, 10, 10, 0.06);
  padding: 0.75rem;
}

.raw-box {
  max-height: 260px;
  overflow: auto;
  background: #0f1720;
  color: #e6eef8;
  padding: 8px;
  border-radius: 4px;
}
</style>
