import './App.css'
import { HashRouter as Router, Routes, Route } from 'react-router-dom'
import LandingPage from './Pages/LandingPage'


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage/>} />
      </Routes>
    </Router>
  )
}

export default App
