// components/Home.js
import React, { useEffect, useState } from 'react';
import ExpensesTable from '../components/ExpensesTable';
import { get_expenses } from '../utils/api';
import { get_today_date } from '../utils/dates';

const Home = () => {
  const [expenses, setExpenses] = useState([]);
  const today = get_today_date();

  useEffect(() => {
    get_expenses(today, today)
      .then(response => setExpenses(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container">
      <h3 className='center-align'>Today's Expenses</h3>
      <div className="card">
        <div className="card-content">
          <ExpensesTable expenses={expenses} />
        </div>
      </div>
    </div>
  );
};

export default Home;
