<script setup lang="ts"></script>
<template>
  <div class="z-grid-container">
    <aside class="menu mt-5 mx-5 sidebar">
      <div class="brand mt-2 mb-3 has-text-weight-bold">AI Models</div>
      <p class="menu-label">General</p>
      <ul class="menu-list">
        <li>
          <RouterLink to="/models/car-price">Car Price</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/bike-toll">Bike Toll</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/cirrhosis">Cirrhosis</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/hepatitis">Hepatitis</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/stroke">Stroke</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/face-recognition">Facial Recognition</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/car-price">Car Price</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/aguacate">Aguacate</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/bitcoin">Bitcoin</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/vino">Vino</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/telecomunicaciones">Telecomunicaciones</RouterLink>
        </li>
        <li>
          <RouterLink to="/models/grasa">Grasa</RouterLink>
        </li>
        <li>
          <RouterLink to="/voice">Asistente de voz</RouterLink>
        </li>
      </ul>
    </aside>
    <main class="mt-5 mx-5">
      <router-view />
    </main>
  </div>
</template>
<style scoped>
.z-grid-container {
  width: 100%;
  display: grid;
  grid-template-areas: "sidebar main";
  grid-template-columns: 200px auto;
}

.sidebar {
  background: #fbfdff;
  border-right: 1px solid rgba(10, 10, 10, 0.04);
  padding: 1rem;
}

.brand {
  font-size: 1.05rem;
  color: #3273dc;
}
</style>
