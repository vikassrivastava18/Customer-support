<template>
    <section class="container">
        <h4>All Tickets
            
        </h4>
        <div class="d-flex flex-row flex-wrap mb-3">
            <div v-for="ticket in tickets" :key="ticket.id" class="card mt-4 mx-4" style="width: 20rem;">
                <div class="card-body">
                    <div class="mt-3">
                        <div class="card-body">
                            <h5 v-if="ticket.book" class="card-title"><b>Book</b>: {{ ticket.book }}</h5>
                            <p><b>Query</b>: {{ ticket.query }}</p>
                            <p :style="{ color: ticket.status_display === 'Resolved' ? 'green' : 'inherit' }">
                                <b>Status</b>: {{ ticket.status_display }}
                            </p>
                            <p v-if="ticket.status_display == 'Resolved'">
                                <b>Response</b>: {{ ticket.response }}
                            </p>
                        </div>
                        <button class="btn btn-primary" @click="reply(ticket)">Reply</button>
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

async function reply(ticket: Ticket): Promise<void> {
    if (!ticket || !ticket.id) return

    proxy.$router.push(`/admin/reply/${ticket.id}`).catch((error: any) => {
        console.error('Navigation error:', error)
    })
}
</script>

<style scoped>
.container {
    border: 1px solid #fff;
}
</style>