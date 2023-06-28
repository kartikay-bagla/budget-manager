// components/Budget.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Budget = () => {
  const [budgets, setBudgets] = useState([]);
  const month = new Date().getMonth() + 1;
  const year = new Date().getFullYear();

  useEffect(() => {
    axios.get(`http://localhost:8000/api/v1/budgets/?month=${month}&year=${year}`)
      .then(response => setBudgets(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h2>Monthly Budgets</h2>
      {budgets.map(budget => (
        <p key={budget.id}>Category {budget.category_id}: {budget.amount}</p>
      ))}
    </div>
  );
};

export default Budget;
