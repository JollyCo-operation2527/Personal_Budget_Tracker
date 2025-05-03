// This is to test
import React, { useEffect, useState } from 'react';

function Transactions() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/transactions/')
      .then(response => response.json())
      .then(data => setTransactions(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h2>Transactions</h2>
      <ul>
        {transactions.map(tx => (
          <li key={tx.id}>
            <strong>{tx.store}</strong>: ${tx.amount} on {tx.date}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Transactions;