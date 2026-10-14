<template>
  <section class="homepage-shell">
    <div class="hero-card">
      <div class="welcome-copy">
        <span class="eyebrow">Support Center</span>
        <h1>Welcome, {{ username || 'Author' }}</h1>

        <p class="lead">
          Get quick support for your published books by submitting a support ticket or
          browsing our frequently asked questions on publishing, royalties, and more.
        </p>

        <p class="subtext">
          If you need additional assistance, raise a ticket and our support team will
          work to resolve your issue as quickly as possible.
        </p>

        <div class="actions">
          <router-link to="/tickets" class="action-btn primary">
            View tickets
          </router-link>
          <router-link to="/books" class="action-btn secondary">
            My books
          </router-link>
        </div>
      </div>

      <div class="support-panel">
        <div class="panel-header">
          <span class="status-dot"></span>
          <span>Fast help</span>
        </div>

        <ul class="support-list">
          <li>
            <strong>Publishing</strong>
            <span>Guidance & setup</span>
          </li>
          <li>
            <strong>Royalties</strong>
            <span>Payments & reports</span>
          </li>
          <li>
            <strong>Account</strong>
            <span>Profile & access</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- <div class="info-grid">
      <article class="info-card">
        <div class="card-icon">📚</div>
        <h3>Book support</h3>
        <p>Resolve publishing, formatting, and distribution issues quickly.</p>
      </article>

      <article class="info-card">
        <div class="card-icon">💸</div>
        <h3>Royalties</h3>
        <p>Track earnings, payment questions, and sales-related inquiries.</p>
      </article>

      <article class="info-card">
        <div class="card-icon">⚡</div>
        <h3>Fast response</h3>
        <p>Open a ticket and get help from our support team without delays.</p>
      </article>
    </div> -->
  </section>
</template>

<script setup>
const username = localStorage.getItem('Username')
</script>

<style scoped>
.homepage-shell {
  min-height: calc(100vh - 80px);
  padding: 2.5rem 1.25rem 4rem;
  background:
    radial-gradient(circle at top left, rgba(232, 179, 168, 0.18), transparent 28%),
    linear-gradient(180deg, #fffaf9 0%, #fff 100%);
}

.hero-card {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.5fr 0.85fr;
  align-items: center;
  gap: 2rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(173, 120, 112, 0.12);
  border-radius: 28px;
  box-shadow: 0 18px 45px rgba(109, 84, 86, 0.08);
  padding: 2.2rem 2.2rem;
}

.welcome-copy {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.eyebrow {
  display: inline-flex;
  align-self: flex-start;
  padding: 0.45rem 0.8rem;
  border-radius: 999px;
  background: rgba(217, 127, 107, 0.12);
  color: #a75d4a;
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-weight: 700;
}

h1 {
  margin: 0;
  font-size: clamp(2rem, 3vw, 3.1rem);
  line-height: 1.1;
  color: #2e1f22;
}

.lead,
.subtext {
  margin: 0;
  color: #5b4a4d;
  font-size: 1.08rem;
  line-height: 1.8;
  max-width: 680px;
}

.subtext {
  color: #6d5a5d;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.9rem 1.4rem;
  border-radius: 999px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #d97f6b 0%, #c26452 100%);
  color: white;
  box-shadow: 0 10px 20px rgba(201, 105, 86, 0.25);
}

.action-btn.secondary {
  background: #fff;
  color: #5c3d3a;
  border: 1px solid rgba(122, 82, 74, 0.12);
}

.action-btn:hover {
  transform: translateY(-2px);
}

.support-panel {
  background: linear-gradient(160deg, #fff5f2 0%, #fdf0ef 100%);
  border: 1px solid rgba(217, 127, 107, 0.15);
  border-radius: 24px;
  padding: 1.25rem;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-weight: 700;
  color: #4d3637;
  margin-bottom: 1rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #57b77b;
  box-shadow: 0 0 0 6px rgba(87, 183, 123, 0.12);
}

.support-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.support-list li {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  background: rgba(255, 255, 255, 0.65);
  border: 1px solid rgba(157, 115, 110, 0.08);
  padding: 0.9rem 0.95rem;
  border-radius: 14px;
}

.support-list strong {
  color: #2f2124;
  font-size: 0.98rem;
}

.support-list span {
  color: #6f5b5e;
  font-size: 0.9rem;
}

.info-grid {
  max-width: 1180px;
  margin: 2rem auto 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
}

.info-card {
  background: #ffffff;
  border: 1px solid rgba(120, 82, 82, 0.08);
  border-radius: 22px;
  padding: 1.5rem;
  box-shadow: 0 14px 28px rgba(44, 31, 34, 0.04);
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #f9ebe7 0%, #f5d9d5 100%);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.info-card h3 {
  margin: 0 0 0.5rem;
  color: #302123;
}

.info-card p {
  margin: 0;
  color: #62575a;
  line-height: 1.7;
}

@media (max-width: 900px) {
  .hero-card {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .homepage-shell {
    padding: 1.5rem 0.9rem 3rem;
  }

  .hero-card {
    padding: 1.3rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .actions {
    flex-direction: column;
    align-items: stretch;
  }

  .action-btn {
    width: 100%;
  }
}
</style>