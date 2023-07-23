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
          <th>Description</th>
          <th>Amount</th>
          <th>Date</th>
          <th>Category</th>
        </tr>
      </thead>
      <tbody>
        {expenses.map(expense => (
          <tr key={expense.id}>
            <td>{expense.description}</td>
            <td>{expense.amount}</td>
            <td>{expense.date}</td>
            <td>{expense.category.name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ExpensesTable;
