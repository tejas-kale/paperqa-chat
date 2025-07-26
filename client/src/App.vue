<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <header class="bg-white shadow-md p-4 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">PaperQA Chatbot</h1>
      <div>
        <input type="file" @change="handleFileUpload" class="hidden" ref="fileInput" />
        <button @click="triggerFileInput" class="bg-green-500 text-white rounded-full p-2 hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500">
          Upload Paper
        </button>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto p-4">
      <div class="space-y-4">
        <div v-for="message in messages" :key="message.id" class="flex" :class="{'justify-end': message.sender === 'user'}">
          <div class="p-3 rounded-lg max-w-lg" :class="{'bg-blue-500 text-white': message.sender === 'user', 'bg-gray-300 text-gray-800': message.sender === 'bot'}">
            {{ message.text }}
          </div>
        </div>
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
const fileInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://localhost:5000/api/v1/upload', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      messages.value.push({
        id: Date.now(),
        text: `Successfully uploaded ${file.name}`,
        sender: 'bot',
      });
    } else {
      const errorData = await response.json();
      messages.value.push({
        id: Date.now(),
        text: `Error uploading file: ${errorData.error}`,
        sender: 'bot',
      });
    }
  } catch (error) {
    messages.value.push({
      id: Date.now(),
      text: 'An error occurred during the upload.',
      sender: 'bot',
    });
  }
};

const sendMessage = async () => {
  if (newMessage.value.trim() === '') return;

  const userMessage = newMessage.value;
  messages.value.push({
    id: Date.now(),
    text: userMessage,
    sender: 'user',
  });
  newMessage.value = '';

  try {
    const response = await fetch('http://localhost:5000/api/v1/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: userMessage }),
    });

    const data = await response.json();
    messages.value.push({
      id: Date.now() + 1,
      text: data.answer || data.error,
      sender: 'bot',
    });
  } catch (error) {
    messages.value.push({
      id: Date.now() + 1,
      text: 'Failed to get a response from the server.',
      sender: 'bot',
    });
  }
};
</script>