// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Category from './pages/Category';
import Budget from './pages/Budget';
import Expenses from './pages/Expenses';
import ResponsiveAppBar from './components/ResponsiveAppBar';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import 'dayjs/locale/en-gb';


const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const App = () => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale='en-gb'>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Router>
          <ResponsiveAppBar />
          <Box sx={{ padding: 2, flex: 1, display: 'flex', flexFlow: 'column', alignItems: 'center', gap: 2 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/category" element={<Category />} />
              <Route path="/budgets" element={<Budget />} />
              <Route path="/expenses" element={<Expenses />} />
            </Routes>
          </Box>
        </Router>
      </ThemeProvider>
    </LocalizationProvider>
  );
};

export default App;
