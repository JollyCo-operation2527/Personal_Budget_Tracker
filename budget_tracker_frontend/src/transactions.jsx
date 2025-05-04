import React, { useState } from 'react';
import CategoryPieChart from './components/PieChart';
import MonthYearSelector from './components/MonthYearSelector';

function MonthlySpending() {
  const today = new Date();
  const [month, setMonth] = useState(String(today.getMonth() + 1).padStart(2, '0'));
  const [year, setYear] = useState(String(today.getFullYear()));

  return (
    <div>
      <h2>Monthly Spending Breakdown</h2>
      <MonthYearSelector
        month={month}
        year={year}
        onMonthChange={setMonth}
        onYearChange={setYear}
      />
      <CategoryPieChart month={month} year={year} />
    </div>
  );
}

export default MonthlySpending;