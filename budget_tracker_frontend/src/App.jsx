import React, { useState } from 'react';
import CategoryPieChart from './components/PieChart';
import MonthYearSelector from './components/MonthYearSelector';
import './App.css';

function App() {
  const today = new Date();
  const [month, setMonth] = useState(String(today.getMonth() + 1).padStart(2, '0'));
  const [year, setYear] = useState(String(today.getFullYear()));

  if (today.getMonth() + 1 < month){
    return (
      <div class="selector">
        <MonthYearSelector
          month={month}
          year={year}
          onMonthChange={setMonth}
          onYearChange={setYear}
      />
        <h2>No information available</h2>
      </div>
    )
  }

  return (
    <>
      <div class="selector">
        <MonthYearSelector
          month={month}
          year={year}
          onMonthChange={setMonth}
          onYearChange={setYear}
        />
        <h2>Monthly Spending Breakdown</h2>
      </div>

      <div class="piechart">
        <CategoryPieChart month={month} year={year} />
      </div>
    </>
  );
}

export default App;
