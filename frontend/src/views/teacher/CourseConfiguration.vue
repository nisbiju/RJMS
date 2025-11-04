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
            <router-link :to="`/teacher/course/${courseId}/configure`" style="display: block; padding: 10px; text-decoration: none; color: var(--text-dark); border-radius: 6px; margin-top: 5px; background-color: var(--popup);">
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
        <div style="flex: 1; max-width: 800px;">
          <h1 style="text-align: center; margin-bottom: 40px;">Configuration</h1>

          <div class="card">
            <div class="form-group">
              <label>Framework</label>
              <select v-model="config.framework">
                <option value="">Select Framework</option>
                <option value="Bloom's Taxonomy">Bloom's Taxonomy</option>
                <option value="5 WHYs">5 WHYs</option>
                <option value="1-H">1-H</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label>Course Start Date</label>
              <input v-model="config.start_date" type="date" />
            </div>

            <div class="form-group">
              <label>Course End Date</label>
              <input v-model="config.end_date" type="date" />
            </div>

            <div class="form-group">
              <label>Each Reflection Due Date (days post reflection start)</label>
              <select v-model="config.reflection_due_days">
                <option value="1">1 day</option>
                <option value="2">2 days</option>
                <option value="3">3 days</option>
                <option value="5">5 days</option>
              </select>
            </div>

            <div class="form-group">
              <label>Recurrence (per week)</label>
              <select v-model="config.recurrence_days">
                <option value="1">1 day</option>
                <option value="2">2 days</option>
                <option value="3">3 days</option>
                <option value="5">5 days</option>
              </select>
            </div>

            <div class="form-group">
              <label>Select Days</label>
              <div class="checkbox-group">
                <label v-for="day in days" :key="day">
                  <input type="checkbox" :value="day" v-model="config.selected_days" />
                  {{ day }}
                </label>
              </div>
            </div>

            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid var(--border);">
              <h3 style="margin-bottom: 15px;">Custom Reflection Structure</h3>
              <p style="color: var(--text-light); font-size: 14px; margin-bottom: 15px;">
                Add custom fields to structure your reflection journal
              </p>

              <div v-for="(item, index) in customItems" :key="index" class="card" style="margin-bottom: 15px; padding: 15px;">
                <div class="form-group">
                  <label>Field Label</label>
                  <input v-model="item.label" type="text" placeholder="e.g., What did you learn?" />
                </div>
                <div class="form-group">
                  <label>Field Description (optional)</label>
                  <textarea v-model="item.description" rows="2" placeholder="Additional instructions for this field"></textarea>
                </div>
                <button @click="removeItem(index)" class="btn btn-secondary" style="font-size: 12px; padding: 5px 10px;">
                  Remove
                </button>
              </div>

              <button @click="addCustomItem" class="btn btn-secondary">
                + Add Item
              </button>
            </div>

            <!-- Reflection Date Preview -->
            <div v-if="canPreviewDates" style="margin-top: 30px; padding-top: 20px; border-top: 2px solid var(--border);">
              <h3 style="margin-bottom: 15px;">Preview Reflection Dates</h3>
              <p style="color: var(--text-light); font-size: 14px; margin-bottom: 15px;">
                Review the scheduled reflection dates. Uncheck any dates you want to exclude.
              </p>
              
              <button @click="generatePreviewDates" class="btn btn-secondary" style="margin-bottom: 15px;">
                Generate Preview
              </button>

              <div v-if="previewDates.length > 0" style="max-height: 300px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; padding: 15px;">
                <div v-for="(date, index) in previewDates" :key="index" style="margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                  <input type="checkbox" :checked="!deselectedDates.includes(date.dateStr)" @change="toggleDateSelection(date.dateStr)" />
                  <span>{{ date.displayText }}</span>
                </div>
              </div>
              
              <p v-if="previewDates.length > 0" style="margin-top: 10px; font-size: 14px; color: var(--text-light);">
                {{ selectedDatesCount }} reflection(s) will be created
              </p>
            </div>

            <button @click="saveConfiguration" class="btn btn-primary" style="margin-top: 20px;">
              Submit Configuration
            </button>

            <p v-if="saveMessage" style="margin-top: 15px; color: #4CAF50; font-weight: 500;">
              {{ saveMessage }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CourseConfiguration',
  data() {
    return {
      courseId: this.$route.params.id,
      config: {
        framework: '',
        start_date: '',
        end_date: '',
        reflection_due_days: '3',
        recurrence_days: '1',
        selected_days: []
      },
      customItems: [],
      days: ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
      saveMessage: '',
      showUserMenu: false,
      isLoadingConfig: false,
      previewDates: [],
      deselectedDates: []
    }
  },
  computed: {
    canPreviewDates() {
      return this.config.start_date && this.config.end_date && this.config.selected_days.length > 0
    },
    selectedDatesCount() {
      return this.previewDates.length - this.deselectedDates.length
    }
  },
  watch: {
    'config.framework'(newFramework, oldFramework) {
      // Only auto-populate if framework changed and not during initial load
      if (!this.isLoadingConfig && newFramework !== oldFramework) {
        this.populatePredefinedStructure(newFramework)
      }
    }
  },
  methods: {
    async loadConfiguration() {
      try {
        this.isLoadingConfig = true
        const response = await axios.get(`/api/courses/${this.courseId}`)
        const course = response.data.course
        
        if (course.framework) this.config.framework = course.framework
        if (course.start_date) this.config.start_date = course.start_date.split('T')[0]
        if (course.end_date) this.config.end_date = course.end_date.split('T')[0]
        if (course.reflection_due_days) this.config.reflection_due_days = course.reflection_due_days.toString()
        if (course.recurrence_days) this.config.recurrence_days = course.recurrence_days.toString()
        if (course.selected_days) this.config.selected_days = course.selected_days.split(',')
        if (course.custom_structure) {
          try {
            this.customItems = JSON.parse(course.custom_structure)
          } catch (e) {
            this.customItems = []
          }
        }
        this.isLoadingConfig = false
      } catch (error) {
        console.error('Error loading configuration:', error)
        this.isLoadingConfig = false
      }
    },
    populatePredefinedStructure(framework) {
      if (framework === "Bloom's Taxonomy") {
        this.customItems = [
          { label: 'Remember', description: '' },
          { label: 'Understand', description: '' },
          { label: 'Apply', description: '' },
          { label: 'Analyze', description: '' },
          { label: 'Evaluate', description: '' },
          { label: 'Create', description: '' }
        ]
      } else if (framework === '5 WHYs') {
        this.customItems = [
          { label: 'Why', description: '' },
          { label: 'Why', description: '' },
          { label: 'Why', description: '' },
          { label: 'Why', description: '' },
          { label: 'Why', description: '' }
        ]
      } else if (framework === '1-H') {
        this.customItems = [
          { label: 'How', description: '' }
        ]
      } else if (framework === 'Other') {
        // Clear for custom structure
        this.customItems = []
      }
    },
    async saveConfiguration() {
      if (!this.config.framework || !this.config.start_date || !this.config.end_date) {
        alert('Please fill in all required fields')
        return
      }

      try {
        const configData = {
          ...this.config,
          custom_structure: JSON.stringify(this.customItems)
        }
        await axios.put(`/api/courses/${this.courseId}/configure`, configData)
        this.saveMessage = 'Configuration saved successfully'
        setTimeout(() => {
          this.saveMessage = ''
        }, 3000)
      } catch (error) {
        console.error('Error saving configuration:', error)
        alert('Failed to save configuration')
      }
    },
    addCustomItem() {
      this.customItems.push({
        label: '',
        description: ''
      })
    },
    removeItem(index) {
      this.customItems.splice(index, 1)
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
    },
    generatePreviewDates() {
      if (!this.config.start_date || !this.config.end_date || this.config.selected_days.length === 0) {
        alert('Please fill in course dates and select days first')
        return
      }

      const dayMap = {
        'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thurs': 4, 'Fri': 5, 'Sat': 6, 'Sun': 0
      }
      
      const selectedDayNumbers = this.config.selected_days.map(d => dayMap[d])
      const startDate = new Date(this.config.start_date)
      const endDate = new Date(this.config.end_date)
      const dates = []
      
      let currentDate = new Date(startDate)
      
      while (currentDate <= endDate) {
        if (selectedDayNumbers.includes(currentDate.getDay())) {
          const dateStr = currentDate.toISOString().split('T')[0]
          const dayName = Object.keys(dayMap).find(key => dayMap[key] === currentDate.getDay())
          const displayText = `${dateStr} (${dayName})`
          dates.push({ dateStr, displayText })
        }
        currentDate.setDate(currentDate.getDate() + 1)
      }
      
      this.previewDates = dates
      this.deselectedDates = []
    },
    toggleDateSelection(dateStr) {
      const index = this.deselectedDates.indexOf(dateStr)
      if (index > -1) {
        this.deselectedDates.splice(index, 1)
      } else {
        this.deselectedDates.push(dateStr)
      }
    }
  },
  mounted() {
    this.loadConfiguration()
  }
}
</script>
