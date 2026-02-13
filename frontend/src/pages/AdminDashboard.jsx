import { useState, useEffect } from 'react'
import axiosInstance from '../api/axiosConfig'
import './AdminDashboard.css'

function AdminDashboard() {
  const [courses, setCourses] = useState([])
  const [enrollments, setEnrollments] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [newCourse, setNewCourse] = useState({ name: '', description: '', instructor: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchCourses()
    fetchEnrollments()
  }, [])

  const fetchCourses = async () => {
    try {
      const response = await axiosInstance.get('/api/courses')
      setCourses(response.data)
      setLoading(false)
    } catch (err) {
      setError('Failed to load courses: ' + (err.response?.data?.error || err.message))
      setLoading(false)
    }
  }

  const fetchEnrollments = async () => {
    try {
      const response = await axiosInstance.get('/api/enrollments')
      setEnrollments(response.data)
    } catch (err) {
      setError('Failed to load enrollments: ' + (err.response?.data?.error || err.message))
    }
  }

  const handleAddCourse = async (e) => {
    e.preventDefault()
    setError('')

    if (!newCourse.name || !newCourse.description || !newCourse.instructor) {
      setError('Please fill all fields')
      return
    }

    try {
      await axiosInstance.post('/api/courses', newCourse)
      setSuccess('Course added successfully!')
      setNewCourse({ name: '', description: '', instructor: '' })
      setShowForm(false)
      setTimeout(() => setSuccess(''), 3000)
      fetchCourses()
    } catch (err) {
      setError('Failed to add course: ' + (err.response?.data?.error || err.message))
    }
  }

  const handleDeleteCourse = async (courseId) => {
    if (!window.confirm('Are you sure you want to delete this course?')) return

    try {
      await axiosInstance.delete(`/api/courses/${courseId}`)
      setSuccess('Course deleted successfully!')
      setTimeout(() => setSuccess(''), 3000)
      fetchCourses()
      fetchEnrollments()
    } catch (err) {
      setError('Failed to delete course: ' + (err.response?.data?.error || err.message))
    }
  }

  if (loading) return <div className="container"><p>Loading...</p></div>

  const courseMap = Object.fromEntries(
    courses.map(c => [c.id, c])
  )

  return (
    <div className="container">
      <div className="admin-header">
        <h2>Admin Dashboard</h2>
        <button onClick={() => setShowForm(!showForm)} className="add-btn">
          {showForm ? '✕ Cancel' : '+ Add Course'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {showForm && (
        <form onSubmit={handleAddCourse} className="course-form">
          <h3>Add New Course</h3>
          <input
            type="text"
            placeholder="Course Name"
            value={newCourse.name}
            onChange={(e) => setNewCourse({ ...newCourse, name: e.target.value })}
            required
          />
          <textarea
            placeholder="Course Description"
            value={newCourse.description}
            onChange={(e) => setNewCourse({ ...newCourse, description: e.target.value })}
            rows="4"
            required
          />
          <input
            type="text"
            placeholder="Instructor Name"
            value={newCourse.instructor}
            onChange={(e) => setNewCourse({ ...newCourse, instructor: e.target.value })}
            required
          />
          <button type="submit">Create Course</button>
        </form>
      )}

      <div className="admin-content">
        <div className="section">
          <h3>Courses ({courses.length})</h3>
          {courses.length === 0 ? (
            <p>No courses yet. Add one to get started!</p>
          ) : (
            <div className="courses-list">
              {courses.map(course => {
                const courseEnrollments = enrollments.filter(e => e.courseId === course.id)
                return (
                  <div key={course.id} className="course-item">
                    <div>
                      <h4>{course.name}</h4>
                      <p>{course.description}</p>
                      <p className="instructor">Instructor: {course.instructor}</p>
                      <p className="enrollment-count">📊 {courseEnrollments.length} students enrolled</p>
                    </div>
                    <button
                      onClick={() => handleDeleteCourse(course.id)}
                      className="delete-btn"
                    >
                      Delete
                    </button>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        <div className="section">
          <h3>All Enrollments ({enrollments.length})</h3>
          {enrollments.length === 0 ? (
            <p>No enrollments yet</p>
          ) : (
            <div className="enrollments-table">
              <table>
                <thead>
                  <tr>
                    <th>Student Email</th>
                    <th>Course</th>
                    <th>Enrolled Date</th>
                  </tr>
                </thead>
                <tbody>
                  {enrollments.map(enrollment => (
                    <tr key={enrollment.id}>
                      <td>{enrollment.studentEmail}</td>
                      <td>{courseMap[enrollment.courseId]?.name || 'Unknown Course'}</td>
                      <td>{new Date(enrollment.enrollmentDate).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
