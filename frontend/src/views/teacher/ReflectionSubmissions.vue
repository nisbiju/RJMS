<template>
  <div>
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/teacher" class="navbar-title">RJMS</router-link>
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
              </td>
              <td>
                <span v-if="submission.ai_feedback" style="max-width: 200px; display: inline-block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  {{ submission.ai_feedback }}
                </span>
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
      selectAllChecked: false
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
    }
  },
  mounted() {
    this.loadSubmissions()
  }
}
</script>
