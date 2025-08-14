import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-gray-800">
      <h1 className="text-3xl font-bold mb-6">React + Vite + Tailwind</h1>

      <div className="flex space-x-6 mb-6">
        <img src={viteLogo} className="h-16 animate-pulse" alt="Vite logo" />
        <img src={reactLogo} className="h-16 animate-spin-slow" alt="React logo" />
      </div>
      
      <div className="bg-white shadow-md rounded-xl p-6 w-64 text-center">
        <p className="text-lg mb-4">Count: <span className="font-semibold">{count}</span></p>
        <button
          onClick={() => setCount(count + 1)}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition"
        >
          Increment
        </button>
      </div>
    </div>
    </>
  )
}

export default App
