// components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <div className="nav-wrapper container">
        <Link to="/" className="brand-logo">Budgeting App</Link>
        <ul id="nav-mobile" className="right hide-on-med-and-down">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/category">Category</Link></li>
          <li><Link to="/budgets">Budgets</Link></li>
          <li><Link to="/expenses">Expenses</Link></li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
