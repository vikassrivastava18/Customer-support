<template>
    <section class="container">
        <h4 style="color: #000;">My Books</h4>
        <div class="d-flex flex-row mb-3">
            <div v-for="book in books" :key="book.id" class="card mt-4 mx-4" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title"><b>Title</b>: {{ book.title }}</h5>
                    <p class="card-text"><b>ISBN</b>: {{ book.isbn }}</p>
                    <p class="card-text"><b>Publication Date</b>: {{ book.pub_date }}</p>
                    <p class="card-text"><b>Genre</b>: {{ book.genre_display }}</p>
                    <p class="card-text"><b>MRP</b>: {{ book.mrp }}</p>
                    <p class="card-text"><b>Publication Date</b>: {{ book.pub_date }}</p>
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
const books = ref([])


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
</script>

<style>

</style>