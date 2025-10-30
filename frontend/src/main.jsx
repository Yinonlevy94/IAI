import React from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// mount react app to #root div in index.html
createRoot(document.getElementById('root')).render(<App />)