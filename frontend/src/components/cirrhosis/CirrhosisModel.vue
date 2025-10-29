<script setup lang="ts">
import { ref } from 'vue';

const prediction = ref("");
async function submit(form: any) {
  const formData = new FormData(form.target as unknown as HTMLFormElement);
  const params = new URLSearchParams(formData as unknown as any);
  const response = await fetch(`http://localhost:8080/api/models/cirrhosis?${params.toString()}`, { method: "GET" });
  const result = await response.json();
  prediction.value = result.prediction;
}
</script>
<template>
  <div>
    <h1 class="title">Cirrhosis Class Prediction</h1>
    <h2 class="subtitle">Predicted: {{ prediction }}</h2>
    <form @submit.prevent="submit">
      <div class="field">
        <label class="label" for="n-days">N Days</label>
        <div class="control">
          <input type="number" class="input" name="n-days" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="drug-code" class="label">Drug</label>
        <div class="control">
          <select name="drug-code" id="drug-code" class="select" required>
            <option :value="0">D-penicillamine</option>
            <option :value="1">Placebo</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="age" class="label">Age</label>
        <div class="control">
          <input type="number" class="input" required placeholder="0">
        </div>
      </div>
      <div class="columns">
        <div class="column">
          <div class="field">
            <label for="sex-code" class="label">Sex</label>
            <div class="control">
              <select name="sex-code" id="sex-code" class="select" required>
                <option :value="0">F</option>
                <option :value="1">M</option>
              </select>
            </div>
          </div>
        </div>
        <div class="column">
          <div class="field">
            <label for="ascites-code" class="label">Ascites?</label>
            <div class="control">
              <select name="ascites-code" id="ascites-code" class="select" required>
                <option :value="0">N</option>
                <option :value="1">Y</option>
              </select>
            </div>
          </div>
        </div>
        <div class="column">
          <div class="field">
            <label for="hepatomegaly-code" class="label">Hepatomegaly?</label>
            <div class="control">
              <select name="hepatomegaly-code" id="hepatomegaly-code" class="select" required>
                <option :value="0">N</option>
                <option :value="1">Y</option>
              </select>
            </div>
          </div>
        </div>
        <div class="column">
          <div class="field">
            <label for="spiders-code" class="label">Spiders?</label>
            <div class="control">
              <select name="spiders-code" id="spiders-code" class="select" required>
                <option :value="0">N</option>
                <option :value="1">Y</option>
              </select>
            </div>
          </div>
        </div>
        <div class="column">
          <div class="field">
            <label for="edema-code" class="label">Edema Type</label>
            <div class="control">
              <select name="edema-code" id="edema-code" class="select" required>
                <option :value="0">N</option>
                <option :value="1">S</option>
                <option :value="2">Y</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="field">
        <label for="billirubin" class="label">Billirubin</label>
        <div class="control">
          <input type="number" step="0.01" name="billirubin" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="cholesterol" class="label">Cholesterol</label>
        <div class="control">
          <input type="number" step="0.01" name="cholesterol" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="albumin" class="label">Albumin</label>
        <div class="control">
          <input type="number" step="0.01" name="albumin" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="copper" class="label">Copper</label>
        <div class="control">
          <input type="number" step="0.01" name="copper" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="alk_phos" class="label">Alkaline Phosphatase</label>
        <div class="control">
          <input type="number" step="0.01" name="alk_phos" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="sgot" class="label">Aspartate Transaminase</label>
        <div class="control">
          <input type="number" step="0.01" name="sgot" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="tryglicerides" class="label">Tryglicerides</label>
        <div class="control">
          <input type="number" step="0.01" name="tryglicerides" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="platelets" class="label">Platelets</label>
        <div class="control">
          <input type="number" step="0.01" name="platelets" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="prothrombin" class="label">Prothrombin</label>
        <div class="control">
          <input type="number" step="0.01" name="prothrombin" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="stage" class="label">Stage</label>
        <div class="control">
          <input type="number" name="stage" class="input" required placeholder="0">
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
