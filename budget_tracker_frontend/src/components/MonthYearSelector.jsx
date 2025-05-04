import React from 'react';

function MonthYearSelector({month, year, onMonthChange, onYearChange}){
    const months = [
        {value: "01", label: "January"},
        {value: "02", label: "February"},
        {value: "03", label: "March"},
        {value: "04", label: "April"},
        {value: "05", label: "May"},
        {value: "06", label: "June"},
        {value: "07", label: "July"},
        {value: "08", label: "August"},
        {value: "09", label: "September"},
        {value: "10", label: "October"},
        {value: "11", label: "November"},
        {value: "12", label: "December"},
    ];

    const years = ["2025"]; // Only year 2025 for now

    return (
        <div>
            <label>
                Month:
                <select value={month} onChange={e => onMonthChange(e.target.value)}>
                    {months.map(m => (
                        <option key={m.value} value={m.value}>{m.label}</option>
                    ))}
                </select>
            </label>    
            
            <label> {" "}
                Year:
                <select value={year} onChange={e => onYearChange(e.target.value)}>
                    {years.map(y => (
                        <option key={y} value={y}>{y}</option>
                    ))}
                </select>
            </label>
        </div>
    );
}

export default MonthYearSelector;

