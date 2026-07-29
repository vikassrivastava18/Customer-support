<template>
  <div v-if="isAuthenticated">
    <!-- Chat window -->
    <button class="open-button" @click="openForm()">Chat</button>

    <div class="chat-popup" id="myForm">
      <div class="form-container">
        <i class="fa-solid fa-chalkboard-user"></i>
        <h3>Chat with us
        </h3>
        <button type="button" class="close mb-4" id="closeChatBtn" aria-label="Close" @click="closeForm()">
          <span aria-hidden="true">&times;</span>
        </button>
        <label for="msg" class="p-2">Message</label>
        <textarea placeholder="Type message.." name="msg" v-model="form.query" required></textarea>

        <button type="submit" class="btn" @click="submitForm()" :disabled="disableChatBtn">Send</button>
        <!-- Add loader -->
      
        <div v-if="disableChatBtn" class="text-center">
          <div class="spinner-border" role="status">
            <span class="sr-only"></span>
          </div>
        </div>

        <div class="container queryResults">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, getCurrentInstance, reactive } from 'vue'
import { useStore } from 'vuex'
import { baseUrl } from '../config'

interface ChatForm {
  query: string
}

interface AxiosProxy {
  $axios?: {
    post: (url: string, data: FormData) => Promise<{ status: number; data: unknown }>
  }
}

const store = useStore()
const instance = getCurrentInstance()
const proxy = instance?.proxy as AxiosProxy | undefined
const form = reactive<ChatForm>({
  query: ''
})

const disableChatBtn = ref(false)
const isAuthenticated = computed<boolean>(() => Boolean(store.state.auth?.isAuthenticated))

const openForm = (): void => {
  const chatForm = document.getElementById('myForm')
  if (chatForm) {
    chatForm.style.display = 'block'
  }
}

const closeForm = (): void => {
  const chatForm = document.getElementById('myForm')
  if (chatForm) {
    chatForm.style.display = 'none'
  }
}

const submitForm = async (): Promise<void> => {
  disableChatBtn.value = true
  const url = `${baseUrl}/author-chat`
  const formData = new FormData()
  formData.append('query', form.query)

  try {
    if (!proxy?.$axios) {
      throw new Error('Axios instance not available')
    }
    const response = await proxy.$axios.post(url, formData)

    if (response.status === 200) {
      const resultText = response.data
      const resultsContainer = document.querySelector('.queryResults')
      if (resultsContainer instanceof HTMLElement) {
        resultsContainer.innerHTML = `<p>Answer: ${resultText}</p>` + resultsContainer.innerHTML
      }
    }
  } catch (error) {
    store.dispatch('error/showError', {
      title: 'Sorry, some error occured',
      message: 'Sorry, some error occured'
    })
  } finally {
    disableChatBtn.value = false
    // form.query = ''
  }
}
</script>

<style>
/* Button used to open the chat form - fixed at the bottom of the page */
.open-button {
  padding: 10px 40px;
  background-color: rgb(64, 64, 64);
  color: #fff;
  font-size: 17px;
  max-width: 300px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  position: fixed;
  bottom: 60px;
  right: 28px;
}

/* The popup chat - hidden by default */
.chat-popup {
  display: none;
  position: fixed;
  bottom: 0;
  right: 15px;
  z-index: 9;

}

/* Add styles to the form container */
.form-container {
  max-width: 300px;
  padding: 20px;
  border-radius: 20px;
  background-color: rgb(65, 59, 59);
  color: #ede7e7;
  height: 400px;
  max-height: 400px;
  overflow: auto;
}

/* Full-width textarea */
.form-container textarea {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  border: none;
  border-radius: 20px;
  background: #ddd;
  resize: none;
  min-height: 25px;
  color: #777;
}

/* When the textarea gets focus, do something */
.form-container textarea:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/send button */
.form-container .btn {
  background-color: #42b983;
  color: white;
  font-size: 17px;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  width: 100%;
  margin-bottom: 10px;
}

/* Add a red background color to the cancel button */
.form-container .cancel {
  background-color: #1974D2;
}

/* Add some hover effects to buttons */
.form-container .btn:hover,
.open-button:hover {
  opacity: 0.8;
}

#closeChatBtn {
  float: right;
  position: relative;
  bottom: 40px;
}
</style>