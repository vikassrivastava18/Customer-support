<template>
    <div class="d-flex flex-row flex-wrap mb-3">

        <div class="card-body">
            <h5 v-if="ticket.book" class="card-title"><b>Book</b>: {{ ticket.book }}</h5>
            <p><b>Query</b>: {{ ticket.query }}</p>
            <p :style="{ color: ticket.status_display === 'Resolved' ? 'green' : 'inherit' }">
                <b>Status</b>: {{ ticket.status_display }}
            </p>
            <p>
                <textarea v-model="ticket.response" name="ticketResponse" 
                id="ticketResponse" cols="100" rows="20">
                    {{ ticket.response }}
                </textarea>
            </p>
            <button class="btn btn-primary" @click="sendResponse(ticket)">Reply</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { baseUrl } from '@/config'
import { getCurrentInstance, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

interface Ticket {
    id: number | string
    book: string
    query: string
    status_display: string
    response?: string
}

const route = useRoute()
const instance = getCurrentInstance()
const proxy = instance?.proxy as {
    $axios: {
        get: <T = any>(url: string) => Promise<{ data: T }>
    }
    $store: {
        dispatch: (action: string, payload: any) => void
    }
} | undefined

const ticket = ref<Ticket>({
    id: '',
    book: '',
    query: '',
    status_display: '',
    response: ''
})

onMounted(() => {
    const rawId = route.params.id
    const id = Array.isArray(rawId) ? rawId[0] : rawId

    if (!id) {
        proxy?.$store.dispatch('error/showError', {
            title: 'Invalid ticket',
            message: 'Ticket ID is missing from the route.'
        })
        return
    }

    getTicket(id)
})

async function getTicket(id: string | number): Promise<void> {
    if (!proxy?.$axios) {
        console.error('Axios instance not available')
        return
    }

    const url = `${baseUrl}/staff/tickets/${id}`

    try {
        const res = await proxy.$axios.get<Ticket>(url)
        ticket.value = res.data
    } catch (error: unknown) {
        const message = error instanceof Error ? error.message : 'Unable to load ticket details.'
        console.error('Error:', message)
        proxy?.$store.dispatch('error/showError', {
            title: 'Unable to load ticket',
            message
        })
    }
}

async function sendResponse(ticket: Ticket): Promise<void> {
    if (!ticket.response || !ticket.response.trim()) return

    const url = baseUrl + `/staff/tickets/${ticket.id}`
    try {
        await proxy?.$axios.put(url, {
            id: ticket.id,
            query: ticket.query,
            response: ticket.response.trim(),
            status: 're'
        })
        ticket.response = ''
        proxy?.$store.dispatch('success/showSucsess', {
            title: 'Response saved',
            message: 'Item updated successfully.'
        })
    } catch (error: any) {
        proxy?.$store.dispatch('error/showError', {
            title: 'Unable to send response',
            message: 'Please try again later.'
        })
    }
}

</script>