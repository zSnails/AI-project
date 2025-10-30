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
                requestUrl.value = `${apiUrl('/api/models/aguacate')}?${params.toString()}`;
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
                    <h1 class="title">Aguacate — Precio</h1>
                    <h2 class="subtitle">{{ prediction !== null ? prediction.toFixed(4) : '—' }}</h2>
                    <form @submit.prevent="submit">
                        <div class="field"><label class="label">Total Volume<input class="input" name="total-volume" type="number" step="0.01" value="64236.62" required /></label></div>
                        <div class="field"><label class="label">4046<input class="input" name="4046" type="number" step="0.01" value="1036.74" required /></label></div>
                        <div class="field"><label class="label">4225<input class="input" name="4225" type="number" step="0.01" value="54454.85" required /></label></div>
                        <div class="field"><label class="label">4770<input class="input" name="4770" type="number" step="0.01" value="48.16" required /></label></div>
                        <div class="field"><label class="label">Total Bags<input class="input" name="total-bags" type="number" step="0.01" value="8696.87" required /></label></div>
                        <div class="field"><label class="label">Small Bags<input class="input" name="small-bags" type="number" step="0.01" value="8603.62" required /></label></div>
                        <div class="field"><label class="label">Large Bags<input class="input" name="large-bags" type="number" step="0.01" value="93.25" required /></label></div>
                        <div class="field"><label class="label">XLarge Bags<input class="input" name="xlarge-bags" type="number" step="0.01" value="0.0" required /></label></div>
                        <div class="field"><label class="label">Type<select class="select" name="type"><option>conventional</option><option>organic</option></select></label></div>
                        <div class="field"><label class="label">Year<input class="input" name="year" type="number" value="2015" required /></label></div>
                        <div class="field"><label class="label">Region<input class="input" name="region" type="text" value="Albany" required /></label></div>
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
