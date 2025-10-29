<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<number | null>(null);

async function submit(e: Event) {
    const formData = new FormData(e.target as HTMLFormElement);
    const params = new URLSearchParams(formData as unknown as any);
    const res = await fetch(`http://localhost:8080/api/models/grasa?${params.toString()}`);
    const body = await res.json();
    prediction.value = body.prediction;
}
</script>
<template>
    <div>
        <h1 class="title">Grasa corporal — BodyFat</h1>
        <h2 class="subtitle">{{ prediction !== null ? prediction : '—' }}</h2>
        <form @submit.prevent="submit">
            <div class="field"><label class="label">Age<input class="input" name="age" type="number" value="23"
                        required /></label></div>
            <div class="field"><label class="label">Weight<input class="input" name="weight" type="number" step="0.01"
                        value="154.25" required /></label></div>
            <div class="field"><label class="label">Height<input class="input" name="height" type="number" step="0.01"
                        value="67.75" required /></label></div>
            <div class="field"><label class="label">Neck<input class="input" name="neck" type="number" step="0.01"
                        value="36.2" required /></label></div>
            <div class="field"><label class="label">Chest<input class="input" name="chest" type="number" step="0.01"
                        value="93.1" required /></label></div>
            <div class="field"><label class="label">Abdomen<input class="input" name="abdomen" type="number" step="0.01"
                        value="85.2" required /></label></div>
            <div class="field"><label class="label">Hip<input class="input" name="hip" type="number" step="0.01"
                        value="94.5" required /></label></div>
            <div class="field"><label class="label">Thigh<input class="input" name="thigh" type="number" step="0.01"
                        value="59.0" required /></label></div>
            <div class="field"><label class="label">Knee<input class="input" name="knee" type="number" step="0.01"
                        value="37.3" required /></label></div>
            <div class="field"><label class="label">Ankle<input class="input" name="ankle" type="number" step="0.01"
                        value="21.9" required /></label></div>
            <div class="field"><label class="label">Biceps<input class="input" name="biceps" type="number" step="0.01"
                        value="32.0" required /></label></div>
            <div class="field"><label class="label">Forearm<input class="input" name="forearm" type="number" step="0.01"
                        value="27.4" required /></label></div>
            <div class="field"><label class="label">Wrist<input class="input" name="wrist" type="number" step="0.01"
                        value="17.1" required /></label></div>
            <div class="field"><button class="button is-link" type="submit">Enviar</button></div>
        </form>
    </div>
</template>
