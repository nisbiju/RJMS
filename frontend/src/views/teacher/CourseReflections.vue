<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/teacher" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <div class="dropdown">
            <button @click="toggleUserMenu">👤</button>
            <div v-if="showUserMenu" class="dropdown-menu">
              <router-link to="/teacher/profile">Profile</router-link>
              <button @click="logout">Sign Out</button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="container" style="padding: 40px 20px;">
      <div style="display: flex; gap: 30px;">
        <!-- Side Panel -->
        <div style="width: 200px; flex-shrink: 0;">
          <div class="card" style="padding: 10px;">
            <router-link :to="`/teacher/course/${courseId}/overview`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px;">
              Overview
            </router-link>
            <router-link :to="`/teacher/course/${courseId}/configure`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px;">
              Configure
            </router-link>
            <router-link :to="`/teacher/course/${courseId}/students`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px;">
              Manage Students
            </router-link>
            <router-link :to="`/teacher/course/${courseId}/reflections`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px; background-color: var(--popup);">
              Reflections
            </router-link>
          </div>
        </div>

        <!-- Main Content -->
        <div style="flex: 1;">
          <h1 style="text-align: center; margin-bottom: 40px;">Reflections</h1>

          <div class="grid">
            <div
              v-for="reflection in paginatedReflections"
              :key="reflection.id"
              class="card"
              @click="viewReflection(reflection.id)"
              style="cursor: pointer;"
            >
              <h3 style="margin-bottom: 10px;">{{ reflection.name }}</h3>
              <p v-if="reflection.description" style="color: var(--text-light); font-size: 14px; margin-bottom: 10px;">
                {{ reflection.description }}
              </p>
              <p style="font-size: 14px;">
                <strong>Start:</strong> {{ formatDate(reflection.start_date) }}<br>
                <strong>Due:</strong> {{ formatDate(reflection.due_date) }}
              </p>
            </div>
          </div>

          <div v-if="reflections.length === 0" style="text-align: center; padding: 60px 20px; color: var(--text-light);">
            <p>No reflections configured for this course yet</p>
          </div>

          <!-- Pagination Controls -->
          <div v-if="totalPages > 1" style="margin-top: 30px; display: flex; justify-content: center; align-items: center; gap: 10px;">
            <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="btn btn-secondary" style="padding: 8px 15px;">
              Previous
            </button>
            <span style="color: var(--text-dark);">Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="btn btn-secondary" style="padding: 8px 15px;">
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CourseReflections',
  data() {
    return {
      courseId: this.$route.params.id,
      reflections: [],
      currentPage: 1,
      itemsPerPage: 30,  // 10 rows × 3 cards per row
      showUserMenu: false
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.reflections.length / this.itemsPerPage)
    },
    paginatedReflections() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.reflections.slice(start, end)
    }
  },
  methods: {
    async loadReflections() {
      try {
        const response = await axios.get(`/api/reflections/course/${this.courseId}`)
        this.reflections = response.data.reflections
      } catch (error) {
        console.error('Error loading reflections:', error)
      }
    },
    viewReflection(reflectionId) {
      this.$router.push(`/teacher/reflection/${reflectionId}/submissions`)
    },
    formatDate(dateStr) {
      if (!dateStr) return 'Not set'
      return new Date(dateStr).toLocaleDateString()
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        window.scrollTo({ top: 0, behavior: 'smooth' })
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
    this.loadReflections()
  }
}
</script>
