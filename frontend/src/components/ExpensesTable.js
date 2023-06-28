// components/ExpensesTable.js
import React from 'react';

const ExpensesTable = ({expenses}) => {
  return (
    <table className="highlight striped responsive-table">
      <thead>
        <tr>
          <th>Description</th>
          <th>Amount</th>
          <th>Category ID</th>
        </tr>
      </thead>
      <tbody>
        {expenses.map(expense => (
          <tr key={expense.id}>
            <td>{expense.description}</td>
            <td>{expense.amount}</td>
            <td>{expense.category_id}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ExpensesTable;
