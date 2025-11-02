<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/student" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <router-link to="/student/dashboard">Dashboard</router-link>
          
          <div class="dropdown">
            <button @click="toggleUserMenu">👤</button>
            <div v-if="showUserMenu" class="dropdown-menu">
              <router-link to="/student/profile">Profile</router-link>
              <button @click="logout">Sign Out</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="container" style="padding: 40px 20px;">
      <div style="max-width: 600px; margin: 0 auto;">
        <div class="card">
          <h1 style="margin-bottom: 30px;">My Profile</h1>

          <div class="form-group">
            <label>Name</label>
            <input type="text" :value="user.name" readonly />
          </div>

          <div class="form-group">
            <label>Email</label>
            <input type="email" :value="user.email" readonly />
          </div>

          <div class="form-group">
            <label>Role</label>
            <input type="text" value="Student" readonly />
          </div>

          <button @click="$router.push('/student')" class="btn btn-secondary">
            Back to Home
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentProfile',
  data() {
    return {
      user: {},
      showUserMenu: false
    }
  },
  methods: {
    async loadProfile() {
      try {
        const response = await axios.get('/api/auth/me')
        this.user = response.data.user
      } catch (error) {
        console.error('Error loading profile:', error)
      }
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
    },
    async logout() {
      try {
        await axios.post('/api/auth/logout')
        this.$router.push('/login/student')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
  },
  mounted() {
    this.loadProfile()
  }
}
</script>
