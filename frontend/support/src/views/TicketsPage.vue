<template>
    <section class="container">
        <h4>My Tickets
            <router-link to="/create-ticket"
                style="display: inline; background-color: #fff;"
                class="p-2 pb-3 ms-3">        
                    <img src="../assets/create.png" width="35" alt="Create new ticket">                
            </router-link>

        </h4>
        <div class="d-flex flex-row flex-wrap mb-3">
            <div v-for="ticket in tickets" :key="ticket.id" class="card mt-4 mx-4" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title"><b>Book</b>: {{ ticket.book }}</h5>
                    <p><b>Query</b>: {{ ticket.query }}</p>
                    <p :style="{ color: ticket.status_display === 'Resolved' ? 'green' : 'inherit' }">
                        <b>Status</b>: {{ ticket.status_display }}</p>
                    <p v-if="ticket.status_display == 'Resolved'">
                        <b>Response</b>: {{ ticket.response }}</p>                    
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
    import { baseUrl } from '@/config'
    import { onMounted, onUnmounted, getCurrentInstance, ref } from 'vue'

    interface Ticket {
        id: number | string
        book: string
        query: string
        status_display: string
        response?: string
    }

    const instance = getCurrentInstance()
    const proxy = instance?.proxy as {
        $axios: {
            get: <T = any>(url: string) => Promise<{ data: T }>
        }
    } | undefined

    const tickets = ref<Ticket[]>([])
    let ticketInterval: ReturnType<typeof setInterval> | null = null

    onMounted(() => {
        getTickets()
        ticketInterval = setInterval(getTickets, 10000)
    })

    onUnmounted(() => {
        if (ticketInterval !== null) {
            clearInterval(ticketInterval)
            ticketInterval = null
        }
    })

    async function getTickets() {
        const url = `${baseUrl}/tickets`
        try {
            if (!proxy) {
                throw new Error('Axios instance not available')
            }
            const res = await proxy.$axios.get<Ticket[]>(url)
            console.log('Tickets data: ', res)
            tickets.value = res.data
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.error('Error:', error.message)
            } else {
                console.error('Error:', error)
            }
        }
    }
</script>

<style>

</style>