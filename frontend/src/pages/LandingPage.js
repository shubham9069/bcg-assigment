import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const handleButtonClick = () => {
    navigate(isAuthenticated ? '/dashboard' : '/login');
  };

  return (
    <div className="landing-container">
      <div className="content">
        <h1>Price Optimization Tool</h1>
        <div className="documentation">
          <section className="doc-section">
            <h2>Please read the Page before you start using the application</h2>
            <p>
              The project effectively evaluates a candidate's knowledge. I focused primarily on functionality and project completion.
              On the backend, I aimed to write efficient and scalable code, showcasing my backend skills.
              On the frontend, I prioritized implementing functionality over design and UI due to time constraints, ensuring all features work correctly.
            </p>
          </section>

          <section className="doc-section">
            <h2>Key Features</h2>
            <ul>
              <li>User Authentication with Role-based Access Control</li>
              <li>Product Management System</li>
              <li>Demand Forecasting with Visual Analytics</li>
              <li>Price Optimization Algorithm</li>
              <li>Real-time Data Visualization</li>
            </ul>
          </section>

          <section className="doc-section">
            <h2>Areas for Improvement</h2>
            <ul>
              <li>Implement more advanced forecasting algorithms</li>
              <li>we can store the chart data in redis for faster access when we are doing for large scale and in front we can store chart json in local storage</li>
              <li>we can create a logs of forecast data in a when ever demand and selling price changes so in long term we can use this data to predict the demand</li>
              <li>JWT token can be stored in cookies right now it is in local storage so it is not secure if you need more secure for production you can use cookies for storing token</li>
              <li>JWT implimentation refresh token concept so we can expire the token after few  hour and refresh token will be used to get new access token automatically</li>
              <li>Improve mobile responsiveness</li>
              <li>Add unit tests and integration tests</li>
            </ul>
          </section>

          <section className="doc-section">
            <h2>Technical Stack</h2>
            <ul>
              <li>Frontend: React.js with Material-UI</li>
              <li>State Management: React Context API</li>
              <li>Charts: Chart.js with react-chartjs-2</li>
              <li>Routing: React Router v6</li>
              <li>Notifications: React Toastify</li>
              <li>HTTP Client: Axios</li>
            </ul>
          </section>
        
        </div>
        
        <button 
          className="cta-button"
          onClick={handleButtonClick}
        >
          {isAuthenticated ? 'Go to Dashboard' : 'Login to Get Started'}
        </button>
      </div>
    </div>
  );
};

export default LandingPage; 