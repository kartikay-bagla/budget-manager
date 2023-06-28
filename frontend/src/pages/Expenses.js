// components/Expenses.js
import React, { useEffect, useState } from 'react';
import ExpensesTable from '../components/ExpensesTable';
import { get_expenses } from '../utils/api';
import { get_current_month_start_date, get_next_month_start_date } from '../utils/dates';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);

  const startDateDefault = get_current_month_start_date();
  const endDateDefault = get_next_month_start_date();

  const [startDate, setStartDate] = useState(startDateDefault);
  const [endDate, setEndDate] = useState(endDateDefault);

  const callAPI = () => {
    get_expenses(startDate, endDate)
      .then(response => setExpenses(response.data))
      .catch(error => console.error(error));
  }
  
  useEffect(() => callAPI(), [startDate, endDate]);

  const handleSubmit = (e) => {
    e.preventDefault();
    callAPI();
  };

  return (
    <div className="container">
      <h3 className='center-align'>Expenses</h3>
      <form onSubmit={handleSubmit} className="row">
        <div className="input-field col s12 m4">
          <input type="date" id="start_date" value={startDate} onChange={e => setStartDate(e.target.value)} />
          <label htmlFor="start_date">Start Date</label>
        </div>
        <div className="input-field col s12 m4">
          <input type="date" id="end_date" value={endDate} onChange={e => setEndDate(e.target.value)} />
          <label htmlFor="end_date">End Date</label>
        </div>
        <div className="input-field col s12 m4">
          <button type="submit" className="btn">Submit</button>
        </div>
      </form>
      <ExpensesTable expenses={expenses} />
    </div>
  );
};

export default Expenses;
