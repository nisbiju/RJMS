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
      <h1 style="margin-bottom: 10px;">{{ course.name }}</h1>
      <p style="color: var(--text-light); margin-bottom: 30px;">{{ course.course_code }}</p>

      <h2 style="margin-bottom: 20px;">Reflection Journals</h2>

      <div class="grid">
        <div
          v-for="reflection in reflections"
          :key="reflection.id"
          class="card"
          @click="navigateToReflection(reflection.id)"
          style="cursor: pointer;"
        >
          <h3 style="margin-bottom: 10px;">{{ reflection.name }}</h3>
          <p style="color: var(--text-light); font-size: 14px; margin-bottom: 10px;">
            Due: {{ formatDate(reflection.due_date) }}
          </p>
          <span v-if="reflection.submission && reflection.submission.submitted" class="badge" style="background-color: #90EE90;">
            Submitted
          </span>
          <span v-else class="badge" style="background-color: #FFB6C1;">
            Not Submitted
          </span>
        </div>
      </div>

      <div v-if="reflections.length === 0" style="text-align: center; padding: 60px 20px; color: var(--text-light);">
        <p>No reflection journals for this course yet</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentCourse',
  data() {
    return {
      course: {},
      reflections: [],
      showUserMenu: false
    }
  },
  methods: {
    async loadCourseData() {
      const courseId = this.$route.params.id
      try {
        const [courseRes, reflectionsRes] = await Promise.all([
          axios.get(`/api/courses/${courseId}`),
          axios.get(`/api/reflections/course/${courseId}`)
        ])
        this.course = courseRes.data.course
        this.reflections = reflectionsRes.data.reflections
      } catch (error) {
        console.error('Error loading course data:', error)
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
    this.loadCourseData()
  }
}
</script>
