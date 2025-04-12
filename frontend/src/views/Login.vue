<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "../store/sessionStore";

const sessionStore = useSessionStore();
const router = useRouter();

const username = ref("");
const password = ref("");
const errorMessage = ref("");

// Handle login
const handleLogin = async (e) => {
  e.preventDefault();
  errorMessage.value = ""; // Reset error

  try {
    await sessionStore.login(username.value, password.value);
    if (sessionStore.isAuthenticated) {
      router.push("/");
    }
  } catch (err) {
    errorMessage.value = err;
  }
};

// Check if already logged in
onMounted(async () => {
  await sessionStore.checkSession();
  console.log(sessionStore.isAuthenticated)
  if (sessionStore.isAuthenticated) {
    router.push("/");
  }
});
</script>

<template>
  <div class="container-fluid login-container d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 rounded" style="max-width: 500px; width: 100%;">
      <div class="card-body">
        <div class="row">
          <img src="/csp10.png" class="rounded mx-auto d-block w-50" alt="...">
          <h3 class="text-center mb-4">CSCTF Login</h3>

          <!-- Error Alert -->
          <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
          </div>

          <form @submit="handleLogin">
            <div class="mb-3">
              <label for="inputName" class="form-label">Username</label>
              <input
                type="text"
                class="form-control rounded-pill"
                id="inputUsername"
                v-model="username"
                required
              />
            </div>
            <div class="mb-3">
              <label for="inputEmail" class="form-label">Password</label>
              <input
                type="password"
                class="form-control rounded-pill"
                id="inputPassword"
                v-model="password"
                required
              />
            </div>
            <div class="text-center pt-2">
              <button type="submit" class="btn btn-primary w-50 rounded-pill">Login</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
}
</style>
