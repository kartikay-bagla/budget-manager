// components/Home.js
import React, { useEffect, useState } from 'react';
import ExpensesTable from '../components/ExpensesTable';
import { get_budgets, get_recent_expenses, get_total_expenses } from '../utils/api';
import CreateExpensePopup from '../components/CreateExpensePopup';
import { get_current_month_start_date, get_next_month_start_date } from '../utils/dates';
import BudgetProgressBar from '../components/BudgetProgressBar';

const Home = () => {
  const [expenses, setExpenses] = useState([]);
  const [totalExpenses, setTotalExpenses] = useState(undefined);
  const [budgets, setBudgets] = useState([]);

  useEffect(() => {
    get_recent_expenses(0, 10)
      .then(response => setExpenses(response.data))
      .catch(error => console.error(error));

    let cmsd = get_current_month_start_date()
    let nmsd = get_next_month_start_date()
    get_total_expenses(cmsd, nmsd)
      .then(response => setTotalExpenses(response.data?.total))
      .catch(error => console.error(error));

    get_budgets(new Date().getMonth() + 1, new Date().getFullYear())
      .then(response => setBudgets(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="container">
      <div className='row'>
        <h4 className='center-align'>Total expenses for this month: {totalExpenses}</h4>
      </div>
      <div className='row'>
        <h5 className='center-align'>Current Month's Budgets</h5>
        {/* for budget in budgets, show budget progress bar */}
        {budgets.map(budget => (
          <div className='col s12 m6 l4' key={budget.id}>
            <BudgetProgressBar budget={budget} />
          </div>
        ))}
      </div>
      <div className='row'>
        <h5 className='center-align'>Recent Expenses</h5>
        <ExpensesTable expenses={expenses} />
        <br />
        <CreateExpensePopup />
      </div>
    </div>
  );
};

export default Home;
