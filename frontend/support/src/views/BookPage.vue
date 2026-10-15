<template>
    <section class="books-page">
        <div class="books-panel">
            <header class="books-header">
                <div class="header-copy">
                    <span class="eyebrow">Your library</span>
                    <h1>My Books</h1>
                    <p>Browse the books in your publishing catalog and their details.</p>
                </div>
                <div class="book-count" aria-live="polite">
                    <strong>{{ books.length }}</strong>
                    <span>{{ books.length === 1 ? 'book' : 'books' }}</span>
                </div>
            </header>

            <div v-if="books.length" class="books-grid">
                <article v-for="book in books" :key="book.id" class="book-card">
                    <div class="book-card-heading">
                        <span class="book-mark" aria-hidden="true">B</span>
                        <span class="genre-tag">{{ book.genre_display || 'Book' }}</span>
                    </div>

                    <h2>{{ book.title || 'Untitled book' }}</h2>

                    <dl class="book-details">
                        <div class="detail-row">
                            <dt>ISBN</dt>
                            <dd>{{ book.isbn || '—' }}</dd>
                        </div>
                        <div class="detail-row">
                            <dt>Published</dt>
                            <dd>{{ book.pub_date || '—' }}</dd>
                        </div>
                        <div class="detail-row">
                            <dt>MRP</dt>
                            <dd>{{ book.mrp ?? '—' }}</dd>
                        </div>
                    </dl>
                </article>
            </div>

            <div v-else class="empty-state">
                <span class="empty-mark" aria-hidden="true">B</span>
                <h2>Your library is waiting</h2>
                <p>Books in your catalog will appear here once they’re available.</p>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { baseUrl } from '@/config'
import { onMounted, getCurrentInstance, ref } from 'vue'

interface Book {
    id: number | string
    title?: string
    isbn?: string
    pub_date?: string
    genre_display?: string
    mrp?: number | string
    [key: string]: any
}

const instance = getCurrentInstance()
// proxy may be undefined in some contexts; type as any to access $axios
const proxy: any = instance && (instance.proxy as any)
const books = ref<Book[]>([])

onMounted(() => {
    getBooks()
})

async function getBooks(): Promise<void> {
    const url = baseUrl + '/books'
    try {
        const res = await proxy.$axios.get(url)
        books.value = res.data as Book[]
    } catch (error: unknown) {
        console.error('Error:', (error as Error).message)
    }
}
</script>

<style scoped>
.books-page {
    min-height: calc(100vh - 80px);
    padding: 2.5rem 1.25rem 4rem;
    background:
        radial-gradient(circle at top left, rgba(232, 179, 168, 0.18), transparent 28%),
        linear-gradient(180deg, #fffaf9 0%, #fff 100%);
}

.books-panel {
    max-width: 1180px;
    margin: 0 auto;
    padding: 2.2rem;
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(173, 120, 112, 0.12);
    border-radius: 28px;
    box-shadow: 0 18px 45px rgba(109, 84, 86, 0.08);
}

.books-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.header-copy {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
}

.eyebrow {
    display: inline-flex;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    background: rgba(217, 127, 107, 0.12);
    color: #a75d4a;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 700;
}

h1,
h2,
p {
    margin: 0;
}

h1 {
    color: #2e1f22;
    font-size: clamp(2rem, 3vw, 3.1rem);
    line-height: 1.1;
}

.header-copy p {
    max-width: 680px;
    color: #6d5a5d;
    font-size: 1.05rem;
    line-height: 1.7;
}

.book-count {
    display: flex;
    min-width: 82px;
    min-height: 82px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(217, 127, 107, 0.15);
    border-radius: 22px;
    background: linear-gradient(160deg, #fff5f2 0%, #fdf0ef 100%);
    color: #6d5a5d;
}

.book-count strong {
    color: #a75d4a;
    font-size: 1.6rem;
    line-height: 1;
}

.book-count span {
    margin-top: 0.35rem;
    font-size: 0.8rem;
}

.books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: 1.25rem;
}

.book-card {
    min-width: 0;
    padding: 1.4rem;
    border: 1px solid rgba(120, 82, 82, 0.09);
    border-radius: 22px;
    background: #fff;
    box-shadow: 0 14px 28px rgba(44, 31, 34, 0.045);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.book-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 32px rgba(44, 31, 34, 0.08);
}

.book-card-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 1.2rem;
}

.book-mark,
.empty-mark {
    display: grid;
    place-items: center;
    width: 46px;
    height: 46px;
    flex: 0 0 auto;
    border-radius: 14px;
    background: linear-gradient(135deg, #f9ebe7 0%, #f5d9d5 100%);
    color: #a75d4a;
    font-size: 1.25rem;
    font-weight: 700;
}

.genre-tag {
    max-width: 70%;
    overflow: hidden;
    padding: 0.4rem 0.7rem;
    border-radius: 999px;
    background: #fff5f2;
    color: #a75d4a;
    font-size: 0.78rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.book-card h2 {
    min-height: 3.2rem;
    color: #302123;
    font-size: 1.2rem;
    line-height: 1.35;
    overflow-wrap: anywhere;
}

.book-details {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin: 1.15rem 0 0;
    border-top: 1px solid rgba(120, 82, 82, 0.09);
}

.detail-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(120, 82, 82, 0.07);
    font-size: 0.9rem;
}

.detail-row:last-child {
    border-bottom: 0;
}

.detail-row dt {
    color: #6f5b5e;
}

.detail-row dd {
    margin: 0;
    color: #302123;
    font-weight: 600;
    text-align: right;
    overflow-wrap: anywhere;
}

.empty-state {
    display: flex;
    min-height: 260px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    border: 1px dashed rgba(173, 120, 112, 0.28);
    border-radius: 22px;
    background: linear-gradient(160deg, rgba(255, 245, 242, 0.65), rgba(255, 255, 255, 0.7));
    text-align: center;
}

.empty-mark {
    width: 56px;
    height: 56px;
    margin-bottom: 1rem;
    font-size: 1.5rem;
}

.empty-state h2 {
    margin-bottom: 0.5rem;
    color: #302123;
    font-size: 1.25rem;
}

.empty-state p {
    max-width: 400px;
    color: #6d5a5d;
    line-height: 1.7;
}

@media (max-width: 640px) {
    .books-page {
        padding: 1.5rem 0.9rem 3rem;
    }

    .books-panel {
        padding: 1.3rem;
        border-radius: 22px;
    }

    .books-header {
        align-items: flex-start;
    }

    .book-count {
        min-width: 68px;
        min-height: 68px;
        border-radius: 18px;
    }

    .book-card {
        padding: 1.2rem;
    }
}
</style>
