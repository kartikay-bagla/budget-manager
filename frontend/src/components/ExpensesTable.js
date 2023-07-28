// components/ExpensesTable.js
import React from 'react';

const ExpensesTable = ({expenses}) => {
  // check if length of expenses is 0 and return a simple message in that case
  if (expenses.length === 0) {
    return <p className='center-align'>No expenses for this date.</p>;
  }
  return (
    <table className="highlight striped">
      <thead>
        <tr>
          <th className='px-0 py-1'>Description</th>
          <th className='px-0 py-1'>Amount</th>
          <th className='px-0 py-1'>Date</th>
          <th className='px-0 py-1'>Category</th>
        </tr>
      </thead>
      <tbody>
        {expenses.map(expense => (
          <tr key={expense.id}>
            <td className='px-0 py-0'>{expense.description}</td>
            <td className='px-0 py-0'>{expense.amount}</td>
            <td className='px-0 py-0'>{expense.date}</td>
            <td className='px-0 py-0'>{expense.category.name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ExpensesTable;
