<template>
  <main class="home">
    <section class="wrap">
      <h1 class="title">Random Interaction</h1>
      <p class="desc">Prosty eksperyment z rozmową, logiką i stanem aplikacji.</p>

      <form class="form" @submit.prevent="onStart">
        <input
          v-model="name"
          type="text"
          class="input"
          placeholder="Wpisz swoje imię…"
          autocomplete="off"
          @input="onInput"
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

function onInput() {
  if (name.value.trim()) {
    error.value = false
  }
}

function onStart() {
  const trimmedName = name.value.trim()

  if (!trimmedName) {
    error.value = true
    return
  }

  error.value = false
  router.push({
    path: '/chat',
    query: { name: trimmedName },
  })
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 2rem 1rem;
  background: #0f0f0f;
  color: #d9d9d9;
}

.wrap {
  width: 100%;
  max-width: 560px;
}

.title {
  margin: 0 0 0.75rem;
  font-size: clamp(2rem, 5vw, 3.25rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
}

.desc {
  margin: 0 0 1.5rem;
  max-width: 46ch;
  color: #aaaaaa;
}

.form {
  display: grid;
  gap: 0.75rem;
}

.input,
.btn {
  height: 44px;
  font-size: 1rem;
}

.input {
  padding: 0 0.85rem;
  border: 1px solid #2a2a2a;
  background: #111111;
  color: #e8e8e8;
  outline: none;
}

.input::placeholder {
  color: #6f6f6f;
}

.input:focus {
  border-color: #3b82f6;
}

.btn {
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
  margin: 0.5rem 0 0;
  color: #ef4444;
  font-size: 0.9rem;
}

.version {
  margin: 1.25rem 0 0;
  color: #7a7a7a;
  font-size: 0.8rem;
}
</style>
