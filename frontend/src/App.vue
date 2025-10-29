<script setup lang="ts"></script>
<template>
  <div class="z-grid-container">
    <aside class="menu mt-5 mx-5">
      <p class="menu-label">General</p>
      <ul class="menu-list">
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
</style>
