import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Tooltip, Cell, Legend } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A28EFF'];

function CategoryPieChart({ month, year }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/spending_by_month/?month=${month}&year=${year}`)
      .then(res => res.json())
      .then(transactions => {
        const categoryTotals = {};
        transactions.forEach(tx => {
          categoryTotals[tx.category] = (categoryTotals[tx.category] || 0) + parseFloat(tx.total_amount);
        });

        const chartData = Object.entries(categoryTotals).map(([category, total_amount]) => ({
          name: category,
          value: Math.round(total_amount * 100) / 100,
        }));

        setData(chartData);
      });
  }, [month, year]);

  return (
    <div>
      <h3>Spending in {month}/{year}</h3>
      <PieChart width={400} height={300}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          outerRadius={120}
          label
        >
          {data.map((_, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}

export default CategoryPieChart;