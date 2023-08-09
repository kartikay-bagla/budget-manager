// components/Home.js
import React, { useEffect, useState } from 'react';
import ExpensesTable from '../components/ExpensesTable';
import { get_budgets, get_expenses, get_total_expenses } from '../utils/api';
import CreateExpensePopup from '../components/CreateExpensePopup';
import { get_current_month_start_date, get_next_month_start_date, get_today_date } from '../utils/dates';
import BudgetProgressBar from '../components/BudgetProgressBar';
import { Box, Grid, Paper, Table, TableBody, TableCell, TableRow, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import numberFormatter from '../utils/utils';



const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  display: 'flex',
  flexDirection: 'column',
  alignContent: 'center',
  alignItems: 'center',
  justifyContent: 'center',
  color: theme.palette.text.secondary,
  height: '100%'
}));


const Home = () => {
  const [dashboardDate, setDashboardDate] = useState(dayjs());
  const [expenses, setExpenses] = useState([]);
  const [upcomingExpenses, setUpcomingExpenses] = useState([]);
  const [totalExpenses, setTotalExpenses] = useState(0);
  const [upcomingTotalExpenses, setUpcomingTotalExpenses] = useState(0);
  const [budgets, setBudgets] = useState([]);
  const [isCurrentMonth, setIsCurrentMonth] = useState(true);

  useEffect(() => {

    let dash_start_date = dashboardDate.set('date', 1);
    let dash_end_date = null;
    let dash_today_date = null;
    if (dash_start_date.month === 11) {
      dash_end_date = dash_start_date.set('month', 0).set('year', dash_start_date.year() + 1);
    } else {
      dash_end_date = dash_start_date.set('month', dash_start_date.month() + 1);
    }
    if (dash_start_date.month() == dayjs().month() & dash_start_date.year() == dayjs().year()) {
      dash_today_date = dayjs().format('YYYY-MM-DD');
      setIsCurrentMonth(true);
    } else {
      dash_today_date = null;
      setIsCurrentMonth(false);
    }
    dash_end_date = dash_end_date.format('YYYY-MM-DD');
    dash_start_date = dash_start_date.format('YYYY-MM-DD');

    console.log(isCurrentMonth);

    let end_date = null;
    if (dash_today_date === null) {
      end_date = dash_end_date;
      setUpcomingExpenses([]);
      setUpcomingTotalExpenses(0);
    } else {
      end_date = dash_today_date;
      get_expenses(dash_today_date, dash_end_date, "date", true)
        .then(response => setUpcomingExpenses(response.data))
        .catch(error => console.error(error));
      get_total_expenses(dash_today_date, dash_end_date)
        .then(response => setUpcomingTotalExpenses(response.data?.total))
        .catch(error => console.error(error));
    }
    get_expenses(dash_start_date, end_date)
      .then(response => setExpenses(response.data))
      .catch(error => console.error(error));
    get_total_expenses(dash_start_date, end_date)
      .then(response => setTotalExpenses(response.data?.total))
      .catch(error => console.error(error));
    get_budgets(dashboardDate.month() + 1, dashboardDate.year())
      .then(response => setBudgets(response.data))
      .catch(error => console.error(error));
  }, [dashboardDate]);

  return (
    <>
      <Grid container spacing={2}>
        <Grid item md={8} sm={12}>
          <Typography variant='h3'>Dashboard</Typography>
        </Grid>
        <Grid item md={4} sm={12} sx={{ display: 'flex', justifyContent: 'end' }}>
          <DatePicker
            label={'Month'} views={['month', 'year']}
            value={dashboardDate}
            onChange={(e) => setDashboardDate(e)}
          />
        </Grid>
      </Grid>
      <Grid container spacing={2}>
        <Grid item md={budgets.length != 0 ? 4 : 12 } xs={12}>
          <Item>
            <Table size="small" aria-label='total expenses'>
              <TableBody sx={{ 'td': { border: 0 } }}>
                {isCurrentMonth && <><TableRow>
                  <TableCell>Expenses Till Date:</TableCell>
                  <TableCell align='right'>{numberFormatter.format(totalExpenses)}</TableCell>
                </TableRow>
                  <TableRow>
                    <TableCell>Upcoming Expenses:</TableCell>
                    <TableCell align='right'>{numberFormatter.format(upcomingTotalExpenses)}</TableCell>
                  </TableRow></>
                }
                <TableRow>
                  <TableCell>Total Expenses:</TableCell>
                  <TableCell align='right'>{numberFormatter.format(totalExpenses + upcomingTotalExpenses)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Total Budgets:</TableCell>
                  <TableCell align='right'>{numberFormatter.format(budgets.length === 0 ? 0 : budgets.reduce((total, current_budget) => total + current_budget.amount, 0))}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </Item>
        </Grid>
        { budgets.length != 0 && 
        <Grid item md={8} xs={12}>
          <Item>
            <Typography variant='h6' gutterBottom>Budgets</Typography>
            <Grid container spacing={2}>
              {budgets.map(budget => (
                <Grid item lg={4} md={6} xs={12} key={budget.id}>
                  <BudgetProgressBar budget={budget} />
                </Grid>
              ))}
            </Grid>
          </Item>
        </Grid>
        }
        {
          isCurrentMonth && <Grid item xs={12}>
            <Item>
              <Typography variant='h6' gutterBottom>Upcoming Expenses</Typography>
              <ExpensesTable expenses={upcomingExpenses} />
            </Item>
          </Grid>
        }
        <Grid item xs={12}>
          <Item>
            <Typography variant='h6' gutterBottom>{isCurrentMonth ? 'Recent Expenses' : 'Expenses'}</Typography>
            <ExpensesTable expenses={expenses} />
          </Item>
        </Grid>
      </Grid>
      <CreateExpensePopup />
    </>
  );
};

export default Home;
