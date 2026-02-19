<template>
  <main class="home">
    <section class="wrap">
      <h1 class="title">Random Interaction</h1>
      <p class="desc">
        Prosty eksperyment z rozmową, logiką i stanem aplikacji.
      </p>

      <form class="form" @submit.prevent="onStart">
        <input
          v-model="name"
          type="text"
          class="input"
          placeholder="Wpisz swoje imię…"
          autocomplete="off"
        />
        <button type="submit" class="btn">Start</button>
      </form>

      <p v-if="error" class="error">Podaj imię.</p>

      <p class="version">v0.1 – dev mode</p>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const name = ref('')
const error = ref(false)
const router = useRouter()

function onStart() {
  if (!name.value.trim()) {
    error.value = true
    return
  }

  error.value = false

  // opcja A: od razu przekierowanie
  router.push('/chat')

  // opcja B: na teraz tylko log
  // console.log('Start for:', name.value)
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: #0f0f0f;
  color: #d9d9d9;
  display: grid;
  place-items: center;
  padding: 2rem 1rem;
}

.wrap {
  width: 100%;
  max-width: 560px;
}

.title {
  margin: 0 0 0.75rem 0;
  font-size: clamp(2rem, 5vw, 3.25rem);
  line-height: 1.05;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.desc {
  margin: 0 0 1.5rem 0;
  color: #aaaaaa;
  max-width: 46ch;
}

.form {
  display: grid;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.input {
  height: 44px;
  padding: 0 0.85rem;
  border: 1px solid #2a2a2a;
  background: #111;
  color: #e8e8e8;
  outline: none;
  font-size: 1rem;
}

.input::placeholder {
  color: #6f6f6f;
}

.input:focus {
  border-color: #3b82f6;
}

.btn {
  height: 44px;
  border: 1px solid #3b82f6;
  background: #1f2937;
  color: #e5e7eb;
  font-weight: 600;
  cursor: pointer;
}

.btn:hover {
  background: #111827;
}

.error {
  margin: 0.25rem 0 1rem 0;
  color: #ef4444;
  font-size: 0.9rem;
}

.version {
  margin-top: 1.25rem;
  color: #7a7a7a;
  font-size: 0.8rem;
}
</style>
