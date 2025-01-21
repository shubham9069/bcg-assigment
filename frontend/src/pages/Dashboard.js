import React from 'react';
import Header from '../components/Header/Header';
import Sidebar from '../components/Sidebar/Sidebar';
import ProductTable from '../components/ProductTable/ProductTable';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();

    const cards = [
        {
            title: "Create and Manage Product",
            description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            onClick: () => navigate("/create-manage-product")
        },
        {
            title: "Pricing Optimization",
            description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            onClick: () => navigate("/pricing-optimization")
        }
    ]

    return (
        <div className="dashboard">
        <h1>Price Optimization Tool</h1>
        <p>Learn to optimize pricing strategies with ease.</p>
        <div className="cards">
          {cards.map((card, index) => (
            <div className="card" key={index} onClick={card.onClick}>
              <h2>{card.title}</h2>
              <p>{card.description}</p>
            </div>
          ))}
        </div>
      </div>
    );
};

export default Dashboard; 