<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow-sm" style="width: 350px;">
      <div class="card-body p-4">
        <h2 class="card-title text-center mb-4">Login</h2>
        <form name="login-form">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              class="form-control"
              v-model="input.username"
              required
              placeholder="Enter your username"
            />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              class="form-control"
              v-model="input.password"
              required
              placeholder="Enter your password"
            />
          </div>

          <div v-if="errorMessage" class="alert alert-danger mb-3">
            {{ errorMessage }}
          </div>

          <button
            class="btn btn-primary w-100"
            type="submit"
            v-on:click.prevent="login()"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

// return fungsi data dengan nama input yang berisi username dan password
export default {
  name: "Login",
  data() {
    return {
      input: {
        username: "",
        password: "",
      },
      errorMessage: ""
    };
  },
  
  // method login() akan mengirimkan data username dan password ke backend
  methods: {
    async login() {
      this.errorMessage = "";

      // validasi input sederhana
      if (!this.input.username || !this.input.password) {
        this.errorMessage = "Username dan Password tidak boleh kosong";
        return;
      }

      try {
        // send POST ke backend 
        const response = await axios.post("http://127.0.0.1:8000/login", {
          username: this.input.username,
          password: this.input.password,
        });
        
        // redirect ke main kalau status 200
        if (response.status === 200 && response.data.access_token) {
          localStorage.setItem('jwt_token', response.data.access_token);
          this.$router.push('/main');
        } else {
          this.errorMessage = "Login gagal: Response tidak valid";
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Login gagal: Terjadi kesalahan";
        console.error("Login error:", error);
      }
    },
  },
};
</script>
