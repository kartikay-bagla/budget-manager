import React, { useState, useEffect } from 'react';
import M from 'materialize-css';
import { add_non_recurring_expense, add_recurring_expense, get_categories } from '../utils/api';

const ExpenseForm = () => {
  const [categories, setCategories] = useState([]);
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [expenseDate, setExpenseDate] = useState('');
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurringStartDate, setRecurringStartDate] = useState('');
  const [recurringEndDate, setRecurringEndDate] = useState('');
  const [recurringFrequency, setRecurringFrequency] = useState('');

  useEffect(() => {
    // Call the function to get the list of categories and set the state
    get_categories()
        .then(response => {
            setCategories(response.data);
            console.log(response.data)
            M.FormSelect.init(document.querySelectorAll('select'), {});
        })
        .catch(error => console.error(error));

  }, []);

  const handleFormSubmit = (e) => {
    e.preventDefault();

    // Do something with the form data, e.g., submit it to a backend API
    if (isRecurring) {
        add_recurring_expense(
            category, description, amount, expenseDate,
            recurringStartDate, recurringEndDate, recurringFrequency
        )
    } else {
        add_non_recurring_expense(
            category, description, amount, expenseDate
        )
    }
    // Reset the form after submission (optional)
    resetForm();
  };

  const resetForm = () => {
    setCategory('');
    setDescription('');
    setAmount('');
    setExpenseDate('');
    setIsRecurring(false);
    setRecurringStartDate('');
    setRecurringEndDate('');
    setRecurringFrequency('');
  };

  return (
    <form onSubmit={handleFormSubmit}>
      <div className='input-field col s12'>
        <label htmlFor="category">Category:</label>
        <select id="category" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="" disabled>Select a category</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="description">Description:</label>
        <input
          type="text"
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="amount">Amount:</label>
        <input
          type="number"
          id="amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="expenseDate">Expense Date:</label>
        <input
          type="date"
          id="expenseDate"
          value={expenseDate}
          onChange={(e) => setExpenseDate(e.target.value)}
        />
      </div>

      <div>
        <label>
          Is recurring expense:
          <input
            type="checkbox" className='filled-in'
            checked={isRecurring}
            onChange={(e) => setIsRecurring(e.target.checked)}
          />
        </label>
      </div>

      {isRecurring && (
        <div>
          <label htmlFor="recurringStartDate">Recurring Start Date:</label>
          <input
            type="date"
            id="recurringStartDate"
            value={recurringStartDate}
            onChange={(e) => setRecurringStartDate(e.target.value)}
          />
        </div>
      )}

      {isRecurring && (
        <div>
          <label htmlFor="recurringEndDate">Recurring End Date:</label>
          <input
            type="date"
            id="recurringEndDate"
            value={recurringEndDate}
            onChange={(e) => setRecurringEndDate(e.target.value)}
          />
        </div>
      )}

      {isRecurring && (
        <div>
          <label htmlFor="recurringFrequency">Recurring Frequency:</label>
          <input
            type="text"
            id="recurringFrequency"
            value={recurringFrequency}
            onChange={(e) => setRecurringFrequency(e.target.value)}
          />
        </div>
      )}

      <button type="submit">Submit</button>
    </form>
  );
};

export default ExpenseForm;