import React, { useState, useEffect } from 'react';
import { add_non_recurring_expense, add_recurring_expense, get_categories } from '../utils/api';
import { Box, Button, FormControl, FormControlLabel, InputLabel, MenuItem, Select, Switch, TextField } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';


const ExpenseForm = () => {
  const [categories, setCategories] = useState([]);
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [expenseDate, setExpenseDate] = useState(dayjs());
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurringStartDate, setRecurringStartDate] = useState(dayjs());
  const [recurringEndDate, setRecurringEndDate] = useState(dayjs());
  const [recurringFrequency, setRecurringFrequency] = useState('1M');

  useEffect(() => {
    // Call the function to get the list of categories and set the state
    get_categories()
      .then(response => {
        setCategories(response.data);
        console.log(response.data)
      })
      .catch(error => console.error(error));

  }, []);

  const handleFormSubmit = (e) => {
    e.preventDefault();

    // Do something with the form data, e.g., submit it to a backend API
    if (isRecurring) {
      add_recurring_expense(
        category, description, amount, expenseDate.format("YYYY-MM-DD"),
        recurringStartDate.format("YYYY-MM-DD"), recurringEndDate.format("YYYY-MM-DD"),
        recurringFrequency
      )
    } else {
      add_non_recurring_expense(
        category, description, amount, expenseDate.format("YYYY-MM-DD")
      )
    }
    // Reset the form after submission (optional)
    resetForm();
  };

  const resetForm = () => {
    setCategory('');
    setDescription('');
    setAmount('');
    setExpenseDate(dayjs());
    setIsRecurring(false);
    setRecurringStartDate(dayjs());
    setRecurringEndDate(dayjs());
    setRecurringFrequency('');
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }} component="form" onSubmit={handleFormSubmit}>
      <FormControl fullWidth>
        <InputLabel id="category">Category:</InputLabel>
        <Select
          labelId="category" value={category} label="Category"
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="" disabled>Select a category</option>
          {categories.map((category) => (
            <MenuItem key={category.id} value={category.id}>
              {category.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <TextField
        id="description" label="Description" variant="outlined"
        value={description} onChange={(e) => setDescription(e.target.value)}
      />

      <TextField
        id="amount" label="Amount" variant="outlined" type='number'
        value={amount} onChange={(e) => setAmount(e.target.value)}
      />

      <DatePicker
        label="Expense Date" value={expenseDate}
        onChange={(e) => setExpenseDate(e)}
      />

      <FormControlLabel control={
        <Switch
          checked={isRecurring}
          onChange={(e) => setIsRecurring(e.target.checked)}
          inputProps={{ 'aria-label': 'controlled' }}
        />
      } label="Recurring expense?" />

      {isRecurring && (
        <>
          <DatePicker
            label="Recurring Start Date"
            value={recurringStartDate}
            onChange={(e) => setRecurringStartDate(e)}
          />
          <DatePicker
            label="Recurring End Date"
            value={recurringEndDate}
            onChange={(e) => setRecurringEndDate(e)}
          />
          <TextField
            id="recurringFrequency" label="Recurring Frequency" variant="outlined"
            value={amount}
            onChange={(e) => setRecurringFrequency(e.target.value)}
          />
        </>
      )}
      <Button variant='contained' type='submit'>Submit</Button>
    </Box>
    
  );
};

export default ExpenseForm;