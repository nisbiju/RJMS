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
      <h1 style="text-align: center; margin-bottom: 40px;">Reflection Details</h1>

      <div style="max-width: 800px; margin: 0 auto;">
        <div class="card">
          <h2 style="margin-bottom: 20px;">{{ reflection.name }}</h2>
          <p v-if="reflection.description" style="color: var(--text-light); margin-bottom: 20px;">
            {{ reflection.description }}
          </p>
          <p v-if="reflection.due_date" style="margin-bottom: 30px;">
            <strong>Due Date:</strong> {{ formatDate(reflection.due_date) }}
          </p>

          <div class="form-group">
            <label>Your Reflection</label>
            <textarea
              v-model="content"
              rows="15"
              placeholder="Write your reflection here..."
              :disabled="isSubmitted"
            ></textarea>
          </div>

          <button
            @click="submitReflection"
            class="btn btn-primary"
            :disabled="isSubmitted"
            style="margin-top: 20px;"
          >
            {{ isSubmitted ? 'Submitted' : 'Submit' }}
          </button>

          <div v-if="isSubmitted" style="margin-top: 10px;">
            <p style="color: #4CAF50; font-weight: 500;">
              ✓ Submitted on {{ formatDate(submission.submitted_at) }}
            </p>
          </div>
        </div>

        <!-- Feedback Section -->
        <div v-if="submission && submission.feedback" class="card" style="margin-top: 30px;">
          <h2 style="margin-bottom: 20px;">Feedback</h2>
          <p style="white-space: pre-wrap;">{{ submission.feedback }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ReflectionDetails',
  data() {
    return {
      reflection: {},
      submission: {},
      content: '',
      showUserMenu: false
    }
  },
  computed: {
    isSubmitted() {
      return this.submission && this.submission.submitted
    }
  },
  methods: {
    async loadReflection() {
      const reflectionId = this.$route.params.id
      try {
        const response = await axios.get(`/api/reflections/${reflectionId}`)
        this.reflection = response.data
        this.submission = response.data.submission || {}
        this.content = this.submission.content || ''
      } catch (error) {
        console.error('Error loading reflection:', error)
      }
    },
    async submitReflection() {
      if (!this.content.trim()) {
        alert('Please write your reflection before submitting')
        return
      }

      try {
        await axios.post('/api/reflections/submit', {
          reflection_id: this.reflection.id,
          content: this.content
        })
        alert('Reflection submitted successfully!')
        this.loadReflection()
      } catch (error) {
        console.error('Error submitting reflection:', error)
        alert('Failed to submit reflection. Please try again.')
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString()
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
    this.loadReflection()
  }
}
</script>
