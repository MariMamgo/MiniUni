import { useState, useEffect } from 'react'
import LoginPage from './pages/LoginPage'
import StudentDashboard from './pages/StudentDashboard'
import AdminDashboard from './pages/AdminDashboard'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const userRole = localStorage.getItem('role')
    if (token) {
      setUser({ token, role: userRole })
    }
    setLoading(false)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('userId')
    setUser(null)
  }

  if (loading) return <div className="container"><p>Loading...</p></div>

  if (!user) {
    return <LoginPage setUser={setUser} />
  }

  return (
    <div>
      <nav className="navbar">
        <div className="container">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <img src="/mortarboard.png" alt="MiniUni Logo" style={{ width: '35px', height: '35px' }} />
            <h1 style={{ margin: 0 }}>MiniUni</h1>
          </div>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      {user.role === 'admin' ? (
        <AdminDashboard />
      ) : (
        <StudentDashboard />
      )}
    </div>
  )
}

export default App
