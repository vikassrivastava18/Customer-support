<template>
    <section class="container">
        <h4>All Tickets
            <router-link to="/create-ticket" style="display: inline; background-color: #fff;" class="p-2 pb-3 ms-3">
                <img src="../assets/create.png" width="35" alt="Create new ticket">
            </router-link>
        </h4>
        <div class="d-flex flex-row mb-3">
            <div v-for="ticket in tickets" :key="ticket.id" class="card mt-4 mx-4" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title"><b>Book</b>: {{ ticket.book }}</h5>
                    <p><b>Query</b>: {{ ticket.query }}</p>
                    <p><b>Status</b>: {{ ticket.status_display }}</p>
                    <div class="mt-3">
                        <textarea name="detailed-message" rows="4" cols="50" 
                            placeholder="Type response and press Enter"
                            class="form-control" v-model="ticket.response"
                            @keyup.enter="sendResponse(ticket)"></textarea>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { baseUrl } from '@/config'
import { onMounted, getCurrentInstance, ref } from 'vue'

const instance = getCurrentInstance()
const proxy = instance && instance.proxy
const tickets = ref([])


onMounted(() => {
    getTickets()
})


async function getTickets() {
    const url = baseUrl + '/staff/tickets'
    try {

        const res = await proxy.$axios.get(url)
        console.log("Tickets data: ", res);
        tickets.value = res.data.map(ticket => ({
            ...ticket,
            response: ''
        }))

    } catch (error) {
        console.error('Error:', error.message)
        proxy.$store.dispatch('error/showError', {
            title: 'You do not have access to this page',
            message: 'Please login as staff.'
        })
    }}

    async function sendResponse(ticket) {
        if (!ticket.response || !ticket.response.trim()) {
            return
        }

        const url = baseUrl + '/staff-response'
        try {
            await proxy.$axios.post(url, {
                ticket_id: ticket.id,
                message: ticket.response.trim()
            })
            ticket.response = ''
        } catch (error) {
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