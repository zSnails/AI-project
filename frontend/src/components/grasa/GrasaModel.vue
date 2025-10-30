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

async function submit(e: Event) {
        isLoading.value = true;
        try {
                const formData = new FormData(e.target as HTMLFormElement);
                const params = new URLSearchParams(formData as unknown as never);
                requestUrl.value = `${apiUrl('/api/models/grasa')}?${params.toString()}`;
                const res = await fetch(requestUrl.value);
                const body = await res.json();
                rawResponse.value = body;
                prediction.value = body.prediction;
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
                    <h1 class="title">Grasa corporal — BodyFat</h1>
                    <h2 class="subtitle">{{ prediction !== null ? prediction : '—' }}</h2>
                    <form @submit.prevent="submit">
                        <div class="field"><label class="label">Age<input class="input" name="age" type="number" value="23" required /></label></div>
                        <div class="field"><label class="label">Weight<input class="input" name="weight" type="number" step="0.01" value="154.25" required /></label></div>
                        <div class="field"><label class="label">Height<input class="input" name="height" type="number" step="0.01" value="67.75" required /></label></div>
                        <div class="field"><label class="label">Neck<input class="input" name="neck" type="number" step="0.01" value="36.2" required /></label></div>
                        <div class="field"><label class="label">Chest<input class="input" name="chest" type="number" step="0.01" value="93.1" required /></label></div>
                        <div class="field"><label class="label">Abdomen<input class="input" name="abdomen" type="number" step="0.01" value="85.2" required /></label></div>
                        <div class="field"><label class="label">Hip<input class="input" name="hip" type="number" step="0.01" value="94.5" required /></label></div>
                        <div class="field"><label class="label">Thigh<input class="input" name="thigh" type="number" step="0.01" value="59.0" required /></label></div>
                        <div class="field"><label class="label">Knee<input class="input" name="knee" type="number" step="0.01" value="37.3" required /></label></div>
                        <div class="field"><label class="label">Ankle<input class="input" name="ankle" type="number" step="0.01" value="21.9" required /></label></div>
                        <div class="field"><label class="label">Biceps<input class="input" name="biceps" type="number" step="0.01" value="32.0" required /></label></div>
                        <div class="field"><label class="label">Forearm<input class="input" name="forearm" type="number" step="0.01" value="27.4" required /></label></div>
                        <div class="field"><label class="label">Wrist<input class="input" name="wrist" type="number" step="0.01" value="17.1" required /></label></div>
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
