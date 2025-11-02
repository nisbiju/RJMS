<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/teacher" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <div class="dropdown">
            <button @click="toggleUserMenu">👤</button>
            <div v-if="showUserMenu" class="dropdown-menu">
              <button @click="logout">Sign Out</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="container" style="padding: 40px 20px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        <div>
          <h1 style="margin-bottom: 10px;">My Courses</h1>
          <p style="color: var(--text-light);">
            {{ courses.length }} {{ courses.length === 1 ? 'course' : 'courses' }}
          </p>
        </div>
        <button @click="createCourse" class="btn btn-primary">
          + Add New Course
        </button>
      </div>

      <div style="display: flex; gap: 30px;">
        <!-- Main Content -->
        <div style="flex: 1;">
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
              <p style="color: var(--text-light); font-size: 14px;">{{ course.course_code || 'No code' }}</p>
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

    <!-- Create Course Modal -->
    <div v-if="showCreateModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
      <div class="card" style="max-width: 500px; width: 100%; margin: 20px;">
        <h2 style="margin-bottom: 20px;">Create New Course</h2>
        
        <div class="form-group">
          <label>Course Name</label>
          <input v-model="newCourse.name" type="text" placeholder="Enter course name" />
        </div>

        <div class="form-group">
          <label>Course Code (Optional)</label>
          <input v-model="newCourse.course_code" type="text" placeholder="Enter course code" />
        </div>

        <div style="display: flex; gap: 10px; margin-top: 20px;">
          <button @click="saveNewCourse" class="btn btn-primary">Create Course</button>
          <button @click="showCreateModal = false" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TeacherHome',
  data() {
    return {
      courses: [],
      searchQuery: '',
      statusFilter: 'all',
      showUserMenu: false,
      showCreateModal: false,
      newCourse: {
        name: '',
        course_code: ''
      }
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
      this.$router.push(`/teacher/course/${courseId}/overview`)
    },
    createCourse() {
      this.newCourse = { name: '', course_code: '' }
      this.showCreateModal = true
    },
    async saveNewCourse() {
      if (!this.newCourse.name) {
        alert('Please enter a course name')
        return
      }

      try {
        await axios.post('/api/courses', this.newCourse)
        this.showCreateModal = false
        this.loadCourses()
      } catch (error) {
        console.error('Error creating course:', error)
        alert('Failed to create course')
      }
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu
    },
    async logout() {
      try {
        await axios.post('/api/auth/logout')
        this.$router.push('/login/teacher')
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
