<template>    
    <div class="loginC p-5">        
        <form @submit.prevent="submit" class="p-4">
            <h2 class="p-2 mt-0">Login</h2>
            <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label">Username</label>
                <input type="text" class="form-control" v-model="formData.username" id="exampleInputEmail1"
                    aria-describedby="emailHelp">
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Password</label>
                <input type="password" class="form-control" v-model="formData.password" id="exampleInputPassword1">
            </div>
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="exampleCheck1">
                <label class="form-check-label" for="exampleCheck1">Remember Me</label>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>      
    </div>
</template>

<script>
// import { baseUrl } from '../../config';

import { mapActions } from 'vuex';
const baseUrl = ''

export default {
    name: 'LoginComponent',
    data() {
        return {
            formData: {
                username: null,
                password: null
            }
        }
    },
    components: {
    },
    methods: {
        ...mapActions('auth', ['login']),
        
        async submit() {            
            const url = baseUrl + '/auth/login'
            const init_obj = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.formData)
            }

            try {
                const res = await fetch(url, init_obj)
                if (!res.ok) {
                    this.$store.dispatch('error/showError', {
                    title: 'Login Failed',
                    message: 'Invalid username or password'
                }) 
                return                
                }
                const data = await res.json()
                // Seth the token in local storage
                localStorage.setItem('Authentication-Token', data.token)
                // Set the state of isAuthenticated to true
                this.login()
                // Redirect to the home page
                this.$router.push({ path: '/' })
                // handle success (e.g., show a success message, redirect, etc.)
            } catch (error) {
                this.$store.dispatch('error/showError', {
                    title: 'Something went wrong',
                    message: 'Please try again later.'
                })
            }
        },
    }
}
</script>


<style scoped>
    .loginC {
        height: 100vh;
        width: 40vw;
        margin: 0 auto;
    }

    form {
        width: 100%;
        border-radius: 10px;
        border: 2px solid;
        border-radius: 5px;
    }
    h2 {
        text-align: center;
    }
</style>
