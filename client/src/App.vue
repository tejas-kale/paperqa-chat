<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <header class="bg-white shadow-md p-4">
      <h1 class="text-2xl font-bold text-gray-800">PaperQA Chatbot</h1>
    </header>

    <main class="flex-1 overflow-y-auto p-4">
      <div class="space-y-4">
        <!-- Chat messages will go here -->
      </div>
    </main>

    <footer class="bg-white p-4">
      <div class="flex items-center">
        <input
          type="text"
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Ask a question about the papers..."
          class="flex-1 border rounded-full py-2 px-4 mr-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="sendMessage"
          class="bg-blue-500 text-white rounded-full p-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newMessage = ref('');
const messages = ref([]);

const sendMessage = () => {
  if (newMessage.value.trim() === '') return;

  messages.value.push({
    id: Date.now(),
    text: newMessage.value,
    sender: 'user',
  });

  // Placeholder for bot response
  setTimeout(() => {
    messages.value.push({
      id: Date.now() + 1,
      text: 'This is a placeholder response.',
      sender: 'bot',
    });
  }, 1000);

  newMessage.value = '';
};
</script>