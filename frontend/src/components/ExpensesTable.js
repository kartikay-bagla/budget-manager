// components/ExpensesTable.js
import React from 'react';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { Typography } from '@mui/material';
import numberFormatter from '../utils/utils';


const ExpensesTable = ({ expenses }) => {
  // check if length of expenses is 0 and return a simple message in that case
  if (expenses.length === 0) {
    return <Typography variant='subtitle1'>No expenses for this date.</Typography>;
  }
  return (
    <TableContainer>
      <Table sx={{ minWidth: 450 }} size="small" aria-label="upcoming expenses">
        <colgroup>
          <col width="40%" />
          <col width="20%" />
          <col width="20%" />
          <col width="20%" />
        </colgroup>
        <TableHead>
          <TableRow>
            <TableCell>Description</TableCell>
            <TableCell align="right">Amount</TableCell>
            <TableCell align="right">Date</TableCell>
            <TableCell align="right">Category</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {expenses.map(expense => (
            <TableRow key={expense.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">{expense.description}</TableCell>
              <TableCell align="right">{numberFormatter.format(expense.amount)}</TableCell>
              <TableCell align="right">{expense.date}</TableCell>
              <TableCell align="right">{expense.category.name}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ExpensesTable;
