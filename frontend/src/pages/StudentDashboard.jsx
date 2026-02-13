import { useState, useEffect } from 'react'
import axiosInstance from '../api/axiosConfig'
import './StudentDashboard.css'

function StudentDashboard() {
  const [courses, setCourses] = useState([])
  const [enrolledCourses, setEnrolledCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    fetchCourses()
    fetchEnrolledCourses()
  }, [])

  const fetchCourses = async () => {
    try {
      const response = await axiosInstance.get('/api/courses')
      setCourses(response.data)
      setError('')
    } catch (err) {
      setError('Failed to load courses: ' + (err.response?.data?.error || err.message))
    }
  }

  const fetchEnrolledCourses = async () => {
    try {
      const response = await axiosInstance.get('/api/enrollments/my-courses')
      setEnrolledCourses(response.data.map(e => e.courseId))
      setLoading(false)
    } catch (err) {
      setError('Failed to load enrollments')
      setLoading(false)
    }
  }

  const handleEnroll = async (courseId) => {
    try {
      await axiosInstance.post(
        '/api/enrollments',
        { courseId }
      )
      setSuccess('Successfully enrolled!')
      setTimeout(() => setSuccess(''), 3000)
      fetchEnrolledCourses()
    } catch (err) {
      setError('Failed to enroll: ' + (err.response?.data?.error || err.message))
      setTimeout(() => setError(''), 3000)
    }
  }

  if (loading) return <div className="container"><p>Loading courses...</p></div>

  return (
    <div className="container">
      <div className="dashboard-header">
        <h2>Available Courses</h2>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="courses-grid">
        {courses.length === 0 ? (
          <p>No courses available yet</p>
        ) : (
          courses.map(course => (
            <div key={course.id} className="course-card">
              <h3>{course.name}</h3>
              <p>{course.description}</p>
              <p className="instructor">Instructor: {course.instructor}</p>
              
              {enrolledCourses.includes(course.id) ? (
                <button className="enrolled-btn" disabled>✓ Enrolled</button>
              ) : (
                <button onClick={() => handleEnroll(course.id)}>Enroll Now</button>
              )}
            </div>
          ))
        )}
      </div>

      {enrolledCourses.length > 0 && (
        <div className="enrolled-section">
          <h2>My Enrollments ({enrolledCourses.length})</h2>
          <p>You are enrolled in {enrolledCourses.length} course(s)</p>
        </div>
      )}
    </div>
  )
}

export default StudentDashboard
