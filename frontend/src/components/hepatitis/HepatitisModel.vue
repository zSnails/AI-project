<script setup lang="ts">
import { ref } from 'vue';
const prediction = ref("");
async function submit(form: any) {
  const formData = new FormData(form.target as unknown as HTMLFormElement);
  const params = new URLSearchParams(formData as unknown as any);
  const response = await fetch(`http://localhost:8080/api/models/hepatitis?${params.toString()}`, { method: "GET" });
  const result = await response.json();
  prediction.value = result.prediction;
}
</script>
<template>
  <div>
    <h1 class="title">Predicted Result</h1>
    <h2 class="subtitle">{{prediction}}</h2>
    <form @submit.prevent="submit">
      <div class="field">
        <label for="age" class="label">Age</label>
        <div class="control">
          <input type="number" name="age" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="sex-code" class="label">Sex</label>
        <div class="control">
          <select name="sex-code" id="sex-code" class="select" required>
            <option :value="0">F</option>
            <option :value="1">M</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="alb" class="label">ALB</label>
        <div class="control">
          <input type="number" name="alb" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="alp" class="label">ALP</label>
        <div class="control">
          <input type="number" name="alp" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="alt" class="label">ALT</label>
        <div class="control">
          <input type="number" name="alt" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="ast" class="label">AST</label>
        <div class="control">
          <input type="number" name="ast" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="bil" class="label">BIL</label>
        <div class="control">
          <input type="number" name="bil" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="che" class="label">CHE</label>
        <div class="control">
          <input type="number" name="che" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="chol" class="label">CHOL</label>
        <div class="control">
          <input type="number" name="chol" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="crea" class="label">CREA</label>
        <div class="control">
          <input type="number" name="crea" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="ggt" class="label">GGT</label>
        <div class="control">
          <input type="number" name="ggt" class="input" required placeholder="0">
        </div>
      </div>
      <div class="field">
        <label for="prot" class="label">PROT</label>
        <div class="control">
          <input type="number" name="prot" class="input" required placeholder="0">
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
