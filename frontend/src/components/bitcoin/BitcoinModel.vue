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
        requestUrl.value = `${apiUrl('/api/models/bitcoin')}?${params.toString()}`;
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
                    <h1 class="title">Bitcoin — Dirección</h1>
                    <h2 class="subtitle">{{ prediction !== null ? (prediction ? 'Subirá' : 'No subirá') : '—' }}</h2>
                    <form @submit.prevent="submit">
                        <div class="field"><label class="label">Open<input class="input" name="open" type="number"
                                    step="0.01" value="2763.24" required /></label></div>
                        <div class="field"><label class="label">High<input class="input" name="high" type="number"
                                    step="0.01" value="2889.62" required /></label></div>
                        <div class="field"><label class="label">Low<input class="input" name="low" type="number"
                                    step="0.01" value="2720.61" required /></label></div>
                        <div class="field"><label class="label">Close<input class="input" name="close" type="number"
                                    step="0.01" value="2875.34" required /></label></div>
                        <div class="field"><label class="label">Volume<input class="input" name="volume" type="number"
                                    step="1" value="860575000" required /></label></div>
                        <div class="field"><label class="label">Market Cap<input class="input" name="market-cap"
                                    type="number" step="1" value="45535800000" required /></label></div>
                        <div class="field"><label class="label">Return<input class="input" name="return" type="number"
                                    step="0.0001" value="0.01" required /></label></div>
                        <div class="field"><label class="label">MA3<input class="input" name="ma3" type="number"
                                    value="2800" required /></label></div>
                        <div class="field"><label class="label">MA7<input class="input" name="ma7" type="number"
                                    value="2750" required /></label></div>
                        <div class="field"><label class="label">Volatility<input class="input" name="volatility"
                                    type="number" value="10" required /></label></div>
                        <div class="field"><button class="button is-link" :class="{ 'is-loading': isLoading }"
                                type="submit">Consultar</button></div>
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
