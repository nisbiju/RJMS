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
      <h1 style="margin-bottom: 30px;">Reflection Submissions</h1>

      <div style="margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; gap: 10px; align-items: center;">
          <input v-model="searchQuery" type="search" placeholder="Search by student name..." style="max-width: 300px;" />
          <button @click="selectAll" class="btn btn-secondary" style="padding: 8px 15px;">
            Select All
          </button>
        </div>
      </div>

      <div class="card" style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th style="width: 50px;"><input type="checkbox" v-model="selectAllChecked" @change="toggleSelectAll" style="width: auto;" /></th>
              <th>Student</th>
              <th>Submission</th>
              <th>AI Feedback</th>
              <th>Score</th>
              <th>Display Feedback</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="submission in paginatedSubmissions" :key="submission.student_id">
              <td><input type="checkbox" v-if="submission.submission_id" v-model="selectedSubmissions" :value="submission.submission_id" style="width: auto;" /></td>
              <td>{{ submission.student_name }}</td>
              <td>
                <span v-if="submission.submitted" class="badge" style="background-color: #90EE90;">
                  Submitted
                </span>
                <span v-else class="badge" style="background-color: #FFB6C1;">
                  Not Submitted
                </span>
                <button v-if="submission.submitted" @click="viewSubmission(submission)" class="btn btn-secondary" style="margin-left: 10px; font-size: 12px; padding: 5px 10px;">
                  View
                </button>
              </td>
              <td>
                <button v-if="submission.ai_feedback" @click="editFeedback(submission)" class="btn btn-secondary" style="font-size: 12px; padding: 5px 10px;">
                  Edit Feedback
                </button>
                <span v-else style="color: var(--text-light);">-</span>
              </td>
              <td>
                <input
                  v-if="submission.submitted"
                  type="number"
                  :value="submission.score || ''"
                  @change="updateScore(submission.submission_id, $event.target.value)"
                  style="width: 80px; padding: 5px;"
                  min="0"
                  max="100"
                />
                <span v-else style="color: var(--text-light);">-</span>
              </td>
              <td>
                <input
                  v-if="submission.submitted"
                  type="checkbox"
                  :checked="submission.display_feedback"
                  @change="toggleFeedback(submission.submission_id, $event.target.checked)"
                  style="width: auto;"
                />
                <span v-else style="color: var(--text-light);">-</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="submissions.length === 0" style="text-align: center; padding: 40px 20px; color: var(--text-light);">
          <p>No student records found</p>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div v-if="totalPages > 1" style="margin-top: 20px; display: flex; justify-content: center; align-items: center; gap: 10px;">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="btn btn-secondary" style="padding: 8px 15px;">
          Previous
        </button>
        <span style="color: var(--text-dark);">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="btn btn-secondary" style="padding: 8px 15px;">
          Next
        </button>
      </div>

      <!-- Submission View Modal -->
      <div v-if="viewingSubmission" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;" @click.self="viewingSubmission = null">
        <div class="card" style="max-width: 800px; width: 90%; max-height: 80vh; overflow-y: auto; background: var(--container);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h2>{{ viewingSubmission.student_name }}'s Submission</h2>
            <button @click="viewingSubmission = null" class="btn btn-secondary">Close</button>
          </div>
          
          <div v-if="viewingSubmission.content">
            <div v-if="isStructuredContent(viewingSubmission.content)">
              <div v-for="(item, index) in parseStructuredContent(viewingSubmission.content)" :key="index" style="margin-bottom: 25px;">
                <h4 style="color: var(--text-dark); margin-bottom: 10px;">{{ item.label }}</h4>
                <div style="background: var(--popup); padding: 15px; border-radius: 6px; white-space: pre-wrap;">
                  {{ item.response }}
                </div>
              </div>
            </div>
            <div v-else style="background: var(--popup); padding: 15px; border-radius: 6px; white-space: pre-wrap;">
              {{ viewingSubmission.content }}
            </div>
          </div>

          <div v-if="viewingSubmission.ai_feedback" style="margin-top: 30px; padding-top: 20px; border-top: 2px solid var(--border);">
            <h3 style="margin-bottom: 10px;">AI Feedback</h3>
            <div style="background: var(--popup); padding: 15px; border-radius: 6px; white-space: pre-wrap;">
              {{ viewingSubmission.ai_feedback }}
            </div>
          </div>
        </div>
      </div>

      <!-- Feedback Edit Modal -->
      <div v-if="editingFeedback" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;" @click.self="editingFeedback = null">
        <div class="card" style="max-width: 600px; width: 90%; background: var(--container);">
          <h2 style="margin-bottom: 20px;">Edit AI Feedback</h2>
          
          <div class="form-group">
            <label>Feedback for {{ editingFeedback.student_name }}</label>
            <textarea v-model="feedbackEditText" rows="10" style="width: 100%;"></textarea>
          </div>

          <div style="display: flex; gap: 10px; margin-top: 20px;">
            <button @click="saveFeedback" class="btn btn-primary">Save</button>
            <button @click="editingFeedback = null" class="btn btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ReflectionSubmissions',
  data() {
    return {
      reflectionId: this.$route.params.id,
      submissions: [],
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 10,
      selectedSubmissions: [],
      selectAllChecked: false,
      viewingSubmission: null,
      editingFeedback: null,
      feedbackEditText: '',
      showUserMenu: false
    }
  },
  computed: {
    filteredSubmissions() {
      if (!this.searchQuery) return this.submissions
      
      return this.submissions.filter(s =>
        s.student_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    },
    totalPages() {
      return Math.ceil(this.filteredSubmissions.length / this.itemsPerPage)
    },
    paginatedSubmissions() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredSubmissions.slice(start, end)
    }
  },
  methods: {
    async loadSubmissions() {
      try {
        const response = await axios.get(`/api/reflections/${this.reflectionId}/submissions`)
        this.submissions = response.data.submissions
      } catch (error) {
        console.error('Error loading submissions:', error)
      }
    },
    async updateScore(submissionId, score) {
      try {
        await axios.put(`/api/reflections/submission/${submissionId}/update`, {
          score: parseFloat(score) || null
        })
      } catch (error) {
        console.error('Error updating score:', error)
      }
    },
    async toggleFeedback(submissionId, display) {
      try {
        await axios.put(`/api/reflections/submission/${submissionId}/update`, {
          display_feedback: display
        })
      } catch (error) {
        console.error('Error updating feedback display:', error)
      }
    },
    toggleSelectAll() {
      if (this.selectAllChecked) {
        // Select all submissions that have submission_id
        this.selectedSubmissions = this.filteredSubmissions
          .map(s => s.submission_id)
          .filter(id => id)
      } else {
        this.selectedSubmissions = []
      }
    },
    selectAll() {
      this.selectAllChecked = true
      this.toggleSelectAll()
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    },
    viewSubmission(submission) {
      this.viewingSubmission = submission
    },
    editFeedback(submission) {
      this.editingFeedback = submission
      this.feedbackEditText = submission.ai_feedback || ''
    },
    async saveFeedback() {
      try {
        await axios.put(`/api/reflections/submission/${this.editingFeedback.submission_id}/update`, {
          ai_feedback: this.feedbackEditText
        })
        
        // Update local data
        const sub = this.submissions.find(s => s.submission_id === this.editingFeedback.submission_id)
        if (sub) {
          sub.ai_feedback = this.feedbackEditText
        }
        
        this.editingFeedback = null
        alert('Feedback updated successfully!')
      } catch (error) {
        console.error('Error updating feedback:', error)
        alert('Failed to update feedback')
      }
    },
    isStructuredContent(content) {
      try {
        const parsed = JSON.parse(content)
        return Array.isArray(parsed) && parsed.length > 0 && parsed[0].label
      } catch {
        return false
      }
    },
    parseStructuredContent(content) {
      try {
        return JSON.parse(content)
      } catch {
        return []
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
    this.loadSubmissions()
  }
}
</script>
