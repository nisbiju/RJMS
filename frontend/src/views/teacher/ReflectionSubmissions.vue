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
        <input v-model="searchQuery" type="search" placeholder="Search by student name..." style="max-width: 300px;" />
      </div>

      <div class="card" style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Student</th>
              <th>Submission</th>
              <th>AI Feedback</th>
              <th>Score</th>
              <th>Display Feedback</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="submission in filteredSubmissions" :key="submission.student_id">
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
      searchQuery: ''
    }
  },
  computed: {
    filteredSubmissions() {
      if (!this.searchQuery) return this.submissions
      
      return this.submissions.filter(s =>
        s.student_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
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
    }
  },
  mounted() {
    this.loadSubmissions()
  }
}
</script>
