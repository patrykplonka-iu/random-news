<template>
  <main class="chat-placeholder">
    <section>
      <h2>/chat – placeholder</h2>
      <p v-if="name" class="greeting">Cześć, {{ name }} 👋</p>
      <p v-else class="greeting">Brak imienia w URL query.</p>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const name = computed(() => {
  const candidate = route.query.name
  return typeof candidate === 'string' ? candidate : ''
})
</script>

<style scoped>
.chat-placeholder {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: #0f0f0f;
  color: #d9d9d9;
}

.greeting {
  margin-top: 0.75rem;
  color: #aaaaaa;
}
</style>
