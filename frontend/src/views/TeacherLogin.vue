<template>
  <div>
    <!-- Top Navigation Bar -->
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <div class="dropdown">
            <button @click="toggleMenu" class="btn btn-primary">Login</button>
            <div v-if="showMenu" class="dropdown-menu">
              <router-link to="/login/student">Student</router-link>
              <router-link to="/login/teacher">Teacher</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Split Layout Login -->
    <div class="login-container">
      <!-- Left side - Image -->
      <div class="login-image">
        <img 
          src="https://media.istockphoto.com/id/1376135709/photo/young-indian-teacher-teaching-on-laptop-with-school-uniform-students-at-classroom-concept-of.jpg?s=612x612&w=0&k=20&c=pWzHOpDsvc-m59NpFQgIVvKcNcnc0KtEsvC9COvZ_uM=" 
          alt="Teacher Login"
        />
      </div>

      <!-- Right side - Login form -->
      <div class="login-form">
        <div class="login-content">
          <h1>Teacher Login</h1>
          <p class="login-subtitle">Sign in with your Google account to access RJMS</p>
          
          <div id="g_id_onload"
               :data-client_id="clientId"
               data-context="signin"
               data-ux_mode="popup"
               data-callback="handleCredentialResponse"
               data-auto_prompt="false">
          </div>

          <div class="g_id_signin"
               data-type="standard"
               data-shape="rectangular"
               data-theme="outline"
               data-text="signin_with"
               data-size="large"
               data-logo_alignment="left">
          </div>

          <p class="login-footer">
            Are you a student? 
            <router-link to="/login/student">Login here</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TeacherLogin',
  data() {
    return {
      clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID || '480850099535-p2tqrm1jq676upf9kaauq558497dblb4.apps.googleusercontent.com',
      showMenu: false
    }
  },
  mounted() {
    // Load Google Identity Services script
    this.loadGoogleScript()
    
    // Set up global callback
    window.handleCredentialResponse = this.handleCredentialResponse
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu
    },
    loadGoogleScript() {
      const script = document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true
      document.head.appendChild(script)
    },
    async handleCredentialResponse(response) {
      try {
        const result = await axios.post('/api/auth/google', {
          token: response.credential,
          role: 'teacher'
        }, {
          withCredentials: true
        })

        if (result.data.user) {
          this.$router.push('/teacher')
        }
      } catch (error) {
        console.error('Login error:', error)
        if (error.response?.data?.error) {
          alert(error.response.data.error)
        } else {
          alert('Login failed. Please try again.')
        }
      }
    }
  },
  beforeUnmount() {
    // Clean up global callback
    delete window.handleCredentialResponse
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  height: calc(100vh - 56px); /* Subtract navbar height */
  width: 100%;
}

.login-image {
  flex: 1;
  overflow: hidden;
  background: #000;
}

.login-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.login-form {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  padding: 40px;
}

.login-content {
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.login-content h1 {
  font-size: 32px;
  font-weight: 700;
  color: #000;
  margin-bottom: 12px;
}

.login-subtitle {
  font-size: 16px;
  color: var(--text-light);
  margin-bottom: 40px;
}

.g_id_signin {
  margin: 0 auto;
}

.login-footer {
  margin-top: 30px;
  font-size: 14px;
  color: var(--text-light);
}

.login-footer a {
  color: #000;
  font-weight: 600;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }

  .login-image {
    height: 200px;
    flex: none;
  }

  .login-form {
    flex: 1;
  }
}
</style>
