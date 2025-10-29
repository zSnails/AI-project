<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<number | null>(null);

async function submit(e: Event) {
    const formData = new FormData(e.target as HTMLFormElement);
    const params = new URLSearchParams(formData as unknown as never);
    const res = await fetch(`http://localhost:8080/api/models/aguacate?${params.toString()}`);
    const body = await res.json();
    prediction.value = body.prediction;
}
</script>
<template>
    <div>
        <h1 class="title">Aguacate — Predicción precio</h1>
        <h2 class="subtitle">{{ prediction !== null ? prediction : '—' }}</h2>
        <form @submit.prevent="submit">
            <div class="field"><label class="label">Total Volume<input class="input" name="total-volume" type="number"
                        step="0.01" value="64236.62" required /></label></div>
            <div class="field"><label class="label">4046<input class="input" name="4046" type="number" step="0.01"
                        value="1036.74" required /></label></div>
            <div class="field"><label class="label">4225<input class="input" name="4225" type="number" step="0.01"
                        value="54454.85" required /></label></div>
            <div class="field"><label class="label">4770<input class="input" name="4770" type="number" step="0.01"
                        value="48.16" required /></label></div>
            <div class="field"><label class="label">Total Bags<input class="input" name="total-bags" type="number"
                        step="0.01" value="8696.87" required /></label></div>
            <div class="field"><label class="label">Small Bags<input class="input" name="small-bags" type="number"
                        step="0.01" value="8603.62" required /></label></div>
            <div class="field"><label class="label">Large Bags<input class="input" name="large-bags" type="number"
                        step="0.01" value="93.25" required /></label></div>
            <div class="field"><label class="label">XLarge Bags<input class="input" name="xlarge-bags" type="number"
                        step="0.01" value="0.0" required /></label></div>
            <div class="field"><label class="label">Type<select class="select" name="type">
                        <option>conventional</option>
                        <option>organic</option>
                    </select></label></div>
            <div class="field"><label class="label">Year<input class="input" name="year" type="number" value="2015"
                        required /></label></div>
            <div class="field"><label class="label">Region<input class="input" name="region" type="text" value="Albany"
                        required /></label></div>
            <div class="field"><button class="button is-link" type="submit">Enviar</button></div>
        </form>
    </div>
</template>
