<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useSessionStore } from "../store/sessionStore";
import Challenge from "../components/Challenge.vue";
import axios from 'axios';

const sessionStore = useSessionStore();
const router = useRouter();

const challenges = ref([]);

const fetchChallenges = async () => {
  try {
    const response = await axios.get("/api/v1/challenges", { withCredentials: true });
    challenges.value = response.data;
  } catch (error) {
    console.error("Fetching challenges failed:", error.response?.data || error.message);
  }
};

// Check if already logged in
onMounted(async () => {
  await sessionStore.checkSession();
  if (!sessionStore.isAuthenticated) {
    router.push("/login");
  } else {
    await fetchChallenges();
  }
});
</script>

<template>
  <div class="container d-flex main-container align-items-center">
    <div class="row">
      <Challenge v-for="challenge in challenges" :key="challenge.id" :challenge="challenge" @solved="fetchChallenges" />
    </div>
  </div>
</template>

<style scoped>
.main-container {
  min-height: 100vh;
}
</style>
