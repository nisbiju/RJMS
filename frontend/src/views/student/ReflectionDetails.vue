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

          <!-- Dynamic Structure Fields -->
          <div v-if="structureFields.length > 0">
            <div v-for="(field, index) in structureFields" :key="index" class="form-group">
              <label style="font-weight: 600; color: var(--text-dark);">
                {{ field.label }}
              </label>
              <p v-if="field.description" style="color: var(--text-light); font-size: 14px; margin-bottom: 10px; margin-top: 5px;">
                {{ field.description }}
              </p>
              <textarea
                v-model="responses[index]"
                rows="6"
                :placeholder="`Enter your response for: ${field.label}`"
                :disabled="isReadOnly"
                style="width: 100%;"
              ></textarea>
            </div>
          </div>
          
          <!-- Fallback to single textarea if no structure -->
          <div v-else class="form-group">
            <label>Your Reflection</label>
            <textarea
              v-model="content"
              rows="15"
              placeholder="Write your reflection here..."
              :disabled="isReadOnly"
            ></textarea>
          </div>

          <button
            @click="submitReflection"
            class="btn btn-primary"
            :disabled="isReadOnly"
            style="margin-top: 20px;"
          >
            {{ submitButtonText }}
          </button>

          <div v-if="isSubmitted" style="margin-top: 10px;">
            <p style="color: #4CAF50; font-weight: 500;">
              ✓ Submitted on {{ formatDate(submission.submitted_at) }}
            </p>
            <p v-if="!isDueDatePassed" style="color: var(--text-light); font-size: 14px; margin-top: 5px;">
              You can update your submission until {{ formatDate(reflection.due_date) }}
            </p>
            <p v-else style="color: var(--text-light); font-size: 14px; margin-top: 5px;">
              Submission closed (due date passed)
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
      structureFields: [],
      responses: {},
      showUserMenu: false
    }
  },
  computed: {
    isSubmitted() {
      return this.submission && this.submission.submitted_at
    },
    isDueDatePassed() {
      if (!this.reflection.due_date) return false
      const dueDate = new Date(this.reflection.due_date)
      const now = new Date()
      return now > dueDate
    },
    isReadOnly() {
      // Make read-only if due date has passed, regardless of submission status
      return this.isDueDatePassed
    },
    submitButtonText() {
      if (this.isDueDatePassed) {
        return 'Submission Closed (Due Date Passed)'
      } else if (this.isSubmitted) {
        return 'Update Submission'
      } else {
        return 'Submit'
      }
    }
  },
  methods: {
    async loadReflection() {
      const reflectionId = this.$route.params.id
      try {
        const response = await axios.get(`/api/reflections/${reflectionId}`)
        this.reflection = response.data
        this.submission = response.data.submission || {}
        
        // Parse structure from reflection
        if (this.reflection.structure) {
          try {
            this.structureFields = JSON.parse(this.reflection.structure)
          } catch (e) {
            console.error('Error parsing structure:', e)
            this.structureFields = []
          }
        }
        
        // Load existing submission content
        if (this.submission.content) {
          try {
            // Try to parse as JSON (new structured format)
            const parsedContent = JSON.parse(this.submission.content)
            
            // Check if it's an array of {label, response} objects
            if (Array.isArray(parsedContent) && parsedContent.length > 0 && parsedContent[0].label) {
              // Map responses back to the responses object
              this.responses = {}
              parsedContent.forEach((item, index) => {
                this.responses[index] = item.response || ''
              })
            } else {
              // It's some other JSON format, convert to string
              this.content = JSON.stringify(parsedContent)
            }
          } catch (e) {
            // Fall back to plain text (old format)
            this.content = this.submission.content
          }
        } else {
          // Initialize empty responses for each field
          this.responses = {}
          this.structureFields.forEach((field, index) => {
            this.responses[index] = ''
          })
        }
      } catch (error) {
        console.error('Error loading reflection:', error)
      }
    },
    async submitReflection() {
      // Validate based on whether structure exists
      if (this.structureFields.length > 0) {
        // Validate that all structured fields have responses
        const hasEmptyFields = this.structureFields.some((field, index) => {
          return !this.responses[index] || !this.responses[index].trim()
        })
        
        if (hasEmptyFields) {
          alert('Please complete all reflection fields before submitting')
          return
        }

        try {
          // Prepare content as JSON with field labels and responses
          const contentData = this.structureFields.map((field, index) => ({
            label: field.label,
            response: this.responses[index]
          }))
          
          await axios.post('/api/reflections/submit', {
            reflection_id: this.reflection.id,
            content: JSON.stringify(contentData)
          })
          alert('Reflection submitted successfully!')
          this.loadReflection()
        } catch (error) {
          console.error('Error submitting reflection:', error)
          alert('Failed to submit reflection. Please try again.')
        }
      } else {
        // Validate single content field
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
