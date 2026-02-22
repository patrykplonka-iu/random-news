<template>
  <main class="chat">
    <section class="wrap">
      <h1 class="title">Chat</h1>
      <p class="desc">Rozmowa dziala przez backend API w Pythonie.</p>

      <div class="box">
        <div class="messages">
          <p v-for="(m, i) in messages" :key="i" class="line">
            <strong>{{ m.from === 'bot' ? 'Bot' : name }}:</strong>&nbsp;
            <span>{{ m.text }}</span>
          </p>
        </div>
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <form class="form" @submit.prevent="sendMessage">
        <input
          v-model="newMessage"
          type="text"
          class="input"
          placeholder="Napisz wiadomosc..."
          autocomplete="off"
          :disabled="loading || done"
        />
        <button type="submit" class="btn" :disabled="loading || done">
          {{ loading ? 'Wysylanie...' : 'Wyslij' }}
        </button>
      </form>

      <br />
      <button class="btn" @click="goHome">Wroc</button>
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

type ChatMsg = {
  from: 'bot' | 'you'
  text: string
}

type ApiPayload = {
  error?: string
  sessionId?: string
  botMessage?: string
  done?: boolean
}

const route = useRoute()
const router = useRouter()

const name = ((route.query.name as string) || 'Ty').trim() || 'Ty'
const newMessage = ref('')
const messages = ref<ChatMsg[]>([])
const sessionId = ref('')
const loading = ref(false)
const done = ref(false)
const error = ref('')

async function readPayload(response: Response): Promise<ApiPayload> {
  const text = await response.text()
  if (!text) return {}

  try {
    return JSON.parse(text) as ApiPayload
  } catch {
    return {}
  }
}

function mapConnectionError(err: unknown): string {
  if (err instanceof Error) {
    return err.message
  }
  return 'Blad polaczenia z backendem.'
}

async function startChat() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/chat/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    })

    const data = await readPayload(response)

    if (!response.ok) {
      throw new Error(data.error || 'Backend niedostepny. Uruchom python backend/main.py')
    }

    if (!data.sessionId || !data.botMessage) {
      throw new Error('Backend zwrocil nieprawidlowe dane startowe.')
    }

    sessionId.value = data.sessionId
    done.value = Boolean(data.done)
    messages.value = [{ from: 'bot', text: data.botMessage }]
  } catch (err) {
    error.value = mapConnectionError(err)
  } finally {
    loading.value = false
  }
}

async function sendMessage() {
  const text = newMessage.value.trim()
  if (!text || loading.value || done.value || !sessionId.value) return

  messages.value.push({ from: 'you', text })
  newMessage.value = ''
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/chat/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sessionId: sessionId.value, message: text }),
    })

    const data = await readPayload(response)

    if (!response.ok) {
      throw new Error(data.error || 'Nie udalo sie wyslac wiadomosci do backendu.')
    }

    if (!data.botMessage) {
      throw new Error('Backend nie zwrocil odpowiedzi bota.')
    }

    messages.value.push({ from: 'bot', text: data.botMessage })
    done.value = Boolean(data.done)
  } catch (err) {
    error.value = mapConnectionError(err)
  } finally {
    loading.value = false
  }
}

function goHome() {
  router.push('/')
}

onMounted(() => {
  void startChat()
})
</script>

<style scoped>
.chat {
  min-height: 100vh;
  background: #0f0f0f;
  color: #d9d9d9;
  display: grid;
  place-items: center;
  padding: 2rem 1rem;
}

.wrap {
  width: 100%;
  max-width: 640px;
}

.title {
  margin: 0 0 0.75rem 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.desc {
  margin: 0 0 1.5rem 0;
  color: #aaaaaa;
}

.box {
  border: 1px solid #2a2a2a;
  background: #111;
  padding: 1rem;
  margin-bottom: 1.5rem;
  min-height: 180px;
}

.btn {
  height: 40px;
  padding: 0 1rem;
  border: 1px solid #3b82f6;
  background: #1f2937;
  color: #e5e7eb;
  cursor: pointer;
}

.btn:hover {
  background: #111827;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.messages {
  display: grid;
  gap: 0.5rem;
  max-height: 260px;
  overflow-y: auto;
}

.form {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  margin-top: 0.75rem;
}

.input {
  flex: 1;
  min-width: 0;
  height: 40px;
  padding: 0 0.75rem;
  border: 1px solid #2a2a2a;
  background: #0f0f0f;
  color: #e5e7eb;
}

.form .btn {
  margin-left: auto;
  flex-shrink: 0;
}

.line {
  margin: 0;
}

.error {
  margin: 0.25rem 0 1rem 0;
  color: #f87171;
}
</style>
