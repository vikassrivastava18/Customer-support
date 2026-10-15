<template>
    <section class="tickets-page">
        <div class="tickets-panel">
            <header class="tickets-header">
                <div class="header-copy">
                    <span class="eyebrow">Support Center</span>
                    <h1>My Tickets</h1>
                    <p>Track your support requests and review responses from our team.</p>
                </div>
                <div class="header-actions">
                    <div class="ticket-count" aria-live="polite">
                        <strong>{{ tickets.length }}</strong>
                        <span>{{ tickets.length === 1 ? 'ticket' : 'tickets' }}</span>
                    </div>
                    <router-link to="/create-ticket" class="create-ticket-btn">
                        <span class="plus-icon" aria-hidden="true">+</span>
                        Create ticket
                    </router-link>
                </div>
            </header>

            <div v-if="tickets.length" class="tickets-grid">
                <article v-for="ticket in tickets" :key="ticket.id" class="ticket-card">
                    <div class="ticket-card-header">
                        <div>
                            <span class="ticket-label">Support request</span>
                            <h2 v-if="ticket.book">{{ ticket.book }}</h2>
                            <h2 v-else>Ticket #{{ ticket.id }}</h2>
                        </div>
                        <span
                            class="status-badge"
                            :class="{ resolved: ticket.status_display === 'Resolved' }"
                        >
                            <span class="status-dot" aria-hidden="true"></span>
                            {{ ticket.status_display }}
                        </span>
                    </div>

                    <div class="ticket-content">
                        <span class="field-label">Your query</span>
                        <p>{{ ticket.query }}</p>
                    </div>

                    <div v-if="ticket.status_display === 'Resolved'" class="response-panel">
                        <span class="field-label">Team response</span>
                        <p>{{ ticket.response || 'Your request has been resolved.' }}</p>
                    </div>
                </article>
            </div>

            <div v-else class="empty-state">
                <span class="empty-icon" aria-hidden="true">?</span>
                <h2>No tickets yet</h2>
                <p>When you need help, create a support ticket and it will show up here.</p>
                <router-link to="/create-ticket" class="create-ticket-btn">
                    <span class="plus-icon" aria-hidden="true">+</span>
                    Create your first ticket
                </router-link>
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

<style scoped>
.tickets-page {
    min-height: calc(100vh - 80px);
    padding: 2.5rem 1.25rem 4rem;
    background:
        radial-gradient(circle at top left, rgba(232, 179, 168, 0.18), transparent 28%),
        linear-gradient(180deg, #fffaf9 0%, #fff 100%);
}

.tickets-panel {
    max-width: 1180px;
    margin: 0 auto;
    padding: 2.2rem;
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(173, 120, 112, 0.12);
    border-radius: 28px;
    box-shadow: 0 18px 45px rgba(109, 84, 86, 0.08);
}

.tickets-header {
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
    max-width: 650px;
    color: #6d5a5d;
    font-size: 1.05rem;
    line-height: 1.7;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.ticket-count {
    display: flex;
    min-width: 76px;
    min-height: 76px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(217, 127, 107, 0.15);
    border-radius: 20px;
    background: linear-gradient(160deg, #fff5f2 0%, #fdf0ef 100%);
    color: #6d5a5d;
}

.ticket-count strong {
    color: #a75d4a;
    font-size: 1.5rem;
    line-height: 1;
}

.ticket-count span {
    margin-top: 0.35rem;
    font-size: 0.78rem;
}

.create-ticket-btn {
    display: inline-flex;
    min-height: 48px;
    align-items: center;
    justify-content: center;
    gap: 0.55rem;
    padding: 0.75rem 1.15rem;
    border: 0;
    border-radius: 999px;
    background: linear-gradient(135deg, #d97f6b 0%, #c26452 100%);
    box-shadow: 0 10px 20px rgba(201, 105, 86, 0.2);
    color: #fff;
    font-weight: 700;
    text-decoration: none;
    white-space: nowrap;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.create-ticket-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 13px 24px rgba(201, 105, 86, 0.27);
    color: #fff;
}

.plus-icon {
    font-size: 1.35rem;
    font-weight: 400;
    line-height: 1;
}

.tickets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
    gap: 1.25rem;
}

.ticket-card {
    min-width: 0;
    padding: 1.4rem;
    border: 1px solid rgba(120, 82, 82, 0.09);
    border-radius: 22px;
    background: #fff;
    box-shadow: 0 14px 28px rgba(44, 31, 34, 0.045);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ticket-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 32px rgba(44, 31, 34, 0.08);
}

.ticket-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: 1.15rem;
    border-bottom: 1px solid rgba(120, 82, 82, 0.09);
}

.ticket-label,
.field-label {
    display: block;
    margin-bottom: 0.45rem;
    color: #8b7477;
    font-size: 0.73rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.ticket-card h2 {
    color: #302123;
    font-size: 1.1rem;
    line-height: 1.4;
    overflow-wrap: anywhere;
}

.status-badge {
    display: inline-flex;
    flex: 0 0 auto;
    align-items: center;
    gap: 0.45rem;
    padding: 0.45rem 0.7rem;
    border: 1px solid rgba(217, 127, 107, 0.14);
    border-radius: 999px;
    background: #fff5f2;
    color: #a75d4a;
    font-size: 0.78rem;
    font-weight: 700;
}

.status-badge.resolved {
    border-color: rgba(87, 183, 123, 0.18);
    background: #eff9f2;
    color: #347c50;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: currentColor;
}

.ticket-content {
    padding-top: 1.15rem;
}

.ticket-content p,
.response-panel p {
    color: #5b4a4d;
    font-size: 0.96rem;
    line-height: 1.7;
    overflow-wrap: anywhere;
    white-space: pre-wrap;
}

.response-panel {
    margin-top: 1.2rem;
    padding: 1rem;
    border: 1px solid rgba(87, 183, 123, 0.14);
    border-radius: 15px;
    background: linear-gradient(160deg, #f3faf5 0%, #f8fcf9 100%);
}

.response-panel .field-label {
    color: #347c50;
}

.empty-state {
    display: flex;
    min-height: 300px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    border: 1px dashed rgba(173, 120, 112, 0.28);
    border-radius: 22px;
    background: linear-gradient(160deg, rgba(255, 245, 242, 0.65), rgba(255, 255, 255, 0.7));
    text-align: center;
}

.empty-icon {
    display: grid;
    width: 56px;
    height: 56px;
    place-items: center;
    margin-bottom: 1rem;
    border-radius: 17px;
    background: linear-gradient(135deg, #f9ebe7 0%, #f5d9d5 100%);
    color: #a75d4a;
    font-size: 1.5rem;
    font-weight: 700;
}

.empty-state h2 {
    margin-bottom: 0.5rem;
    color: #302123;
    font-size: 1.25rem;
}

.empty-state p {
    max-width: 420px;
    margin-bottom: 1.2rem;
    color: #6d5a5d;
    line-height: 1.7;
}

@media (max-width: 760px) {
    .tickets-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .header-actions {
        width: 100%;
        justify-content: space-between;
    }
}

@media (max-width: 640px) {
    .tickets-page {
        padding: 1.5rem 0.9rem 3rem;
    }

    .tickets-panel {
        padding: 1.3rem;
        border-radius: 22px;
    }

    .ticket-count {
        min-width: 68px;
        min-height: 68px;
        border-radius: 18px;
    }

    .create-ticket-btn {
        padding: 0.7rem 0.95rem;
    }

    .ticket-card {
        padding: 1.2rem;
    }
}
</style>