import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <nav className="sidebar">
      <ul>
        <li>
          <Link to="/">Dashboard</Link>
        </li>
        <li>
          <Link to="/create-manage">Create/Manage Products</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Sidebar; 