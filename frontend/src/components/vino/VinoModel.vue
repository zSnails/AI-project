<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<number | null>(null);

async function submit(e: Event) {
    const formData = new FormData(e.target as HTMLFormElement);
    const params = new URLSearchParams(formData as unknown as any);
    const res = await fetch(`http://localhost:8080/api/models/vino?${params.toString()}`);
    const body = await res.json();
    prediction.value = body.prediction;
}
</script>
<template>
    <div>
        <h1 class="title">Vino — Predicción calidad</h1>
        <h2 class="subtitle">{{ prediction !== null ? prediction : '—' }}</h2>
        <form @submit.prevent="submit">
            <div class="field"><label class="label">Type<select class="select" name="type">
                        <option>white</option>
                        <option>red</option>
                    </select></label></div>
            <div class="field"><label class="label">Fixed Acidity<input class="input" name="fixed-acidity" type="number"
                        step="0.01" value="7" required /></label></div>
            <div class="field"><label class="label">Volatile Acidity<input class="input" name="volatile-acidity"
                        type="number" step="0.01" value="0.27" required /></label></div>
            <div class="field"><label class="label">Citric Acid<input class="input" name="citric-acid" type="number"
                        step="0.01" value="0.36" required /></label></div>
            <div class="field"><label class="label">Residual Sugar<input class="input" name="residual-sugar"
                        type="number" step="0.01" value="20.7" required /></label></div>
            <div class="field"><label class="label">Chlorides<input class="input" name="chlorides" type="number"
                        step="0.0001" value="0.045" required /></label></div>
            <div class="field"><label class="label">Free sulfur dioxide<input class="input" name="free-sulfur-dioxide"
                        type="number" value="45" required /></label></div>
            <div class="field"><label class="label">Total sulfur dioxide<input class="input" name="total-sulfur-dioxide"
                        type="number" value="170" required /></label></div>
            <div class="field"><label class="label">Density<input class="input" name="density" type="number"
                        step="0.0001" value="1.001" required /></label></div>
            <div class="field"><label class="label">pH<input class="input" name="pH" type="number" step="0.01" value="3"
                        required /></label></div>
            <div class="field"><label class="label">Sulphates<input class="input" name="sulphates" type="number"
                        step="0.01" value="0.45" required /></label></div>
            <div class="field"><label class="label">Alcohol<input class="input" name="alcohol" type="number" step="0.1"
                        value="8.8" required /></label></div>
            <div class="field"><button class="button is-link" type="submit">Enviar</button></div>
        </form>
    </div>
</template>
