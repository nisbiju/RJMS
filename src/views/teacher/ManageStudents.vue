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
            <router-link :to="`/teacher/course/${courseId}/students`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px; background-color: var(--popup);">
              Manage Students
            </router-link>
            <router-link :to="`/teacher/course/${courseId}/reflections`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px;">
              Reflections
            </router-link>
          </div>
        </div>

        <!-- Main Content -->
        <div style="flex: 1;">
          <h1 style="margin-bottom: 30px;">Manage Students</h1>

          <div style="margin-bottom: 20px; display: flex; gap: 10px;">
            <button @click="showAddModal = true" class="btn btn-primary">
              + Add Student
            </button>
            <button @click="deleteSelected" class="btn btn-secondary" :disabled="selectedStudents.length === 0">
              Delete Selected
            </button>
          </div>

          <div class="grid">
            <div v-for="student in students" :key="student.id" class="card">
              <div style="display: flex; align-items: start; gap: 15px;">
                <input type="checkbox" :value="student.id" v-model="selectedStudents" style="width: auto; margin-top: 5px;" />
                <div style="flex: 1;">
                  <div style="width: 50px; height: 50px; background-color: var(--filter); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-bottom: 10px;">
                    {{ getInitials(student.name) }}
                  </div>
                  <h3 style="margin-bottom: 5px;">{{ student.name }}</h3>
                  <p style="color: var(--text-light); font-size: 14px;">{{ student.email }}</p>
                </div>
              </div>
            </div>
          </div>

          <div v-if="students.length === 0" style="text-align: center; padding: 60px 20px; color: var(--text-light);">
            <p>No students enrolled yet</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Student Modal -->
    <div v-if="showAddModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
      <div class="card" style="max-width: 500px; width: 100%; margin: 20px;">
        <h2 style="margin-bottom: 20px;">Add Student</h2>
        
        <div class="form-group">
          <label>Student Email</label>
          <input v-model="newStudentEmail" type="email" placeholder="student@example.com" />
        </div>

        <div style="display: flex; gap: 10px; margin-top: 20px;">
          <button @click="addStudent" class="btn btn-primary">Add Student</button>
          <button @click="showAddModal = false" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ManageStudents',
  data() {
    return {
      courseId: this.$route.params.id,
      students: [],
      selectedStudents: [],
      showAddModal: false,
      newStudentEmail: ''
    }
  },
  methods: {
    async loadStudents() {
      try {
        const response = await axios.get(`/api/students/course/${this.courseId}`)
        this.students = response.data.students
      } catch (error) {
        console.error('Error loading students:', error)
      }
    },
    async addStudent() {
      if (!this.newStudentEmail) {
        alert('Please enter student email')
        return
      }

      try {
        await axios.post(`/api/students/course/${this.courseId}`, {
          email: this.newStudentEmail
        })
        this.showAddModal = false
        this.newStudentEmail = ''
        this.loadStudents()
      } catch (error) {
        console.error('Error adding student:', error)
        alert('Failed to add student. Student may not exist or already enrolled.')
      }
    },
    async deleteSelected() {
      if (!confirm(`Delete ${this.selectedStudents.length} selected student(s)?`)) {
        return
      }

      try {
        for (const studentId of this.selectedStudents) {
          await axios.delete(`/api/students/${studentId}/course/${this.courseId}`)
        }
        this.selectedStudents = []
        this.loadStudents()
      } catch (error) {
        console.error('Error deleting students:', error)
        alert('Failed to delete some students')
      }
    },
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    }
  },
  mounted() {
    this.loadStudents()
  }
}
</script>
