<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<boolean | null>(null);
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
    // normalize checkboxes
    const hypertension = formData.get('hypertension');
    formData.set('hypertension', hypertension === 'on' ? '1' : '0');
    const heartDisease = formData.get('heart-disease');
    formData.set('heart-disease', heartDisease === 'on' ? '1' : '0');
    const married = formData.get('ever-married-code');
    formData.set('ever-married-code', married === 'on' ? '1' : '0');

    const params = new URLSearchParams(formData as unknown as never);
    requestUrl.value = `${apiUrl('/api/models/stroke')}?${params.toString()}`;
    const response = await fetch(requestUrl.value);
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
          <h1 class="title">Stroke — Riesgo</h1>
          <h2 class="subtitle">
            <span v-if="prediction === null">—</span>
            <span v-else-if="prediction">Probable</span>
            <span v-else>No probable</span>
          </h2>
          <form @submit.prevent="submit">
            <div class="field"><label class="label">Age<input class="input" name="age" type="number" required /></label></div>
            <div class="field">
              <label class="checkbox"><input type="checkbox" name="hypertension"> Hypertension</label>
              <label class="checkbox"><input type="checkbox" name="heart-disease"> Heart Disease</label>
              <label class="checkbox"><input type="checkbox" name="ever-married-code"> Ever Married</label>
            </div>
            <div class="field"><label class="label">Average Glucose Level<input class="input" name="avg-glocose-level" step="0.01" type="number" required /></label></div>
            <div class="field"><label class="label">BMI<input class="input" name="bmi" step="0.01" type="number" required /></label></div>
            <div class="field"><button class="button is-link" :class="{ 'is-loading': isLoading }" type="submit">Consultar</button></div>
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
.model-card { border-radius: 8px; box-shadow: 0 6px 18px rgba(10,10,10,0.06); padding: 0.75rem; }
.raw-box { max-height: 260px; overflow: auto; background: #0f1720; color: #e6eef8; padding: 8px; border-radius: 4px; }
</style>
