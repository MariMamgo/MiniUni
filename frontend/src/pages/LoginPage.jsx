import { useState } from 'react'
import axiosInstance from '../api/axiosConfig'
import './LoginPage.css'

function LoginPage({ setUser }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const [error, setError] = useState('')

  const handleDemoLogin = (demoRole) => {
    const demoToken = 'demo-token-' + Math.random().toString(36).substr(2, 9)
    const demoId = demoRole === 'admin' ? 1 : 2

    localStorage.setItem('token', demoToken)
    localStorage.setItem('role', demoRole)
    localStorage.setItem('userId', demoId)

    setUser({
      token: demoToken,
      role: demoRole
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    try {
      const endpoint = isSignUp ? '/api/auth/signup' : '/api/auth/login'
      const response = await axiosInstance.post(endpoint, {
        email,
        password,
        role: isSignUp ? 'student' : undefined
      })

      localStorage.setItem('token', response.data.token)
      localStorage.setItem('role', response.data.role)
      localStorage.setItem('userId', response.data.userId)

      setUser({
        token: response.data.token,
        role: response.data.role
      })
    } catch (err) {
      setError(err.response?.data?.message || 'Error occurred')
    }
  }

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>{isSignUp ? 'Sign Up' : 'Login'}</h2>
        
        {error && <div className="error">{error}</div>}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">{isSignUp ? 'Sign Up' : 'Login'}</button>

        <p>
          {isSignUp ? 'Already have an account?' : "Don't have an account?"}
          <button
            type="button"
            onClick={() => {
              setIsSignUp(!isSignUp)
              setError('')
            }}
            className="link-btn"
          >
            {isSignUp ? 'Login' : 'Sign Up'}
          </button>
        </p>

        <hr style={{ margin: '20px 0', borderColor: '#ddd' }} />

        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '10px' }}>
            🎨 <strong>Demo Mode</strong> (Skip login to see the interface):
          </p>
          <button
            type="button"
            onClick={() => handleDemoLogin('student')}
            className="demo-btn"
            style={{ backgroundColor: '#007bff', marginRight: '10px' }}
          >
            👤 View as Student
          </button>
          <button
            type="button"
            onClick={() => handleDemoLogin('admin')}
            className="demo-btn"
            style={{ backgroundColor: '#28a745' }}
          >
            👨‍💼 View as Admin
          </button>
        </div>
      </form>
    </div>
  )
}

export default LoginPage
