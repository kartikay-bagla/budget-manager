// components/Home.js
import React, { useEffect, useState } from 'react';
import ExpensesTable from '../components/ExpensesTable';
import { get_budgets, get_expenses, get_total_expenses } from '../utils/api';
import CreateExpensePopup from '../components/CreateExpensePopup';
import { get_current_month_start_date, get_next_month_start_date, get_today_date } from '../utils/dates';
import BudgetProgressBar from '../components/BudgetProgressBar';

const Home = () => {
  const [expenses, setExpenses] = useState([]);
  const [upcomingExpenses, setUpcomingExpenses] = useState([]);
  const [totalExpenses, setTotalExpenses] = useState(undefined);
  const [upcomingTotalExpenses, setUpcomingTotalExpenses] = useState(undefined);
  const [budgets, setBudgets] = useState([]);

  useEffect(() => {

    let cmsd = get_current_month_start_date();
    let td = get_today_date();
    let nmsd = get_next_month_start_date();

    get_expenses(cmsd, td)
      .then(response => setExpenses(response.data))
      .catch(error => console.error(error));

    get_expenses(td, nmsd, "date", true)
      .then(response => setUpcomingExpenses(response.data))
      .catch(error => console.error(error));

    get_total_expenses(cmsd, td)
      .then(response => setTotalExpenses(response.data?.total))
      .catch(error => console.error(error));

    get_total_expenses(td, nmsd)
      .then(response => setUpcomingTotalExpenses(response.data?.total))
      .catch(error => console.error(error));

    get_budgets(new Date().getMonth() + 1, new Date().getFullYear())
      .then(response => setBudgets(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className='row'>
      <div className='col s8'>
        <div className='row px-2'>
          <h6 className='center-align font-bold mb-0'>Upcoming Expenses</h6>
          <ExpensesTable expenses={upcomingExpenses} />
        </div>
        <div className='flex justify-center'>
          <CreateExpensePopup />
        </div>
        <div className='row px-2'>
          <h6 className='center-align font-bold mb-0'>History</h6>
          <ExpensesTable expenses={expenses} />
        </div>
      </div>
      <div className='col s4'>
        <h6 className='center-align font-bold mb-0'>Totals</h6>
        <div className='flex px-2 pt-2 pb-8 justify-center'>
          <div className='shrink-1'>
            <table>
              <tr>
                <td className='px-1 py-1'>Expenses Till Date:</td>
                <td className='text-right px-1 py-1'>{totalExpenses}</td>
              </tr>
              <tr>
                <td className='px-1 py-1'>Upcoming Expenses:</td>
                <td className='text-right px-1 py-1'>{upcomingTotalExpenses}</td>
              </tr>
              <tr>
                <td className='px-1 py-1'>Total Expenses:</td>
                <td className='text-right px-1 py-1'>{totalExpenses + upcomingTotalExpenses}</td>
              </tr>
              <tr>
                <td className='px-1 py-1'>Total Budgets:</td>
                <td className='text-right px-1 py-1'>{budgets.length === 0 ? 0 : budgets.reduce((total, current_budget) => total + current_budget.amount, 0)}</td>
              </tr>
            </table>
          </div>
        </div>
        <h6 className='center-align font-bold'>Current Month's Budgets</h6>
        <div className='row px-4 pt-2'>
          {/* for budget in budgets, show budget progress bar */}
          {budgets.map(budget => (
            <div className='col s12' key={budget.id}>
              <BudgetProgressBar budget={budget} />
            </div>
          ))}
        </div>
        <h6 className='center-align font-bold'>Bar Chart</h6>
        <div className='row px-4 pt-2'>
          {/* for budget in budgets, show budget progress bar */}
          {budgets.map(budget => (
            <div className='col s12' key={budget.id}>
              <BudgetProgressBar budget={budget} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
