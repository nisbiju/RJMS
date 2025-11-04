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
      <div style="display: flex; gap: 30px;">
        <!-- Main Content -->
        <div style="flex: 1;">
          <h1 style="margin-bottom: 10px;">My Courses</h1>
          <p style="color: var(--text-light); margin-bottom: 20px;">
            {{ courses.length }} {{ courses.length === 1 ? 'course' : 'courses' }}
          </p>

          <div class="search-bar">
            <input v-model="searchQuery" type="search" placeholder="Search courses..." />
          </div>

          <div class="grid">
            <div
              v-for="course in filteredCourses"
              :key="course.id"
              class="card"
              @click="navigateToCourse(course.id)"
              style="cursor: pointer;"
            >
              <h3 style="margin-bottom: 10px;">{{ course.name }}</h3>
              <p style="color: var(--text-light); font-size: 14px;">{{ course.course_code }}</p>
              <span class="badge">{{ course.status }}</span>
            </div>
          </div>

          <div v-if="filteredCourses.length === 0" style="text-align: center; padding: 60px 20px; color: var(--text-light);">
            <p>No courses found</p>
          </div>
        </div>

        <!-- Filter Panel -->
        <div style="width: 250px;">
          <div class="filter-panel">
            <h3 style="margin-bottom: 15px;">Filters</h3>
            
            <div class="form-group">
              <label>Course Status</label>
              <select v-model="statusFilter">
                <option value="all">All</option>
                <option value="active">Active</option>
                <option value="archived">Archived</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentHome',
  data() {
    return {
      courses: [],
      searchQuery: '',
      statusFilter: 'all',
      showUserMenu: false
    }
  },
  computed: {
    filteredCourses() {
      let filtered = this.courses

      if (this.searchQuery) {
        filtered = filtered.filter(c =>
          c.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (c.course_code && c.course_code.toLowerCase().includes(this.searchQuery.toLowerCase()))
        )
      }

      if (this.statusFilter !== 'all') {
        filtered = filtered.filter(c => c.status === this.statusFilter)
      }

      return filtered
    }
  },
  methods: {
    async loadCourses() {
      try {
        const response = await axios.get('/api/courses')
        this.courses = response.data.courses
      } catch (error) {
        console.error('Error loading courses:', error)
      }
    },
    navigateToCourse(courseId) {
      this.$router.push(`/student/course/${courseId}`)
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
    this.loadCourses()
  }
}
</script>
