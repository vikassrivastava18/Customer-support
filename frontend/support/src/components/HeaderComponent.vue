<template>
    <div class="d-flex justify-content-between p-2" style="border: 1px solid black;
        background-color: #404040;">
         <router-link to="/" class="nav-link text_white">
            <h3>BookLane</h3>
         </router-link>        

        <div>
            <router-link to="/books" class="nav-link">
               <h4> My Books </h4>
            </router-link>            
        </div>

        <div>
            <router-link to="/tickets" class="nav-link">
               <h4> Tickets </h4>
            </router-link>            
        </div>


        <div class="text-end" v-if="isAuthenticated">
            <button type="button" class="btn btn-danger me-4" 
            @click="logout">Logout</button>
        </div>
        <div class="text-end" v-else>
            <button type="button" class="btn btn-danger me-4" 
            @click="login">Login</button>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'HeaderComponent',
    computed: {
        ...mapState('auth', ['isAuthenticated'])
    },
    methods: {
        logout() {
            this.$store.dispatch('auth/logout')
            this.$router.push('/login')
        },
        login() {
            this.$router.push('/login')
        }
    }
}
</script>

<style scoped>
ul {
    float: right;
}

h3, h4 {
    color: #e76774;
}

.text_black {
    color: black;
}

.text_white {
    color: white;
    font-size: smaller
}

.nav-link {
    padding: 0.3rem 1rem;
    font-size: x-large;
    line-height: 1.2;
}
</style>