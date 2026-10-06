<template>
    <section class="container p-4">
        <!-- Content Column -->
        <div>
            <h4 class="mt-5">Welcome, {{ username ? username : Author }}</h4>
            <!-- Paragraph -->
            <p class="text-secondary lh-lg mt-4">
                Get quick support for your published books by submitting a support ticket or browsing our Frequently
                Asked Questions (FAQs) on topics such as publishing, royalties, and more.
            </p>
            <p class="text-secondary lh-lg mb-5">If you need additional assistance, raise a ticket and our
                support team will work to resolve your issue as quickly as possible.
            </p>
        </div>
    </section>
</template>

<script setup>
const username = localStorage.getItem('Username')
</script>

<style scoped>
h4 {
    color: rgb(217 127 107);
}

.text-secondary {
    font-size: larger;
}
</style>