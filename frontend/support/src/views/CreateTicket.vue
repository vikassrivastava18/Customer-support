<template>
    <section class="container">

        <h4>Create Ticket</h4>
        <div v-if="isLoading">
            <LoaderComponent />
        </div>
        <form v-else class="p-4 mt-3" @submit.prevent="submitTicket">

            <!-- Book Select -->
            <div class="mb-3">
                <label for="bookSelect" class="form-label">Select Book</label>

                <select class="form-select" id="bookSelect" v-model="form.book_isbn" required>
                    <option disabled value="">Choose a book...</option>
                    <option v-for="book in books" :key="book.isbn" :value="book.isbn">{{ book.title }}</option>
                </select>
            </div>

            <!-- Ticket Title -->
            <div class="mb-3">
                <label for="ticketTitle" class="form-label">Ticket Title</label>

                <input type="text" class="form-control" id="ticketTitle" placeholder="Enter ticket title"
                    v-model="form.query" required />
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

<script setup lang="ts">
import LoaderComponent from '@/components/LoaderComponent.vue'
import { baseUrl } from '@/config'
import { getCurrentInstance, reactive, ref, onMounted } from 'vue'

interface Book {
    isbn: string
    title: string
}

interface TicketForm {
    book_isbn: string
    query: string
    description: string
    attachment: File | null
}

const instance = getCurrentInstance()
const proxy = instance?.proxy as any

const books = ref<Book[]>([])
const isLoading = ref(false)

onMounted(() => {
    getBooks()
})

async function getBooks() {
    const url = `${baseUrl}/books`
    try {
        const res = await proxy.$axios.get<Book[]>(url)
        books.value = res.data

    } catch (error: unknown) {
        console.error('Error:', error instanceof Error ? error.message : String(error))
    }
}

const form = reactive<TicketForm>({
    book_isbn: '',
    query: '',
    description: '',
    attachment: null
})

const handleFileUpload = (event: Event) => {
    const target = event.target as HTMLInputElement
    form.attachment = target.files?.[0] ?? null
}

const submitTicket = async () => {
    try {
        const url = `${baseUrl}/create-ticket`
        const formData = new FormData()
        formData.append('isbn', form.book_isbn)
        formData.append('query', form.query)
        formData.append('description', form.description)

        if (form.attachment) {
            formData.append('attachment', form.attachment)
        }

        isLoading.value = true
        await proxy.$axios.post(url, formData)
        proxy.$router.push('/tickets')
        proxy.$store.dispatch('success/showSucsess', {
            title: 'Ticket Created',
            message: 'Item updated successfully.'
        })

    } catch (error: unknown) {
        console.error('Error creating ticket:', error instanceof Error ? error.message : String(error))
    } finally {
        isLoading.value = false
    }
}
</script>

<style>
form {
        border: 1px solid;
    }
</style>