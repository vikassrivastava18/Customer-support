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
            <div v-for="ticket in tickets" class="card mt-4 mx-4"
            :key="ticket.id" 
            style="max-height: 400px; overflow: auto; width: 18rem;">
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
import { onMounted, onUnmounted, getCurrentInstance, ref, ComponentInternalInstance } from 'vue'

const instance: ComponentInternalInstance | null = getCurrentInstance()
const proxy = instance && instance.proxy
const tickets = ref<any[]>([])
let ticketInterval: NodeJS.Timeout | null = null

onMounted(() => {
    getTickets()
    ticketInterval = setInterval(getTickets, 10000)
})

onUnmounted(() => {
    if (ticketInterval) {
        clearInterval(ticketInterval)
    }
})

async function getTickets(): Promise<void> {
    const url: string = baseUrl + '/tickets'
    try {
        const res = await proxy.$axios.get(url)
        tickets.value = res.data

    } catch (error: any) {
        console.error('Error:', error.message)
    }
}
</script>

<style>

</style>