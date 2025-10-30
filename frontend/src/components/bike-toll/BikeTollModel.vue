<script setup lang="ts">
import { ref } from 'vue';

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
    requestUrl.value = `${apiUrl('/api/models/bike-toll')}?${params.toString()}`;
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
          <h1 class="title">Bike Toll — Precio</h1>
          <h2 class="subtitle">{{ prediction !== null ? prediction : '—' }}</h2>
          <form @submit.prevent="submit">
            <div class="field">
              <label for="distance" class="label">Distance</label>
              <div class="control">
                <input type="number" name="distance" class="input" step="0.01" placeholder="0" required>
              </div>
            </div>
            <div class="field">
              <label for="rate-code" class="label">Rate Code</label>
              <div class="control">
                <select name="rate-code" id="rate-code" class="select">
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5</option>
                  <option value="6">6</option>
                  <option value="99">99</option>
                </select>
              </div>
            </div>
            <div class="field is-group">
              <div class="control">
                <button class="button is-link" :class="{ 'is-loading': isLoading }" type="submit">Consultar</button>
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
