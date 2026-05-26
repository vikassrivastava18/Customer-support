<template>
    <section class="container">

        <h4>Create Ticket</h4>
        <div v-if="isLoading">
            <LoaderComponent />
        </div>
        <form v-else class="p-4" @submit.prevent="submitTicket">

            <!-- Book Select -->
            <div class="mb-3">
                <label for="bookSelect" class="form-label">Select Book</label>

                <select class="form-select" id="bookSelect" v-model="form.book_id" required>
                    <option disabled value="">Choose a book...</option>
                    <option v-for="book in books" :key="book.id" :value="book.id">{{ book.title }}</option>
                </select>
            </div>

            <!-- Ticket Title -->
            <div class="mb-3">
                <label for="ticketTitle" class="form-label">Ticket Title</label>

                <input type="text" class="form-control" id="ticketTitle" placeholder="Enter ticket title"
                    v-model="form.title" required />
            </div>

            <!-- Description -->
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>

                <textarea class="form-control" id="description" rows="5" placeholder="Describe your issue..."
                    v-model="form.description" required></textarea>
            </div>

            <!-- File Attachment -->
            <div class="mb-4">
                <label for="attachment" class="form-label">Attachment</label>

                <input class="form-control" type="file" id="attachment" @change="handleFileUpload" />
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn btn-primary">
                Submit Ticket
            </button>

        </form>
            
    </section>
</template>

<script setup>
import LoaderComponent from '@/components/LoaderComponent.vue'
import { baseUrl } from '@/config'
import { getCurrentInstance } from 'vue'
import { reactive, ref, onMounted } from 'vue'

const instance = getCurrentInstance()
const proxy = instance && instance.proxy

const books = ref([])
const isLoading = ref(false)

onMounted(() => {
    getBooks()
})

async function getBooks() {
    const url = baseUrl + '/books'
    try {

        const res = await proxy.$axios.get(url)
        console.log("Books data: ", res);
        books.value = res.data

    } catch (error) {
        console.error('Error:', error.message)
    }
}

const form = reactive({
    book_id: '',
    title: '',
    description: '',
    attachment: null
})

const handleFileUpload = (event) => {
    form.attachment = event.target.files[0]
}

const submitTicket = async () => {
    try {
        const url = baseUrl + "/create-ticket"
        const formData = new FormData()
        formData.append('book', form.book_id)
        formData.append('query', form.title)
        // formData.append('description', form.description)
        isLoading.value = true
        const response = await proxy.$axios.post(
            url,
            formData
        )
        proxy.$router.push('/tickets')
        proxy.$store.dispatch('success/showSucsess', {
            title: 'Ticket Created',
            message: 'Item updated successfully.'
        })
        
    } catch (error) {
        console.error('Error creating ticket:', error)
    } finally {
        isLoading.value = false;
    }
}
</script>