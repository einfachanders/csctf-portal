import { defineStore } from "pinia";
import axios from "axios";

export const useSessionStore = defineStore("session", {
  state: () => ({
    isAuthenticated: false,
  }),
  actions: {
    async checkSession() {
      try {
        const response = await axios.get("/api/v1/auth/check-session", { withCredentials: true });
        if (response.status === 200) {
          this.isAuthenticated = true;
        }
      } catch (error) {
        this.isAuthenticated = false;
      }
    },

    async login(username, password) {
      try {
        await axios.post(
          "/api/v1/auth/login",
          { username: username, password: password},
          { withCredentials: true }
        );
        this.isAuthenticated = true;
        // await this.checkGuestSession();
      } catch (error) {
        console.log(error)
        alert(error.response.data.message);
      }
    },
  },
});
