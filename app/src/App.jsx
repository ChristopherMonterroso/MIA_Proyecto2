import React from 'react'
import './App.css'
import Navbar from './components/navbar'
import Text_editor from './components/text_editor'
import { useState } from 'react'
import ReportList from './components/reports'

function App() {
  const [view, setView] = useState('text_editor')
  const toggleForm = (viewName) => {
    setView(viewName);
  }
  return (

    <div className="App">
      <Navbar onFormSwitch={toggleForm} />
      {
        view === "text_editor" ? <Text_editor  /> : <ReportList  />
      }
    </div>
  )

}

export default App
