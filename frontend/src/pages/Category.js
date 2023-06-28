// components/Category.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Category = () => {
  const [categories, setCategories] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const month = new Date().getMonth() + 1;
  const year = new Date().getFullYear();

  useEffect(() => {
    axios.get(`http://localhost:8000/api/v1/categories`)
      .then(response => setCategories(response.data))
      .catch(error => console.error(error));
  }, []);

  const handleClick = (id) => {
    axios.get(`http://localhost:8000/api/v1/expenses/?start_date=${year}-${month}-01&end_date=${year}-${month+1}-01&category=${id}`)
      .then(response => setExpenses(response.data))
      .catch(error => console.error(error));
  };

  return (
    <div>
      <h2>Categories</h2>
      {categories.map(category => (
        <button key={category.id} onClick={() => handleClick(category.id)}>{category.name}</button>
      ))}
      <h2>Expenses</h2>
      {expenses.map(expense => (
        <p key={expense.id}>{expense.name}: {expense.amount}</p>
      ))}
    </div>
  );
};

export default Category;
