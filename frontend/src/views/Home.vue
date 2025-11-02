<template>
  <div>
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="container navbar-content">
        <router-link to="/" class="navbar-title">RJMS</router-link>
        <div class="navbar-menu">
          <a href="#product" @click.prevent="scrollTo('product')">Product</a>
          <a href="#features" @click.prevent="scrollTo('features')">Features</a>
          <a href="#about" @click.prevent="scrollTo('about')">About Us</a>
          
          <div class="dropdown">
            <button @click="toggleLoginMenu" class="btn btn-primary">Login</button>
            <div v-if="showLoginMenu" class="dropdown-menu">
              <router-link to="/login/student">Student</router-link>
              <router-link to="/login/teacher">Teacher</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Content Sections -->
    <div class="container">
      <!-- Product Section -->
      <section id="product" class="section">
        <h2>Product</h2>
        <p>
          The Reflection Journal Management System (RJMS) is a digital platform designed to streamline the creation, management, and evaluation of reflection journals in educational contexts. It supports both teachers and students in fostering deeper learning, self-awareness, and critical thinking through structured reflection processes. RJMS integrates a flexible framework that allows teachers to set reflection models (such as Bloom's Taxonomy or the 5Ws & 1H), while students can record their reflections in guided spaces aligned with these models.
        </p>
        <br><br>
        <p>
          The system incorporates an AI-driven evaluation engine that provides scaffolded, question-based feedback, which teachers can refine and approve before sharing with students. By combining automation with a teacher-in-the-loop workflow, RJMS ensures meaningful feedback, encourages active student engagement, and enhances the overall reflective learning experience in both small and large classroom settings.
        </p>
      </section>

      <!-- Features Section -->
      <section id="features" class="section">
        <h2>Features</h2>
        <p>
          The Reflection Journal Management System (RJMS) is designed with two primary user roles in mind — Students and Teachers. Each role has a tailored set of features that support reflective learning and feedback.
        </p>
        <br><br>
        <p><strong>For Teachers:</strong></p>
        <p>RJMS equips you with powerful tools to manage reflections, guide learning, and ensure meaningful engagement:</p>
        <ul>
          <li>Secure Access: Log in easily with your Gmail account and access your teacher dashboard.</li>
          <li>Course Setup: Upload your student roster and configure the reflection framework that best suits your course (e.g., Bloom's six levels or the 5Ws & 1H approach).</li>
          <li>AI-Powered Evaluation: Get automated analysis of student reflections across three stages</li>
          <li>Scaffolded Feedback – Students receive layered, question-based feedback that guides learning rather than providing direct answers.</li>
          <li>Teacher-in-the-Loop – Teachers can review, edit, and approve AI-generated feedback before it is shared with students.</li>
          <li>Secure Login – Gmail OAuth ensures safe and reliable access for all users.</li>
        </ul>
      </section>

      <!-- About Us Section -->
      <section id="about" class="section">
        <h2>About Us</h2>
        <p>
          The Reflection Journal Management System (RJMS) is a student-developed project born out of a vision to make reflective learning more structured, scalable, and impactful in higher education. This project was undertaken as part of the course [Reflection Journal Management System] at IIT Bombay.
        </p>
        <br><br>
        <p>
          RJMS has been designed and developed by a dedicated group of students: Nisha, Hamid, Tanvi, Kushal, Vinay. Guided by the vision of Professor Shashi Kant Shankar, Ahmedabad University, the project aims to address the challenges faced by both students and teachers in managing reflection journals. While students often struggle with structuring their reflections meaningfully, teachers need efficient tools to evaluate and provide constructive feedback, especially in courses with large enrollments. RJMS bridges this gap by combining structured journal frameworks with AI-assisted evaluation and teacher-in-the-loop feedback.
        </p>
        <br><br>
        <p>
          Our mission is to create a platform that not only simplifies journal management but also fosters deeper learning, self-awareness, and critical thinking. We believe that reflective practice is a cornerstone of effective education, and RJMS is our contribution towards making this practice more engaging, interactive, and meaningful for both learners and educators.
        </p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      showLoginMenu: false
    }
  },
  methods: {
    toggleLoginMenu() {
      this.showLoginMenu = !this.showLoginMenu
    },
    scrollTo(section) {
      const element = document.getElementById(section)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }
  },
  mounted() {
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.dropdown')) {
        this.showLoginMenu = false
      }
    })
  }
}
</script>
