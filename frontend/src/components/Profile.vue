<template>
    <div class="profile-container">
      <h1 class="profile-title">User Profile</h1>
      <div v-if="user">
        <img :src="user.picture" alt="Profile Picture" class="profile-picture" />
        <h2 class="profile-name">{{ user.name }}</h2>
        <p class="profile-email">{{ user.email }}</p>
        <p class="profile-provider">Logged in with: {{ user.provider }}</p>
        <button @click="logout" class="logout-button">Logout</button>
      </div>
      <div v-else>
        <p>Loading user data...</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "UserProfile",
    data() {
      return {
        user: null, // User data will be stored here
      };
    },
    created() {
      this.fetchUserProfile();
    },
    methods: {
      fetchUserProfile() {
        // Fetch user profile data from your API
        fetch("/api/user/profile", {
          method: "GET",
          credentials: "include", // Include cookies for authentication
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            this.user = data; // Set user data to the component state
          })
          .catch((error) => {
            console.error("Error fetching user profile:", error);
          });
      },
      logout() {
        // Implement logout logic (e.g., clear session and redirect)
        window.location.href = "/api/auth/logout"; // Example logout API
      },
    },
  };
  </script>
  
  <style scoped>
  .profile-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2em;
    background-color: #302a2a;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    margin: auto;
  }
  
  .profile-title {
    font-size: 2em;
    margin-bottom: 1em;
  }
  
  .profile-picture {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-bottom: 1em;
  }
  
  .profile-name {
    font-size: 1.5em;
    margin: 0.5em 0;
  }
  
  .profile-email {
    font-size: 1em;
    color: #666;
  }
  
  .profile-provider {
    font-size: 0.9em;
    color: #999;
    margin: 0.5em 0;
  }
  
  .logout-button {
    margin-top: 1em;
    padding: 0.5em 1em;
    background-color: #ff4d4f;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .logout-button:hover {
    background-color: #e63946;
  }
  </style>