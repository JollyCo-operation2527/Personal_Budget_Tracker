import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import React from 'react'
import Transactions from './transactions'

function App() {

  return (
    <div>
      <h1>Personal Budget Tracker</h1>
      <Transactions />
    </div> 
  );
}

export default App;
