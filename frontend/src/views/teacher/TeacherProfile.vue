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
      <div style="max-width: 600px; margin: 0 auto;">
        <div class="card">
          <h1 style="text-align: center; margin-bottom: 30px;">Teacher Profile</h1>

          <!-- Profile Image Section -->
          <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 30px;">
            <div style="width: 150px; height: 150px; border-radius: 50%; overflow: hidden; background-color: var(--filter); display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
              <img v-if="form.profile_image" :src="form.profile_image" style="width: 100%; height: 100%; object-fit: cover;" alt="Profile" />
              <span v-else style="font-size: 48px; color: var(--text-light);">👤</span>
            </div>
            
            <div style="display: flex; gap: 10px;">
              <label class="btn btn-secondary" style="cursor: pointer; font-size: 14px; padding: 6px 12px;">
                Update Picture
                <input type="file" ref="fileInput" @change="handleImageUpload" accept="image/*" style="display: none;" />
              </label>
              <button v-if="form.profile_image" @click="removeImage" class="btn btn-secondary" style="font-size: 14px; padding: 6px 12px;">
                Remove Picture
              </button>
            </div>
          </div>

          <!-- Profile Fields -->
          <div class="form-group">
            <label>Name</label>
            <input v-model="form.name" type="text" placeholder="Enter your name" />
          </div>

          <div class="form-group">
            <label>Email (View Only)</label>
            <input :value="user.email" type="email" readonly style="background-color: var(--container); cursor: not-allowed;" />
          </div>

          <div class="form-group">
            <label>Department</label>
            <input v-model="form.department" type="text" placeholder="Enter your department" />
          </div>

          <div class="form-group">
            <label>Experience</label>
            <input v-model="form.experience" type="text" placeholder="e.g., 5 years" />
          </div>

          <div class="form-group">
            <label>Area of Interest</label>
            <input v-model="form.area_of_interest" type="text" placeholder="Enter your area of interest" />
          </div>

          <div style="display: flex; justify-content: center; margin-top: 30px;">
            <button @click="saveProfile" class="btn btn-primary">
              Save
            </button>
          </div>

          <p v-if="saveMessage" style="margin-top: 15px; color: #4CAF50; font-weight: 500;">
            {{ saveMessage }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TeacherProfile',
  data() {
    return {
      user: {},
      form: {
        name: '',
        department: '',
        experience: '',
        area_of_interest: '',
        profile_image: null
      },
      showUserMenu: false,
      saveMessage: ''
    }
  },
  methods: {
    async loadProfile() {
      try {
        const response = await axios.get('/api/auth/me')
        this.user = response.data.user
        
        // Populate form with user data
        this.form.name = this.user.name || ''
        this.form.department = this.user.department || ''
        this.form.experience = this.user.experience || ''
        this.form.area_of_interest = this.user.area_of_interest || ''
        this.form.profile_image = this.user.profile_image || null
      } catch (error) {
        console.error('Error loading profile:', error)
      }
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      // Check file size (limit to 2MB)
      if (file.size > 2 * 1024 * 1024) {
        alert('Image size should be less than 2MB')
        event.target.value = ''
        return
      }

      const reader = new FileReader()
      reader.onload = (e) => {
        this.form.profile_image = e.target.result
      }
      reader.readAsDataURL(file)
    },
    removeImage() {
      this.form.profile_image = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },
    async saveProfile() {
      try {
        await axios.put('/api/auth/profile', this.form)
        this.saveMessage = 'Profile updated successfully!'
        
        // Reload profile to get updated data
        await this.loadProfile()
        
        setTimeout(() => {
          this.saveMessage = ''
        }, 3000)
      } catch (error) {
        console.error('Error saving profile:', error)
        alert('Failed to save profile. Please try again.')
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
    this.loadProfile()
  }
}
</script>
