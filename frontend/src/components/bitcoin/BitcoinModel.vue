<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<number | null>(null);

async function submit(e: Event) {
    const formData = new FormData(e.target as HTMLFormElement);
    const params = new URLSearchParams(formData as unknown as never);
    const res = await fetch(`http://localhost:8080/api/models/bitcoin?${params.toString()}`);
    const body = await res.json();
    prediction.value = body.prediction;
}
</script>
<template>
    <div>
        <h1 class="title">Bitcoin — Dirección</h1>
        <h2 class="subtitle">{{ prediction !== null ? prediction : '—' }}</h2>
        <form @submit.prevent="submit">
            <div class="field"><label class="label">Open<input class="input" name="open" type="number" step="0.01"
                        value="2763.24" required /></label></div>
            <div class="field"><label class="label">High<input class="input" name="high" type="number" step="0.01"
                        value="2889.62" required /></label></div>
            <div class="field"><label class="label">Low<input class="input" name="low" type="number" step="0.01"
                        value="2720.61" required /></label></div>
            <div class="field"><label class="label">Close<input class="input" name="close" type="number" step="0.01"
                        value="2875.34" required /></label></div>
            <div class="field"><label class="label">Volume<input class="input" name="volume" type="number" step="1"
                        value="860575000" required /></label></div>
            <div class="field"><label class="label">Market Cap<input class="input" name="market-cap" type="number"
                        step="1" value="45535800000" required /></label></div>
            <div class="field"><label class="label">Return<input class="input" name="return" type="number" step="0.0001"
                        value="0.01" required /></label></div>
            <div class="field"><label class="label">MA3<input class="input" name="ma3" type="number" value="2800"
                        required /></label></div>
            <div class="field"><label class="label">MA7<input class="input" name="ma7" type="number" value="2750"
                        required /></label></div>
            <div class="field"><label class="label">Volatility<input class="input" name="volatility" type="number"
                        value="10" required /></label></div>
            <div class="field"><button class="button is-link" type="submit">Enviar</button></div>
        </form>
    </div>
</template>
