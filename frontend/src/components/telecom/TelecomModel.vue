<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<boolean | null>(null);

async function submit(e: Event) {
    const formData = new FormData(e.target as HTMLFormElement);
    const params = new URLSearchParams(formData as unknown as never);
    const res = await fetch(`http://localhost:8080/api/models/telecomunicaciones?${params.toString()}`);
    const body = await res.json();
    prediction.value = body.prediction;
}
</script>
<template>
    <div>
        <h1 class="title">Telecomunicaciones — Churn</h1>
        <h2 class="subtitle">{{ prediction !== null ? prediction : '—' }}</h2>
        <form @submit.prevent="submit">
            <div class="field"><label class="label">Gender<select class="select" name="gender">
                        <option>Female</option>
                        <option>Male</option>
                    </select></label></div>
            <div class="field"><label class="label">Senior Citizen<input class="input" name="senior-citizen"
                        type="number" value="0" required /></label></div>
            <div class="field"><label class="label">Partner<select class="select" name="partner">
                        <option>Yes</option>
                        <option>No</option>
                    </select></label></div>
            <div class="field"><label class="label">Dependents<select class="select" name="dependents">
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Tenure<input class="input" name="tenure" type="number" value="1"
                        required /></label></div>
            <div class="field"><label class="label">Phone Service<select class="select" name="phone-service">
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Multiple Lines<select class="select" name="multiple-lines">
                        <option>No phone service</option>
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Internet Service<select class="select" name="internet-service">
                        <option>DSL</option>
                        <option>Fiber</option>
                        <option>No</option>
                    </select></label></div>
            <div class="field"><label class="label">Online Security<select class="select" name="online-security">
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Online Backup<select class="select" name="online-backup">
                        <option>Yes</option>
                        <option>No</option>
                    </select></label></div>
            <div class="field"><label class="label">Device Protection<select class="select" name="device-protection">
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Tech Support<select class="select" name="tech-support">
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Streaming TV<select class="select" name="streaming-tv">
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Streaming Movies<select class="select" name="streaming-movies">
                        <option>No</option>
                        <option>Yes</option>
                    </select></label></div>
            <div class="field"><label class="label">Contract<select class="select" name="contract">
                        <option>Month-to-month</option>
                        <option>One year</option>
                        <option>Two year</option>
                    </select></label></div>
            <div class="field"><label class="label">Paperless Billing<select class="select" name="paperless-billing">
                        <option>Yes</option>
                        <option>No</option>
                    </select></label></div>
            <div class="field"><label class="label">Payment Method<select class="select" name="payment-method">
                        <option>Electronic check</option>
                        <option>Mailed check</option>
                        <option>Bank transfer (automatic)</option>
                        <option>Credit card (automatic)</option>
                    </select></label></div>
            <div class="field"><label class="label">Monthly Charges<input class="input" name="monthly-charges"
                        type="number" step="0.01" value="29.85" required /></label></div>
            <div class="field"><label class="label">Total Charges<input class="input" name="total-charges" type="number"
                        step="0.01" value="29.85" required /></label></div>
            <div class="field"><button class="button is-link" type="submit">Enviar</button></div>
        </form>
    </div>
</template>
