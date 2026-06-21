<template>
    <section class="container">
        <h4>All Tickets
            <router-link to="/create-ticket" style="display: inline; background-color: #fff;" class="p-2 pb-3 ms-3">
                <img src="../assets/create.png" width="35" alt="Create new ticket">
            </router-link>
        </h4>
        <div class="d-flex flex-row flex-wrap mb-3">
            <div v-for="ticket in tickets" :key="ticket.id" class="card mt-4 mx-4" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title"><b>Book</b>: {{ ticket.book }}</h5>
                    <p><b>Query</b>: {{ ticket.query }}</p>
                    <p><b>Status</b>: {{ ticket.status_display }}</p>
                    <div class="mt-3">
                        <textarea name="detailed-message" rows="10" cols="50" placeholder="Type response and press Enter"
                            class="form-control" v-model="ticket.response"></textarea>
                        <button class="btn btn-primary" @click="sendResponse(ticket)">Submit</button>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { baseUrl } from '@/config'
import { onMounted, onUnmounted, getCurrentInstance, ref } from 'vue'

interface Ticket {
    id: number
    book: string
    query: string
    status_display?: string
    response?: string
}

const instance = getCurrentInstance()
const proxy = (instance && instance.proxy) as any
const tickets = ref<Ticket[]>([])
let ticketInterval: number | null = null

onMounted(() => {
    getTickets()
    ticketInterval = window.setInterval(getTickets, 10000)
})

onUnmounted(() => {
    if (ticketInterval !== null) {
        clearInterval(ticketInterval)
    }
})

async function getTickets(): Promise<void> {
    const url = baseUrl + '/staff/tickets'
    try {
        const res = await proxy.$axios.get(url)
        tickets.value = res.data.map((ticket: any) => ({ ...ticket }))
    } catch (error: any) {
        console.error('Error:', error.message)
        proxy.$store.dispatch('error/showError', {
            title: 'Please login as staff.',
            message: 'You do not have access to this page'
        })
    }
}

async function sendResponse(ticket: Ticket): Promise<void> {
    if (!ticket.response || !ticket.response.trim()) return

    const url = baseUrl + `/staff/tickets/${ticket.id}`
    try {
        await proxy.$axios.put(url, {
            id: ticket.id,
            query: ticket.query,
            response: ticket.response.trim(),
            status: 're'
        })
        ticket.response = ''
    } catch (error: any) {
        console.error('Error sending response:', error.message)
        proxy.$store.dispatch('error/showError', {
            title: 'Unable to send response',
            message: 'Please try again later.'
        })
    }
}
</script>

<style>
.container {
    border: 1px solid #fff;
    min-height: 75vh;
}
</style>