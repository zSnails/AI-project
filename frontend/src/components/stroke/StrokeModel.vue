<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref(null);
async function submit(form: any) {
  const formData = new FormData(form.target as unknown as HTMLFormElement);

  const hypertension = formData.get("hypertension")
  formData.set("hypertension", hypertension === "on" ? '1' : '0');
  const heartDisease = formData.get("heart-disease")
  formData.set("heart-disease", heartDisease === "on" ? '1' : '0');
  const married = formData.get("ever-married-code")
  formData.set("ever-married-code", married === "on" ? '1' : '0');

  const params = new URLSearchParams(formData as unknown as any);
  const response = await fetch(`http://localhost:8080/api/models/stroke?${params.toString()}`, { method: "GET" });
  const result = await response.json();
  prediction.value = result.prediction;
}
</script>
<template>
  <div>
    <h1 class="title">Prediction Result</h1>
    <h2 v-if="prediction !== null" class="subtitle">
      <p1 v-if="prediction">Will have a stroke</p1>
      <p1 v-else>Will not have a stroke</p1>
    </h2>
    <form @submit.prevent="submit">
      <div class="field">
        <label for="age" class="label">Age</label>
        <div class="control">
          <input type="number" name="age" class="input" placeholder="0" required>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <div class="checkboxes">
            <label for="hypertension" class="checkbox">
              <input type="checkbox" name="hypertension" class="checkbox">
              Hypertension
            </label>
            <label for="heart-disease" class="checkbox">
              <input type="checkbox" name="heart-disease" class="checkbox">
              Heart Disease
            </label>
            <label for="ever-married-code" class="checkbox">
              <input type="checkbox" name="ever-married-code" class="checkbox">
              Ever Married
            </label>
          </div>
        </div>
      </div>
      <div class="field">
        <label for="avg-glucose-level" class="label">Average Glucose Level</label>
        <div class="control">
          <input type="number" for="avg-glucose-level" step="0.01" class="input" placeholder="0" required>
        </div>
      </div>
      <div class="field">
        <label for="bmi" class="label">BMI</label>
        <div class="control">
          <input type="number" for="bmi" step="0.01" class="input" placeholder="0" required>
        </div>
      </div>
      <div class="field is-group">
        <div class="control">
          <button type="submit" class="button is-link">Predict</button>
        </div>
      </div>
    </form>
  </div>
</template>
