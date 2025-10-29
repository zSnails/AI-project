<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref<number>(0);

async function submit(form: any) {
  const formData = new FormData(form.target as HTMLFormElement);
  const params = new URLSearchParams(formData as unknown as any);
  const response = await fetch(`http://localhost:8080/api/models/bike-toll?${params.toString()}`, { method: "GET"});
  const result = await response.json();
  prediction.value = result.prediction;
}

</script>
<template>
  <div>
    <h1 class="title">Final Prediction</h1>
    <h2 class="subtitle">${{ prediction }}</h2>
    <form @submit.prevent="submit">
      <div class="field">
        <label for="distance" class="label">Distance</label>
        <div class="control">
          <input type="number" name="distance" class="input" step="0.01" placeholder="0" required>
        </div>
      </div>
      <div class="field">
        <label for="rate-code" class="label">Rate Code</label>
        <div class="control">
          <select name="rate-code" id="rate-code" class="select">
            <option :value="1">1</option>
            <option :value="2">2</option>
            <option :value="3">3</option>
            <option :value="4">4</option>
            <option :value="5">5</option>
            <option :value="6">6</option>
            <option :value="99">99</option>
          </select>
        </div>
      </div>
      <div class="field is-group">
        <div class="control">
          <button class="button is-link" type="submit">Predict</button>
        </div>
      </div>
    </form>
  </div>
</template>
