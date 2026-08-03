<template>    
    <div class="card mt-2">        
        <form @submit.prevent="submit" class="p-4 mt-2">
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

<script setup lang="ts">
import { baseUrl } from '@/config';
import { ref } from 'vue'
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';

interface LoginForm {
    username: string;
    password: string;
}

interface TokenData {
    username: string
    token: string,
    staff: Boolean
}

const store = useStore();
const router = useRouter();

const formData = ref<LoginForm>({
    username: '',
    password: ''
});

const submit = async (): Promise<void> => {            
    const url = `${baseUrl}/login`;
    const requestFormData = new FormData();
    requestFormData.append('username', formData.value.username);
    requestFormData.append('password', formData.value.password);

    try {
        const res = await axios.post<TokenData>(url, requestFormData);
        if (res.status === 200) {
            const data = res.data;
            localStorage.setItem('Authentication-Token', data.token);
            localStorage.setItem('Username', data.username)
            await store.dispatch('auth/login');            
            // Check staff
                if (data.staff) {
                    localStorage.setItem('Is-Staff', 'true')
                await store.dispatch('auth/setStaff');
                await router.push({ path: '/admin' });                
            }
            else {
                localStorage.setItem('Is-Staff', 'false')
                await router.push({ path: '/' });
            }
                        
        }
    } catch (error: unknown) {
        if (axios.isAxiosError(error) && error.response && (error.response.status === 401 || error.response.status === 400)) {
            store.dispatch('error/showError', {
                title: 'Login Failed',
                message: 'Invalid username or password'
            });
        } else {
            store.dispatch('error/showError', {
                title: 'Something went wrong',
                message: 'Please try again later.'
            });
        }
    }
}
</script>


<style scoped>
    .card {
        width: 40vw;
        margin: 0 auto;
    }

    form {
        width: 100%;
    }
    h2 {
        text-align: center;
    }
</style>
