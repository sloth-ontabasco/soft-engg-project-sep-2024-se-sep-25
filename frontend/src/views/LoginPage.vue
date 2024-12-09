<script setup>
import HelloWorld from '@/components/HelloWorld.vue'
</script>
<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="wrapper flex flex-col">
      <img
        alt="IITM Logo"
        class="logo"
        src="https://upload.wikimedia.org/wikipedia/en/thumb/6/69/IIT_Madras_Logo.svg/1200px-IIT_Madras_Logo.svg.png"
        width="200"
        height="200"
      />

      <HelloWorld msg="Made by IITM Team 25" />
    </div>
    
    <div class="vertical-line"></div>
    <button @click="loginWithGoogle" class="google-login-button">
      <img
        src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png"
        alt="Google icon"
        class="google-icon"
      />
      <span class="google-text">Login with Google</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'GoogleLoginButton',
  methods: {
    loginWithGoogle() {
      window.location.href =
        import.meta.env.VITE_SERVER_BASE_URL + '/google/login'
    },
  },
}
</script>

<style scoped>
.google-login-button {
  display: flex;
  align-items: center;
  padding: 1em;
  font-size: 1.2em;
  background-color: #171a19;
  color: white;
  border: 2px solid #13a56d;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 3em;
  margin-left: 20em;
}

.google-login-button:hover {
  background-color: #0f8c5a;
}

.google-icon {
  width: 40px;
  height: 40px;
  margin-right: 0.5em;
}

.google-text {
  font-size: 1.2em;
}
.vertical-line {
  width: 2px;
  margin-left: 250px;
  height: 300px;
  background-color: #ccc;
}
</style>
