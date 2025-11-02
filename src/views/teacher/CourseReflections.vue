<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/teacher" class="navbar-title">RJMS</router-link>
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
              v-for="reflection in reflections"
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
      reflections: []
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
    }
  },
  mounted() {
    this.loadReflections()
  }
}
</script>
