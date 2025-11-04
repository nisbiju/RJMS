<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/teacher" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <div class="dropdown">
            <button @click="toggleUserMenu" class="btn btn-secondary">👤</button>
            <div v-if="showUserMenu" class="dropdown-menu">
              <router-link to="/teacher/profile">Profile</router-link>
              <button @click="logout" class="btn">Sign Out</button>
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
            <router-link :to="`/teacher/course/${courseId}/overview`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; background-color: var(--popup);">
              Overview
            </router-link>
            <router-link :to="`/teacher/course/${courseId}/configure`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px;">
              Configure
            </router-link>
            <router-link :to="`/teacher/course/${courseId}/students`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px;">
              Manage Students
            </router-link>
            <router-link :to="`/teacher/course/${courseId}/reflections`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px;">
              Reflections
            </router-link>
          </div>
        </div>

        <!-- Main Content -->
        <div style="flex: 1;">
          <h1 style="margin-bottom: 30px;">Course Overview</h1>

          <div class="card">
            <table>
              <thead>
                <tr>
                  <th>Reflection Name</th>
                  <th>Reflections Received</th>
                  <th>Total Enrolled Students</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in overview" :key="item.reflection_name">
                  <td>{{ item.reflection_name }}</td>
                  <td>{{ item.reflections_received }}</td>
                  <td>{{ item.total_enrolled_students }}</td>
                </tr>
              </tbody>
            </table>

            <div v-if="overview.length === 0" style="text-align: center; padding: 40px 20px; color: var(--text-light);">
              <p>No reflections configured for this course yet</p>
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
  name: 'CourseOverview',
  data() {
    return {
      courseId: this.$route.params.id,
      overview: [],
      showUserMenu: false
    }
  },
  methods: {
    async loadOverview() {
      try {
        const response = await axios.get(`/api/teacher/course/${this.courseId}/overview`)
        this.overview = response.data.overview
      } catch (error) {
        console.error('Error loading overview:', error)
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
    this.loadOverview()
  }
}
</script>
