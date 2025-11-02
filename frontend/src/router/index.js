import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import StudentLogin from '../views/StudentLogin.vue'
import TeacherLogin from '../views/TeacherLogin.vue'
import StudentHome from '../views/student/StudentHome.vue'
import StudentCourse from '../views/student/StudentCourse.vue'
import StudentDashboard from '../views/student/StudentDashboard.vue'
import StudentProfile from '../views/student/StudentProfile.vue'
import ReflectionDetails from '../views/student/ReflectionDetails.vue'
import TeacherHome from '../views/teacher/TeacherHome.vue'
import TeacherProfile from '../views/teacher/TeacherProfile.vue'
import CourseOverview from '../views/teacher/CourseOverview.vue'
import CourseConfiguration from '../views/teacher/CourseConfiguration.vue'
import ManageStudents from '../views/teacher/ManageStudents.vue'
import CourseReflections from '../views/teacher/CourseReflections.vue'
import ReflectionSubmissions from '../views/teacher/ReflectionSubmissions.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login/student',
    name: 'StudentLogin',
    component: StudentLogin
  },
  {
    path: '/login/teacher',
    name: 'TeacherLogin',
    component: TeacherLogin
  },
  {
    path: '/student',
    name: 'StudentHome',
    component: StudentHome,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/profile',
    name: 'StudentProfile',
    component: StudentProfile,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/course/:id',
    name: 'StudentCourse',
    component: StudentCourse,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/reflection/:id',
    name: 'ReflectionDetails',
    component: ReflectionDetails,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/teacher',
    name: 'TeacherHome',
    component: TeacherHome,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/profile',
    name: 'TeacherProfile',
    component: TeacherProfile,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/course/:id/overview',
    name: 'CourseOverview',
    component: CourseOverview,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/course/:id/configure',
    name: 'CourseConfiguration',
    component: CourseConfiguration,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/course/:id/students',
    name: 'ManageStudents',
    component: ManageStudents,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/course/:id/reflections',
    name: 'CourseReflections',
    component: CourseReflections,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/reflection/:id/submissions',
    name: 'ReflectionSubmissions',
    component: ReflectionSubmissions,
    meta: { requiresAuth: true, role: 'teacher' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  }
})

export default router
