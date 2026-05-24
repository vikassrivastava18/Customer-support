<template>
    <section class="p-4 mt-4 container">

        <h4>Create Ticket</h4>

        <form class="p-4" @submit.prevent="submitTicket">

            <!-- Book Select -->
            <div class="mb-3">
                <label for="bookSelect" class="form-label">Select Book</label>

                <select class="form-select" id="bookSelect" v-model="form.book_id" required>
                    <option disabled value="">Choose a book...</option>
                    <option value="1">The Great Gatsby</option>
                    <option value="3">To Kill a Mockingbird</option>
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
import { baseUrl } from '@/config'
import { onMounted, getCurrentInstance, ref } from 'vue'
import { reactive } from 'vue'



const instance = getCurrentInstance()
const proxy = instance && instance.proxy

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
        formData.append('book', 1)
        formData.append('query', form.title)
        // formData.append('description', form.description)

        const response = await proxy.$axios.post(
            url,
            formData
        )


        proxy.$store.dispatch('success/showSucsess', {
            title: 'Update Successful',
            message: 'Item updated successfully.'
        })

    } catch (error) {
        console.error('Error creating ticket:', error)
        alert('Failed to submit ticket')
    }
}
</script>