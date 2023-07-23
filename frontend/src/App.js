// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Category from './pages/Category';
import Budget from './pages/Budget';
import Expenses from './pages/Expenses';
import Navbar from './components/Navbar';

const App = () => {
  return (
    <>
      <Router>
        <Navbar />
        <div className='container'>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/category" element={<Category />} />
            <Route path="/budgets" element={<Budget />} />
            <Route path="/expenses" element={<Expenses />} />
          </Routes>
        </div>
      </Router>
    </>
  );
};

export default App;