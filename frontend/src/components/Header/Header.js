import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

  return (
    <header className="header">
      <h1>Product Management System</h1>
      <div className="user-section">
        <Link to="/dashboard" className="user-button">Dashboard</Link>
        <button className="user-button" onClick={toggleUserMenu}>
          <span className="user-name">{user?.name || 'User'}</span>
          <span className="arrow-down"></span>
        </button>
        {showUserMenu && (
          <div className="user-menu">
            <div className="menu-item user-info">
              <span className="user-email">{user?.email}</span>
              <span className="user-role">{user?.role_name}</span>
            </div>
            <button className="menu-item logout-button" onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header; 