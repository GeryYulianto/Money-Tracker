<!-- Tambahkan Error Handling -->

<template>
  <div class="login-container">
    <!-- <form @submit.prevent="login" name="login-form"> -->
    <form name="login-form">
      <div class="mb-3">
        <!-- username dan password disimpan di input -->

        <label for="username">Username: </label>
        <input
          type="text"
          id="username"
          name="username"
          v-model="input.username"
          required
        />
      </div>

      <div class="mb-3">
        <label for="password">Password: </label>
        <input
          type="password"
          id="password"
          name="password"
          v-model="input.password"
          required
        />
      </div>

      <!-- v.on:clik akan mengaktifkan method login() -->
      <button
        class="btn btn-outline-dark"
        type="submit"
        v-on:click.prevent="login()">
        Login
      </button>

    </form>
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
    };
  },
  
  // method login() akan mengirimkan data username dan password ke backend
  methods: {
    async login() {

      // validasi input sederhana
      if (!this.input.username || !this.input.password) {
        // this.errorMessage = "Username dan Password tidak boleh kosong";
        return;
      }

      try {
        // send POST ke backend 
        const response = await axios.post("http://127.0.0.1:8000/login", {
          username: this.input.username,
          password: this.input.password,
        });
        
        // redirect ke main kalau status 200
        if (response.status == 200) {
          this.$router.push('/main')
        } else {
          console.error("Login error:", response);
        }
      } catch (error) {
        console.error("Login error:", error);
      }
    },
  },
};
</script>
