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
                    <p><b>Status</b>: {{ ticket.status_display }}</p>                    
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
    const url = baseUrl + '/tickets'
    try {

        const res = await proxy.$axios.get(url)
        console.log("Tickets data: ", res);
        tickets.value = res.data

    } catch (error) {
        console.error('Error:', error.message)
    }
}
</script>

<style>

</style>