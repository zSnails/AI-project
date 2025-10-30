<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<string | null>(null);
const isLoading = ref(false);
const requestUrl = ref<string | null>(null);
const rawResponse = ref<unknown>(null);
const resultAt = ref<string | null>(null);

function apiUrl(path: string) {
  if (/^https?:\/\//.test(path)) return path;
  return `http://localhost:8080${path}`;
}

async function submit(e: Event) {
  isLoading.value = true;
  try {
    const formData = new FormData(e.target as HTMLFormElement);
    const params = new URLSearchParams(formData as unknown as never);
    requestUrl.value = `${apiUrl('/api/models/cirrhosis')}?${params.toString()}`;
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
          <h1 class="title">Cirrhosis — Etapa</h1>
          <h2 class="subtitle">{{ prediction ?? '—' }}</h2>
          <form @submit.prevent="submit">
            <div class="field">
              <label class="label">N Days<input class="input" name="n-days" type="number" required /></label>
            </div>
            <div class="field">
              <label class="label">Drug<select class="select" name="drug-code"><option value="0">D-penicillamine</option><option value="1">Placebo</option></select></label>
            </div>
            <div class="field"><label class="label">Age<input class="input" name="age" type="number" required /></label></div>
            <div class="columns">
              <div class="column"><label class="label">Sex<select class="select" name="sex-code"><option value="0">F</option><option value="1">M</option></select></label></div>
              <div class="column"><label class="label">Ascites<select class="select" name="ascites-code"><option value="0">N</option><option value="1">Y</option></select></label></div>
              <div class="column"><label class="label">Hepatomegaly<select class="select" name="hepatomegaly-code"><option value="0">N</option><option value="1">Y</option></select></label></div>
              <div class="column"><label class="label">Spiders<select class="select" name="spiders-code"><option value="0">N</option><option value="1">Y</option></select></label></div>
              <div class="column"><label class="label">Edema<select class="select" name="edema-code"><option value="0">N</option><option value="1">S</option><option value="2">Y</option></select></label></div>
            </div>
            <div class="field"><label class="label">Bilirubin<input class="input" name="bilirubin" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Cholesterol<input class="input" name="cholesterol" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Albumin<input class="input" name="albumin" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Copper<input class="input" name="copper" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Alk Phos<input class="input" name="alk_phos" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">SGOT<input class="input" name="sgot" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Tryglicerides<input class="input" name="tryglicerides" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Platelets<input class="input" name="platelets" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Prothrombin<input class="input" name="prothrombin" type="number" step="0.01" required /></label></div>
            <div class="field"><label class="label">Stage<input class="input" name="stage" type="number" required /></label></div>
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
