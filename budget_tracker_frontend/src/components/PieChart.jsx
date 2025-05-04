import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Tooltip, Cell, Legend } from 'recharts';

const CATEGORY_COLOURS = {
    'Rent': '#F7545A',
    'Entertainment': '#4A84F7',
    'Groceries': '#5CF770',
    'Takeout/Restaurants': '#FAE05C',
    'Phone/Internet': '#A28EFF',
    'Default': '#CCCCCC',
  };

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
    <>
        <div>
        <h3>Spending in {month}/{year}</h3>
        <PieChart width={500} height={350}>
            <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius={120}
            label={({value}) => `$${value}`}
            >
            {data.map((entry, index) => (
                <Cell key={index} fill={CATEGORY_COLOURS[entry.name] || CATEGORY_COLOURS['Default']} />
            ))}
            </Pie>
            <Tooltip />
        </PieChart>
        </div>
        
        {/* Legend */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '10px'}}>
            {data.map((entry, index) => (
                <div key={index} style={{ color: CATEGORY_COLOURS[entry.name] || CATEGORY_COLOURS['Default']}}>
                    {entry.name}
                </div> ))}
        </div>
    </>
  );
}

export default CategoryPieChart;