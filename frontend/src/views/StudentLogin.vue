<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <div class="dropdown">
            <button @click="toggleMenu" class="user-icon">☰</button>
            <div v-if="showMenu" class="dropdown-menu">
              <router-link to="/login/teacher">Teacher Login</router-link>
              <router-link to="/login/student">Student Login</router-link>
              <router-link to="/">Home</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="container" style="padding: 60px 20px;">
      <div style="max-width: 400px; margin: 0 auto;">
        <div class="card">
          <h2 style="text-align: center; margin-bottom: 30px;">Student Login</h2>
          
          <div class="form-group">
            <label>Email (Demo)</label>
            <input v-model="email" type="email" placeholder="Enter your email" />
          </div>

          <div class="form-group">
            <label>Name (Demo)</label>
            <input v-model="name" type="text" placeholder="Enter your name" />
          </div>

          <button @click="handleLogin" class="btn btn-primary" style="width: 100%; margin-top: 20px;">
            Sign in with Google (Demo Mode)
          </button>

          <p style="text-align: center; margin-top: 20px; font-size: 14px; color: var(--text-light);">
            In production, this will use Google OAuth. For demo, just enter your email and name.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentLogin',
  data() {
    return {
      email: '',
      name: '',
      showMenu: false
    }
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu
    },
    async handleLogin() {
      if (!this.email || !this.name) {
        alert('Please enter your email and name')
        return
      }

      try {
        const response = await axios.post('/api/auth/google', {
          token: `demo_${Date.now()}`,
          role: 'student',
          email: this.email,
          name: this.name
        }, {
          withCredentials: true
        })

        if (response.data.user) {
          this.$router.push('/student')
        }
      } catch (error) {
        console.error('Login error:', error)
        alert('Login failed. Please try again.')
      }
    }
  }
}
</script>
