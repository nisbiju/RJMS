<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/student" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <router-link to="/student/dashboard">Dashboard</router-link>
          
          <div class="dropdown">
            <button @click="toggleUserMenu" class="btn btn-secondary">👤</button>
            <div v-if="showUserMenu" class="dropdown-menu">
              <router-link to="/student/profile">Profile</router-link>
              <button @click="logout" class="btn">Sign Out</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="container" style="padding: 40px 20px;">
      <h1 style="margin-bottom: 30px;">Dashboard</h1>

      <div class="form-group" style="max-width: 300px; margin-bottom: 30px;">
        <label>Sort By</label>
        <select v-model="sortBy" @change="loadDashboard">
          <option value="dates">Sort by Dates</option>
          <option value="courses">Sort by Courses</option>
        </select>
      </div>

      <h2 style="margin-bottom: 20px;">Reflections Due</h2>

      <div class="card" style="padding: 0; overflow: hidden;">
        <div
          v-for="reflection in reflections"
          :key="reflection.reflection_id"
          class="card"
          @click="navigateToReflection(reflection.reflection_id)"
          style="cursor: pointer; margin: 0; border-radius: 0; border-bottom: 1px solid var(--border);"
        >
          <h3 style="margin-bottom: 5px;">{{ reflection.reflection_name }}</h3>
          <p style="color: var(--text-light); font-size: 14px; margin-bottom: 5px;">
            {{ reflection.course_name }} ({{ reflection.course_code }})
          </p>
          <p style="font-size: 14px;">
            Due: {{ formatDate(reflection.due_date) }}
            <span v-if="reflection.is_overdue" style="color: #D32F2F; font-weight: 500;"> (Overdue)</span>
          </p>
        </div>
      </div>

      <div v-if="reflections.length === 0" style="text-align: center; padding: 60px 20px; color: var(--text-light);">
        <p>No due or overdue reflections</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentDashboard',
  data() {
    return {
      reflections: [],
      sortBy: 'dates',
      showUserMenu: false
    }
  },
  methods: {
    async loadDashboard() {
      try {
        const response = await axios.get(`/api/reflections/dashboard?sort_by=${this.sortBy}`)
        this.reflections = response.data.reflections
      } catch (error) {
        console.error('Error loading dashboard:', error)
      }
    },
    navigateToReflection(reflectionId) {
      this.$router.push(`/student/reflection/${reflectionId}`)
    },
    formatDate(dateStr) {
      if (!dateStr) return 'No deadline'
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
    this.loadDashboard()
  }
}
</script>
